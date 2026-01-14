#!/usr/bin/env python3
"""
Modular Resume Generator - Main orchestrator for the modular generation process

This module provides the main interface for generating resumes using the modular approach,
with fallback to legacy generation when needed.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import yaml

from .section_generators import SectionManager
from .parallel_executor import ParallelExecutor
from .content_aggregator import ContentAggregator
from .template_engine import TemplateEngine
from .ui_feedback_manager import UIFeedbackManager
from .ai_content_cache import AIContentCache, get_job_directory_from_id
# from .pdf_manager import PDFManager  # Will be implemented later
from .pdf_manager import PDFManager

logger = logging.getLogger(__name__)

class ModularResumeGenerator:
    """
    Main orchestrator for the modular resume generation process.
    
    Coordinates section generation, content aggregation, template rendering,
    and PDF conversion while providing comprehensive user feedback.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the modular generator with configuration.
        
        Args:
            config: Configuration dictionary with settings for modular generation
        """
        self.config = config or {}
        self.section_manager = SectionManager()
        self.parallel_executor = ParallelExecutor()
        self.content_aggregator = ContentAggregator()
        self.template_engine = TemplateEngine()
        self.ui_feedback = UIFeedbackManager()
        # self.pdf_manager = PDFManager()  # Will be implemented later
        self.pdf_manager = PDFManager()
        
        # Configuration flags
        self.use_modular = self.config.get('use_modular_generation', True)
        self.enable_parallel = self.config.get('enable_parallel_processing', True)
        self.section_timeout = self.config.get('section_timeout_seconds', 30)
        
    def generate_resume(self, resume_data: dict, job_data: dict, job_id: str = None, job_directory: str = None, use_cache: bool = True) -> dict:
        """
        Generate resume using modular approach with smart caching behavior.
        
        Args:
            resume_data: Resume information from YAML file
            job_data: Job description and requirements
            job_id: Unique identifier for tracking progress
            job_directory: Path to job directory for caching (optional)
            use_cache: Whether to use cached content when available
            
        Returns:
            Dict containing generated HTML content and metadata
        """
        job_id = job_id or f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            logger.info(f"Starting modular resume generation for job {job_id}")
            
            # Initialize cache if job directory is provided
            cache = None
            smart_cache_decision = None
            if job_directory:
                cache = AIContentCache(job_directory)
                logger.info(f"Initialized AI content cache for job directory: {job_directory}")
                
                # Implement smart caching behavior - NEVER clear ai_content automatically
                if use_cache:
                    should_regenerate_all = cache.should_regenerate_all(expected_sections=7)
                    # SAFETY: Never automatically clear ai_content to preserve user data
                    if should_regenerate_all:
                        logger.info("🔄 Smart cache: All 7 sections exist, but ai_content will be preserved (no auto-clearing)")
                        smart_cache_decision = "preserve_cache"
                    else:
                        cached_count = cache.count_cached_sections()
                        logger.info(f"📋 Smart cache: Only {cached_count}/7 sections cached, will generate missing sections only")
                        smart_cache_decision = "generate_missing"
            
            # Start progress tracking
            self.ui_feedback.start_job_tracking(job_id)
            
            if not self.use_modular:
                logger.info("Modular generation disabled, using legacy method")
                return self._generate_resume_legacy(resume_data, job_data, job_id)
            
            # Phase 1: Job Preparation
            self.ui_feedback.update_phase(job_id, "job_preparation", "in_progress")
            sections = self.section_manager.identify_sections(resume_data)
            generators = self.section_manager.create_section_generators(sections, cache)
            
            # Apply smart caching logic to generators
            if cache and use_cache and smart_cache_decision == "generate_missing":
                # Get list of missing sections
                all_section_names = [gen.section_name for gen in generators]
                missing_sections = cache.get_missing_sections(all_section_names)
                
                # Filter generators to only include missing sections
                generators = [gen for gen in generators if gen.section_name in missing_sections]
                logger.info(f"🎯 Smart cache: Will only generate {len(generators)} missing sections: {[gen.section_name for gen in generators]}")
            
            self.ui_feedback.update_phase(job_id, "job_preparation", "completed")
            
            # Phase 2: Content Generation (with smart caching support)
            self.ui_feedback.update_phase(job_id, "content_generation", "in_progress")
            
            if self.enable_parallel:
                section_results = self.parallel_executor.execute_parallel(
                    generators, resume_data, job_data, 
                    progress_callback=lambda section, progress, status: 
                        self.ui_feedback.update_section_progress(job_id, section, progress, status),
                    use_cache=use_cache
                )
            else:
                section_results = self._execute_sequential(generators, resume_data, job_data, job_id, use_cache)
            
            # If we only generated missing sections, load the rest from cache
            if cache and smart_cache_decision == "generate_missing":
                cached_results = cache.load_all_content()
                # Merge cached results with newly generated results
                section_results.update(cached_results)
                logger.info(f"📥 Smart cache: Merged {len(cached_results)} cached sections with {len(section_results) - len(cached_results)} newly generated sections")
            
            # Save all generated content to cache
            if cache:
                cache.save_all_content(section_results)
                logger.info("💾 Saved all AI-generated content to cache")
                
                # After all 7 AI content files are created, move to generated and validate
                if job_data.get('id'):
                    try:
                        # Import the validation function
                        import sys
                        from pathlib import Path
                        
                        # Add project root to path if not already there
                        project_root = str(Path(__file__).parent.parent)
                        if project_root not in sys.path:
                            sys.path.insert(0, project_root)
                        
                        from step2_generate import move_queued_to_generated_with_validation
                        
                        logger.info(f"🔄 Moving job {job_data['id']} to generated and validating all jobs...")
                        move_success = move_queued_to_generated_with_validation(job_data['id'])
                        
                        if move_success:
                            logger.info(f"✅ Successfully moved job {job_data['id']} to generated directory")
                        else:
                            logger.warning(f"⚠️ Failed to move job {job_data['id']} to generated directory")
                            
                    except Exception as e:
                        logger.error(f"Error moving job to generated after AI content creation: {str(e)}")
                        # Don't fail the entire generation process for this
            
            
            self.ui_feedback.update_phase(job_id, "content_generation", "completed")
            
            # Phase 3: Template Rendering
            self.ui_feedback.update_phase(job_id, "template_rendering", "in_progress")
            
            aggregated_content = self.content_aggregator.aggregate_sections(section_results, resume_data)
            html_resume = self.template_engine.render_resume(aggregated_content)
            html_cover_letter = self.template_engine.render_cover_letter(aggregated_content, job_data)
            
            self.ui_feedback.update_phase(job_id, "template_rendering", "completed")
            
            # Phase 4: PDF Conversion
            self.ui_feedback.update_phase(job_id, "pdf_conversion", "in_progress")
            
            pdf_results = self.pdf_manager.convert_modular_output(
                [html_resume, html_cover_letter],
                progress_callback=lambda file, progress: 
                    self.ui_feedback.update_section_progress(job_id, f"pdf_{file}", progress, "in_progress")
            )
            
            self.ui_feedback.update_phase(job_id, "pdf_conversion", "completed")
            
            # Phase 5: Save HTML and PDF files to job directory
            if job_directory:
                try:
                    from pathlib import Path
                    import re
                    
                    job_dir_path = Path(job_directory)
                    
                    # Extract job info for filename generation
                    job_id_str = job_data.get('id', 'unknown')
                    company = job_data.get('company', 'Unknown_Company')
                    title = job_data.get('title', 'Unknown_Title')
                    
                    # Sanitize for filename
                    def sanitize_filename(text):
                        sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
                        sanitized = re.sub(r'[\s_]+', '_', sanitized)
                        return sanitized.strip('_')[:50]
                    
                    company_clean = sanitize_filename(company)
                    
                    # Generate timestamp (try to extract from existing files or use current)
                    existing_files = list(job_dir_path.glob('*.yaml'))
                    if existing_files:
                        # Extract timestamp from existing file
                        filename_parts = existing_files[0].stem.split('.')
                        timestamp = filename_parts[0] if filename_parts else datetime.now().strftime('%Y%m%d%H%M%S')
                    else:
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    
                    # Save HTML resume file
                    resume_filename = f"{timestamp}.{job_id_str}.{company_clean}.resume.html"
                    resume_path = job_dir_path / resume_filename
                    
                    with open(resume_path, 'w', encoding='utf-8') as f:
                        f.write(html_resume)
                    logger.info(f"💾 Saved HTML resume: {resume_filename}")
                    
                    # Save HTML cover letter file
                    cover_filename = f"{timestamp}.{job_id_str}.{company_clean}.coverletter.html"
                    cover_path = job_dir_path / cover_filename
                    
                    with open(cover_path, 'w', encoding='utf-8') as f:
                        f.write(html_cover_letter)
                    logger.info(f"💾 Saved HTML cover letter: {cover_filename}")
                    
                    # Save PDF files if they were generated
                    if pdf_results and isinstance(pdf_results, dict):
                        for pdf_type, pdf_content in pdf_results.items():
                            if pdf_content:
                                pdf_filename = f"{timestamp}.{job_id_str}.{company_clean}.{pdf_type}.pdf"
                                pdf_path = job_dir_path / pdf_filename
                                
                                if isinstance(pdf_content, bytes):
                                    with open(pdf_path, 'wb') as f:
                                        f.write(pdf_content)
                                    logger.info(f"💾 Saved PDF {pdf_type}: {pdf_filename}")
                                elif isinstance(pdf_content, str) and Path(pdf_content).exists():
                                    # PDF content is a file path, copy it
                                    import shutil
                                    shutil.copy2(pdf_content, pdf_path)
                                    logger.info(f"💾 Copied PDF {pdf_type}: {pdf_filename}")
                    
                except Exception as e:
                    logger.error(f"Error saving HTML/PDF files: {str(e)}")
                    # Don't fail the entire process for file saving errors
            
            result = {
                'success': True,
                'job_id': job_id,
                'html_resume': html_resume,
                'html_cover_letter': html_cover_letter,
                'pdf_results': pdf_results,
                'generation_method': 'modular',
                'sections_generated': list(section_results.keys()),
                'cache_info': cache.get_cache_info() if cache else None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'parallel_processing': self.enable_parallel,
                    'sections_count': len(section_results),
                    'cache_used': use_cache and cache is not None,
                    'job_directory': job_directory,
                    'smart_cache_decision': smart_cache_decision,
                    'version': '1.5.20260110.86'
                }
            }
            
            logger.info(f"Successfully completed modular generation for job {job_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in modular generation for job {job_id}: {str(e)}", exc_info=True)
            
            # Fallback to legacy generation
            logger.info(f"Falling back to legacy generation for job {job_id}")
            return self._generate_resume_legacy(resume_data, job_data, job_id)
    
    def _execute_sequential(self, generators: List, resume_data: dict, job_data: dict, job_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """Execute section generators sequentially (fallback for parallel execution)."""
        results = {}
        
        for i, generator in enumerate(generators):
            section_name = generator.section_name
            try:
                self.ui_feedback.update_section_progress(job_id, section_name, 0.0, "in_progress")
                
                # Use caching-aware generation method
                if hasattr(generator, 'generate_with_cache') and use_cache:
                    content = generator.generate_with_cache(resume_data, job_data, force_regenerate=not use_cache)
                else:
                    content = generator.generate_content(resume_data, job_data)
                
                results[section_name] = {
                    'content': content,
                    'status': 'completed',
                    'generator': generator.__class__.__name__
                }
                
                self.ui_feedback.update_section_progress(job_id, section_name, 1.0, "completed")
                
            except Exception as e:
                logger.error(f"Error generating {section_name}: {str(e)}")
                results[section_name] = {
                    'content': None,
                    'status': 'failed',
                    'error': str(e),
                    'generator': generator.__class__.__name__
                }
                self.ui_feedback.update_section_progress(job_id, section_name, 0.0, "failed")
        
        return results
    
    def _generate_resume_legacy(self, resume_data: dict, job_data: dict, job_id: str) -> dict:
        """
        Fallback to original monolithic generation method.
        
        This method should call the existing step2_generate functions
        to maintain backward compatibility.
        """
        try:
            # Import the legacy generation functions
            from src.step2_generate import llm_generate_custom_resume_legacy, llm_generate_custom_coverletter_legacy
            
            self.ui_feedback.update_phase(job_id, "legacy_generation", "in_progress")
            
            # Generate using legacy method
            html_resume = llm_generate_custom_resume_legacy(resume_data, job_data)
            html_cover_letter = llm_generate_custom_coverletter_legacy(resume_data, job_data, html_resume)
            
            self.ui_feedback.update_phase(job_id, "legacy_generation", "completed")
            
            return {
                'success': True,
                'job_id': job_id,
                'html_resume': html_resume,
                'html_cover_letter': html_cover_letter,
                'generation_method': 'legacy',
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'fallback_reason': 'modular_generation_disabled_or_failed'
                }
            }
            
        except Exception as e:
            logger.error(f"Legacy generation also failed for job {job_id}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'job_id': job_id,
                'error': str(e),
                'generation_method': 'legacy_failed'
            }
    
    def get_generation_progress(self, job_id: str) -> dict:
        """Get real-time progress for job."""
        return self.ui_feedback.get_progress_update(job_id)
    
    def regenerate_html_from_cache(self, job_directory: str, job_data: dict, resume_data: dict = None) -> dict:
        """
        Regenerate HTML and PDF files using cached AI content.
        
        Args:
            job_directory: Path to job directory containing cached content
            job_data: Job information for template rendering
            
        Returns:
            Dict containing regenerated HTML content and metadata
        """
        try:
            logger.info(f"Regenerating HTML from cached content in: {job_directory}")
            
            # Initialize cache
            cache = AIContentCache(job_directory)
            
            # Check if cache has content
            cached_sections = cache.get_cached_sections()
            if not cached_sections:
                raise Exception("No cached AI content found in job directory")
            
            # Load all cached content
            section_results = cache.load_all_content()
            logger.info(f"Loaded {len(section_results)} sections from cache: {list(section_results.keys())}")
            
            # Aggregate content
            aggregated_content = self.content_aggregator.aggregate_sections(section_results, resume_data)
            
            # Render templates
            html_resume = self.template_engine.render_resume(aggregated_content)
            html_cover_letter = self.template_engine.render_cover_letter(aggregated_content, job_data)
            
            # Convert to PDF
            pdf_results = self.pdf_manager.convert_modular_output([html_resume, html_cover_letter])
            
            result = {
                'success': True,
                'html_resume': html_resume,
                'html_cover_letter': html_cover_letter,
                'pdf_results': pdf_results,
                'generation_method': 'cached_content',
                'sections_used': list(section_results.keys()),
                'cache_info': cache.get_cache_info(),
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'regenerated_from_cache': True,
                    'job_directory': job_directory
                }
            }
            
            logger.info("Successfully regenerated HTML/PDF from cached content")
            return result
            
        except Exception as e:
            logger.error(f"Error regenerating from cache: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'generation_method': 'cached_content_failed'
            }
    
    def generate_resume_legacy(self, resume_data: dict, job_data: dict) -> str:
        """
        Public interface for legacy generation (backward compatibility).
        
        Returns:
            HTML string (legacy format)
        """
        job_id = f"legacy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = self._generate_resume_legacy(resume_data, job_data, job_id)
        
        if result.get('success'):
            return result.get('html_resume', '')
        else:
            raise Exception(f"Legacy generation failed: {result.get('error', 'Unknown error')}")