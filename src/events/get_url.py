from __future__ import annotations

from pathlib import Path
import requests
from urllib.parse import urlparse

from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_text, dump_yaml
from src.lib.logging_utils import append_job_log

HEADERS = {"User-Agent":"Mozilla/5.0 (Resumai2)"}

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    job_yaml_path = job_path / "job.yaml"
    if not job_yaml_path.exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml missing")
    job = load_yaml(job_yaml_path)
    url = job.get("url") or job.get("source",{}).get("url")
    if not url:
        return EventResult(ok=False, job_path=job_path, message="job.yaml has no url")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    html = r.text
    dump_text(job_path / "job.html", html)
    # augment job.yaml with domain if missing
    domain = urlparse(url).netloc
    job.setdefault("source", {})
    job["source"].setdefault("type", "url")
    job["source"].setdefault("provider", domain)
    job["source"]["url"] = url
    dump_yaml(job_yaml_path, job)
    append_job_log(job_path, f"get_url: fetched {len(html)} chars from {domain}")
    return EventResult(ok=True, job_path=job_path, message="fetched", artifacts=["job.html"])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")
