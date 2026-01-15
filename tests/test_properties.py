"""
Property-based tests for job application automation system.

Feature: job-application-automation
"""

from hypothesis import given, strategies as st
from pathlib import Path
import pytest
import asyncio
from src.lib.types import EventContext, EventResult


@given(
    state_key=st.text(min_size=1, max_size=50),
    state_value=st.text(min_size=0, max_size=100)
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 24: Event Context Immutability")
def test_event_context_immutability(state_key, state_value):
    """
    Property 24: For any event execution, modifications to the EventContext.state
    should not affect other concurrent event executions.
    
    Validates: Requirements 3.7
    """
    # Create two separate EventContext instances
    ctx1 = EventContext(
        jobs_root=Path("jobs"),
        resumes_root=Path("resumes"),
        default_resume="test.yaml",
        state={}
    )
    
    ctx2 = EventContext(
        jobs_root=Path("jobs"),
        resumes_root=Path("resumes"),
        default_resume="test.yaml",
        state={}
    )
    
    # Modify ctx1's state
    ctx1.state[state_key] = state_value
    
    # Verify ctx2's state is not affected
    assert state_key not in ctx2.state
    assert ctx1.state != ctx2.state
    
    # Verify ctx1 has the modification
    assert ctx1.state[state_key] == state_value



@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 7: Event Discovery Completeness")
def test_event_discovery_completeness():
    """
    Property 7: For any Python module in `src/events/` (excluding event_bus.py),
    the event bus should discover and include it in the events mapping.
    
    Validates: Requirements 3.1
    """
    from src.events.event_bus import discover_events
    import os
    
    # Get all Python files in src/events/
    events_dir = Path("src/events")
    python_files = [f.stem for f in events_dir.glob("*.py") 
                   if f.stem not in ("event_bus", "__init__") and not f.stem.startswith("_")]
    
    # Discover events
    discovered = discover_events()
    
    # Verify all Python modules are discovered
    for module_name in python_files:
        assert module_name in discovered, f"Module {module_name} not discovered"
        assert discovered[module_name] == f"src.events.{module_name}"
    
    # Verify event_bus itself is not in the mapping
    assert "event_bus" not in discovered



@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 8: Event Execution Error Handling")
@pytest.mark.asyncio
async def test_event_error_handling():
    """
    Property 8: For any event that raises an exception, the event bus should catch it,
    log to application logs, and return a failed EventResult without crashing.
    
    Validates: Requirements 3.6
    """
    from src.events.event_bus import run_event
    import tempfile
    
    # Create a temporary test event that raises an exception
    test_event_code = '''
from pathlib import Path
from src.lib.types import EventContext, EventResult

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    raise ValueError("Test error for property testing")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    raise ValueError("Test error for property testing")
'''
    
    # Write the test event to a temporary file
    test_event_path = Path("src/events/test_error_event.py")
    test_event_path.write_text(test_event_code)
    
    try:
        # Create test context
        ctx = EventContext(
            jobs_root=Path("jobs"),
            resumes_root=Path("resumes"),
            default_resume="test.yaml",
            test_mode=False
        )
        
        # Run the event that will raise an exception
        result = await run_event("test_error_event", Path("test/job"), ctx)
        
        # Verify the event bus caught the exception and returned a failed result
        assert result.ok is False
        assert "Test error for property testing" in result.message
        assert len(result.errors) > 0
        
    finally:
        # Clean up the test event file
        if test_event_path.exists():
            test_event_path.unlink()



@given(
    company=st.text(min_size=1, max_size=100),
    title=st.text(min_size=1, max_size=100),
    date=st.datetimes(),
    job_id=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 1: Folder Name Round Trip")
def test_folder_name_round_trip(company, title, date, job_id):
    """
    Property 1: For any valid job data (company, title, date, id), generating a folder name
    and then parsing it back should produce equivalent job identity components.
    
    Validates: Requirements 1.1, 1.4
    """
    from src.lib.job_folders import JobIdentity, folder_name, parse_job_folder_name, slug_part
    
    identity = JobIdentity(
        company=company,
        title=title,
        posted_at=date,
        job_id=job_id
    )
    
    folder = folder_name(identity)
    parsed = parse_job_folder_name(folder)
    
    assert parsed is not None, f"Failed to parse folder name: {folder}"
    assert parsed.company == slug_part(company)
    assert parsed.title == slug_part(title)
    assert parsed.job_id == job_id
    # Date comparison - allow for second-level precision
    assert abs((parsed.posted_at - date).total_seconds()) < 1



@given(
    text_with_special_chars=st.text(min_size=1, max_size=100)
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 2: Folder Name Sanitization")
def test_folder_name_sanitization(text_with_special_chars):
    """
    Property 2: For any string containing special characters, the sanitized folder name
    component should contain only alphanumeric characters and underscores, with no
    consecutive special characters.
    
    Validates: Requirements 1.2
    """
    from src.lib.job_folders import slug_part
    import re
    
    sanitized = slug_part(text_with_special_chars)
    
    # Should only contain alphanumeric and underscores
    assert re.match(r'^[A-Za-z0-9_]*$', sanitized), f"Sanitized string contains invalid characters: {sanitized}"
    
    # Should not be empty (returns "Unknown" if input becomes empty after sanitization)
    assert len(sanitized) > 0



@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 3: Unique ID Generation")
@pytest.mark.asyncio
async def test_unique_id_generation():
    """
    Property 3: For any job data without an ID, creating a job folder should generate
    a unique identifier that doesn't collide with existing job IDs.
    
    Validates: Requirements 1.3
    """
    from src.events.create_jobfolder import execute
    import tempfile
    import shutil
    
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    jobs_root = temp_dir / "jobs"
    jobs_root.mkdir()
    (jobs_root / "1_Queued").mkdir()
    
    try:
        # Create multiple jobs without IDs
        generated_ids = set()
        
        for i in range(10):
            job_data = {
                "company": f"Company{i}",
                "title": f"Engineer{i}",
                "date_posted": "2026-01-14 12:00:00"
                # No ID provided
            }
            
            ctx = EventContext(
                jobs_root=jobs_root,
                resumes_root=Path("resumes"),
                default_resume="test.yaml",
                state={"job": job_data}
            )
            
            result = await execute(Path("placeholder"), ctx)
            
            assert result.ok is True
            assert "id" in job_data  # ID should be generated
            assert job_data["id"] not in generated_ids  # Should be unique
            generated_ids.add(job_data["id"])
            
    finally:
        # Clean up
        shutil.rmtree(temp_dir)



@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 4: Folder Creation Idempotence")
@pytest.mark.asyncio
async def test_folder_creation_idempotence():
    """
    Property 4: For any job folder, attempting to create it twice should return the
    existing path on the second attempt with success=False, without creating duplicates.
    
    Validates: Requirements 1.6
    """
    from src.events.create_jobfolder import execute
    import tempfile
    import shutil
    
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    jobs_root = temp_dir / "jobs"
    jobs_root.mkdir()
    (jobs_root / "1_Queued").mkdir()
    
    try:
        job_data = {
            "id": "test123",
            "company": "TestCorp",
            "title": "Engineer",
            "date_posted": "2026-01-14 12:00:00"
        }
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=Path("resumes"),
            default_resume="test.yaml",
            state={"job": job_data.copy()}
        )
        
        # First creation should succeed
        result1 = await execute(Path("placeholder"), ctx)
        assert result1.ok is True
        first_path = result1.job_path
        
        # Second creation should fail but return existing path
        ctx.state = {"job": job_data.copy()}
        result2 = await execute(Path("placeholder"), ctx)
        assert result2.ok is False
        assert result2.job_path == first_path
        assert "exists already" in result2.message
        
        # Verify only one folder was created
        queued_folders = list((jobs_root / "1_Queued").iterdir())
        assert len(queued_folders) == 1
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)



@given(
    num_files=st.integers(min_value=1, max_value=20),
    file_names=st.lists(
        st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        min_size=1,
        max_size=20,
        unique=True
    )
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 5: Phase Transition File Preservation")
@pytest.mark.asyncio
async def test_phase_transition_file_preservation(num_files, file_names):
    """
    Property 5: For any job folder with arbitrary files, moving between phases should
    preserve all files without loss or corruption.
    
    Validates: Requirements 2.3, 2.4
    """
    from src.events._helpers import move_job_to_phase
    from src.lib.job_folders import PHASES
    import tempfile
    import shutil
    
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    jobs_root = temp_dir / "jobs"
    jobs_root.mkdir()
    
    # Create all phase directories
    for phase in PHASES:
        (jobs_root / phase).mkdir()
    
    try:
        # Create a job folder in 1_Queued
        job_folder = jobs_root / "1_Queued" / "TestCorp.Engineer.20260114-120000.test123"
        job_folder.mkdir()
        
        # Create arbitrary files with content
        file_contents = {}
        for i, name in enumerate(file_names[:num_files]):
            file_path = job_folder / f"{name}.txt"
            content = f"Test content {i}: {name}"
            file_path.write_text(content)
            file_contents[f"{name}.txt"] = content
        
        # Also create job.yaml and job.log
        (job_folder / "job.yaml").write_text("company: TestCorp\ntitle: Engineer")
        (job_folder / "job.log").write_text("Initial log entry")
        file_contents["job.yaml"] = "company: TestCorp\ntitle: Engineer"
        file_contents["job.log"] = "Initial log entry"
        
        # Move through several phases
        current_path = job_folder
        test_phases = ["2_Data_Generated", "3_Docs_Generated", "4_Applied"]
        
        for phase in test_phases:
            # Move to next phase
            new_path = move_job_to_phase(current_path, jobs_root, phase)
            
            # Verify all files exist in new location
            for filename, expected_content in file_contents.items():
                file_path = new_path / filename
                assert file_path.exists(), f"File {filename} missing after move to {phase}"
                actual_content = file_path.read_text()
                assert actual_content == expected_content, f"File {filename} content corrupted after move to {phase}"
            
            # Verify old location no longer exists
            assert not current_path.exists(), f"Old path {current_path} still exists after move"
            
            current_path = new_path
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)



@given(
    phase_index=st.integers(min_value=0, max_value=10)
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 6: Phase Transition Logging")
@pytest.mark.asyncio
async def test_phase_transition_logging(phase_index):
    """
    Property 6: For any phase transition, a log entry should be appended to job.log
    documenting the transition with timestamp and phase name.
    
    Validates: Requirements 2.5
    """
    from src.events.event_bus import run_event
    from src.lib.job_folders import PHASES
    import tempfile
    import shutil
    
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    jobs_root = temp_dir / "jobs"
    jobs_root.mkdir()
    
    # Create all phase directories
    for phase in PHASES:
        (jobs_root / phase).mkdir()
    
    try:
        # Select a phase to test (skip 1_Queued since we start there)
        target_phase = PHASES[phase_index]
        
        # Skip if trying to move to the same phase we start in
        if target_phase == "1_Queued":
            return
        
        # Create a job folder in 1_Queued
        job_folder = jobs_root / "1_Queued" / "TestCorp.Engineer.20260114-120000.test123"
        job_folder.mkdir()
        
        # Create job.yaml and initial job.log
        (job_folder / "job.yaml").write_text("company: TestCorp\ntitle: Engineer")
        (job_folder / "job.log").write_text("Initial log entry\n")
        
        # Get initial log content
        initial_log = (job_folder / "job.log").read_text()
        
        # Determine which move event to call based on target phase
        event_map = {
            "1_Queued": "move_queue",
            "2_Data_Generated": "move_data_gen",
            "3_Docs_Generated": "move_docs_gen",
            "4_Applied": "move_applied",
            "5_FollowUp": "move_followup",
            "6_Interviewing": "move_interviewing",
            "7_Negotiating": "move_negotiating",
            "8_Accepted": "move_accepted",
            "Skipped": "move_skipped",
            "Expired": "move_expired",
            "Errored": "move_errored"
        }
        
        event_name = event_map.get(target_phase)
        if not event_name:
            return  # Skip if no event for this phase
        
        # Create context
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=Path("resumes"),
            default_resume="test.yaml",
            test_mode=False
        )
        
        # Run the move event
        result = await run_event(event_name, job_folder, ctx)
        
        # Verify the event succeeded
        assert result.ok is True
        
        # Find the new job location
        new_job_folder = jobs_root / target_phase / "TestCorp.Engineer.20260114-120000.test123"
        assert new_job_folder.exists(), f"Job folder not found in {target_phase}"
        
        # Read the log file
        log_file = new_job_folder / "job.log"
        assert log_file.exists(), "job.log not found after phase transition"
        
        new_log = log_file.read_text()
        
        # Verify log was appended (not overwritten)
        assert "Initial log entry" in new_log, "Original log content was lost"
        
        # Verify new log entry was added
        assert len(new_log) > len(initial_log), "No new log entry was added"
        
        # Verify log entry mentions the event and phase
        assert event_name in new_log or target_phase in new_log, f"Log entry doesn't mention {event_name} or {target_phase}"
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
