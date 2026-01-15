from __future__ import annotations

import os
import asyncio
from pathlib import Path
from typing import Any

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from src.lib.types import EventContext
from src.events.event_bus import run_event
from src.lib.yaml_utils import load_yaml
from src.lib.job_folders import PHASES, phase_path

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    # Needed for flash() messages
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    def ctx() -> EventContext:
        jobs_root = Path(os.getenv("JOBS_ROOT", "./jobs")).resolve()
        resumes_root = Path(os.getenv("RESUMES_ROOT", "./resumes")).resolve()
        default_resume = os.getenv("DEFAULT_RESUME", "Stephen_Hilton.yaml")

        mode = request.form.get("mode", "llm")
        verbatim_mode = bool(request.form.get("verbatim"))  # checkbox

        c = EventContext(
            jobs_root=jobs_root,
            resumes_root=resumes_root,
            default_resume=default_resume,
            state={
                "mode": mode,
                "verbatim_mode": verbatim_mode,
            },
        )
        return c

    def _list_jobs_for_phase(jobs_root: Path, phase: str) -> list[dict[str, Any]]:
        p = phase_path(jobs_root, phase)
        if not p.exists():
            return []
        jobs = []
        for child in sorted(p.iterdir()):
            if child.is_dir():
                jobs.append({"name": child.name})
        return jobs

    @app.get("/")
    def dashboard():
        jobs_root = Path(os.getenv("JOBS_ROOT", "./jobs")).resolve()
        phases = []
        for ph in PHASES:
            phases.append({"phase": ph, "jobs": _list_jobs_for_phase(jobs_root, ph)})
        return render_template("dashboard.html", phases=phases)

    # --- Settings page (to satisfy base.html nav link) ---
    @app.get("/settings")
    def settings():
        env = {
            "JOBS_ROOT": os.getenv("JOBS_ROOT", "./jobs/"),
            "RESUMES_ROOT": os.getenv("RESUMES_ROOT", "./resumes/"),
            "DEFAULT_RESUME": os.getenv("DEFAULT_RESUME", "Stephen_Hilton.yaml"),
            "LLM_PROVIDER": os.getenv("LLM_PROVIDER", ""),
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL", ""),
            "GMAIL_USERNAME": os.getenv("GMAIL_USERNAME", ""),
        }
        return render_template("settings.html", env=env)

    # --- Option B: global importer from dashboard ---
    @app.post("/import/gmail/linkedin")
    def import_gmail_linkedin():
        c = ctx()
        # This event creates job folders under jobs/1_Queued (and/or other phases)
        res = asyncio.run(run_event("get_gmail_linkedin", c.jobs_root, c))
        if res.ok:
            flash(f"Imported LinkedIn jobs from Gmail: {res.message}")
        else:
            flash(f"Import FAILED: {res.message}")
        return redirect(url_for("dashboard"))

    @app.get("/job/<phase>/<job_folder>")
    def job_detail(phase: str, job_folder: str):
        jobs_root = Path(os.getenv("JOBS_ROOT", "./jobs")).resolve()
        job_path = phase_path(jobs_root, phase) / job_folder

        job_yaml_path = job_path / "job.yaml"
        job = load_yaml(job_yaml_path) if job_yaml_path.exists() else {}

        sub = {}
        invalid = {}
        for sec in ["summary", "skills", "highlights", "experience", "education", "awards"]:
            p = job_path / f"subcontent.{sec}.yaml"
            if p.exists():
                sub[sec] = p.read_text(encoding="utf-8")
            inv = job_path / f"subcontent.{sec}.invalid.yaml"
            if inv.exists():
                invalid[sec] = inv.read_text(encoding="utf-8")

        artifacts = {
            "job_html_exists": (job_path / "job.html").exists(),
            "resume_html_exists": (job_path / "resume.html").exists(),
            "resume_pdf_exists": (job_path / "resume.pdf").exists(),
            "coverletter_html_exists": (job_path / "coverletter.html").exists(),
            "coverletter_pdf_exists": (job_path / "coverletter.pdf").exists(),
        }

        return render_template(
            "job_detail.html",
            phase=phase,
            job_folder=job_folder,
            job=job,
            sub=sub,
            invalid=invalid,
            artifacts=artifacts,
        )

    @app.post("/job/<phase>/<job_folder>/run")
    def run_job_event(phase: str, job_folder: str):
        event = request.form.get("event")
        if not event:
            flash("No event selected.")
            return redirect(url_for("job_detail", phase=phase, job_folder=job_folder))

        jobs_root = Path(os.getenv("JOBS_ROOT", "./jobs")).resolve()
        job_path = phase_path(jobs_root, phase) / job_folder
        res = asyncio.run(run_event(event, job_path, ctx()))
        flash(f"Event {event}: {'OK' if res.ok else 'FAILED'} - {res.message}")
        new_phase = res.job_path.parent.name
        new_folder = res.job_path.name
        return redirect(url_for("job_detail", phase=new_phase, job_folder=new_folder))

    @app.post("/job/<phase>/<job_folder>/move")
    def move_job(phase: str, job_folder: str):
        target_phase = request.form.get("target_phase")
        if not target_phase:
            flash("No target phase selected.")
            return redirect(url_for("job_detail", phase=phase, job_folder=job_folder))

        jobs_root = Path(os.getenv("JOBS_ROOT", "./jobs")).resolve()
        job_path = phase_path(jobs_root, phase) / job_folder

        move_event = {
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
            "Errored": "move_errored",
        }.get(target_phase)

        if not move_event:
            flash(f"Unknown target phase: {target_phase}")
            return redirect(url_for("job_detail", phase=phase, job_folder=job_folder))

        res = asyncio.run(run_event(move_event, job_path, ctx()))
        flash(f"Moved to {target_phase}: {'OK' if res.ok else 'FAILED'}")
        return redirect(url_for("job_detail", phase=res.job_path.parent.name, job_folder=res.job_path.name))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
