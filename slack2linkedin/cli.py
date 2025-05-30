#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["emoji", "beautifulsoup4", "PyQt5"]
# ///

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData
from .convert import convert_html, convert_plain, _convert_rtf


"""
Convert whatever Slack put on your clipboard (HTML → RTF → plain)
into a LinkedIn-friendly plain-text snippet:

 • keeps **bold**, *italic* via Unicode "𝗯𝗼𝗹𝗱" / "𝘪𝘵𝘢𝘭𝘪𝘤" sans-serif alphabets
 • replaces :emoji: codes *and* Slack <img …> emoji stubs with real emoji
 • puts the cleaned text back on the clipboard and prints it

"""

# ───── Main entry-point ─────────────────────────────────────────────────────
def convert_clipboard():
    """Convert the current clipboard content and update the clipboard."""

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
