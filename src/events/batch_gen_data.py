from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml
from src.events.event_bus import run_event
from src.events._helpers import move_job_to_phase


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Batch generate all subcontent data for a job.
    
    Reads subcontent_events from job.yaml and executes all events serially.
    On success, moves job to 2_Data_Generated.
    On failure after 3 retries, moves to Errored.
    """
    try:
        # Load job.yaml to get subcontent_events configuration
        job_yaml_path = job_path / "job.yaml"
        if not job_yaml_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="job.yaml not found",
                errors=[{"error": "job.yaml not found"}]
            )
        
        job_data = load_yaml(job_yaml_path)
        subcontent_events = job_data.get("subcontent_events", [])
        
        if not subcontent_events:
            return EventResult(
                ok=False,
                job_path=job_path,
                message="No subcontent_events configured in job.yaml",
                errors=[{"error": "subcontent_events missing or empty"}]
            )
        
        # Track results
        successful_events = []
        failed_events = []
        artifacts = []
        
        # Execute each subcontent event serially
        for event_config in subcontent_events:
            # Each config is a dict with one key-value pair: {section: event_name}
            if not isinstance(event_config, dict):
                failed_events.append(f"Invalid config: {event_config}")
                continue
            
            for section, event_name in event_config.items():
                # Run the event with retry logic (up to 3 attempts)
                max_retries = 3
                success = False
                last_error = None
                
                for attempt in range(max_retries):
                    result = await run_event(event_name, job_path, ctx)
                    
                    if result.ok:
                        successful_events.append(f"{section}: {event_name}")
                        artifacts.extend(result.artifacts)
                        success = True
                        break
                    else:
                        last_error = result.message
                        # Wait before retry (except on last attempt)
                        if attempt < max_retries - 1:
                            import asyncio
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                if not success:
                    failed_events.append(f"{section}: {event_name} - {last_error}")
        
        # Check if all events succeeded
        if failed_events:
            # Move to Errored phase
            try:
                new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
                
                # Create error.md with details
                error_md = new_path / "error.md"
                error_content = f"""# Batch Data Generation Failed

## Failed Events
{chr(10).join(f'- {event}' for event in failed_events)}

## Successful Events
{chr(10).join(f'- {event}' for event in successful_events)}

## Recommended Next Steps
1. Review the error messages above
2. Check job.yaml and resume.yaml for issues
3. Verify LLM API key is configured correctly
4. Retry the batch_gen_data event after fixing issues
"""
                error_md.write_text(error_content)
                
                return EventResult(
                    ok=False,
                    job_path=new_path,
                    message=f"Batch generation failed: {len(failed_events)} events failed, moved to Errored",
                    errors=[{"failed_events": failed_events}],
                    artifacts=artifacts + [str(error_md)]
                )
            except Exception as e:
                return EventResult(
                    ok=False,
                    job_path=job_path,
                    message=f"Batch generation failed and couldn't move to Errored: {str(e)}",
                    errors=[{"failed_events": failed_events, "move_error": str(e)}]
                )
        
        # All events succeeded - move to 2_Data_Generated
        try:
            new_path = move_job_to_phase(job_path, ctx.jobs_root, "2_Data_Generated")
            
            return EventResult(
                ok=True,
                job_path=new_path,
                message=f"Successfully generated all subcontent data ({len(successful_events)} events)",
                artifacts=artifacts
            )
        except Exception as e:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Data generation succeeded but couldn't move to 2_Data_Generated: {str(e)}",
                errors=[{"move_error": str(e)}],
                artifacts=artifacts
            )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Batch generation failed: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate job.yaml exists and has subcontent_events."""
    job_yaml_path = job_path / "job.yaml"
    if not job_yaml_path.exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    
    try:
        job_data = load_yaml(job_yaml_path)
        subcontent_events = job_data.get("subcontent_events", [])
        
        if not subcontent_events:
            return EventResult(ok=False, job_path=job_path, message="No subcontent_events configured")
        
        return EventResult(
            ok=True,
            job_path=job_path,
            message=f"Test: would generate {len(subcontent_events)} subcontent files"
        )
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Test failed: {str(e)}")
