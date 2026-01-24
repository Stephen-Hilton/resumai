"""
YAML export service for exporting data from SQLite.
"""

import sqlite3
from pathlib import Path
from typing import Optional
import yaml

from ..db.connection import get_connection
from ..repositories.resume_repository import ResumeRepository
from ..repositories.job_repository import JobRepository
from ..repositories.subcontent_repository import SubcontentRepository, SECTIONS


class LiteralScalarString(str):
    """A string that should be dumped as a literal block scalar."""
    pass


def literal_representer(dumper, data):
    """Custom YAML representer for literal block scalars."""
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


# Register the custom representer
yaml.add_representer(LiteralScalarString, literal_representer)


class YamlExportService:
    """
    Service for exporting SQLite data to YAML files.

    Used for backup and compatibility with file-based workflows.
    """

    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize the service.

        Args:
            conn: Optional database connection.
        """
        self.conn = conn or get_connection()
        self.resume_repo = ResumeRepository(self.conn)
        self.job_repo = JobRepository(self.conn)
        self.subcontent_repo = SubcontentRepository(self.conn)

    # =========================================================================
    # RESUME EXPORT
    # =========================================================================

    def export_resume(self, resume_id: int, output_path: Path) -> bool:
        """
        Export a resume to a YAML file.

        Args:
            resume_id: Resume database ID.
            output_path: Path to write the YAML file.

        Returns:
            True if exported, False if resume not found.
        """
        data = self.resume_repo.to_dict(resume_id)
        if not data:
            return False

        # Convert summary to literal block scalar if multiline
        if data.get('summary') and '\n' in data['summary']:
            data['summary'] = LiteralScalarString(data['summary'])

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        return True

    def export_resume_by_slug(self, slug: str, output_path: Path) -> bool:
        """
        Export a resume by slug to a YAML file.

        Args:
            slug: Resume slug.
            output_path: Path to write the YAML file.

        Returns:
            True if exported, False if resume not found.
        """
        row = self.resume_repo._fetch_one(
            "SELECT id FROM resumes WHERE slug = ?",
            (slug,)
        )
        if not row:
            return False
        return self.export_resume(row['id'], output_path)

    def export_all_resumes(self, output_dir: Path) -> list[str]:
        """
        Export all resumes to a directory.

        Args:
            output_dir: Directory to write YAML files.

        Returns:
            List of exported resume slugs.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        exported = []

        for resume in self.resume_repo.get_all():
            output_path = output_dir / f"{resume.slug}.yaml"
            if self.export_resume(resume.id, output_path):
                exported.append(resume.slug)

        return exported

    # =========================================================================
    # JOB EXPORT
    # =========================================================================

    def export_job(self, job_id: int, output_folder: Path) -> bool:
        """
        Export a job and its subcontent to a folder.

        Args:
            job_id: Job database ID.
            output_folder: Folder to write files.

        Returns:
            True if exported, False if job not found.
        """
        job_data = self.job_repo.to_dict(job_id)
        if not job_data:
            return False

        # Get job to access the folder name
        job = self.job_repo.get_by_id(job_id)
        if not job:
            return False

        # Ensure output folder exists
        output_folder.mkdir(parents=True, exist_ok=True)

        # Convert description to literal block scalar
        if job_data.get('description') and '\n' in job_data['description']:
            job_data['description'] = LiteralScalarString(job_data['description'])

        # Write job.yaml
        job_yaml_path = output_folder / "job.yaml"
        with open(job_yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                job_data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        # Export subcontent
        self._export_subcontent(job_id, output_folder)

        # Export artifacts
        self._export_artifacts(job_id, output_folder)

        return True

    def export_job_by_folder(self, folder_name: str, output_folder: Path) -> bool:
        """
        Export a job by folder name.

        Args:
            folder_name: Job folder name.
            output_folder: Folder to write files.

        Returns:
            True if exported, False if job not found.
        """
        job = self.job_repo.get_by_folder_name(folder_name)
        if not job:
            return False
        return self.export_job(job.id, output_folder)

    def export_all_jobs(self, output_root: Path) -> dict:
        """
        Export all jobs organized by phase.

        Args:
            output_root: Root directory for job folders.

        Returns:
            Dictionary with phase: count mappings.
        """
        results = {}

        for job_summary in self.job_repo.get_all():
            job = self.job_repo.get_by_id(job_summary.id)
            if not job:
                continue

            phase_dir = output_root / job.phase
            output_folder = phase_dir / job.folder_name

            if self.export_job(job.id, output_folder):
                results[job.phase] = results.get(job.phase, 0) + 1

        return results

    def _export_subcontent(self, job_id: int, output_folder: Path) -> None:
        """Export all subcontent sections for a job."""
        for section in SECTIONS:
            data = self.subcontent_repo.to_dict(job_id, section)
            if data is None:
                continue

            filename = f"subcontent.{section}.yaml"
            output_path = output_folder / filename

            # Handle string content (summary, coverletter)
            if isinstance(data, str):
                # Convert to literal block scalar if multiline
                if '\n' in data:
                    data = LiteralScalarString(data)

                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(
                        data,
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                    )
            else:
                # List or dict data
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(
                        data,
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False,
                    )

    def _export_artifacts(self, job_id: int, output_folder: Path) -> None:
        """Export artifact files for a job."""
        artifact_types = [
            "resume_html",
            "resume_pdf",
            "coverletter_html",
            "coverletter_pdf",
        ]

        for artifact_type in artifact_types:
            artifact = self.subcontent_repo.get_artifact(job_id, artifact_type)
            if artifact and artifact.content:
                output_path = output_folder / artifact.filename
                with open(output_path, 'wb') as f:
                    f.write(artifact.content)

    # =========================================================================
    # BACKUP / FULL EXPORT
    # =========================================================================

    def export_all(self, output_root: Path) -> dict:
        """
        Export everything (resumes and jobs) for backup.

        Args:
            output_root: Root directory for export.

        Returns:
            Dictionary with export counts.
        """
        resumes_dir = output_root / "resumes"
        jobs_dir = output_root / "jobs"

        resume_slugs = self.export_all_resumes(resumes_dir)
        job_counts = self.export_all_jobs(jobs_dir)

        return {
            "resumes": len(resume_slugs),
            "jobs": job_counts,
        }
