"""
Repository for resume data access.
"""

import sqlite3
from datetime import datetime
from typing import Optional

from .base_repository import BaseRepository
from ..db.models import (
    Resume, Contact, Company, Role, Bullet, Education, Award
)


class ResumeRepository(BaseRepository):
    """
    Repository for managing resume data.

    Handles full resume CRUD with nested entities (contacts, skills,
    experience with companies/roles/bullets, education, awards, etc.).
    """

    # =========================================================================
    # READ OPERATIONS
    # =========================================================================

    def get_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        Get a full resume by ID with all nested data.

        Args:
            resume_id: Resume database ID.

        Returns:
            Resume object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM resumes WHERE id = ?",
            (resume_id,)
        )
        if not row:
            return None

        return self._build_resume(row)

    def get_by_slug(self, slug: str) -> Optional[Resume]:
        """
        Get a full resume by slug with all nested data.

        Args:
            slug: Resume slug (filename without .yaml).

        Returns:
            Resume object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM resumes WHERE slug = ?",
            (slug,)
        )
        if not row:
            return None

        return self._build_resume(row)

    def get_all(self) -> list[Resume]:
        """
        Get all resumes (metadata only, no nested data).

        Returns:
            List of Resume objects with basic info.
        """
        rows = self._fetch_all("SELECT * FROM resumes ORDER BY name")
        return [
            Resume(
                id=row['id'],
                slug=row['slug'],
                name=row['name'],
                location=row['location'],
                summary=row['summary'],
                icon_folder_url=row['icon_folder_url'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
            for row in rows
        ]

    def get_all_slugs(self) -> list[str]:
        """
        Get all resume slugs.

        Returns:
            List of slug strings.
        """
        rows = self._fetch_all("SELECT slug FROM resumes ORDER BY slug")
        return [row['slug'] for row in rows]

    def exists(self, slug: str) -> bool:
        """Check if a resume with the given slug exists."""
        return self._exists("resumes", "slug = ?", (slug,))

    # =========================================================================
    # WRITE OPERATIONS
    # =========================================================================

    def create(self, resume: Resume) -> int:
        """
        Create a new resume with all nested data.

        Args:
            resume: Resume object to create.

        Returns:
            ID of the created resume.
        """
        self.begin_transaction()
        try:
            # Insert main resume
            resume_id = self._insert("resumes", {
                "slug": resume.slug,
                "name": resume.name,
                "location": resume.location,
                "summary": resume.summary,
                "icon_folder_url": resume.icon_folder_url,
            })

            # Insert nested data
            self._save_contacts(resume_id, resume.contacts)
            self._save_skills(resume_id, resume.skills)
            self._save_experience(resume_id, resume.experience)
            self._save_education(resume_id, resume.education)
            self._save_awards(resume_id, resume.awards_and_keynotes)
            self._save_passions(resume_id, resume.passions)
            self._save_enjoys(resume_id, resume.enjoys)

            self.commit()
            return resume_id
        except Exception:
            self.rollback()
            raise

    def update(self, resume_id: int, resume: Resume) -> None:
        """
        Update an existing resume with all nested data.

        This replaces all nested data (contacts, skills, etc.).

        Args:
            resume_id: ID of the resume to update.
            resume: Resume object with new data.
        """
        self.begin_transaction()
        try:
            # Update main resume
            self._update("resumes", {
                "name": resume.name,
                "location": resume.location,
                "summary": resume.summary,
                "icon_folder_url": resume.icon_folder_url,
                "updated_at": datetime.now().isoformat(),
            }, "id = ?", (resume_id,))

            # Delete existing nested data
            self._delete_nested_data(resume_id)

            # Re-insert nested data
            self._save_contacts(resume_id, resume.contacts)
            self._save_skills(resume_id, resume.skills)
            self._save_experience(resume_id, resume.experience)
            self._save_education(resume_id, resume.education)
            self._save_awards(resume_id, resume.awards_and_keynotes)
            self._save_passions(resume_id, resume.passions)
            self._save_enjoys(resume_id, resume.enjoys)

            self.commit()
        except Exception:
            self.rollback()
            raise

    def delete(self, resume_id: int) -> bool:
        """
        Delete a resume and all nested data.

        Args:
            resume_id: ID of the resume to delete.

        Returns:
            True if deleted, False if not found.
        """
        rowcount = self._delete("resumes", "id = ?", (resume_id,))
        return rowcount > 0

    def upsert(self, resume: Resume) -> int:
        """
        Create or update a resume based on slug.

        Args:
            resume: Resume object.

        Returns:
            ID of the resume.
        """
        existing = self._fetch_one(
            "SELECT id FROM resumes WHERE slug = ?",
            (resume.slug,)
        )
        if existing:
            self.update(existing['id'], resume)
            return existing['id']
        else:
            return self.create(resume)

    # =========================================================================
    # EXPORT
    # =========================================================================

    def to_dict(self, resume_id: int) -> Optional[dict]:
        """
        Export a resume as a YAML-compatible dictionary.

        Args:
            resume_id: Resume database ID.

        Returns:
            Dictionary matching original YAML structure.
        """
        resume = self.get_by_id(resume_id)
        if not resume:
            return None

        result = {
            "name": resume.name,
            "location": resume.location,
            "summary": resume.summary,
        }

        # Add internal section if icon_folder_url exists
        if resume.icon_folder_url:
            result["internal"] = {
                "folders": [{"icons": resume.icon_folder_url}]
            }

        # Add contacts
        if resume.contacts:
            result["contacts"] = [
                {
                    "name": c.name,
                    "label": c.label,
                    "url": c.url,
                    "icon": c.icon,
                }
                for c in resume.contacts
            ]

        # Add skills
        if resume.skills:
            result["skills"] = resume.skills

        # Add experience
        if resume.experience:
            result["experience"] = [
                self._company_to_dict(c) for c in resume.experience
            ]

        # Add education
        if resume.education:
            result["education"] = [
                {
                    "course": e.course,
                    "school": e.school,
                    "dates": e.dates,
                }
                for e in resume.education
            ]

        # Add awards
        if resume.awards_and_keynotes:
            result["awards_and_keynotes"] = [
                {
                    "award": a.award,
                    "reward": a.reward,
                    "dates": a.dates,
                }
                for a in resume.awards_and_keynotes
            ]

        # Add passions
        if resume.passions:
            result["passions"] = resume.passions

        # Add enjoys
        if resume.enjoys:
            result["enjoys"] = resume.enjoys

        return result

    def to_dict_by_slug(self, slug: str) -> Optional[dict]:
        """
        Export a resume by slug as a YAML-compatible dictionary.

        Args:
            slug: Resume slug.

        Returns:
            Dictionary matching original YAML structure.
        """
        row = self._fetch_one("SELECT id FROM resumes WHERE slug = ?", (slug,))
        if not row:
            return None
        return self.to_dict(row['id'])

    # =========================================================================
    # PRIVATE HELPERS - BUILD
    # =========================================================================

    def _build_resume(self, row: dict) -> Resume:
        """Build a full Resume object from a database row."""
        resume_id = row['id']

        return Resume(
            id=row['id'],
            slug=row['slug'],
            name=row['name'],
            location=row['location'],
            summary=row['summary'],
            icon_folder_url=row['icon_folder_url'],
            contacts=self._load_contacts(resume_id),
            skills=self._load_skills(resume_id),
            experience=self._load_experience(resume_id),
            education=self._load_education(resume_id),
            awards_and_keynotes=self._load_awards(resume_id),
            passions=self._load_passions(resume_id),
            enjoys=self._load_enjoys(resume_id),
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )

    def _load_contacts(self, resume_id: int) -> list[Contact]:
        """Load contacts for a resume."""
        rows = self._fetch_all(
            "SELECT * FROM resume_contacts WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
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

    def _load_skills(self, resume_id: int) -> list[str]:
        """Load skills for a resume."""
        rows = self._fetch_all(
            "SELECT skill FROM resume_skills WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
        )
        return [row['skill'] for row in rows]

    def _load_experience(self, resume_id: int) -> list[Company]:
        """Load experience (companies with roles and bullets) for a resume."""
        company_rows = self._fetch_all(
            "SELECT * FROM resume_companies WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
        )

        companies = []
        for comp_row in company_rows:
            company_id = comp_row['id']

            # Load URLs
            url_rows = self._fetch_all(
                "SELECT url FROM resume_company_urls WHERE company_id = ? ORDER BY sort_order",
                (company_id,)
            )
            urls = [r['url'] for r in url_rows]

            # Load roles
            role_rows = self._fetch_all(
                "SELECT * FROM resume_roles WHERE company_id = ? ORDER BY sort_order",
                (company_id,)
            )

            roles = []
            for role_row in role_rows:
                role_id = role_row['id']

                # Load bullets
                bullet_rows = self._fetch_all(
                    "SELECT * FROM resume_bullets WHERE role_id = ? ORDER BY sort_order",
                    (role_id,)
                )

                bullets = []
                for bullet_row in bullet_rows:
                    bullet_id = bullet_row['id']

                    # Load tags
                    tag_rows = self._fetch_all(
                        "SELECT tag FROM resume_bullet_tags WHERE bullet_id = ?",
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

    def _load_education(self, resume_id: int) -> list[Education]:
        """Load education for a resume."""
        rows = self._fetch_all(
            "SELECT * FROM resume_education WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
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

    def _load_awards(self, resume_id: int) -> list[Award]:
        """Load awards for a resume."""
        rows = self._fetch_all(
            "SELECT * FROM resume_awards WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
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

    def _load_passions(self, resume_id: int) -> list[str]:
        """Load passions for a resume."""
        rows = self._fetch_all(
            "SELECT passion FROM resume_passions WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
        )
        return [row['passion'] for row in rows]

    def _load_enjoys(self, resume_id: int) -> list[str]:
        """Load enjoys for a resume."""
        rows = self._fetch_all(
            "SELECT enjoy FROM resume_enjoys WHERE resume_id = ? ORDER BY sort_order",
            (resume_id,)
        )
        return [row['enjoy'] for row in rows]

    # =========================================================================
    # PRIVATE HELPERS - SAVE
    # =========================================================================

    def _save_contacts(self, resume_id: int, contacts: list[Contact]) -> None:
        """Save contacts for a resume."""
        for i, contact in enumerate(contacts):
            self._insert("resume_contacts", {
                "resume_id": resume_id,
                "name": contact.name,
                "label": contact.label,
                "url": contact.url,
                "icon": contact.icon,
                "sort_order": i,
            })

    def _save_skills(self, resume_id: int, skills: list[str]) -> None:
        """Save skills for a resume."""
        for i, skill in enumerate(skills):
            self._insert("resume_skills", {
                "resume_id": resume_id,
                "skill": skill,
                "sort_order": i,
            })

    def _save_experience(self, resume_id: int, companies: list[Company]) -> None:
        """Save experience (companies with roles and bullets) for a resume."""
        for i, company in enumerate(companies):
            company_id = self._insert("resume_companies", {
                "resume_id": resume_id,
                "company_name": company.company_name,
                "employees": company.employees,
                "dates": company.dates,
                "location": company.location,
                "company_description": company.company_description,
                "sort_order": i,
            })

            # Save URLs
            for j, url in enumerate(company.company_urls):
                self._insert("resume_company_urls", {
                    "company_id": company_id,
                    "url": url,
                    "sort_order": j,
                })

            # Save roles
            for j, role in enumerate(company.roles):
                role_id = self._insert("resume_roles", {
                    "company_id": company_id,
                    "original_id": role.original_id,
                    "role": role.role,
                    "dates": role.dates,
                    "location": role.location,
                    "sort_order": j,
                })

                # Save bullets
                for k, bullet in enumerate(role.bullets):
                    bullet_id = self._insert("resume_bullets", {
                        "role_id": role_id,
                        "original_id": bullet.original_id,
                        "text": bullet.text,
                        "sort_order": k,
                    })

                    # Save tags
                    for tag in bullet.tags:
                        self._insert("resume_bullet_tags", {
                            "bullet_id": bullet_id,
                            "tag": tag,
                        })

    def _save_education(self, resume_id: int, education: list[Education]) -> None:
        """Save education for a resume."""
        for i, edu in enumerate(education):
            self._insert("resume_education", {
                "resume_id": resume_id,
                "course": edu.course,
                "school": edu.school,
                "dates": edu.dates,
                "sort_order": i,
            })

    def _save_awards(self, resume_id: int, awards: list[Award]) -> None:
        """Save awards for a resume."""
        for i, award in enumerate(awards):
            self._insert("resume_awards", {
                "resume_id": resume_id,
                "award": award.award,
                "reward": award.reward,
                "dates": award.dates,
                "sort_order": i,
            })

    def _save_passions(self, resume_id: int, passions: list[str]) -> None:
        """Save passions for a resume."""
        for i, passion in enumerate(passions):
            self._insert("resume_passions", {
                "resume_id": resume_id,
                "passion": passion,
                "sort_order": i,
            })

    def _save_enjoys(self, resume_id: int, enjoys: list[str]) -> None:
        """Save enjoys for a resume."""
        for i, enjoy in enumerate(enjoys):
            self._insert("resume_enjoys", {
                "resume_id": resume_id,
                "enjoy": enjoy,
                "sort_order": i,
            })

    def _delete_nested_data(self, resume_id: int) -> None:
        """Delete all nested data for a resume (preserves the main resume row)."""
        # Note: ON DELETE CASCADE handles most of this, but we need to
        # delete the top-level children explicitly

        # Get company IDs first
        company_rows = self._fetch_all(
            "SELECT id FROM resume_companies WHERE resume_id = ?",
            (resume_id,)
        )

        # Delete in reverse dependency order
        for comp_row in company_rows:
            company_id = comp_row['id']
            # Roles will cascade delete bullets, which cascade delete tags
            self._delete("resume_company_urls", "company_id = ?", (company_id,))
            self._delete("resume_roles", "company_id = ?", (company_id,))

        self._delete("resume_companies", "resume_id = ?", (resume_id,))
        self._delete("resume_enjoys", "resume_id = ?", (resume_id,))
        self._delete("resume_passions", "resume_id = ?", (resume_id,))
        self._delete("resume_awards", "resume_id = ?", (resume_id,))
        self._delete("resume_education", "resume_id = ?", (resume_id,))
        self._delete("resume_skills", "resume_id = ?", (resume_id,))
        self._delete("resume_contacts", "resume_id = ?", (resume_id,))

    # =========================================================================
    # PRIVATE HELPERS - EXPORT
    # =========================================================================

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
