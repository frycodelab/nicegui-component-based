"""Print page — renders HTML snippets, base64 images and structured pages into an
A4-style print view.  Other components import the encode_* helpers to build the
URL token; the /print/{data} route calls content() to decode and display it.

Typical usage from another component
─────────────────────────────────────
from components.print_component import encode_html, encode_image, encode_page, open_print

# Raw HTML
open_print(encode_html('<h1>Hello</h1><p>World</p>'))

# Single image  (plain base64 string — no data-URI prefix)
open_print(encode_image(my_b64_str, mime='image/png', caption='Scan result'))

# Structured document with mixed sections
token = encode_page(
    title    = 'Daily Report',
    subtitle = '2026-02-27',
    sections = [
        {'type': 'html',  'content': '<p>Summary paragraph…</p>'},
        {'type': 'image', 'content': img_b64, 'mime': 'image/jpeg', 'caption': 'Chart A'},
        {'type': 'html',  'content': some_table_html},
    ],
)
open_print(token)
"""

import base64
import json

from nicegui import ui

# ── Print-specific stylesheet (screen preview + @media print) ─────────────────
_PRINT_CSS = """
<style>
  /* Screen preview wrapper */
  @media screen {
    body { background: #f3f4f6; margin: 0; font-family: system-ui, -apple-system, sans-serif; }
    #pw  {
      max-width: 210mm; margin: 24px auto; background: #fff;
      padding: 32px 40px; box-shadow: 0 2px 16px rgba(0,0,0,.12);
      border-radius: 6px; min-height: 100vh;
    }
    .no-print { display: flex; }
  }
  /* Actual print output — strip chrome */
  @media print {
    body { margin: 0; }
    #pw  { box-shadow: none; padding: 0; margin: 0; border-radius: 0; }
    .no-print { display: none !important; }
  }
  /* Typography */
  .pw-title    { font-size: 22px; font-weight: 700; margin: 0 0 4px;  color: #111827; }
  .pw-subtitle { font-size: 13px; color: #6b7280;   margin: 0 0 24px; }
  .pw-section  { margin-bottom: 24px; }
  h1 { font-size: 18px; font-weight: 600; margin-bottom: 12px; color: #111827; }
  h2 { font-size: 15px; font-weight: 600; margin-bottom: 10px; color: #111827; }
  p, li { font-size: 13px; line-height: 1.6; color: #374151; }
  /* Images */
  .pw-img-wrap img { max-width: 100%; height: auto; display: block; border-radius: 4px; }
  .pw-caption { text-align: center; font-size: 11px; color: #9ca3af; margin-top: 6px; }
  /* Tables */
  table  { width: 100%; border-collapse: collapse; margin: 4px 0 12px; }
  th     { background: #f9fafb; font-weight: 600; text-align: left; }
  th, td { padding: 8px 12px; border: 1px solid #e5e7eb; font-size: 13px; }
  tr:nth-child(even) td { background: #f9fafb; }
  /* Screen-only print/close toolbar */
  #pw-toolbar {
    position: fixed; top: 12px; right: 16px;
    display: flex; gap: 8px; z-index: 100;
  }
    #pw-toolbar button {
        padding: 8px 18px; border-radius: 7px; border: none;
        font-size: 15px; font-weight: 600; cursor: pointer;
        background: #18181b; color: #fff; transition: background .15s;
        display: flex; align-items: center; gap: 7px;
    }
  #pw-toolbar button:hover { background: #3f3f46; }
    #pw-toolbar button.secondary {
        background: #f4f4f5; color: #18181b; border: 1px solid #d4d4d8;
    }
    #pw-toolbar button.secondary:hover { background: #e4e4e7; }

    /* Moderately larger print icon */
    #pw-toolbar .print-icon {
        font-size: 20px;
        margin-right: 6px;
        vertical-align: middle;
        line-height: 1;
    }
</style>
"""


# ── Public encoding helpers ────────────────────────────────────────────────────

def encode_html(html: str) -> str:
    """Encode a raw HTML fragment for the /print/{data} URL."""
    return _encode({"type": "html", "html": html})


def encode_image(b64_data: str, mime: str = "image/png", caption: str = "") -> str:
    """Encode a base64 image for the /print/{data} URL.

    b64_data must be a plain base64 string — no 'data:…;base64,' prefix.
    """
    return _encode({"type": "image", "data": b64_data, "mime": mime, "caption": caption})


def encode_page(
    title: str,
    subtitle: str = "",
    sections: list[dict] | None = None,
) -> str:
    """Encode a structured multi-section document for the /print/{data} URL.

    Each section dict:
      type    : 'html' | 'image'
      content : HTML string  OR  plain base64 image string
      mime    : (images) e.g. 'image/jpeg'  [default: 'image/png']
      caption : (images) caption text        [default: '']
    """
    return _encode({"type": "page", "title": title, "subtitle": subtitle, "sections": sections or []})


def open_print(token: str) -> None:
    """Open /print/{token} in a new browser tab — call after encode_*."""
    ui.run_javascript(f"window.open('/print/{token}', '_blank')")


# ── Internal helpers ───────────────────────────────────────────────────────────

def _encode(obj: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode()


def _decode(raw: str) -> dict | str:
    """Return a decoded dict (new envelope) or a plain HTML string (legacy)."""
    try:
        # New format: JSON → urlsafe-base64
        return json.loads(base64.urlsafe_b64decode(raw + "==").decode("utf-8"))
    except Exception:
        pass
    try:
        # Legacy: plain base64-encoded HTML
        return base64.b64decode(raw + "==").decode("utf-8")
    except Exception as e:
        return {"type": "html", "html": f'<p style="color:red">Decode error: {e}</p>'}


def _image_html(data: str, mime: str, caption: str) -> str:
    cap = f'<div class="pw-caption">{caption}</div>' if caption else ""
    return (
        f'<div class="pw-section pw-img-wrap">'
        f'<img src="data:{mime};base64,{data}" alt="{caption}">'
        f'{cap}</div>'
    )


def _section_html(sec: dict) -> str:
    if sec.get("type") == "image":
        return _image_html(sec.get("content", ""), sec.get("mime", "image/png"), sec.get("caption", ""))
    return f'<div class="pw-section">{sec.get("content", "")}</div>'


def _build_inner(decoded: dict | str) -> str:
    if isinstance(decoded, str):
        # Legacy plain-HTML fallback
        return f'<div class="pw-section">{decoded}</div>'

    kind = decoded.get("type", "html")

    if kind == "image":
        return _image_html(decoded["data"], decoded.get("mime", "image/png"), decoded.get("caption", ""))

    if kind == "page":
        parts: list[str] = []
        if decoded.get("title"):
            parts.append(f'<div class="pw-title">{decoded["title"]}</div>')
        if decoded.get("subtitle"):
            parts.append(f'<div class="pw-subtitle">{decoded["subtitle"]}</div>')
        for sec in decoded.get("sections", []):
            parts.append(_section_html(sec))
        return "".join(parts)

    # kind == "html"
    return f'<div class="pw-section">{decoded.get("html", "")}</div>'


# ── Page handler — called by /print/{data} route in main.py ───────────────────

def content(data: str) -> None:
    ui.add_head_html(_PRINT_CSS, shared=False)

    inner = _build_inner(_decode(data))

    # Screen-only toolbar lets the user manually print or dismiss the tab
    ui.html(
        '<div id="pw-toolbar" class="no-print">'
        '  <button onclick="window.print()">'
        '    <span class="print-icon">🖨</span>'
        '    <span>Print</span>'
        '  </button>'
        '  <button class="secondary" onclick="window.close()">'
        '    <span style="font-size: 17px; vertical-align: middle;">✕</span>'
        '    <span style="font-size: 14px; margin-left: 5px;">Close</span>'
        '  </button>'
        '</div>'
        f'<div id="pw">{inner}</div>',
        sanitize=False,
    )

    # Small delay so Vue has painted the DOM before the print dialog opens;
    # onafterprint closes the tab automatically once the user is done
    ui.run_javascript("""
        setTimeout(function () {
            window.print();
            window.onafterprint = function () { window.close(); };
        }, 350);
    """)