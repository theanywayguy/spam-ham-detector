# preprocess.py - Email text extraction and conversion utilities

from html import unescape
import re
from email.message import EmailMessage

def html_to_plain_text(html: str) -> str:
    """
    Convert HTML content to plain text by removing head, tags, and replacing links.
    """
    html = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    html = re.sub('<a\s.*?>', ' HYPERLINK ', html, flags=re.M | re.S | re.I)
    html = re.sub('<.*?>', '', html)
    html = re.sub(r'(\s*\n)+', '\n', html)
    return unescape(html)

def email_to_text(msg):
    """
    Extract plain text from an EmailMessage object.
    Handles both 'text/plain' and 'text/html'.
    """
    if isinstance(msg, str):
        return msg
    html = None
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype not in ("text/plain", "text/html"):
            continue
        try:
            content = part.get_content()
        except:
            content = str(part.get_payload())
        if ctype == "text/plain":
            return content
        else:
            html = content
    if html:
        return html_to_plain_text(html)
    return ""

def make_email_message_from_text(text: str, subject: str = None):
    """
    Wrap plain text (and optional subject) into an EmailMessage object.
    """
    msg = EmailMessage()
    if subject:
        msg['Subject'] = subject
    msg.set_content(text)
    return msg
