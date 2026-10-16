"""Full-size preview of the public card page, with made-up details.

Writes minmed-card-preview.html, a page that needs no other file, and gives
build.py the same preview for the dialog in the scope. Both use the card from
mocks.py and its styles from scope.css, scaled from the mockups' 282px-wide
screen to a real phone.
"""
import re
from pathlib import Path

import mocks as M

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "minmed-card-preview.html"
SCALE = 1.25

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">'
)
NOTE = "Preview with made-up details"


def _px(value):
    v = float(value)
    if v == 1:
        return "1px"
    return f"{round(v * SCALE, 1):g}px"


def card_css():
    """The public card's rules from scope.css, scaled for a real phone and scoped to .pvw."""
    css = (SRC / "scope.css").read_text()
    block = css[css.index("/* public card */"):css.index("/* message pages */")]
    base = ".ic { width: 18px; height: 18px; flex: none; }\n.mk { flex: none; display: block; }\n"
    src = re.sub(r"/\*.*?\*/", "", base + block, flags=re.S)
    out = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", src):
        scoped = ", ".join(".pvw " + s.strip() for s in sel.split(",") if s.strip())
        body = re.sub(r"(\d*\.?\d+)px", lambda m: _px(m.group(1)), body)
        out.append(f"{scoped} {{{body}}}")
    return "\n".join(out)


FRAME_CSS = """
.pvw .blogo .mk { width: 28px; height: 28px; }
.pvw .lk { width: 12px; height: 12px; flex: none; opacity: 0.55; }
.pvw .pv-dev { width: 412px; height: var(--dev-h, min(844px, calc(100vh - 48px))); margin: 0 auto; border: 11px solid #101216; border-radius: 54px; background: #fff; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 24px 60px rgba(25, 38, 55, 0.28); text-align: left; }
.pvw .pv-sb { height: 46px; flex: none; display: flex; align-items: center; justify-content: space-between; padding: 6px 30px 0 36px; font: 700 15px/1 "Open Sans", sans-serif; color: #111; background: #fff; }
.pvw .pv-scr { flex: 1; min-height: 0; overflow-y: auto; display: flex; flex-direction: column; background: #fff; }
.pvw .pv-bar { flex: none; padding: 9px 16px 18px; background: #f5f5f7; border-top: 1px solid #e4e4e8; display: flex; justify-content: center; }
.pvw .pv-bar span { display: inline-flex; align-items: center; gap: 6px; background: #e6e6ea; border-radius: 13px; padding: 8px 18px; font: 600 14px/1 "Open Sans", sans-serif; color: #2b2f36; }
.pvw .pv-note { flex: none; text-align: center; font: 600 12px/1.4 "Open Sans", sans-serif; color: #8f95a0; padding: 0 16px 18px; }
"""


def device():
    """The card page at full size in a phone frame; the frame drops away on a phone."""
    return (
        '<div class="pvw"><div class="pv-dev">'
        f'<div class="pv-sb"><span>9:41</span>{M._SB_ICONS}</div>'
        f'<div class="pv-scr">{M.card_body()}<div class="pv-note">{NOTE}</div></div>'
        f'<div class="pv-bar"><span>{M.ic("lock", "lk")}me.minmed.sg</span></div>'
        "</div></div>"
    )


PAGE_CSS = """
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: linear-gradient(#f8f0f6, #f2eef2) fixed; color: #2b2f36; font: 15px/1.5 "Open Sans", system-ui, -apple-system, "Segoe UI", sans-serif; }
.pv-stage { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; padding: 24px 16px; --dev-h: min(844px, calc(100vh - 150px)); }
.pv-intro { text-align: center; max-width: 440px; }
.pv-intro b { display: block; font: 900 20px/1.25 "Lato", sans-serif; color: #192637; }
.pv-intro span { display: block; margin-top: 4px; font-size: 14px; color: #5f6673; }
@media (max-width: 520px) {
  body { background: #fff; }
  .pv-stage { display: block; padding: 0; }
  .pv-intro, .pvw .pv-sb, .pvw .pv-bar { display: none; }
  .pvw .pv-dev { width: auto; height: auto; min-height: 100vh; min-height: 100dvh; border: 0; border-radius: 0; box-shadow: none; }
  .pvw .pv-scr { overflow: visible; }
}
"""


def page():
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<meta name="robots" content="noindex">
<meta name="description" content="Preview of a Minmed digital name card as a visitor sees it after scanning the QR code. Made-up details.">
<title>Card Preview</title>
{FONTS}
<style>
{card_css()}
{FRAME_CSS}
{PAGE_CSS}
</style>
</head>
<body>
<main class="pv-stage">
<div class="pv-intro"><b>Minmed digital name card</b><span>What a visitor sees after scanning a staff member's QR code. Made-up details; the buttons don't work.</span></div>
{device()}
</main>
</body>
</html>
"""


def write():
    doc = page()
    OUT.write_text(doc)
    print(f"wrote {OUT} ({len(doc):,} bytes)")


if __name__ == "__main__":
    write()
