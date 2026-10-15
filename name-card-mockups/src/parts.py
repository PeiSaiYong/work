"""Reusable HTML pieces for the name-card mockups.

Rule for everything drawn inside a phone: use wording quoted from the spec
(draft 0.2) or a dashed placeholder. Never invent UI wording.
"""

import html
import random
from pathlib import Path

SRC = Path(__file__).resolve().parent
E = html.escape

# Fictional sample person. Labelled "Sample data" wherever it appears.
P = {
    "name": "Alex Tan",
    "desig": "Corporate Sales Manager",
    "desig_new": "Senior Corporate Sales Manager",
    "email": "alex.tan@minmed.sg",
    "mobile": "+65 8000 1234",
    "slug": "alex-tan",
    "langs": "English, Mandarin",
    "time": "10:42 am, 15 Oct 2026",
}

BADGES = {
    "proposed": ("b-proposed", "Proposed", "In the spec for review, not yet approved"),
    "pending": ("b-pending", "Pending", "Decision still needed"),
    "candidate": ("b-candidate", "Candidate", "Named in the spec as an option, not chosen"),
    "example": ("b-example", "Example only", "Number given as an example, not a setting"),
    "sample": ("b-sample", "Sample data", "Fictional person and values"),
    "notspec": ("b-notspec", "Not in spec", "The spec does not describe this"),
    "rec": ("b-rec", "Recommended", "A recommendation for the spec, not yet in it"),
    "spec": ("b-spec", "In spec", "Described in the spec"),
}


def badge(kind, text=None, mini=False):
    cls, label, tip = BADGES[kind]
    extra = " mini" if mini else ""
    return f'<span class="badge {cls}{extra}" title="{E(tip)}">{E(text or label)}</span>'


def ph(text):
    """Block placeholder for wording or layout the spec has not defined."""
    return f'<div class="ph">[{E(text)}]</div>'


def phi(text):
    """Inline placeholder (button labels and the like)."""
    return f'<span class="ph-inline">[{E(text)}]</span>'


def mark(cls="mark"):
    # Stand-in "mm" mark from the minmed repo (frontend/src/components/Logo.tsx).
    return (
        f'<svg class="{cls}" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="16" fill="#96487F"/>'
        '<text x="16" y="21" text-anchor="middle" font-family="Lato, Arial, sans-serif" font-size="14" '
        'font-weight="900" fill="#fff">mm</text></svg>'
    )


LOCK = (
    '<svg width="11" height="12" viewBox="0 0 11 12" aria-hidden="true"><rect x="1" y="5" width="9" height="7" rx="1.5" '
    'fill="currentColor"/><path d="M3 5V3.5a2.5 2.5 0 0 1 5 0V5" stroke="currentColor" stroke-width="1.4" fill="none"/></svg>'
)


def qr(seed=7, size=21):
    """Illustrative QR-like pattern. Not scannable on purpose."""
    rnd = random.Random(seed)
    cells = []
    for y in range(size):
        for x in range(size):
            corner = (x < 8 and y < 8) or (x >= size - 8 and y < 8) or (x < 8 and y >= size - 8)
            if not corner and rnd.random() < 0.48:
                cells.append(f"M{x} {y}h1v1h-1z")
    finders = ""
    for fx, fy in ((0, 0), (size - 7, 0), (0, size - 7)):
        finders += (
            f'<rect x="{fx}" y="{fy}" width="7" height="7" fill="#192637"/>'
            f'<rect x="{fx + 1}" y="{fy + 1}" width="5" height="5" fill="#fff"/>'
            f'<rect x="{fx + 2}" y="{fy + 2}" width="3" height="3" fill="#192637"/>'
        )
    return (
        f'<svg class="qr" viewBox="-1 -1 {size + 2} {size + 2}" role="img" aria-label="Illustrative QR code (not scannable)">'
        f'<rect x="-1" y="-1" width="{size + 2}" height="{size + 2}" fill="#fff"/>'
        f'<path d="{"".join(cells)}" fill="#192637"/>{finders}</svg>'
    )


# ---------------------------------------------------------------- phone frame

def addr(domain="me.minmed.sg", path=None, fake=False):
    path = f"/{P['slug']}" if path is None else path
    cls = "addr fake" if fake else "addr"
    return f'<div class="{cls}">{LOCK}<span class="url"><b>{E(domain)}</b><span class="path">{E(path)}</span></span></div>'


def apphead(sub=""):
    s = f'<span class="sub">{sub}</span>' if sub else ""
    return f'<div class="apphead">{mark()}<span>Minmed</span>{s}</div>'


def chathead(who):
    return f'<div class="chathead"><span class="dot"></span><span>{who}</span></div>'


def phone(body, top="", kind="", cap="", short=False):
    screen_cls = "screen short" if short else "screen"
    caption = f'<div class="phone-cap">{cap}</div>' if cap else ""
    return (
        f'<div class="phone {kind}"><div class="sbar"></div>{top}'
        f'<div class="{screen_cls}">{body}</div></div>{caption}'
    )


# ---------------------------------------------------------------- statuses

def st_active(time=None):
    return (
        '<div class="status st-active"><span class="ic" aria-hidden="true">✓</span>'
        f'<span class="t">Active staff profile<span class="s">Checked {E(time or P["time"])}</span></span></div>'
    )


def st_unavail():
    return '<div class="status st-unavail"><span class="ic" aria-hidden="true">⊘</span><span class="t">Card unavailable</span></div>'


def st_error():
    return (
        '<div class="status st-error"><span class="ic" aria-hidden="true">!</span>'
        '<span class="t">Temporary verification error</span></div>'
    )


STAFF_STATES = {
    "approved": ("st-active", "●", "Approved and Active"),
    "pending": ("st-pending", "◷", "Pending review"),
    "rejected": ("st-rejected", "✕", "Changes not approved"),
    "deactivated": ("st-unavail", "⊘", "Card deactivated"),
}


def staff_status(kind, extra=""):
    cls, ic, label = STAFF_STATES[kind]
    return (
        f'<div class="status {cls}"><span class="ic" aria-hidden="true">{ic}</span>'
        f'<span class="t">{label}{extra}</span></div>'
    )


# ---------------------------------------------------------------- the card

def ncard(name=None, desig=None, email=None, mobile=None, seed=7, dim=False, hl=(), hl_cls="hl"):
    name = name or P["name"]
    desig = desig or P["desig"]
    email = email or P["email"]
    mobile = P["mobile"] if mobile is None else mobile

    def mk(field, text):
        return f'<span class="{hl_cls}">{E(text)}</span>' if field in hl else E(text)

    mob = f'<div class="line">{mk("mobile", mobile)}</div>' if mobile else ""
    return (
        f'<div class="ncard{" dim" if dim else ""}"><div class="band"></div><div class="body"><div class="info">'
        f'<div class="nm">{mk("name", name)}</div><div class="line">{mk("desig", desig)}</div>'
        f'<div class="co">Minmed</div><div class="line">{mk("email", email)}</div>{mob}'
        f'<div class="lk">me.minmed.sg/{P["slug"]}</div></div>{qr(seed)}</div></div>'
    )


# ---------------------------------------------------------------- recipient page

def public_page(desig=None, status="active", time=None, mobile=True, hl=(), extras=True):
    desig = desig or P["desig"]
    stat = {"active": st_active(time), "unavail": st_unavail(), "error": st_error()}[status]
    d = f'<span class="hl">{E(desig)}</span>' if "desig" in hl else E(desig)
    calls = (
        '<div class="btnrow"><div class="btn">Email</div><div class="btn">Call</div><div class="btn">WhatsApp</div></div>'
        if mobile
        else '<div class="btnrow"><div class="btn">Email</div></div>'
    )
    more = ""
    if extras:
        more = (
            '<dl class="kv"><div><dt>Languages</dt><dd style="margin:0">' + E(P["langs"]) + "</dd></div>"
            '<div><dt>LinkedIn</dt><dd style="margin:0" class="linktext">linkedin.com/in/…</dd></div></dl>'
        )
    return (
        '<div class="avatar">Photo<br>(optional)</div>'
        f'<p class="pname">{E(P["name"])}</p><p class="pdesig">{d}</p><p class="pco">Minmed</p>'
        f"{stat}"
        f'<span class="howto">How to verify {badge("proposed", mini=True)}</span>'
        '<div class="btn primary">Save contact</div>'
        f"{calls}{more}"
        '<div class="foot-link">About Minmed</div>'
    )


def not_found():
    return (
        '<div class="big-msg"><div class="ic" style="background:var(--grey-soft);color:var(--muted)">?</div>'
        "<p><b>No card found at this address.</b> Check the link or visit minmed.sg.</p></div><div class=\"blank\"></div>"
    )


# ---------------------------------------------------------------- staff view

def staff_buttons(share_on=True, edit_on=True, note=True):
    def b(label, on=True, extra=""):
        cls = "btn" if on else "btn off"
        return f'<div class="{cls}">{label}{extra}</div>'

    off_note = "" if share_on or not note else f'<div class="small muted" style="font-size:11px">Sharing, QR and downloads off until approval {badge("proposed", mini=True)}</div>'
    return (
        off_note
        + '<div class="btngrid">'
        + b("Share link", share_on)
        + b("Show QR", share_on)
        + b("Download QR", share_on)
        + b("Download image", share_on, " " + badge("pending", mini=True))
        + b("Edit my details", edit_on)
        + b("View public profile", True)
        + "</div>"
    )


def staff_view(state, card=None, between="", share_on=True, edit_on=True, buttons=True):
    card = ncard() if card is None else card
    return (
        staff_status(state) + between + card + (staff_buttons(share_on, edit_on) if buttons else "")
    )


def diff_table(rows, date="15 Oct 2026", labels=("Current public value", "You submitted")):
    """rows: list of (field, current public value, submitted value)."""
    out = [f'<div class="diff"><div class="row hd"><div>{labels[0]}</div><div>{labels[1]}</div></div>']
    for field, old, new in rows:
        out.append(
            f'<div class="row"><div class="fld">{E(field)}</div></div>'
            f'<div class="row"><div class="old">{E(old)}</div><div class="new">{E(new)}</div></div>'
        )
    out.append(f'<div class="row"><div class="fld" style="font-weight:400;color:var(--muted)">Submitted {E(date)}</div></div></div>')
    return "".join(out)


# ---------------------------------------------------------------- chat + email

def wa_preview(desig=None, open_line=True, mobile=True):
    desig = desig or P["desig"]
    mob = f"<div>{E(P['mobile'])}</div>" if mobile else ""
    open_txt = f'<div style="margin-top:3px">Open link for current details. {badge("proposed", mini=True)}</div>' if open_line else ""
    return (
        '<div class="preview"><div class="img">Photo (optional)</div><div class="txt">'
        f'<div class="ttl">{E(P["name"])}</div><div>{E(desig)} · Minmed</div>'
        f'<div>{E(P["email"])}</div>{mob}{open_txt}<div class="dom">me.minmed.sg</div></div></div>'
    )


def wa_bubble(desig=None, me=True, time="9:14 am", text="", open_line=True):
    cls = "bubble me" if me else "bubble"
    t = f"<div>{text}</div>" if text else ""
    return (
        f'<div class="{cls}">{wa_preview(desig, open_line)}'
        f'<div class="linktext">https://me.minmed.sg/{P["slug"]}</div>{t}<div class="time">{time}</div></div>'
    )


def email_phone(to, subject_ph, body_html, cap=""):
    head = (
        '<div class="mailhead">'
        f'<div><span class="k">From</span>{phi("sender address not specified")}</div>'
        f'<div><span class="k">To</span>{E(to)}</div>'
        f'<div><span class="k">Subject</span>{phi(subject_ph)}</div></div>'
    )
    return phone(head + body_html, top=apphead("Email"), cap=cap)


# ---------------------------------------------------------------- layout

def step(n, title, who, visual, notes, refs):
    lis = "".join(f"<li>{n_}</li>" for n_ in notes)
    return (
        f'<div class="step"><div class="step-head"><span class="num">{n}</span><div><h3>{title}</h3>'
        f'<div class="who">{who}</div></div></div>{visual}<ul class="notes">{lis}</ul>'
        f'<div class="ref">Spec: <b>{refs}</b></div></div>'
    )


def section(sid, eyebrow, title, intro, inner):
    return (
        f'<section class="section" id="{sid}"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>'
        f'<div class="intro">{intro}</div>{inner}</section>'
    )


NAV = [
    ("index.html", "Overview"),
    ("1-not-verified.html", "Not verified"),
    ("2-pending-change.html", "Pending change"),
    ("3-left-minmed.html", "Left Minmed"),
    ("4-security.html", "Security"),
    ("5-recommended.html", "Recommended"),
]


def legend():
    items = [
        (badge("proposed"), "In the spec for review, not yet approved."),
        (badge("pending"), "A decision is still needed."),
        (badge("candidate"), "Named in the spec as an option, not chosen (for example Cloudflare Turnstile)."),
        (badge("example"), "A number the spec gives as an example, not a setting."),
        (phi("…"), "Placeholder. The spec has not defined this wording or layout, so nothing was invented."),
        (badge("notspec"), "Something you might expect that the spec does not describe."),
        (badge("sample"), "Alex Tan is fictional. Names, titles, numbers and times are made up."),
    ]
    return '<div class="legend">' + "".join(f"<div>{b}<br>{t}</div>" for b, t in items) + "</div>"


def page(fname, title, desc, body, js=""):
    css = (SRC / "styles.css").read_text()
    on = ' class="on"'
    nav = "".join(f'<a href="{href}"{on if href == fname else ""}>{label}</a>' for href, label in NAV)
    script = f"<script>\n{js}\n</script>" if js else ""
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{E(desc)}">
<title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<header class="top"><div class="top-inner"><a class="brandline" href="index.html">{mark()}<span>Name Cards · mockups</span></a><nav class="nav" aria-label="Pages">{nav}</nav></div></header>
<main>
{body}
<div class="footer">Mockup based on Minmed Digital Name Cards Technical Specification draft 0.2 (15/10/2026). Not a final design: the spec fixes wording and behaviour, not visuals. Brand colours and fonts come from the minmed repo; the "mm" mark is the stand-in mark used in that repo, not a confirmed official logo. QR codes are illustrative and not scannable. Alex Tan and every other person shown are fictional.</div>
</main>
{script}
</body>
</html>
"""
