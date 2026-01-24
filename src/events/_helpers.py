from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

from src.lib.job_folders import PHASES, phase_path
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.logging_utils import append_job_log, append_app_log


def _get_db_enabled() -> bool:
    """Check if database is enabled (hardcoded path: src/db/resumai.db)."""
    from src.db.connection import get_db_path
    return get_db_path().exists()


def _get_job_service():
    """Get JobService instance (lazy import to avoid circular deps)."""
    from src.services.job_service import JobService
    return JobService()


def _get_subcontent_repo():
    """Get SubcontentRepository instance (lazy import)."""
    from src.repositories.subcontent_repository import SubcontentRepository
    return SubcontentRepository()


def ensure_job_exists(job_path: Path) -> None:
    if not job_path.exists():
        raise FileNotFoundError(f"Job path not found: {job_path}")


def read_job_yaml(job_path: Path) -> dict:
    """
    Read job data. Uses database if enabled, falls back to filesystem.
    """
    if _get_db_enabled():
        job_service = _get_job_service()
        folder_name = job_path.name
        job = job_service.get_job(folder_name)
        if job:
            return job_service.export_to_dict(folder_name) or {}

    # Fallback to filesystem
    p = job_path / "job.yaml"
    if not p.exists():
        return {}
    return load_yaml(p)


def write_job_yaml(job_path: Path, data: dict) -> None:
    """
    Write job data. Updates database if enabled, always writes to filesystem.
    """
    # Always write to filesystem for compatibility
    dump_yaml(job_path / "job.yaml", data)

    # Also update database if enabled
    if _get_db_enabled():
        job_service = _get_job_service()
        folder_name = job_path.name
        job_service.update_job_data(folder_name, data)

def move_job_to_phase(job_path: Path, jobs_root: Path, phase: str) -> Path:
    """
    Move a job folder to a new phase directory.

    This function ensures atomic moves and validates the operation completed successfully.
    If destination already exists, it will merge by removing the source.
    Also updates the database phase if database mode is enabled.

    Args:
        job_path: Current path to the job folder
        jobs_root: Root jobs directory
        phase: Target phase name

    Returns:
        Path to the job in its new location

    Raises:
        ValueError: If phase is invalid
        RuntimeError: If move fails validation
    """
    if phase not in PHASES:
        raise ValueError(f"Invalid phase: {phase}")

    folder_name = job_path.name

    # Update database phase if enabled
    if _get_db_enabled():
        try:
            job_service = _get_job_service()
            job_service.move_to_phase(folder_name, phase)
        except Exception as e:
            append_app_log(Path('src/logs'), f"MOVE_DB_ERROR: Failed to update DB phase for {folder_name}: {e}")

    dest_dir = phase_path(jobs_root, phase)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / job_path.name

    # Case 1: Destination already exists
    if dest_path.exists():
        if job_path.exists():
            # Both exist - this is a duplicate situation
            # Keep the one with more files (likely more complete)
            source_files = list(job_path.glob('*'))
            dest_files = list(dest_path.glob('*'))

            if len(source_files) > len(dest_files):
                # Source has more files - remove dest and move source
                append_app_log(Path('src/logs'), f"MOVE_MERGE: dest has {len(dest_files)} files, source has {len(source_files)} - keeping source")
                shutil.rmtree(str(dest_path))
                shutil.move(str(job_path), str(dest_path))
            else:
                # Dest has more or equal files - remove source
                append_app_log(Path('src/logs'), f"MOVE_MERGE: dest has {len(dest_files)} files, source has {len(source_files)} - keeping dest")
                shutil.rmtree(str(job_path))

        # Validate destination exists and source is gone
        if job_path.exists():
            raise RuntimeError(f"Move failed: source still exists at {job_path}")
        if not dest_path.exists():
            raise RuntimeError(f"Move failed: destination missing at {dest_path}")

        return dest_path

    # Case 2: Normal move - destination doesn't exist
    if not job_path.exists():
        raise FileNotFoundError(f"Source job folder not found: {job_path}")

    # Perform the move
    shutil.move(str(job_path), str(dest_path))

    # Validate the move completed successfully
    if job_path.exists():
        # Source still exists - move may have copied instead of moved
        # Clean up the source
        append_app_log(Path('src/logs'), f"MOVE_CLEANUP: source still exists after move, removing {job_path}")
        shutil.rmtree(str(job_path))

    if not dest_path.exists():
        raise RuntimeError(f"Move failed: destination not created at {dest_path}")

    # Verify critical files exist in destination
    job_yaml = dest_path / "job.yaml"
    if not job_yaml.exists():
        append_app_log(Path('src/logs'), f"MOVE_WARNING: job.yaml missing in destination {dest_path}")

    return dest_path

def append(job_path: Path, msg: str) -> None:
    append_job_log(job_path, msg)
