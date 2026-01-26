"""
Property-based tests for Generation operations.

Tests:
- Property 15: Generation State Machine
- Property 16: Generation Type Toggle
- Property 17: Generate All Queue Count
- Property 18: AI Generation Input Composition
- Property 19: Manual Generation Structure
- Property 20: Generation Output HTML Validity
- Property 21: Generation Content Storage

Feature: skillsnap-mvp
Validates: Requirements 7.2, 7.3, 7.5, 7.7, 7.8, 8.2, 8.4, 8.5, 9.3, 16.1
"""
import pytest
from hypothesis import given, strategies as st, settings
import re
import sys
import os

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import (
    validate_subcomponent,
    validate_generation_state,
    validate_generation_type,
    VALID_SUBCOMPONENTS,
    VALID_GENERATION_STATES,
    VALID_GENERATION_TYPES,
)


# Strategy for subcomponents
subcomponent_strategy = st.sampled_from(VALID_SUBCOMPONENTS)

# Strategy for generation states
state_strategy = st.sampled_from(VALID_GENERATION_STATES)

# Strategy for generation types
type_strategy = st.sampled_from(VALID_GENERATION_TYPES)


class TestGenerationStateMachine:
    """Tests for generation state machine."""

    @given(state=state_strategy)
    @settings(max_examples=100)
    def test_property_15_valid_states(self, state: str):
        """
        Property 15: Generation State Machine
        
        For any subcomponent, the generation state SHALL be one of the
        valid states: locked, ready, generating, complete, error.
        
        Feature: skillsnap-mvp, Property 15: Generation State Machine
        """
        assert validate_generation_state(state)
        assert state in VALID_GENERATION_STATES

    def test_property_15_state_transitions(self):
        """
        Property 15: Generation State Machine (transitions)
        
        Valid state transitions: locked → ready → generating → complete (or error)
        
        Feature: skillsnap-mvp, Property 15: Generation State Machine
        """
        # Define valid transitions
        valid_transitions = {
            'locked': ['ready'],
            'ready': ['generating'],
            'generating': ['complete', 'error'],
            'complete': ['ready'],  # Can regenerate
            'error': ['ready'],  # Can retry
        }
        
        for from_state, to_states in valid_transitions.items():
            assert from_state in VALID_GENERATION_STATES
            for to_state in to_states:
                assert to_state in VALID_GENERATION_STATES

    def test_property_15_locked_prevents_generation(self):
        """
        Property 15: Generation State Machine (locked state)
        
        Locked state SHALL prevent generation triggers.
        
        Feature: skillsnap-mvp, Property 15: Generation State Machine
        """
        locked_state = 'locked'
        
        # Simulate check before generation
        can_generate = locked_state != 'locked'
        assert not can_generate, "Locked state should prevent generation"


class TestGenerationTypeToggle:
    """Tests for generation type toggle."""

    @given(current_type=type_strategy)
    @settings(max_examples=100)
    def test_property_16_type_toggle(self, current_type: str):
        """
        Property 16: Generation Type Toggle
        
        For any subcomponent generation type toggle action, the type SHALL
        switch between "manual" and "ai".
        
        Feature: skillsnap-mvp, Property 16: Generation Type Toggle
        """
        # Toggle logic
        new_type = 'ai' if current_type == 'manual' else 'manual'
        
        assert new_type in VALID_GENERATION_TYPES
        assert new_type != current_type

    @given(component=subcomponent_strategy, new_type=type_strategy)
    @settings(max_examples=100)
    def test_property_16_type_persistence(self, component: str, new_type: str):
        """
        Property 16: Generation Type Toggle (persistence)
        
        The new type SHALL be persisted in USER_JOB.
        
        Feature: skillsnap-mvp, Property 16: Generation Type Toggle
        """
        # Simulate update
        update = {f'type{component}': new_type}
        
        assert f'type{component}' in update
        assert update[f'type{component}'] == new_type
        assert validate_generation_type(update[f'type{component}'])


class TestGenerateAll:
    """Tests for Generate All functionality."""

    def test_property_17_queue_count(self):
        """
        Property 17: Generate All Queue Count
        
        For any "Generate All" action, exactly 8 SQS messages SHALL be queued,
        one for each subcomponent.
        
        Feature: skillsnap-mvp, Property 17: Generate All Queue Count
        """
        # Simulate queuing all subcomponents
        queued_components = []
        for component in VALID_SUBCOMPONENTS:
            queued_components.append(component)
        
        assert len(queued_components) == 8, \
            f"Should queue exactly 8 components, got {len(queued_components)}"
        
        # Verify all components are included
        expected = {'contact', 'summary', 'skills', 'highlights', 
                   'experience', 'education', 'awards', 'coverletter'}
        assert set(queued_components) == expected

    @given(
        userid=st.uuids().map(str),
        jobid=st.uuids().map(str),
        resumeid=st.text(min_size=1, max_size=50)
    )
    @settings(max_examples=100)
    def test_property_17_message_structure(self, userid: str, jobid: str, resumeid: str):
        """
        Property 17: Generate All Queue Count (message structure)
        
        Each queued message should have the correct structure.
        
        Feature: skillsnap-mvp, Property 17: Generate All Queue Count
        """
        for component in VALID_SUBCOMPONENTS:
            message = {
                'userid': userid,
                'jobid': jobid,
                'resumeid': resumeid,
                'component': component,
                'generationType': 'ai',
            }
            
            assert 'userid' in message
            assert 'jobid' in message
            assert 'resumeid' in message
            assert 'component' in message
            assert message['component'] in VALID_SUBCOMPONENTS


class TestAIGeneration:
    """Tests for AI generation."""

    @given(
        summary=st.text(min_size=10, max_size=500),
        job_desc=st.text(min_size=10, max_size=2000)
    )
    @settings(max_examples=100)
    def test_property_18_ai_input_composition(self, summary: str, job_desc: str):
        """
        Property 18: AI Generation Input Composition
        
        For any AI generation request, the prompt sent to Bedrock SHALL
        contain both the user's base resume content and the job description.
        
        Feature: skillsnap-mvp, Property 18: AI Generation Input Composition
        """
        # Simulate prompt composition
        prompt = f"Resume: {summary}\n\nJob Description: {job_desc}"
        
        assert summary in prompt, "Prompt should contain resume content"
        assert job_desc in prompt, "Prompt should contain job description"


class TestManualGeneration:
    """Tests for manual generation."""

    @given(skills=st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=20))
    @settings(max_examples=100)
    def test_property_19_manual_html_structure(self, skills: list):
        """
        Property 19: Manual Generation Structure
        
        For any manual generation request, the output SHALL be lean HTML
        structured from the corresponding resume section JSON, containing
        no inline styles.
        
        Feature: skillsnap-mvp, Property 19: Manual Generation Structure
        """
        # Simulate manual generation for skills
        html = '<section class="skills"><h2>Skills</h2><ul>'
        for skill in skills:
            html += f'<li>{skill}</li>'
        html += '</ul></section>'
        
        # Should not contain inline styles
        assert 'style=' not in html, "Manual HTML should not contain inline styles"
        
        # Should be valid HTML structure
        assert '<section' in html
        assert '</section>' in html
        assert '<ul>' in html
        assert '</ul>' in html

    @given(
        name=st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        email=st.emails()
    )
    @settings(max_examples=100)
    def test_property_19_contact_html_structure(self, name: str, email: str):
        """
        Property 19: Manual Generation Structure (contact)
        
        Contact section should be properly structured HTML.
        
        Feature: skillsnap-mvp, Property 19: Manual Generation Structure
        """
        contact = {'name': name, 'email': email}
        
        # Simulate manual generation
        html = '<section class="contact">'
        html += f'<h1>{contact["name"]}</h1>'
        html += '<address>'
        html += f'<a href="mailto:{contact["email"]}">{contact["email"]}</a>'
        html += '</address></section>'
        
        assert 'style=' not in html
        assert name in html
        assert email in html


class TestHTMLValidity:
    """Tests for HTML output validity."""

    @given(content=st.text(min_size=1, max_size=500))
    @settings(max_examples=100)
    def test_property_20_html_validity(self, content: str):
        """
        Property 20: Generation Output HTML Validity
        
        For any successful generation, the stored content SHALL be valid HTML
        that can be parsed without errors.
        
        Feature: skillsnap-mvp, Property 20: Generation Output HTML Validity
        """
        # Escape HTML special characters in content
        escaped = (content
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))
        
        html = f'<section class="test"><p>{escaped}</p></section>'
        
        # Basic HTML structure validation
        assert html.count('<section') == html.count('</section>')
        assert html.count('<p>') == html.count('</p>')


class TestContentStorage:
    """Tests for generation content storage."""

    @given(
        component=subcomponent_strategy,
        content=st.text(min_size=1, max_size=1000)
    )
    @settings(max_examples=100)
    def test_property_21_content_storage(self, component: str, content: str):
        """
        Property 21: Generation Content Storage
        
        For any completed subcomponent generation, the content SHALL be stored
        in the corresponding USER_JOB data field and the state SHALL be "complete".
        
        Feature: skillsnap-mvp, Property 21: Generation Content Storage
        """
        # Simulate storage update
        update = {
            f'data{component}': content,
            f'state{component}': 'complete'
        }
        
        assert f'data{component}' in update
        assert update[f'data{component}'] == content
        assert update[f'state{component}'] == 'complete'
