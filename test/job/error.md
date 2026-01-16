# Error Report

**Generated:** 2026-01-15 10:37:47  
**Event:** `move_errored`  
**Phase:** test  
**Job:** job

## Error Summary

Event failed after 4 attempts: Destination job folder already exists: jobs/Errored/job

## Error Details

- **Exception Type**: FileExistsError
- **Attempts**: 5
- **Max Retries**: 3
- **Event**: move_errored

## Traceback

```
Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/test_error_event.py", line 6, in execute
    raise ValueError("Test error for property testing")
ValueError: Test error for property testing

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/test_error_event.py", line 6, in execute
    raise ValueError("Test error for property testing")
ValueError: Test error for property testing

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/test_error_event.py", line 6, in execute
    raise ValueError("Test error for property testing")
ValueError: Test error for property testing

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/test_error_event.py", line 6, in execute
    raise ValueError("Test error for property testing")
ValueError: Test error for property testing

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/stephen.hilton/Dev/resumai/src/events/event_bus.py", line 54, in run_event
    res = await fn(job_path, ctx)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/move_errored.py", line 8, in execute
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stephen.hilton/Dev/resumai/src/events/_helpers.py", line 33, in move_job_to_phase
    raise FileExistsError(f"Destination job folder already exists: {dest_path}")
FileExistsError: Destination job folder already exists: jobs/Errored/job

```

## Recommended Actions

1. **Review Error Details**: Examine the error message and traceback above
2. **Check Logs**: Review application logs in src/logs/ for more context
3. **Verify Configuration**: Ensure all environment variables are set correctly in .env
4. **Check Dependencies**: Verify all required files and services are available
5. **Retry**: Try running the event again
6. **Seek Help**: If the error persists, consult documentation or seek support

## Recovery Steps

To recover from this error:

1. **Fix the Issue**: Address the root cause based on recommended actions above
2. **Move Job Back**: Move the job back to the appropriate phase for retry
3. **Retry Event**: Run the failed event again
4. **Monitor Progress**: Check logs and job status to ensure success

**Note**: This error.md file will be preserved for reference. You can delete it once the issue is resolved.
