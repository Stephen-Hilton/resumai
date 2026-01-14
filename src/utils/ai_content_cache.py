#!/usr/bin/env python3
"""
AI Content Cache - Saves and loads AI-generated content for future use

This module handles saving AI-generated content to files in job directories
and loading that content for downstream processes like HTML/PDF regeneration.
"""

import logging
import yaml
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class AIContentCache:
    """
    Manages saving and loading AI-generated content to/from job directories.
    
    Content is saved in structured YAML files within each job's directory,
    allowing for future editing and reuse without re-running AI generation.
    """
    
    def __init__(self, job_directory: str):
        """
        Initialize cache for a specific job directory.
        
        Args:
            job_directory: Path to the job directory (e.g., src/jobs/2_generated/JobName.ID.Timestamp/)
        """
        self.job_directory = Path(job_directory)
        self.cache_dir = self.job_directory / "ai_content"
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Ensure job directory exists first
        self.job_directory.mkdir(parents=True, exist_ok=True)
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def save_section_content(self, section_name: str, content: dict, metadata: Optional[dict] = None) -> bool:
        """
        Save AI-generated content for a specific section.
        
        Args:
            section_name: Name of the section (e.g., "summary", "skills", "experience")
            content: The AI-generated content dictionary
            metadata: Optional metadata about the generation (timestamps, model used, etc.)
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            cache_file = self.cache_dir / f"{section_name}.yaml"
            
            # Prepare data structure
            cache_data = {
                'section_name': section_name,
                'generated_at': datetime.now().isoformat(),
                'content': content,
                'metadata': metadata or {}
            }
            
            # Add generation metadata
            cache_data['metadata'].update({
                'cache_version': '1.0',
                'generator_type': 'ai_generated',
                'editable': True
            })
            
            # Save to YAML file
            with open(cache_file, 'w', encoding='utf-8') as f:
                yaml.dump(cache_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            self.logger.info(f"Saved AI content for section '{section_name}' to {cache_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving AI content for section '{section_name}': {str(e)}")
            return False
    
    def load_section_content(self, section_name: str) -> Optional[dict]:
        """
        Load AI-generated content for a specific section.
        
        Args:
            section_name: Name of the section to load
            
        Returns:
            Content dictionary if found, None otherwise
        """
        try:
            cache_file = self.cache_dir / f"{section_name}.yaml"
            
            if not cache_file.exists():
                self.logger.debug(f"No cached content found for section '{section_name}'")
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = yaml.safe_load(f)
            
            if not isinstance(cache_data, dict) or 'content' not in cache_data:
                self.logger.error(f"Invalid cache data structure for section '{section_name}'")
                return None
            
            self.logger.info(f"Loaded cached AI content for section '{section_name}'")
            return cache_data['content']
            
        except Exception as e:
            self.logger.error(f"Error loading AI content for section '{section_name}': {str(e)}")
            return None
    
    def has_cached_content(self, section_name: str) -> bool:
        """
        Check if cached content exists for a section.
        
        Args:
            section_name: Name of the section to check
            
        Returns:
            True if cached content exists, False otherwise
        """
        cache_file = self.cache_dir / f"{section_name}.yaml"
        return cache_file.exists()
    
    def get_cached_sections(self) -> List[str]:
        """
        Get list of sections that have cached content.
        
        Returns:
            List of section names with cached content
        """
        try:
            if not self.cache_dir.exists():
                return []
            
            sections = []
            for cache_file in self.cache_dir.glob("*.yaml"):
                section_name = cache_file.stem
                sections.append(section_name)
            
            return sorted(sections)
            
        except Exception as e:
            self.logger.error(f"Error getting cached sections: {str(e)}")
            return []
    
    def save_all_content(self, section_results: Dict[str, Any]) -> bool:
        """
        Save all section results to cache.
        
        Args:
            section_results: Dictionary mapping section names to their results
            
        Returns:
            True if all sections saved successfully, False otherwise
        """
        success_count = 0
        total_count = 0
        
        for section_name, result in section_results.items():
            total_count += 1
            
            if result.get('status') == 'completed' and result.get('content'):
                metadata = {
                    'generator': result.get('generator', 'unknown'),
                    'status': result.get('status'),
                    'generation_method': 'ai_generated'
                }
                
                if self.save_section_content(section_name, result['content'], metadata):
                    success_count += 1
            else:
                self.logger.warning(f"Skipping cache save for failed section: {section_name}")
        
        self.logger.info(f"Saved {success_count}/{total_count} sections to cache")
        return success_count == total_count
    
    def load_all_content(self) -> Dict[str, Any]:
        """
        Load all cached content as section results.
        
        Returns:
            Dictionary mapping section names to their cached results
        """
        section_results = {}
        cached_sections = self.get_cached_sections()
        
        for section_name in cached_sections:
            content = self.load_section_content(section_name)
            if content:
                section_results[section_name] = {
                    'status': 'completed',
                    'content': content,
                    'generator': 'cached',
                    'source': 'ai_content_cache'
                }
        
        self.logger.info(f"Loaded {len(section_results)} sections from cache")
        return section_results
    
    def clear_cache(self, section_name: Optional[str] = None) -> bool:
        """
        Clear cached content.
        
        Args:
            section_name: Specific section to clear, or None to clear all
            
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            if section_name:
                # Clear specific section
                cache_file = self.cache_dir / f"{section_name}.yaml"
                if cache_file.exists():
                    cache_file.unlink()
                    self.logger.info(f"Cleared cache for section '{section_name}'")
                return True
            else:
                # Clear all cached content
                if self.cache_dir.exists():
                    for cache_file in self.cache_dir.glob("*.yaml"):
                        cache_file.unlink()
                    self.logger.info("Cleared all cached content")
                return True
                
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def count_cached_sections(self) -> int:
        """
        Count the number of cached section files.
        
        Returns:
            Number of cached section files
        """
        try:
            cached_sections = self.get_cached_sections()
            return len(cached_sections)
        except Exception as e:
            self.logger.error(f"Error counting cached sections: {str(e)}")
            return 0
    
    def should_regenerate_all(self, expected_sections: int = 7) -> bool:
        """
        Determine if all cache should be cleared and regenerated.
        
        IMPORTANT: ai_content is never automatically deleted to preserve user data.
        This method now always returns False to prevent automatic cache clearing.
        
        Args:
            expected_sections: Total number of expected sections (default 7: summary, skills, highlights, experience, education, awards, cover_letter)
            
        Returns:
            Always False - ai_content should never be automatically cleared
        """
        cached_count = self.count_cached_sections()
        
        # NEVER automatically clear ai_content - preserve user data
        self.logger.info(f"Found {cached_count}/{expected_sections} sections cached. ai_content will be preserved.")
        return False
    
    def get_missing_sections(self, all_sections: List[str]) -> List[str]:
        """
        Get list of sections that are missing from cache.
        
        Args:
            all_sections: List of all expected section names
            
        Returns:
            List of section names that are not cached
        """
        try:
            cached_sections = self.get_cached_sections()
            missing_sections = [section for section in all_sections if section not in cached_sections]
            
            self.logger.info(f"Missing sections: {missing_sections}")
            return missing_sections
            
        except Exception as e:
            self.logger.error(f"Error getting missing sections: {str(e)}")
            return all_sections  # Return all sections if error occurs
    
    def clear_all_cache(self) -> bool:
        """
        Clear all cached content (convenience method for smart caching).
        
        Returns:
            True if cleared successfully, False otherwise
        """
        return self.clear_cache()

    def get_cache_info(self) -> dict:
        """
        Get information about cached content.
        
        Returns:
            Dictionary with cache statistics and metadata
        """
        try:
            cached_sections = self.get_cached_sections()
            cache_info = {
                'cache_directory': str(self.cache_dir),
                'total_sections': len(cached_sections),
                'cached_sections': cached_sections,
                'cache_exists': self.cache_dir.exists(),
                'sections_detail': {}
            }
            
            # Get detailed info for each section
            for section_name in cached_sections:
                cache_file = self.cache_dir / f"{section_name}.yaml"
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = yaml.safe_load(f)
                    
                    cache_info['sections_detail'][section_name] = {
                        'generated_at': cache_data.get('generated_at'),
                        'file_size': cache_file.stat().st_size,
                        'metadata': cache_data.get('metadata', {})
                    }
                except Exception:
                    cache_info['sections_detail'][section_name] = {
                        'error': 'Could not read cache file'
                    }
            
            return cache_info
            
        except Exception as e:
            self.logger.error(f"Error getting cache info: {str(e)}")
            return {'error': str(e)}
    
    def update_section_content(self, section_name: str, updated_content: dict) -> bool:
        """
        Update cached content for a section (for future user editing capability).
        
        Args:
            section_name: Name of the section to update
            updated_content: New content to save
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            cache_file = self.cache_dir / f"{section_name}.yaml"
            
            # Load existing metadata if file exists
            existing_metadata = {}
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    existing_data = yaml.safe_load(f)
                    existing_metadata = existing_data.get('metadata', {})
            
            # Update metadata
            existing_metadata.update({
                'last_updated': datetime.now().isoformat(),
                'manually_edited': True
            })
            
            return self.save_section_content(section_name, updated_content, existing_metadata)
            
        except Exception as e:
            self.logger.error(f"Error updating section content '{section_name}': {str(e)}")
            return False

def create_cache_for_job(job_directory: str) -> AIContentCache:
    """
    Factory function to create an AIContentCache for a job directory.
    
    Args:
        job_directory: Path to the job directory
        
    Returns:
        AIContentCache instance
    """
    return AIContentCache(job_directory)

def get_job_directory_from_id(job_id: str, base_path: str = "src/jobs/2_generated") -> Optional[str]:
    """
    Find job directory path from job ID.
    
    Args:
        job_id: Job identifier (e.g., "Ladders.Senior_Vice_President_of_Global_Support_and_Custom.4350514507.20251227085032")
        base_path: Base path to search for job directories
        
    Returns:
        Full path to job directory if found, None otherwise
    """
    try:
        base_dir = Path(base_path)
        if not base_dir.exists():
            return None
        
        # Look for directory that matches or contains the job_id
        for job_dir in base_dir.iterdir():
            if job_dir.is_dir() and job_id in job_dir.name:
                return str(job_dir)
        
        return None
        
    except Exception as e:
        logger.error(f"Error finding job directory for ID '{job_id}': {str(e)}")
        return None