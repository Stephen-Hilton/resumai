#!/usr/bin/env python3
"""
Property tests for modular architecture setup

Tests the fundamental properties of the modular resume generation system.
"""

import pytest
import asyncio
import time
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.modular_generator import ModularResumeGenerator
from utils.modular_config import ModularConfig, get_config
from utils.section_generators import SectionManager, SectionType, SectionConfig

class TestModularArchitectureProperties:
    """Property-based tests for modular architecture setup."""
    
    def setup_method(self):
        """Set up test environment."""
        self.config = ModularConfig()
        self.config.set('use_modular_generation', True)
        self.config.set('enable_parallel_processing', True)
    
    @given(
        resume_data=st.dictionaries(
            keys=st.sampled_from(['name', 'Summary', 'skills', 'experience', 'education', 'awards_and_keynotes']),
            values=st.one_of(
                st.text(min_size=1, max_size=100),
                st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=10),
                st.lists(st.dictionaries(
                    keys=st.sampled_from(['company_name', 'dates', 'roles']),
                    values=st.text(min_size=1, max_size=50)
                ), min_size=1, max_size=5)
            ),
            min_size=1
        ),
        job_data=st.dictionaries(
            keys=st.sampled_from(['title', 'company', 'description', 'location']),
            values=st.text(min_size=1, max_size=200),
            min_size=1
        )
    )
    @settings(max_examples=100, deadline=30000)  # 30 second deadline for each test
    def test_parallel_section_generation_property(self, resume_data, job_data):
        """
        Property 1: Parallel section generation
        For any resume generation request, the system should create multiple concurrent 
        LLM requests for different sections rather than a single monolithic request.
        
        **Feature: modular-resume-generation, Property 1: Parallel section generation**
        **Validates: Requirements 1.1, 2.1, 5.2**
        """
        # Mock the LLM calls to track how many are made
        llm_calls = []
        
        def mock_llm_call(*args, **kwargs):
            llm_calls.append({
                'timestamp': time.time(),
                'args': args,
                'kwargs': kwargs
            })
            return "summary: 'Test summary content for validation'"
        
        with patch('src.step2_generate.llm_call', side_effect=mock_llm_call):
            # Create modular generator
            generator = ModularResumeGenerator(self.config.to_dict())
            
            # Mock the components to avoid actual LLM calls
            generator.section_manager = Mock()
            generator.parallel_executor = Mock()
            generator.content_aggregator = Mock()
            generator.template_engine = Mock()
            generator.ui_feedback = Mock()
            generator.pdf_manager = Mock()
            
            # Set up section manager to return multiple sections
            mock_sections = [
                SectionConfig(SectionType.SUMMARY, priority=1),
                SectionConfig(SectionType.SKILLS, priority=2),
                SectionConfig(SectionType.EXPERIENCE, priority=3),
                SectionConfig(SectionType.COVER_LETTER, priority=4)
            ]
            generator.section_manager.identify_sections.return_value = mock_sections
            
            # Mock generators
            mock_generators = [Mock() for _ in mock_sections]
            for i, mock_gen in enumerate(mock_generators):
                mock_gen.section_name = mock_sections[i].section_type.value
            generator.section_manager.create_section_generators.return_value = mock_generators
            
            # Mock parallel executor to simulate multiple section processing
            def mock_execute_parallel(generators, resume_data, job_data, progress_callback=None):
                results = {}
                for gen in generators:
                    results[gen.section_name] = {
                        'content': {'test': 'content'},
                        'status': 'completed'
                    }
                return results
            
            generator.parallel_executor.execute_parallel.side_effect = mock_execute_parallel
            
            # Mock other components
            generator.content_aggregator.aggregate_sections.return_value = {'aggregated': 'content'}
            generator.template_engine.render_resume.return_value = '<html>resume</html>'
            generator.template_engine.render_cover_letter.return_value = '<html>cover letter</html>'
            generator.pdf_manager.convert_modular_output.return_value = {'success': True}
            
            # Generate resume
            result = generator.generate_resume(resume_data, job_data)
            
            # Verify multiple sections were identified and processed
            generator.section_manager.identify_sections.assert_called_once_with(resume_data)
            generator.section_manager.create_section_generators.assert_called_once()
            
            # Verify parallel execution was used (not sequential)
            generator.parallel_executor.execute_parallel.assert_called_once()
            
            # Verify multiple sections were processed
            sections_processed = generator.parallel_executor.execute_parallel.call_args[0][0]
            assert len(sections_processed) >= 2, "Should process multiple sections in parallel"
            
            # Verify result indicates modular generation
            assert result['success'] is True
            assert result['generation_method'] == 'modular'
            assert 'sections_generated' in result
            assert len(result['sections_generated']) >= 2
    
    @given(
        section_count=st.integers(min_value=2, max_value=6)
    )
    @settings(max_examples=50)
    def test_section_manager_creates_multiple_generators(self, section_count):
        """
        Test that SectionManager creates appropriate generators for different sections.
        """
        # Create mock resume data with varying sections
        resume_data = {'name': 'Test User', 'Summary': 'Test summary'}
        
        if section_count >= 3:
            resume_data['skills'] = ['Python', 'JavaScript']
        if section_count >= 4:
            resume_data['experience'] = [{'company_name': 'Test Corp', 'roles': []}]
        if section_count >= 5:
            resume_data['education'] = [{'course': 'Computer Science', 'school': 'Test University'}]
        if section_count >= 6:
            resume_data['awards_and_keynotes'] = [{'award': 'Test Award'}]
        
        section_manager = SectionManager()
        
        # Identify sections
        sections = section_manager.identify_sections(resume_data)
        
        # Should always have at least summary, skills, and cover_letter
        assert len(sections) >= 3
        
        # Create generators
        generators = section_manager.create_section_generators(sections)
        
        # Should create generator for each section
        assert len(generators) == len(sections)
        
        # Each generator should have a section name
        section_names = [gen.section_name for gen in generators]
        assert 'summary' in section_names
        assert 'skills' in section_names
        assert 'cover_letter' in section_names
    
    def test_configuration_system_properties(self):
        """
        Test that configuration system properly manages modular vs legacy settings.
        """
        config = ModularConfig()
        
        # Test default configuration
        assert config.is_modular_enabled() is True
        assert config.is_parallel_enabled() is True
        
        # Test runtime configuration changes
        config.enable_modular_generation(False)
        assert config.is_modular_enabled() is False
        
        config.enable_parallel_processing(False)
        assert config.is_parallel_enabled() is False
        
        # Test configuration validation
        config.set('section_timeout_seconds', 5)  # Too low
        config._validate_configuration()
        assert config.get('section_timeout_seconds') == 10  # Should be corrected
        
        config.set('section_timeout_seconds', 400)  # Too high
        config._validate_configuration()
        assert config.get('section_timeout_seconds') == 300  # Should be corrected
    
    @given(
        modular_enabled=st.booleans(),
        parallel_enabled=st.booleans()
    )
    @settings(max_examples=20)
    def test_generator_respects_configuration(self, modular_enabled, parallel_enabled):
        """
        Test that ModularResumeGenerator respects configuration settings.
        """
        config = {
            'use_modular_generation': modular_enabled,
            'enable_parallel_processing': parallel_enabled
        }
        
        generator = ModularResumeGenerator(config)
        
        assert generator.use_modular == modular_enabled
        assert generator.enable_parallel == parallel_enabled
    
    def test_fallback_to_legacy_on_failure(self):
        """
        Test that system falls back to legacy generation when modular fails.
        """
        config = {'use_modular_generation': True}
        generator = ModularResumeGenerator(config)
        
        # Mock components to simulate failure
        generator.section_manager = Mock()
        generator.section_manager.identify_sections.side_effect = Exception("Simulated failure")
        
        # Mock legacy generation
        with patch.object(generator, '_generate_resume_legacy') as mock_legacy:
            mock_legacy.return_value = {
                'success': True,
                'job_id': 'test_job',
                'html_resume': '<html>legacy resume</html>',
                'generation_method': 'legacy'
            }
            
            resume_data = {'name': 'Test User'}
            job_data = {'title': 'Test Job'}
            
            result = generator.generate_resume(resume_data, job_data, 'test_job')
            
            # Should have fallen back to legacy
            mock_legacy.assert_called_once()
            assert result['generation_method'] == 'legacy'
            assert result['success'] is True

class TestModularConfigurationProperties:
    """Property tests for configuration system."""
    
    @given(
        timeout_seconds=st.integers(min_value=1, max_value=1000),
        max_parallel=st.integers(min_value=1, max_value=20),
        update_interval=st.floats(min_value=0.1, max_value=20.0)
    )
    @settings(max_examples=50)
    def test_configuration_validation_properties(self, timeout_seconds, max_parallel, update_interval):
        """
        Test that configuration validation works correctly for various inputs.
        """
        config = ModularConfig()
        
        # Set values
        config.set('section_timeout_seconds', timeout_seconds)
        config.set('max_parallel_sections', max_parallel)
        config.set('ui_update_interval_seconds', update_interval)
        
        # Validate
        config._validate_configuration()
        
        # Check that values are within reasonable bounds
        final_timeout = config.get('section_timeout_seconds')
        assert 10 <= final_timeout <= 300
        
        final_parallel = config.get('max_parallel_sections')
        assert 1 <= final_parallel <= 10
        
        final_interval = config.get('ui_update_interval_seconds')
        assert 1.0 <= final_interval <= 10.0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])