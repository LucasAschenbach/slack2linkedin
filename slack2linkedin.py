#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["emoji", "beautifulsoup4", "PyQt5"]
# ///

"""
slack2linkedin.py – v2
Convert whatever Slack put on your clipboard (HTML → RTF → plain)
into a LinkedIn-friendly plain-text snippet:

 • keeps **bold**, *italic* via Unicode “𝐛𝐨𝐥𝐝” / “𝑖𝑡𝑎𝑙𝑖𝑐” alphabets
 • replaces :emoji: codes *and* Slack <img …> emoji stubs with real emoji
 • puts the cleaned text back on the clipboard and prints it

Requires:  PyQt5  beautifulsoup4  emoji    →  pip install PyQt5 bs4 emoji
"""

import re, sys, html
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore    import QMimeData
from bs4             import BeautifulSoup, NavigableString, Tag
import emoji

# ───── Unicode style maps ────────────────────────────────────────────────────
def _build_maps():
    bold, italic, bital = {}, {}, {}
    for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        bold[ch]   = chr(0x1D400+i)
        italic[ch] = chr(0x1D434+i)
        bital[ch]  = chr(0x1D468+i)
    for i,ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
        bold[ch]   = chr(0x1D41A+i)
        italic[ch] = chr(0x1D44E+i)
        bital[ch]  = chr(0x1D482+i)
    for i,ch in enumerate("0123456789"):
        bold[ch]   = chr(0x1D7CE+i)
        italic[ch] = bital[ch] = ch
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
def _convert_plain(src: str) -> str:
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

def _convert_html(src: str) -> str:
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
def main():
    app = QApplication(sys.argv)
    cb  = app.clipboard()
    md  = cb.mimeData()

    if md.hasHtml():
        txt, src = _convert_html(md.html()), "HTML"
    elif md.hasFormat("text/rtf"):
        txt, src = _convert_rtf(bytes(md.data("text/rtf"))), "RTF"
    else:
        txt, src = _convert_plain(md.text()), "plain"

    clip = QMimeData()
    clip.setText(txt)
    cb.setMimeData(clip)

    sys.stdout.write(f"[{src}] → plain text now on clipboard\n\n")
    sys.stdout.write(txt + "\n")

if __name__ == "__main__":
    main()
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["emoji", "beautifulsoup4", "PyQt5"]
# ///

"""
slack2linkedin.py – v2
Convert whatever Slack put on your clipboard (HTML → RTF → plain)
into a LinkedIn-friendly plain-text snippet:

 • keeps **bold**, *italic* via Unicode “𝐛𝐨𝐥𝐝” / “𝑖𝑡𝑎𝑙𝑖𝑐” alphabets
 • replaces :emoji: codes *and* Slack <img …> emoji stubs with real emoji
 • puts the cleaned text back on the clipboard and prints it

Requires:  PyQt5  beautifulsoup4  emoji    →  pip install PyQt5 bs4 emoji
"""

import re, sys, html
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore    import QMimeData
from bs4             import BeautifulSoup, NavigableString, Tag
import emoji

# ───── Unicode style maps ────────────────────────────────────────────────────
def _build_maps():
    bold, italic, bital = {}, {}, {}
    for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        bold[ch]   = chr(0x1D400+i)
        italic[ch] = chr(0x1D434+i)
        bital[ch]  = chr(0x1D468+i)
    for i,ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
        bold[ch]   = chr(0x1D41A+i)
        italic[ch] = chr(0x1D44E+i)
        bital[ch]  = chr(0x1D482+i)
    for i,ch in enumerate("0123456789"):
        bold[ch]   = chr(0x1D7CE+i)
        italic[ch] = bital[ch] = ch
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
def _convert_plain(src: str) -> str:
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

def _convert_html(src: str) -> str:
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

                # *** NEW: Slack "paragraph-break" span → newline *************
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
def main():
    app = QApplication(sys.argv)
    cb  = app.clipboard()
    md  = cb.mimeData()

    if md.hasHtml():
        txt, src = _convert_html(md.html()), "HTML"
    elif md.hasFormat("text/rtf"):
        txt, src = _convert_rtf(bytes(md.data("text/rtf"))), "RTF"
    else:
        txt, src = _convert_plain(md.text()), "plain"

    clip = QMimeData()
    clip.setText(txt)
    cb.setMimeData(clip)

    sys.stdout.write(f"[{src}] → plain text now on clipboard\n\n")
    sys.stdout.write(txt + "\n")

if __name__ == "__main__":
    main()

