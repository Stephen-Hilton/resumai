#!/usr/bin/env python3
"""
Parallel Executor - Manages concurrent execution of section generators

This module provides concurrent execution capabilities for section generators,
with timeout handling and progress tracking.
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
import threading

logger = logging.getLogger(__name__)

class ParallelExecutor:
    """
    Executes multiple section generators concurrently with timeout handling.
    
    Provides both asyncio-based and thread-based parallel execution options
    with comprehensive error handling and progress tracking.
    """
    
    def __init__(self, max_workers: int = 6, default_timeout: int = 960):
        """
        Initialize parallel executor.
        
        Args:
            max_workers: Maximum number of concurrent workers
            default_timeout: Default timeout per section in seconds (16 minutes to allow for exponential backoff)
        """
        self.max_workers = max_workers
        self.default_timeout = default_timeout
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def execute_parallel(self, generators: List, resume_data: dict, job_data: dict, 
                        progress_callback: Optional[Callable] = None, use_cache: bool = True) -> Dict[str, Any]:
        """
        Execute section generators in parallel with timeout handling.
        
        Args:
            generators: List of section generator instances
            resume_data: Resume information from YAML file
            job_data: Job description and requirements
            progress_callback: Optional callback for progress updates
            use_cache: Whether to use cached content when available
            
        Returns:
            Dictionary mapping section names to results
        """
        if not generators:
            self.logger.warning("No generators provided for parallel execution")
            return {}
        
        self.logger.info(f"Starting parallel execution of {len(generators)} sections (cache: {use_cache})")
        start_time = time.time()
        
        # Use thread-based execution for better compatibility with existing code
        results = self._execute_with_threads(generators, resume_data, job_data, progress_callback, use_cache)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Parallel execution completed in {execution_time:.2f} seconds")
        
        return results
    
    def _execute_with_threads(self, generators: List, resume_data: dict, job_data: dict,
                             progress_callback: Optional[Callable] = None, use_cache: bool = True) -> Dict[str, Any]:
        """Execute generators using ThreadPoolExecutor."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_generator = {}
            
            for generator in generators:
                if progress_callback:
                    progress_callback(generator.section_name, 0.0, "starting")
                
                future = executor.submit(
                    self._execute_single_generator,
                    generator, resume_data, job_data, use_cache
                )
                future_to_generator[future] = generator
            
            # Collect results as they complete
            for future in as_completed(future_to_generator, timeout=self.default_timeout * 3):
                generator = future_to_generator[future]
                section_name = generator.section_name
                
                try:
                    result = future.result(timeout=self.default_timeout)
                    results[section_name] = {
                        'content': result,
                        'status': 'completed',
                        'generator': generator.__class__.__name__,
                        'execution_time': getattr(result, '_execution_time', None)
                    }
                    
                    if progress_callback:
                        progress_callback(section_name, 1.0, "completed")
                    
                    self.logger.info(f"Section '{section_name}' completed successfully")
                    
                except TimeoutError:
                    self.logger.error(f"Section '{section_name}' timed out after {self.default_timeout}s")
                    results[section_name] = {
                        'content': None,
                        'status': 'timeout',
                        'error': f"Timeout after {self.default_timeout} seconds",
                        'generator': generator.__class__.__name__
                    }
                    
                    if progress_callback:
                        progress_callback(section_name, 0.0, "timeout")
                
                except Exception as e:
                    self.logger.error(f"Section '{section_name}' failed: {str(e)}", exc_info=True)
                    results[section_name] = {
                        'content': None,
                        'status': 'failed',
                        'error': str(e),
                        'generator': generator.__class__.__name__
                    }
                    
                    if progress_callback:
                        progress_callback(section_name, 0.0, "failed")
        
        return results
    
    def _execute_single_generator(self, generator, resume_data: dict, job_data: dict, use_cache: bool = True) -> Any:
        """
        Execute a single generator with timing and error handling.
        
        Args:
            generator: Section generator instance
            resume_data: Resume data
            job_data: Job data
            use_cache: Whether to use cached content when available
            
        Returns:
            Generated content
        """
        start_time = time.time()
        
        try:
            self.logger.debug(f"Starting generation for section: {generator.section_name}")
            
            # Execute the generator with caching support
            if hasattr(generator, 'generate_with_cache') and use_cache:
                content = generator.generate_with_cache(resume_data, job_data, force_regenerate=not use_cache)
            else:
                content = generator.generate_content(resume_data, job_data)
            
            # Validate the content
            if not generator.validate_content(content):
                raise ValueError(f"Generated content validation failed for {generator.section_name}")
            
            execution_time = time.time() - start_time
            
            # Log differently for LLM vs non-LLM generators
            if hasattr(generator, 'get_prompt_template') and generator.get_prompt_template().strip():
                self.logger.info(f"LLM section '{generator.section_name}' generated in {execution_time:.2f}s")
            else:
                self.logger.debug(f"Non-LLM section '{generator.section_name}' processed in {execution_time:.2f}s")
            
            # Attach execution time to result
            if isinstance(content, dict):
                content['_execution_time'] = execution_time
            
            return content
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Generator '{generator.section_name}' failed after {execution_time:.2f}s: {str(e)}")
            raise
    
    def execute_with_progress(self, generators: List, resume_data: dict, job_data: dict,
                            progress_callback: Callable) -> Dict[str, Any]:
        """
        Execute with real-time progress updates.
        
        This is an alias for execute_parallel with required progress callback.
        
        Args:
            generators: List of section generator instances
            resume_data: Resume information
            job_data: Job description
            progress_callback: Callback for progress updates (required)
            
        Returns:
            Dictionary mapping section names to results
        """
        if not progress_callback:
            raise ValueError("progress_callback is required for execute_with_progress")
        
        return self.execute_parallel(generators, resume_data, job_data, progress_callback)
    
    async def execute_async(self, generators: List, resume_data: dict, job_data: dict,
                           progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Execute generators using asyncio (alternative implementation).
        
        Args:
            generators: List of section generator instances
            resume_data: Resume information
            job_data: Job description
            progress_callback: Optional progress callback
            
        Returns:
            Dictionary mapping section names to results
        """
        if not generators:
            return {}
        
        self.logger.info(f"Starting async execution of {len(generators)} sections")
        
        # Create tasks for each generator
        tasks = []
        for generator in generators:
            if progress_callback:
                progress_callback(generator.section_name, 0.0, "starting")
            
            task = asyncio.create_task(
                self._execute_generator_async(generator, resume_data, job_data)
            )
            tasks.append((task, generator))
        
        # Wait for all tasks to complete with timeout
        results = {}
        
        for task, generator in tasks:
            section_name = generator.section_name
            
            try:
                content = await asyncio.wait_for(task, timeout=self.default_timeout)
                results[section_name] = {
                    'content': content,
                    'status': 'completed',
                    'generator': generator.__class__.__name__
                }
                
                if progress_callback:
                    progress_callback(section_name, 1.0, "completed")
                
            except asyncio.TimeoutError:
                self.logger.error(f"Async section '{section_name}' timed out")
                results[section_name] = {
                    'content': None,
                    'status': 'timeout',
                    'error': f"Async timeout after {self.default_timeout} seconds",
                    'generator': generator.__class__.__name__
                }
                
                if progress_callback:
                    progress_callback(section_name, 0.0, "timeout")
            
            except Exception as e:
                self.logger.error(f"Async section '{section_name}' failed: {str(e)}")
                results[section_name] = {
                    'content': None,
                    'status': 'failed',
                    'error': str(e),
                    'generator': generator.__class__.__name__
                }
                
                if progress_callback:
                    progress_callback(section_name, 0.0, "failed")
        
        return results
    
    async def _execute_generator_async(self, generator, resume_data: dict, job_data: dict) -> Any:
        """Execute a single generator asynchronously."""
        loop = asyncio.get_event_loop()
        
        # Run the generator in a thread pool to avoid blocking
        return await loop.run_in_executor(
            None, 
            self._execute_single_generator,
            generator, resume_data, job_data
        )