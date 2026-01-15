from __future__ import annotations

import imaplib
import email
from email.header import decode_header
from pathlib import Path
from datetime import datetime, timedelta
import re, os
from bs4 import BeautifulSoup

from src.lib.types import EventContext, EventResult
from src.events.create_jobfolder import execute as create_jobfolder
from src.lib.logging_utils import append_app_log

LINKEDIN_SUBJECT = "LinkedIn Job Alert"

JOB_ID_RE = re.compile(r"linkedin\.com/jobs/view/(\d+)")
DATEFMT = "%Y-%m-%d %H:%M:%S"

def _decode_subject(raw) -> str:
    parts = decode_header(raw)
    out = ""
    for p, enc in parts:
        if isinstance(p, bytes):
            out += p.decode(enc or "utf-8", errors="ignore")
        else:
            out += p
    return out

def parse_linkedin_email_jobs(html: str) -> list[dict]:
    """Best-effort extraction: find job links and nearby text."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = JOB_ID_RE.search(href)
        if not m:
            continue
        job_id = m.group(1)
        title = a.get_text(" ", strip=True)[:80] or "Unknown"
        # Attempt company from surrounding text
        company = "Unknown"
        parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
        # heuristic: look for 'at <company>'
        m2 = re.search(r"\bat\s+([A-Za-z0-9 &.,'-]{2,60})", parent_text)
        if m2:
            company = m2.group(1).strip()
        jobs.append({
            "id": job_id,
            "company": company,
            "title": title.replace(".", " "),
            "date_posted": datetime.now().strftime(DATEFMT),
            "url": f"https://www.linkedin.com/jobs/view/{job_id}",
            "source": {"type": "email", "provider": "linkedin", "url": f"https://www.linkedin.com/jobs/view/{job_id}"},
        })
    # de-dupe by id
    seen=set()
    ded=[]
    for j in jobs:
        if j["id"] in seen: 
            continue
        seen.add(j["id"])
        ded.append(j)
    return ded

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    host = ctx.state.get("imap_host")  or os.getenv("GMAIL_IMAP_HOST", "imap.gmail.com")
    user = ctx.state.get("username")   or os.getenv("GMAIL_USERNAME")
    pw = ctx.state.get("app_password") or os.getenv("GMAIL_APP_PASSWORD")
    mailbox = ctx.state.get("mailbox") or os.getenv("GMAIL_MAILBOX","INBOX")

    if not user or not pw:
        return EventResult(ok=False, job_path=job_path, message="GMAIL_USERNAME / GMAIL_APP_PASSWORD not set")

    created = 0
    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, pw)
        mail.select(mailbox)

        # last 2 weeks
        since = (datetime.now() - timedelta(days=14)).strftime("%d-%b-%Y")
        status, data = mail.search(None, f'(SINCE {since} SUBJECT "{LINKEDIN_SUBJECT}")')
        if status != "OK":
            return EventResult(ok=False, job_path=job_path, message="IMAP search failed")
        ids = data[0].split()
        for msgid in ids:
            status, msg_data = mail.fetch(msgid, "(RFC822)")
            if status != "OK":
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            subject = _decode_subject(msg.get("Subject",""))
            if LINKEDIN_SUBJECT not in subject:
                continue
            html = None
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/html":
                    html = part.get_payload(decode=True).decode(errors="ignore")
                    break
            if not html:
                continue
            jobs = parse_linkedin_email_jobs(html)
            for j in jobs:
                ctx2 = ctx
                ctx2.state = {**ctx.state, "job": j}
                res = await create_jobfolder(Path("."), ctx2)
                if res.ok:
                    created += 1
        mail.logout()
    except Exception as e:
        append_app_log(Path("src/logs"), f"get_gmail_linkedin error: {e}")
        return EventResult(ok=False, job_path=job_path, message=str(e))

    return EventResult(ok=True, job_path=job_path, message=f"created {created} jobs", artifacts=[])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    sample = ctx.state.get("sample_html","")
    jobs = parse_linkedin_email_jobs(sample)
    return EventResult(ok=True, job_path=job_path, message=f"parsed {len(jobs)} jobs")
