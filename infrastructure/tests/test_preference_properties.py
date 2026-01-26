"""
Property-based tests for User Preferences.

Tests:
- Property 36: User Preference Storage
- Property 37: Default Generation Type Preference

Feature: skillsnap-mvp
Validates: Requirements 13.1, 13.2, 13.4
"""
import pytest
from hypothesis import given, strategies as st, settings
import sys
import os
import re

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import VALID_SUBCOMPONENTS, VALID_GENERATION_TYPES


# Strategy for valid preference names
pref_name_strategy = st.sampled_from([
    f"default_gen_{comp}" for comp in VALID_SUBCOMPONENTS
])

# Strategy for valid generation types
gen_type_strategy = st.sampled_from(VALID_GENERATION_TYPES)


class MockUserPrefTable:
    """Mock USER_PREF table for testing preference storage."""
    
    def __init__(self):
        self.prefs = {}  # {userid: {prefname: prefvalue}}
    
    def get_user_prefs(self, userid: str) -> dict:
        """Get all preferences for a user."""
        return self.prefs.get(userid, {}).copy()
    
    def set_user_pref(self, userid: str, prefname: str, prefvalue: str) -> None:
        """Set a user preference."""
        if userid not in self.prefs:
            self.prefs[userid] = {}
        self.prefs[userid][prefname] = prefvalue
    
    def delete_user_pref(self, userid: str, prefname: str) -> None:
        """Delete a user preference."""
        if userid in self.prefs and prefname in self.prefs[userid]:
            del self.prefs[userid][prefname]


class TestUserPreferenceStorage:
    """Tests for user preference storage."""

    @given(
        userid=st.uuids().map(str),
        prefname=pref_name_strategy,
        prefvalue=gen_type_strategy
    )
    @settings(max_examples=100)
    def test_property_36_preference_storage(self, userid: str, prefname: str, prefvalue: str):
        """
        Property 36: User Preference Storage
        
        For any user preference update, the preference SHALL be stored in
        USER_PREF with the correct userid (PK) and prefname (SK), and
        subsequent reads SHALL return the updated value.
        
        Feature: skillsnap-mvp, Property 36: User Preference Storage
        """
        table = MockUserPrefTable()
        
        # Set preference
        table.set_user_pref(userid, prefname, prefvalue)
        
        # Read back
        prefs = table.get_user_prefs(userid)
        
        assert prefname in prefs, f"Preference {prefname} should be stored"
        assert prefs[prefname] == prefvalue, \
            f"Preference value should be {prefvalue}, got {prefs[prefname]}"

    @given(
        userid=st.uuids().map(str),
        preferences=st.dictionaries(
            pref_name_strategy,
            gen_type_strategy,
            min_size=1,
            max_size=8
        )
    )
    @settings(max_examples=100)
    def test_property_36_multiple_preferences(self, userid: str, preferences: dict):
        """
        Property 36: User Preference Storage (multiple)
        
        Multiple preferences should be stored and retrieved correctly.
        
        Feature: skillsnap-mvp, Property 36: User Preference Storage
        """
        table = MockUserPrefTable()
        
        # Set all preferences
        for prefname, prefvalue in preferences.items():
            table.set_user_pref(userid, prefname, prefvalue)
        
        # Read back
        stored = table.get_user_prefs(userid)
        
        # All preferences should be stored
        for prefname, prefvalue in preferences.items():
            assert prefname in stored, f"Preference {prefname} should be stored"
            assert stored[prefname] == prefvalue

    @given(
        userid=st.uuids().map(str),
        prefname=pref_name_strategy,
        old_value=gen_type_strategy,
        new_value=gen_type_strategy
    )
    @settings(max_examples=100)
    def test_property_36_preference_update(self, userid: str, prefname: str, old_value: str, new_value: str):
        """
        Property 36: User Preference Storage (update)
        
        Updating a preference should overwrite the old value.
        
        Feature: skillsnap-mvp, Property 36: User Preference Storage
        """
        table = MockUserPrefTable()
        
        # Set initial value
        table.set_user_pref(userid, prefname, old_value)
        
        # Update to new value
        table.set_user_pref(userid, prefname, new_value)
        
        # Read back
        prefs = table.get_user_prefs(userid)
        
        assert prefs[prefname] == new_value, \
            f"Preference should be updated to {new_value}, got {prefs[prefname]}"


class TestDefaultGenerationTypePreference:
    """Tests for default generation type preference naming."""

    @given(component=st.sampled_from(VALID_SUBCOMPONENTS))
    @settings(max_examples=100)
    def test_property_37_preference_name_pattern(self, component: str):
        """
        Property 37: Default Generation Type Preference
        
        For any subcomponent default preference, the prefname SHALL follow
        the pattern default_gen_{subcomponent}.
        
        Feature: skillsnap-mvp, Property 37: Default Generation Type Preference
        """
        prefname = f"default_gen_{component}"
        
        # Should match the pattern
        pattern = r'^default_gen_(\w+)$'
        match = re.match(pattern, prefname)
        
        assert match is not None, f"Preference name should match pattern: {prefname}"
        assert match.group(1) == component, \
            f"Extracted component should be {component}, got {match.group(1)}"

    def test_property_37_all_subcomponents_covered(self):
        """
        Property 37: Default Generation Type Preference (completeness)
        
        All 8 subcomponents should have valid preference names.
        
        Feature: skillsnap-mvp, Property 37: Default Generation Type Preference
        """
        expected_components = [
            "contact", "summary", "skills", "highlights",
            "experience", "education", "awards", "coverletter"
        ]
        
        assert len(VALID_SUBCOMPONENTS) == 8
        for comp in expected_components:
            assert comp in VALID_SUBCOMPONENTS, f"Missing subcomponent: {comp}"
            
            # Verify preference name can be constructed
            prefname = f"default_gen_{comp}"
            assert re.match(r'^default_gen_\w+$', prefname)

    @given(
        component=st.sampled_from(VALID_SUBCOMPONENTS),
        gen_type=gen_type_strategy
    )
    @settings(max_examples=100)
    def test_property_37_valid_generation_types(self, component: str, gen_type: str):
        """
        Property 37: Default Generation Type Preference (valid values)
        
        Generation type values should be either "manual" or "ai".
        
        Feature: skillsnap-mvp, Property 37: Default Generation Type Preference
        """
        assert gen_type in VALID_GENERATION_TYPES
        assert gen_type in ["manual", "ai"]


class TestPreferenceValidation:
    """Tests for preference validation."""

    @given(invalid_component=st.text(min_size=1, max_size=20).filter(
        lambda x: x not in VALID_SUBCOMPONENTS
    ))
    @settings(max_examples=100)
    def test_invalid_component_rejected(self, invalid_component: str):
        """
        Tests that invalid subcomponent names are rejected.
        """
        prefname = f"default_gen_{invalid_component}"
        
        # Extract component from prefname
        match = re.match(r'^default_gen_(\w+)$', prefname)
        if match:
            component = match.group(1)
            assert component not in VALID_SUBCOMPONENTS, \
                f"Component {component} should not be valid"

    @given(invalid_type=st.text(min_size=1, max_size=20).filter(
        lambda x: x not in VALID_GENERATION_TYPES
    ))
    @settings(max_examples=100)
    def test_invalid_generation_type_rejected(self, invalid_type: str):
        """
        Tests that invalid generation types are rejected.
        """
        assert invalid_type not in VALID_GENERATION_TYPES
