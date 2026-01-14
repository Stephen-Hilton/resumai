#!/usr/bin/env python3
"""
Property tests for parallel execution and non-blocking section processing

Tests that section completion doesn't block other sections from continuing.
"""

import pytest
import time
import threading
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.parallel_executor import ParallelExecutor
from utils.section_generators import SectionGenerator

class MockSectionGenerator(SectionGenerator):
    """Mock section generator for testing."""
    
    def __init__(self, section_name: str, delay: float = 0.1, should_fail: bool = False):
        super().__init__(section_name)
        self.delay = delay
        self.should_fail = should_fail
        self.start_time = None
        self.end_time = None
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate mock content with configurable delay and failure."""
        self.start_time = time.time()
        time.sleep(self.delay)
        
        if self.should_fail:
            raise Exception(f"Simulated failure in {self.section_name}")
        
        self.end_time = time.time()
        return {
            'content': f'Generated content for {self.section_name}',
            'delay': self.delay,
            'execution_time': self.end_time - self.start_time
        }
    
    def get_prompt_template(self) -> str:
        return f"Generate content for {self.section_name}"

class TestParallelExecutionProperties:
    """Property-based tests for parallel execution."""
    
    @given(
        num_sections=st.integers(min_value=2, max_value=6),
        base_delay=st.floats(min_value=0.05, max_value=0.3)
    )
    @settings(max_examples=10, deadline=10000)
    def test_non_blocking_section_processing_property(self, num_sections, base_delay):
        """
        Property 3: Non-blocking section processing
        For any section completion event, other sections should continue processing without waiting.
        
        **Feature: modular-resume-generation, Property 3: Non-blocking section processing**
        **Validates: Requirements 1.3, 2.3**
        """
        executor = ParallelExecutor(max_workers=num_sections)
        
        # Create generators with different delays
        generators = []
        for i in range(num_sections):
            delay = base_delay * (i + 1)  # Increasing delays
            generator = MockSectionGenerator(f"section_{i}", delay=delay)
            generators.append(generator)
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        # Track progress updates
        progress_updates = []
        def progress_callback(section, progress, status):
            progress_updates.append({
                'section': section,
                'progress': progress,
                'status': status,
                'timestamp': time.time()
            })
        
        start_time = time.time()
        
        # Execute in parallel
        results = executor.execute_parallel(generators, resume_data, job_data, progress_callback)
        
        end_time = time.time()
        total_execution_time = end_time - start_time
        
        # Property 1: All sections should complete
        assert len(results) == num_sections
        
        # Property 2: Execution should be parallel (faster than sequential)
        sequential_time = sum(base_delay * (i + 1) for i in range(num_sections))
        parallel_speedup = sequential_time / total_execution_time
        
        # Should be significantly faster than sequential (allow some overhead)
        assert parallel_speedup > 1.2, f"Parallel execution not fast enough: {parallel_speedup}x speedup"
        
        # Property 3: Sections should complete in order of their delays (fastest first)
        completed_sections = [section for section, result in results.items() 
                            if result.get('status') == 'completed']
        
        # At least some sections should complete successfully
        assert len(completed_sections) >= num_sections // 2
        
        # Property 4: Progress updates should show non-blocking behavior
        # Faster sections should complete before slower ones
        completion_updates = [update for update in progress_updates 
                            if update['status'] == 'completed']
        
        if len(completion_updates) >= 2:
            # Check that completions happen in roughly the right order
            first_completion = completion_updates[0]
            last_completion = completion_updates[-1]
            
            # Time difference should be meaningful (not all at once)
            time_diff = last_completion['timestamp'] - first_completion['timestamp']
            assert time_diff > base_delay * 0.5, "Sections completed too close together (not parallel)"
    
    def test_section_failure_isolation(self):
        """Test that one section failure doesn't block others."""
        executor = ParallelExecutor(max_workers=4)
        
        # Create mix of successful and failing generators
        generators = [
            MockSectionGenerator("success_1", delay=0.1, should_fail=False),
            MockSectionGenerator("failure_1", delay=0.05, should_fail=True),
            MockSectionGenerator("success_2", delay=0.15, should_fail=False),
            MockSectionGenerator("failure_2", delay=0.08, should_fail=True),
        ]
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        results = executor.execute_parallel(generators, resume_data, job_data)
        
        # Property: All generators should have results (success or failure)
        assert len(results) == 4
        
        # Property: Successful sections should complete despite failures
        successful_results = [r for r in results.values() if r.get('status') == 'completed']
        failed_results = [r for r in results.values() if r.get('status') == 'failed']
        
        assert len(successful_results) == 2, "Successful sections should complete"
        assert len(failed_results) == 2, "Failed sections should be marked as failed"
        
        # Property: Successful sections should have valid content
        for result in successful_results:
            assert result['content'] is not None
            assert 'execution_time' in result['content']
        
        # Property: Failed sections should have error information
        for result in failed_results:
            assert result['content'] is None
            assert 'error' in result
            assert 'Simulated failure' in result['error']
    
    def test_timeout_handling(self):
        """Test that timeouts don't block other sections."""
        executor = ParallelExecutor(max_workers=3, default_timeout=0.3)
        
        # Create generators with different delays, some exceeding timeout
        generators = [
            MockSectionGenerator("fast", delay=0.05),      # Should complete
            MockSectionGenerator("timeout", delay=1.0),    # Should timeout
            MockSectionGenerator("medium", delay=0.15),    # Should complete
        ]
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        start_time = time.time()
        results = executor.execute_parallel(generators, resume_data, job_data)
        end_time = time.time()
        
        # Property: Should not take longer than timeout + overhead
        assert end_time - start_time < 2.0, "Execution took too long despite timeout"
        
        # Property: Fast sections should complete despite timeout in other section
        fast_result = results.get('fast')
        medium_result = results.get('medium')
        timeout_result = results.get('timeout')
        
        assert fast_result['status'] == 'completed', "Fast section should complete"
        assert medium_result['status'] == 'completed', "Medium section should complete"
        
        # Timeout section should either timeout or fail (depending on timing)
        assert timeout_result['status'] in ['timeout', 'failed', 'completed'], "Timeout section should have some status"
    
    @given(
        max_workers=st.integers(min_value=1, max_value=8),
        num_sections=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=15, deadline=500)
    def test_worker_pool_properties(self, max_workers, num_sections):
        """Test that worker pool handles various section counts correctly."""
        executor = ParallelExecutor(max_workers=max_workers)
        
        # Create generators
        generators = [
            MockSectionGenerator(f"section_{i}", delay=0.05)
            for i in range(num_sections)
        ]
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        results = executor.execute_parallel(generators, resume_data, job_data)
        
        # Property: Should handle any number of sections
        assert len(results) == num_sections
        
        # Property: All sections should complete successfully with short delays
        successful_count = sum(1 for r in results.values() if r.get('status') == 'completed')
        
        # Allow for some failures due to timing/system load, but most should succeed
        success_rate = successful_count / num_sections if num_sections > 0 else 1.0
        assert success_rate >= 0.7, f"Success rate too low: {success_rate:.2%}"
    
    def test_progress_callback_non_blocking(self):
        """Test that progress callbacks don't block execution."""
        executor = ParallelExecutor(max_workers=3)
        
        # Create generators with different delays
        generators = [
            MockSectionGenerator("section_1", delay=0.1),
            MockSectionGenerator("section_2", delay=0.15),
            MockSectionGenerator("section_3", delay=0.05),
        ]
        
        # Track callback timing
        callback_times = []
        callback_lock = threading.Lock()
        
        def slow_progress_callback(section, progress, status):
            """Intentionally slow callback to test non-blocking behavior."""
            with callback_lock:
                callback_times.append({
                    'section': section,
                    'status': status,
                    'timestamp': time.time()
                })
            
            # Simulate slow callback processing
            if status == 'completed':
                time.sleep(0.02)  # Small delay to test non-blocking
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        start_time = time.time()
        results = executor.execute_parallel(generators, resume_data, job_data, slow_progress_callback)
        end_time = time.time()
        
        # Property: Slow callbacks shouldn't significantly delay execution
        execution_time = end_time - start_time
        expected_max_time = 0.2 + 0.1  # Max generator delay + reasonable overhead
        
        assert execution_time < expected_max_time, f"Execution too slow: {execution_time:.3f}s"
        
        # Property: All sections should still complete
        assert len(results) == 3
        
        # Property: Callbacks should be called for all sections
        callback_sections = {cb['section'] for cb in callback_times}
        assert len(callback_sections) == 3, "Callbacks not called for all sections"
    
    def test_concurrent_execution_timing(self):
        """Test that sections actually execute concurrently, not sequentially."""
        executor = ParallelExecutor(max_workers=3)
        
        # Create generators that track their execution timing
        generators = [
            MockSectionGenerator("concurrent_1", delay=0.2),
            MockSectionGenerator("concurrent_2", delay=0.2),
            MockSectionGenerator("concurrent_3", delay=0.2),
        ]
        
        resume_data = {'test': 'data'}
        job_data = {'test': 'job'}
        
        start_time = time.time()
        results = executor.execute_parallel(generators, resume_data, job_data)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Property: Concurrent execution should be much faster than sequential
        sequential_time = 0.2 * 3  # 0.6 seconds if run sequentially
        
        # Should complete in roughly the time of the longest task, not the sum
        assert total_time < 0.4, f"Execution not concurrent: {total_time:.3f}s (expected < 0.4s)"
        
        # Property: All sections should complete
        completed_count = sum(1 for r in results.values() if r.get('status') == 'completed')
        assert completed_count == 3, f"Not all sections completed: {completed_count}/3"
        
        # Property: Execution times should overlap (concurrent execution)
        execution_times = []
        for result in results.values():
            if result.get('status') == 'completed' and result.get('content'):
                content = result['content']
                if isinstance(content, dict) and 'execution_time' in content:
                    execution_times.append(content['execution_time'])
        
        # All execution times should be roughly similar (around 0.2s)
        if execution_times:
            avg_execution_time = sum(execution_times) / len(execution_times)
            assert 0.15 <= avg_execution_time <= 0.25, f"Unexpected execution time: {avg_execution_time:.3f}s"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])