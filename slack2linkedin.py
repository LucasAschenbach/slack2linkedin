#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["emoji", "beautifulsoup4", "PyQt5"]
# ///

"""
Convert whatever Slack put on your clipboard (HTML → RTF → plain)
into a LinkedIn-friendly plain-text snippet:

 • keeps **bold**, *italic* via Unicode "𝗯𝗼𝗹𝗱" / "𝘪𝘵𝘢𝘭𝘪𝘤" sans-serif alphabets
 • replaces :emoji: codes *and* Slack <img …> emoji stubs with real emoji
 • puts the cleaned text back on the clipboard and prints it

Only the ``convert_clipboard`` helper requires PyQt5. The ``convert_plain``
and ``convert_html`` functions work in any Python environment, including
Pyodide.
"""

import re, sys, html
from bs4 import BeautifulSoup, NavigableString, Tag
import emoji

# ───── Unicode style maps ────────────────────────────────────────────────────
def _build_maps():
    bold, italic, bital = {}, {}, {}
    for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        bold[ch]   = chr(0x1D5D4+i)  # Sans-Serif Bold
        italic[ch] = chr(0x1D608+i)  # Sans-Serif Italic
        bital[ch]  = chr(0x1D608+i)  # No specific Sans Bold-Italic, using Italic
    for i,ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
        bold[ch]   = chr(0x1D5EE+i)  # Sans-Serif Bold
        italic[ch] = chr(0x1D622+i)  # Sans-Serif Italic
        bital[ch]  = chr(0x1D622+i)  # No specific Sans Bold-Italic, using Italic
    for i,ch in enumerate("0123456789"):
        bold[ch]   = chr(0x1D7EC+i)  # Sans-Serif Bold Digits
        italic[ch] = bital[ch] = ch  # No specific Sans-Serif Italic digits
    return bold, italic, bital
_BOLD, _ITALIC, _BITAL = _build_maps()

def _stylize(txt, bold=False, italic=False):
    trans = _BITAL if bold and italic else _BOLD if bold else _ITALIC if italic else None
    if not trans:                                   # nothing to do
        return txt
    return "".join(trans.get(c,c) for c in txt)

# ───── Emoji helpers ────────────────────────────────────────────────────────
_EMOJI_RE = re.compile(r":[\w\-\+]+:")
def _emojize(txt: str) -> str:
    """Convert :rocket: → 🚀 ; leave unknown aliases untouched."""
    return emoji.emojize(txt, language="alias", delimiters=(":",":"))

# ───── Clipboard fallbacks ───────────────────────────────────────────────────
def convert_plain(src: str) -> str:
    return _emojize(src)

def _convert_rtf(src: bytes) -> str:
    s = src.decode("utf-8", "ignore")
    s = re.sub(r"\\par[d]? ?", "\n", s)

    def _rtf_swap(regex, to_bold, to_italic):
        def repl(m):
            return _stylize(_emojize(m.group(1)), to_bold, to_italic)
        return re.sub(regex, repl, s)

    s = _rtf_swap(r"{\\b\s+([^}]*)}", True, False)
    s = _rtf_swap(r"{\\i\s+([^}]*)}", False, True)
    s = _rtf_swap(r"\\b\s+([^\\]+?)\\b0", True, False)
    s = _rtf_swap(r"\\i\s+([^\\]+?)\\i0", False, True)

    s = re.sub(r"[\\][a-z]+\d* ?", "", s)
    s = re.sub(r"[{}]", "", s)
    return s

def convert_html(src: str) -> str:
    soup = BeautifulSoup(src, "html.parser")

    def _emoji_from_img(tag: Tag) -> str:
        alias = tag.get("data-stringify-emoji") or tag.get("alt")
        return _emojize(alias) if alias and _EMOJI_RE.fullmatch(alias) else ""

    def walk(node, bold=False, italic=False) -> str:
        out = []
        for child in node.children:
            # ---------- TAG HANDLING -----------------------------------------
            if isinstance(child, Tag):
                n   = child.name
                cls = child.get("class", [])

                if "c-mrkdwn__br" in cls or child.get("data-stringify-type") == "paragraph-break":
                    out.append("\n\n")
                    continue

                if n in ("b", "strong"):
                    out.append(walk(child, True, italic))
                elif n in ("i", "em"):
                    out.append(walk(child, bold, True))
                elif n in ("br",):
                    out.append("\n")
                elif n in ("p", "div"):
                    out.append(walk(child, bold, italic) + "\n")
                elif n == "li":
                    out.append("• " + walk(child, bold, italic).lstrip() + "\n")
                elif n == "img":
                    out.append(_emoji_from_img(child))
                else:                       # span, a, ul, etc.
                    out.append(walk(child, bold, italic))

            # ---------- TEXT NODES ------------------------------------------
            elif isinstance(child, NavigableString):
                text = html.unescape(str(child)).replace("\u00A0", " ")
                text = _emojize(text)
                out.append(_stylize(text, bold, italic))
        return "".join(out)

    return walk(soup).rstrip()

# ───── Main entry-point ─────────────────────────────────────────────────────
def convert_clipboard():
    """Convert the current clipboard content and update the clipboard."""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QMimeData

    app = QApplication.instance() or QApplication(sys.argv)
    cb = app.clipboard()
    md = cb.mimeData()

    if md.hasHtml():
        txt, src = convert_html(md.html()), "HTML"
    elif md.hasFormat("text/rtf"):
        txt, src = _convert_rtf(bytes(md.data("text/rtf"))), "RTF"
    else:
        txt, src = convert_plain(md.text()), "plain"

    clip = QMimeData()
    clip.setText(txt)
    cb.setMimeData(clip)

    return txt, src


def main():
    txt, src = convert_clipboard()
    sys.stdout.write(f"[{src}] → plain text now on clipboard\n\n")
    sys.stdout.write(txt + "\n")

if __name__ == "__main__":
    main()

