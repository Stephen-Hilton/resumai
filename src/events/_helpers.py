from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

from src.lib.job_folders import PHASES, phase_path
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.logging_utils import append_job_log

def ensure_job_exists(job_path: Path) -> None:
    if not job_path.exists():
        raise FileNotFoundError(f"Job path not found: {job_path}")

def read_job_yaml(job_path: Path) -> dict:
    p = job_path / "job.yaml"
    if not p.exists():
        return {}
    return load_yaml(p)

def write_job_yaml(job_path: Path, data: dict) -> None:
    dump_yaml(job_path / "job.yaml", data)

def move_job_to_phase(job_path: Path, jobs_root: Path, phase: str) -> Path:
    if phase not in PHASES:
        raise ValueError(f"Invalid phase: {phase}")
    dest_dir = phase_path(jobs_root, phase)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / job_path.name
    if dest_path.exists():
        # merge logs by appending and remove source
        # simplest: do not overwrite; raise
        raise FileExistsError(f"Destination job folder already exists: {dest_path}")
    shutil.move(str(job_path), str(dest_path))
    return dest_path

def append(job_path: Path, msg: str) -> None:
    append_job_log(job_path, msg)
