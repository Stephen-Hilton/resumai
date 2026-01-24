"""
Repository for job subcontent data access.
"""

import sqlite3
from typing import Optional

from .base_repository import BaseRepository
from ..db.models import (
    Contact, Company, Role, Bullet, Education, Award,
    SubcontentContacts, SubcontentSummary, SubcontentSkills,
    SubcontentHighlights, SubcontentExperience, SubcontentEducation,
    SubcontentAwards, SubcontentCoverletter, SubcontentStatus,
    Artifact, DocStatus
)


# Section names
SECTIONS = [
    "contacts",
    "summary",
    "skills",
    "highlights",
    "experience",
    "education",
    "awards",
    "coverletter",
]


class SubcontentRepository(BaseRepository):
    """
    Repository for managing job subcontent (generated resume sections).

    Handles CRUD for contacts, summary, skills, highlights, experience,
    education, awards, and cover letter sections per job.
    """

    # =========================================================================
    # STATUS CHECKS
    # =========================================================================

    def section_exists(self, job_id: int, section: str) -> bool:
        """
        Check if a subcontent section has been generated for a job.

        Args:
            job_id: Job database ID.
            section: Section name (contacts, summary, etc.).

        Returns:
            True if section has data, False otherwise.
        """
        if section == "contacts":
            return self._exists("job_subcontent_contacts", "job_id = ?", (job_id,))
        elif section == "summary":
            return self._exists("job_subcontent_summary", "job_id = ?", (job_id,))
        elif section == "skills":
            return self._exists("job_subcontent_skills", "job_id = ?", (job_id,))
        elif section == "highlights":
            return self._exists("job_subcontent_highlights", "job_id = ?", (job_id,))
        elif section == "experience":
            return self._exists("job_subcontent_companies", "job_id = ?", (job_id,))
        elif section == "education":
            return self._exists("job_subcontent_education", "job_id = ?", (job_id,))
        elif section == "awards":
            return self._exists("job_subcontent_awards", "job_id = ?", (job_id,))
        elif section == "coverletter":
            return self._exists("job_subcontent_coverletter", "job_id = ?", (job_id,))
        else:
            return False

    def get_subcontent_status(self, job_id: int) -> SubcontentStatus:
        """
        Get the status of all subcontent sections for a job.

        Args:
            job_id: Job database ID.

        Returns:
            SubcontentStatus with boolean flags for each section.
        """
        return SubcontentStatus(
            contacts=self.section_exists(job_id, "contacts"),
            summary=self.section_exists(job_id, "summary"),
            skills=self.section_exists(job_id, "skills"),
            highlights=self.section_exists(job_id, "highlights"),
            experience=self.section_exists(job_id, "experience"),
            education=self.section_exists(job_id, "education"),
            awards=self.section_exists(job_id, "awards"),
            coverletter=self.section_exists(job_id, "coverletter"),
        )

    # =========================================================================
    # CONTACTS
    # =========================================================================

    def get_contacts(self, job_id: int) -> list[Contact]:
        """Get contacts subcontent for a job."""
        rows = self._fetch_all(
            "SELECT * FROM job_subcontent_contacts WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )
        return [
            Contact(
                id=row['id'],
                name=row['name'],
                label=row['label'],
                url=row['url'],
                icon=row['icon'],
                sort_order=row['sort_order'],
            )
            for row in rows
        ]

    def save_contacts(self, job_id: int, contacts: list[Contact]) -> None:
        """Save contacts subcontent for a job (replaces existing)."""
        self._delete("job_subcontent_contacts", "job_id = ?", (job_id,))

        for i, contact in enumerate(contacts):
            self._insert("job_subcontent_contacts", {
                "job_id": job_id,
                "name": contact.name,
                "label": contact.label,
                "url": contact.url,
                "icon": contact.icon,
                "sort_order": i,
            })

    def delete_contacts(self, job_id: int) -> None:
        """Delete contacts subcontent for a job."""
        self._delete("job_subcontent_contacts", "job_id = ?", (job_id,))

    # =========================================================================
    # SUMMARY
    # =========================================================================

    def get_summary(self, job_id: int) -> Optional[str]:
        """Get summary subcontent for a job."""
        row = self._fetch_one(
            "SELECT content FROM job_subcontent_summary WHERE job_id = ?",
            (job_id,)
        )
        return row['content'] if row else None

    def save_summary(self, job_id: int, content: str) -> None:
        """Save summary subcontent for a job (replaces existing)."""
        existing = self._fetch_one(
            "SELECT id FROM job_subcontent_summary WHERE job_id = ?",
            (job_id,)
        )

        if existing:
            self._update("job_subcontent_summary", {
                "content": content,
            }, "id = ?", (existing['id'],))
        else:
            self._insert("job_subcontent_summary", {
                "job_id": job_id,
                "content": content,
            })

    def delete_summary(self, job_id: int) -> None:
        """Delete summary subcontent for a job."""
        self._delete("job_subcontent_summary", "job_id = ?", (job_id,))

    # =========================================================================
    # SKILLS
    # =========================================================================

    def get_skills(self, job_id: int) -> list[str]:
        """Get skills subcontent for a job."""
        rows = self._fetch_all(
            "SELECT skill FROM job_subcontent_skills WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )
        return [row['skill'] for row in rows]

    def save_skills(self, job_id: int, skills: list[str]) -> None:
        """Save skills subcontent for a job (replaces existing)."""
        self._delete("job_subcontent_skills", "job_id = ?", (job_id,))

        for i, skill in enumerate(skills):
            self._insert("job_subcontent_skills", {
                "job_id": job_id,
                "skill": skill,
                "sort_order": i,
            })

    def delete_skills(self, job_id: int) -> None:
        """Delete skills subcontent for a job."""
        self._delete("job_subcontent_skills", "job_id = ?", (job_id,))

    # =========================================================================
    # HIGHLIGHTS
    # =========================================================================

    def get_highlights(self, job_id: int) -> list[str]:
        """Get highlights subcontent for a job."""
        rows = self._fetch_all(
            "SELECT highlight FROM job_subcontent_highlights WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )
        return [row['highlight'] for row in rows]

    def save_highlights(self, job_id: int, highlights: list[str]) -> None:
        """Save highlights subcontent for a job (replaces existing)."""
        self._delete("job_subcontent_highlights", "job_id = ?", (job_id,))

        for i, highlight in enumerate(highlights):
            self._insert("job_subcontent_highlights", {
                "job_id": job_id,
                "highlight": highlight,
                "sort_order": i,
            })

    def delete_highlights(self, job_id: int) -> None:
        """Delete highlights subcontent for a job."""
        self._delete("job_subcontent_highlights", "job_id = ?", (job_id,))

    # =========================================================================
    # EXPERIENCE
    # =========================================================================

    def get_experience(self, job_id: int) -> list[Company]:
        """Get experience subcontent for a job."""
        company_rows = self._fetch_all(
            "SELECT * FROM job_subcontent_companies WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )

        companies = []
        for comp_row in company_rows:
            company_id = comp_row['id']

            # Load URLs
            url_rows = self._fetch_all(
                "SELECT url FROM job_subcontent_company_urls WHERE subcontent_company_id = ? ORDER BY sort_order",
                (company_id,)
            )
            urls = [r['url'] for r in url_rows]

            # Load roles
            role_rows = self._fetch_all(
                "SELECT * FROM job_subcontent_roles WHERE subcontent_company_id = ? ORDER BY sort_order",
                (company_id,)
            )

            roles = []
            for role_row in role_rows:
                role_id = role_row['id']

                # Load bullets
                bullet_rows = self._fetch_all(
                    "SELECT * FROM job_subcontent_bullets WHERE subcontent_role_id = ? ORDER BY sort_order",
                    (role_id,)
                )

                bullets = []
                for bullet_row in bullet_rows:
                    bullet_id = bullet_row['id']

                    # Load tags
                    tag_rows = self._fetch_all(
                        "SELECT tag FROM job_subcontent_bullet_tags WHERE subcontent_bullet_id = ?",
                        (bullet_id,)
                    )
                    tags = [r['tag'] for r in tag_rows]

                    bullets.append(Bullet(
                        id=bullet_row['id'],
                        original_id=bullet_row['original_id'],
                        text=bullet_row['text'],
                        tags=tags,
                        sort_order=bullet_row['sort_order'],
                    ))

                roles.append(Role(
                    id=role_row['id'],
                    original_id=role_row['original_id'],
                    role=role_row['role'],
                    dates=role_row['dates'],
                    location=role_row['location'],
                    bullets=bullets,
                    sort_order=role_row['sort_order'],
                ))

            companies.append(Company(
                id=comp_row['id'],
                company_name=comp_row['company_name'],
                company_urls=urls,
                employees=comp_row['employees'],
                dates=comp_row['dates'],
                location=comp_row['location'],
                company_description=comp_row['company_description'],
                roles=roles,
                sort_order=comp_row['sort_order'],
            ))

        return companies

    def save_experience(self, job_id: int, companies: list[Company]) -> None:
        """Save experience subcontent for a job (replaces existing)."""
        self.delete_experience(job_id)

        for i, company in enumerate(companies):
            company_id = self._insert("job_subcontent_companies", {
                "job_id": job_id,
                "company_name": company.company_name,
                "employees": company.employees,
                "dates": company.dates,
                "location": company.location,
                "company_description": company.company_description,
                "sort_order": i,
            })

            # Save URLs
            for j, url in enumerate(company.company_urls):
                self._insert("job_subcontent_company_urls", {
                    "subcontent_company_id": company_id,
                    "url": url,
                    "sort_order": j,
                })

            # Save roles
            for j, role in enumerate(company.roles):
                role_id = self._insert("job_subcontent_roles", {
                    "subcontent_company_id": company_id,
                    "original_id": role.original_id,
                    "role": role.role,
                    "dates": role.dates,
                    "location": role.location,
                    "sort_order": j,
                })

                # Save bullets
                for k, bullet in enumerate(role.bullets):
                    bullet_id = self._insert("job_subcontent_bullets", {
                        "subcontent_role_id": role_id,
                        "original_id": bullet.original_id,
                        "text": bullet.text,
                        "sort_order": k,
                    })

                    # Save tags
                    for tag in bullet.tags:
                        self._insert("job_subcontent_bullet_tags", {
                            "subcontent_bullet_id": bullet_id,
                            "tag": tag,
                        })

    def delete_experience(self, job_id: int) -> None:
        """Delete experience subcontent for a job."""
        # Get company IDs
        company_rows = self._fetch_all(
            "SELECT id FROM job_subcontent_companies WHERE job_id = ?",
            (job_id,)
        )

        for comp_row in company_rows:
            company_id = comp_row['id']

            # Get role IDs
            role_rows = self._fetch_all(
                "SELECT id FROM job_subcontent_roles WHERE subcontent_company_id = ?",
                (company_id,)
            )

            for role_row in role_rows:
                role_id = role_row['id']

                # Get bullet IDs
                bullet_rows = self._fetch_all(
                    "SELECT id FROM job_subcontent_bullets WHERE subcontent_role_id = ?",
                    (role_id,)
                )

                # Delete tags
                for bullet_row in bullet_rows:
                    self._delete("job_subcontent_bullet_tags", "subcontent_bullet_id = ?", (bullet_row['id'],))

                # Delete bullets
                self._delete("job_subcontent_bullets", "subcontent_role_id = ?", (role_id,))

            # Delete roles
            self._delete("job_subcontent_roles", "subcontent_company_id = ?", (company_id,))

            # Delete URLs
            self._delete("job_subcontent_company_urls", "subcontent_company_id = ?", (company_id,))

        # Delete companies
        self._delete("job_subcontent_companies", "job_id = ?", (job_id,))

    # =========================================================================
    # EDUCATION
    # =========================================================================

    def get_education(self, job_id: int) -> list[Education]:
        """Get education subcontent for a job."""
        rows = self._fetch_all(
            "SELECT * FROM job_subcontent_education WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )
        return [
            Education(
                id=row['id'],
                course=row['course'],
                school=row['school'],
                dates=row['dates'],
                sort_order=row['sort_order'],
            )
            for row in rows
        ]

    def save_education(self, job_id: int, education: list[Education]) -> None:
        """Save education subcontent for a job (replaces existing)."""
        self._delete("job_subcontent_education", "job_id = ?", (job_id,))

        for i, edu in enumerate(education):
            self._insert("job_subcontent_education", {
                "job_id": job_id,
                "course": edu.course,
                "school": edu.school,
                "dates": edu.dates,
                "sort_order": i,
            })

    def delete_education(self, job_id: int) -> None:
        """Delete education subcontent for a job."""
        self._delete("job_subcontent_education", "job_id = ?", (job_id,))

    # =========================================================================
    # AWARDS
    # =========================================================================

    def get_awards(self, job_id: int) -> list[Award]:
        """Get awards subcontent for a job."""
        rows = self._fetch_all(
            "SELECT * FROM job_subcontent_awards WHERE job_id = ? ORDER BY sort_order",
            (job_id,)
        )
        return [
            Award(
                id=row['id'],
                award=row['award'],
                reward=row['reward'],
                dates=row['dates'],
                sort_order=row['sort_order'],
            )
            for row in rows
        ]

    def save_awards(self, job_id: int, awards: list[Award]) -> None:
        """Save awards subcontent for a job (replaces existing)."""
        self._delete("job_subcontent_awards", "job_id = ?", (job_id,))

        for i, award in enumerate(awards):
            self._insert("job_subcontent_awards", {
                "job_id": job_id,
                "award": award.award,
                "reward": award.reward,
                "dates": award.dates,
                "sort_order": i,
            })

    def delete_awards(self, job_id: int) -> None:
        """Delete awards subcontent for a job."""
        self._delete("job_subcontent_awards", "job_id = ?", (job_id,))

    # =========================================================================
    # COVERLETTER
    # =========================================================================

    def get_coverletter(self, job_id: int) -> Optional[str]:
        """Get cover letter subcontent for a job."""
        row = self._fetch_one(
            "SELECT content FROM job_subcontent_coverletter WHERE job_id = ?",
            (job_id,)
        )
        return row['content'] if row else None

    def save_coverletter(self, job_id: int, content: str) -> None:
        """Save cover letter subcontent for a job (replaces existing)."""
        existing = self._fetch_one(
            "SELECT id FROM job_subcontent_coverletter WHERE job_id = ?",
            (job_id,)
        )

        if existing:
            self._update("job_subcontent_coverletter", {
                "content": content,
            }, "id = ?", (existing['id'],))
        else:
            self._insert("job_subcontent_coverletter", {
                "job_id": job_id,
                "content": content,
            })

    def delete_coverletter(self, job_id: int) -> None:
        """Delete cover letter subcontent for a job."""
        self._delete("job_subcontent_coverletter", "job_id = ?", (job_id,))

    # =========================================================================
    # ARTIFACTS (HTML, PDF)
    # =========================================================================

    def get_artifact(self, job_id: int, artifact_type: str) -> Optional[Artifact]:
        """Get a generated artifact (HTML, PDF) for a job."""
        row = self._fetch_one(
            "SELECT * FROM job_artifacts WHERE job_id = ? AND artifact_type = ?",
            (job_id, artifact_type)
        )
        if not row:
            return None

        return Artifact(
            id=row['id'],
            job_id=row['job_id'],
            artifact_type=row['artifact_type'],
            filename=row['filename'],
            content=row['content'],
            content_type=row['content_type'],
            created_at=row['created_at'],
        )

    def save_artifact(
        self,
        job_id: int,
        artifact_type: str,
        filename: str,
        content: bytes,
        content_type: str
    ) -> None:
        """Save a generated artifact for a job (replaces existing)."""
        existing = self._fetch_one(
            "SELECT id FROM job_artifacts WHERE job_id = ? AND artifact_type = ?",
            (job_id, artifact_type)
        )

        if existing:
            self._update("job_artifacts", {
                "filename": filename,
                "content": content,
                "content_type": content_type,
            }, "id = ?", (existing['id'],))
        else:
            self._insert("job_artifacts", {
                "job_id": job_id,
                "artifact_type": artifact_type,
                "filename": filename,
                "content": content,
                "content_type": content_type,
            })

    def artifact_exists(self, job_id: int, artifact_type: str) -> bool:
        """Check if an artifact exists for a job."""
        return self._exists(
            "job_artifacts",
            "job_id = ? AND artifact_type = ?",
            (job_id, artifact_type)
        )

    def get_doc_status(self, job_id: int) -> DocStatus:
        """Get the status of generated documents for a job."""
        return DocStatus(
            resume_html=self.artifact_exists(job_id, "resume_html"),
            resume_pdf=self.artifact_exists(job_id, "resume_pdf"),
            coverletter_html=self.artifact_exists(job_id, "coverletter_html"),
            coverletter_pdf=self.artifact_exists(job_id, "coverletter_pdf"),
        )

    def delete_artifacts(self, job_id: int) -> None:
        """Delete all artifacts for a job."""
        self._delete("job_artifacts", "job_id = ?", (job_id,))

    # =========================================================================
    # DELETE ALL SUBCONTENT
    # =========================================================================

    def delete_all_subcontent(self, job_id: int) -> None:
        """Delete all subcontent for a job."""
        self.delete_contacts(job_id)
        self.delete_summary(job_id)
        self.delete_skills(job_id)
        self.delete_highlights(job_id)
        self.delete_experience(job_id)
        self.delete_education(job_id)
        self.delete_awards(job_id)
        self.delete_coverletter(job_id)
        self.delete_artifacts(job_id)

    # =========================================================================
    # EXPORT
    # =========================================================================

    def to_dict(self, job_id: int, section: str) -> Optional[dict | list | str]:
        """
        Export a subcontent section as a YAML-compatible value.

        Args:
            job_id: Job database ID.
            section: Section name.

        Returns:
            YAML-compatible value (dict, list, or string depending on section).
        """
        if section == "contacts":
            contacts = self.get_contacts(job_id)
            if not contacts:
                return None
            return [
                {
                    "name": c.name,
                    "label": c.label,
                    "url": c.url,
                    "icon": c.icon,
                }
                for c in contacts
            ]

        elif section == "summary":
            return self.get_summary(job_id)

        elif section == "skills":
            skills = self.get_skills(job_id)
            return skills if skills else None

        elif section == "highlights":
            highlights = self.get_highlights(job_id)
            return highlights if highlights else None

        elif section == "experience":
            companies = self.get_experience(job_id)
            if not companies:
                return None
            return [self._company_to_dict(c) for c in companies]

        elif section == "education":
            education = self.get_education(job_id)
            if not education:
                return None
            return [
                {
                    "course": e.course,
                    "school": e.school,
                    "dates": e.dates,
                }
                for e in education
            ]

        elif section == "awards":
            awards = self.get_awards(job_id)
            if not awards:
                return None
            return [
                {
                    "award": a.award,
                    "reward": a.reward,
                    "dates": a.dates,
                }
                for a in awards
            ]

        elif section == "coverletter":
            return self.get_coverletter(job_id)

        return None

    def _company_to_dict(self, company: Company) -> dict:
        """Convert a Company object to a YAML-compatible dict."""
        result = {
            "company_name": company.company_name,
        }

        # Handle company_urls - single string if one, list if multiple
        if len(company.company_urls) == 1:
            result["company_urls"] = company.company_urls[0]
        elif len(company.company_urls) > 1:
            result["company_urls"] = company.company_urls

        if company.employees:
            result["employees"] = company.employees
        if company.dates:
            result["dates"] = company.dates
        if company.location:
            result["location"] = company.location
        if company.company_description:
            result["company_description"] = company.company_description

        if company.roles:
            result["roles"] = [
                self._role_to_dict(r) for r in company.roles
            ]

        return result

    def _role_to_dict(self, role: Role) -> dict:
        """Convert a Role object to a YAML-compatible dict."""
        result = {
            "role": role.role,
        }

        if role.original_id is not None:
            result["id"] = role.original_id
        if role.dates:
            result["dates"] = role.dates
        if role.location:
            result["location"] = role.location

        if role.bullets:
            result["bullets"] = [
                self._bullet_to_dict(b) for b in role.bullets
            ]

        return result

    def _bullet_to_dict(self, bullet: Bullet) -> dict:
        """Convert a Bullet object to a YAML-compatible dict."""
        result = {
            "text": bullet.text,
        }

        if bullet.original_id is not None:
            result["id"] = bullet.original_id
        if bullet.tags:
            result["tags"] = bullet.tags

        return result
