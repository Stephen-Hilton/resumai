from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os 
import imaplib
import email
import logging
from email.header import decode_header
from email.utils import parsedate_to_datetime
from . import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)

def get_gmails(gmail_address:str,
               app_password:str, 
               unread_only:bool=True, 
               subject_filters:list=None, 
               sender_filters:list=None,
               sent_since:datetime=None, 
               mark_as_read:bool=False, 
               max_results:int=25) -> list:
    """
    Connects to Gmail using OAuth2 and retrieves emails based on specified criteria, which is returned as a list of dictionaries.
    """
    logger.info(f"Connecting to Gmail for {gmail_address}")
    logger.debug(f"Filters - unread_only: {unread_only}, subject_filters: {subject_filters}, sender_filters: {sender_filters}, max_results: {max_results}")
    
    load_dotenv('.env')
    if not gmail_address:
        gmail_address = os.getenv('GMAIL_ADDRESS')
    if not app_password:
        app_password = os.getenv('GMAIL_APP_PASSWORD')
        
    if not gmail_address or not app_password:
        logger.error("Gmail credentials not provided")
        raise ValueError("Gmail credentials required")

    # Do not apply a default `sent_since` filter. Only filter by date
    # when the caller provides `sent_since` explicitly.

    def _decode_mime_words(value):
        if not value:
            return ''
        parts = decode_header(value)
        decoded = ''
        for part, encoding in parts:
            if isinstance(part, bytes):
                try:
                    decoded += part.decode(encoding or 'utf-8', errors='ignore')
                except Exception:
                    decoded += part.decode('utf-8', errors='ignore')
            else:
                decoded += part
        return decoded

    def _get_body(msg):
        text = ''
        html = ''
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in disp:
                    try:
                        text += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                    except Exception:
                        text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                elif ctype == 'text/html' and 'attachment' not in disp:
                    try:
                        html += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                    except Exception:
                        html += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            ctype = msg.get_content_type()
            if ctype == 'text/plain':
                text = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
            elif ctype == 'text/html':
                html = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
        return text, html

    results = []

    # Connect to Gmail IMAP
    imap_host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_host)
    try:
        mail.login(gmail_address, app_password)
    except imaplib.IMAP4.error as e:
        raise RuntimeError(f"IMAP login failed: {e}")

    try:
        mail.select('inbox')

        # Build a simple search query. We'll fetch based on UNSEEN and optionally
        # SINCE (only when `sent_since` supplied). Other filters are applied
        # in Python for flexibility.
        criteria = []
        if unread_only:
            criteria.append('UNSEEN')
        if sent_since is not None:
            # IMAP SINCE expects date in format DD-Mon-YYYY
            since_str = sent_since.strftime('%d-%b-%Y')
            criteria.append(f'SINCE {since_str}')
        if not criteria:
            search_crit = 'ALL'
        else:
            search_crit = ' '.join(criteria)

        status, data = mail.search(None, search_crit)
        if status != 'OK':
            return []

        ids = data[0].split()
        # process newest first
        ids = list(reversed(ids))

        count = 0
        for num in ids:
            if count >= max_results:
                break
            # Use BODY.PEEK[] to avoid marking messages as \Seen when fetching
            # the full message. Include FLAGS so we can inspect read state.
            status, msg_data = mail.fetch(num, '(BODY.PEEK[] FLAGS)')
            if status != 'OK':
                continue
            # Extract the first tuple payload containing the raw message bytes.
            raw = None
            for part in msg_data:
                if isinstance(part, tuple) and part[1]:
                    raw = part[1]
                    break
            if raw is None:
                # Nothing to parse
                continue
            msg = email.message_from_bytes(raw)

            subject = _decode_mime_words(msg.get('Subject'))
            frm = _decode_mime_words(msg.get('From'))
            to = _decode_mime_words(msg.get('To'))
            date_hdr = msg.get('Date')
            try:
                date_dt = parsedate_to_datetime(date_hdr) if date_hdr else None
            except Exception:
                date_dt = None

            # apply python-level filters
            if subject_filters:
                if not any(s.lower() in (subject or '').lower() for s in subject_filters):
                    # skip
                    continue
            if sender_filters:
                if not any(s.lower() in (frm or '').lower() for s in sender_filters):
                    continue
            if sent_since and date_dt:
                # Normalize both datetimes to UTC for safe comparison whether
                # they are timezone-aware or naive.
                try:
                    if date_dt.tzinfo is None:
                        date_cmp = date_dt.replace(tzinfo=timezone.utc)
                    else:
                        date_cmp = date_dt.astimezone(timezone.utc)
                    if sent_since.tzinfo is None:
                        sent_cmp = sent_since.replace(tzinfo=timezone.utc)
                    else:
                        sent_cmp = sent_since.astimezone(timezone.utc)
                except Exception:
                    date_cmp = date_dt
                    sent_cmp = sent_since
                if date_cmp < sent_cmp:
                    continue

            body_text, body_html = _get_body(msg)

            # find flags from fetch response
            is_read = False
            try:
                for part in msg_data:
                    if isinstance(part, tuple) and len(part) > 0:
                        head = part[0]
                        if isinstance(head, bytes) and b'FLAGS' in head:
                            if b'\\Seen' in head:
                                is_read = True
            except Exception:
                pass

            entry = {
                'id': num.decode() if isinstance(num, bytes) else str(num),
                'subject': subject,
                'from': frm,
                'to': to,
                'date': date_dt.astimezone(ZoneInfo("America/Los_Angeles")).isoformat() if date_dt else None,
                'body_text': body_text,
                'body_html': body_html,
                'raw': raw,
                'is_read': is_read,
            }

            results.append(entry)
            count += 1

            if mark_as_read:
                try:
                    mail.store(num, '+FLAGS', '\\Seen')
                except Exception:
                    pass
        
        results.sort(key=lambda x: x.get('date') or '', reverse=True)
        return results
    finally:
        try:
            mail.close()
        except Exception:
            pass
        try:
            mail.logout()
        except Exception:
            pass




def simple_test():
    # Test the function with different parameters
    load_dotenv('.env')
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    gmail_address = os.getenv("GMAIL_ADDRESS")
    
    # emails = get_gmails(gmail_address, app_password, unread_only=True, mark_as_read=False, max_results=3)
    # assert len(emails) >0, "I have verified there is at least one unread email in my inbox."
    # assert len(emails) >= 3, "The number of returned emails should be 3."
    
    emails = get_gmails(gmail_address, app_password, 
                        sender_filters=['LinkedIn Job Alerts'],
                        sent_since=datetime.now() - timedelta(days=3),
                        unread_only=False, 
                        mark_as_read=False, 
                        max_results=10)
    
    
    pass

if __name__ == "__main__":

    # simple_test()
    pass