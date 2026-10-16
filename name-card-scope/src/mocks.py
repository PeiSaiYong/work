"""High-fidelity mockup pieces for the name card scope.

Everything here is illustrative: names, numbers, codes and QR codes are made up,
and the QR patterns are deliberately not scannable.
"""

import html
import random

E = html.escape

# Fictional sample person and link, used across every mockup.
P = {
    "first": "Alex",
    "name": "Alex Tan",
    "initials": "AT",
    "desig": "Corporate Sales Manager",
    "desig_new": "Senior Corporate Sales Manager",
    "email": "alex.tan@minmed.sg",
    "mobile": "+65 8000 1234",
    "bio": "Helps companies plan health screenings and vaccination programmes for their staff.",
    "langs": "English, Mandarin, Malay",
    "linkedin": "linkedin.com/in/alextan-sample",
    "code": "qB8Rh9sTxKuaSF3YkGmD2w",
    "path": "/card/qB8Rh9sTxKuaSF3YkGmD2w",
    "alias": "Alex-Tan",
}
LINK = "me.minmed.sg" + P["path"]
LINK_ALIAS = f"me.minmed.sg/card/{P['alias']}/{P['code']}"


# ---------------------------------------------------------------- small parts

def mark(size=22, circle="#96487F", text="#fff"):
    return (
        f'<svg class="mk" width="{size}" height="{size}" viewBox="0 0 32 32" aria-hidden="true">'
        f'<circle cx="16" cy="16" r="16" fill="{circle}"/>'
        f'<text x="16" y="21" text-anchor="middle" font-family="Lato, Arial, sans-serif" '
        f'font-size="14" font-weight="900" fill="{text}">mm</text></svg>'
    )


_ICONS = {
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18h2"/>',
    "chat": '<path d="M4 5h16v11H10l-5 4v-4H4z"/>',
    "save": '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3.1-7 7-7s7 3 7 7"/><path d="M19 5v6M16 8h6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "ban": '<circle cx="12" cy="12" r="9"/><path d="M5.7 5.7l12.6 12.6"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.6V14"/><path d="M12 17.2v.1"/>',
    "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h8"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "upload": '<path d="M12 15V3M7 8l5-5 5 5M4 20h16"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "more": '<circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "alert": '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4M12 17v.1"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7.5a4 4 0 0 1 8 0V11"/>',
    "wallet": '<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M16 14.5h2"/>',
    "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    "send": '<path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 13.8c1.9.9 3 3 3 6.2"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.1M3.5 12h.1M3.5 18h.1"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "card": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><circle cx="8.5" cy="11" r="2.2"/><path d="M5.5 16c.6-1.5 1.7-2.2 3-2.2s2.4.7 3 2.2M14 10h4.5M14 13.5h3"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "out": '<path d="M15 4h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-4M10 16l4-4-4-4M14 12H4"/>',
}


def ic(name, cls="ic"):
    if name == "in":
        return (
            f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3.5" '
            'fill="currentColor"/><text x="12" y="16.6" text-anchor="middle" font-family="Arial, sans-serif" '
            'font-size="10.5" font-weight="700" fill="#fff">in</text></svg>'
        )
    if name == "aa":
        return (
            f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><text x="12" y="17" text-anchor="middle" '
            'font-family="Lato, Arial, sans-serif" font-size="13" font-weight="900" fill="currentColor">Aa</text></svg>'
        )
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICONS[name]}</svg>'
    )


def qr(seed=7, size=25, dark="#192637", cls="qr"):
    """QR-like pattern for illustration. Deliberately not scannable."""
    rnd = random.Random(seed)
    cells = []
    for y in range(size):
        for x in range(size):
            corner = (x < 8 and y < 8) or (x >= size - 8 and y < 8) or (x < 8 and y >= size - 8)
            if not corner and rnd.random() < 0.47:
                cells.append(f"M{x} {y}h1v1h-1z")
    finders = ""
    for fx, fy in ((0, 0), (size - 7, 0), (0, size - 7)):
        finders += (
            f'<rect x="{fx}" y="{fy}" width="7" height="7" fill="{dark}"/>'
            f'<rect x="{fx + 1}" y="{fy + 1}" width="5" height="5" fill="#fff"/>'
            f'<rect x="{fx + 2}" y="{fy + 2}" width="3" height="3" fill="{dark}"/>'
        )
    return (
        f'<svg class="{cls}" viewBox="-1.5 -1.5 {size + 3} {size + 3}" role="img" '
        'aria-label="Example QR code (not scannable)">'
        f'<rect x="-1.5" y="-1.5" width="{size + 3}" height="{size + 3}" fill="#fff"/>'
        f'<path d="{"".join(cells)}" fill="{dark}"/>{finders}</svg>'
    )


def chip(text, kind="rec"):
    return f'<span class="chip c-{kind}">{text}</span>'


# ---------------------------------------------------------------- frames

_SB_ICONS = (
    '<svg width="44" height="11" viewBox="0 0 44 11" aria-hidden="true">'
    '<rect x="0" y="7" width="3" height="4" rx=".8" fill="currentColor"/><rect x="4.5" y="5" width="3" height="6" rx=".8" fill="currentColor"/>'
    '<rect x="9" y="3" width="3" height="8" rx=".8" fill="currentColor"/><rect x="13.5" y="1" width="3" height="10" rx=".8" fill="currentColor"/>'
    '<rect x="21.5" y=".5" width="19" height="10" rx="3" fill="none" stroke="currentColor" opacity=".45"/>'
    '<rect x="23" y="2" width="14" height="7" rx="1.8" fill="currentColor"/><rect x="41.5" y="3.5" width="1.6" height="4" rx=".8" fill="currentColor" opacity=".45"/></svg>'
)


def phone(body, url="me.minmed.sg", cls=""):
    """iPhone-style frame. `url` shows Safari's address bar; None hides it (apps)."""
    bar = f'<div class="urlbar"><span>{ic("lock", "lk")}{E(url)}</span></div>' if url else ""
    return (
        f'<div class="phone {cls}"><div class="scr"><div class="island"></div>'
        f'<div class="sb"><span>9:41</span>{_SB_ICONS}</div><div class="pbody">{body}</div>{bar}</div></div>'
    )


def browser(url, body, cls=""):
    return (
        f'<div class="browser {cls}"><div class="chrome"><div class="dots"><i></i><i></i><i></i></div>'
        f'<div class="url">{ic("lock", "lk")}<span>{E(url)}</span></div></div><div class="vp">{body}</div></div>'
    )


def thumb(inner, kind="phone"):
    """Scaled-down copy of a screen for the site map. Decorative."""
    return f'<span class="thumb t-{kind}" aria-hidden="true"><span class="tz">{inner}</span></span>'


# ---------------------------------------------------------------- public pages

def band(small=False):
    cls = "band sm" if small else "band"
    return f'<div class="{cls}"><div class="blogo">{mark(22, "#fff", "#96487F")}<span>Minmed</span></div></div>'


def card_body(mobile=True, desig=None, compact=False):
    desig = desig or P["desig"]
    calls = (
        f'<div class="pc-row"><div class="btn-s">{ic("mail")}Email</div><div class="btn-s">{ic("phone")}Call</div>'
        f'<div class="btn-s">{ic("chat")}WhatsApp</div></div>'
        if mobile
        else f'<div class="pc-row one"><div class="btn-s">{ic("mail")}Email</div></div>'
    )
    mob = (
        f'<div class="pc-item">{ic("phone")}<span><span class="k">Mobile</span>{E(P["mobile"])}</span></div>'
        if mobile
        else ""
    )
    about = (
        ""
        if compact
        else (
            '<div class="pc-sec">About</div>'
            f'<p class="pc-bio">{E(P["bio"])}</p>'
            f'<div class="pc-item">{ic("aa")}<span><span class="k">Languages</span>{E(P["langs"])}</span></div>'
            f'<div class="pc-item">{ic("in")}<span><span class="k">LinkedIn</span><span class="lnk">{E(P["linkedin"])}</span></span></div>'
        )
    )
    return (
        f'<div class="pc">{band()}<div class="pc-av">{P["initials"]}</div>'
        f'<div class="pc-name">{E(P["name"])}</div><div class="pc-desig">{E(desig)}</div><div class="pc-co">Minmed</div>'
        f'<div class="pc-act"><div class="btn-p">{ic("save")}Save contact</div>{calls}</div>'
        f'<div class="pc-list"><div class="pc-item">{ic("mail")}<span><span class="k">Work email</span>{E(P["email"])}</span></div>{mob}'
        f"{about}</div>"
        f'<div class="pc-foot"><span>{ic("globe")}About Minmed</span></div></div>'
    )


def card_desktop():
    side = (
        f'<div class="dq">{qr(11)}<div class="dq-t">Scan to save to your phone</div></div>'
    )
    return (
        f'<div class="desk"><div class="desk-col">{card_body(compact=False)}</div>{side}</div>'
    )


def msg_page(icon, title, text="", link="About Minmed", tone="grey"):
    t = f'<p class="mp-text">{text}</p>' if text else ""
    return (
        f'<div class="pc">{band(small=True)}<div class="mp"><div class="mp-ic {tone}">{ic(icon)}</div>'
        f'<div class="mp-title">{title}</div>{t}<div class="mp-link">{ic("globe")}{link}</div></div></div>'
    )


def inactive_page():
    return msg_page("ban", "This card is no longer active.")


def notfound_page():
    return msg_page("question", "No card found at this address.", "Check the link or visit minmed.sg.", link="minmed.sg")


def error_page():
    return (
        f'<div class="pc">{band(small=True)}<div class="mp"><div class="mp-ic amber">{ic("alert")}</div>'
        '<div class="mp-title">Can\'t load this card right now.</div><p class="mp-text">Please try again in a few minutes.</p>'
        '<span class="mp-btn">Try again</span></div></div>'
    )


def turnstile(state="ask"):
    if state == "ask":
        box = '<span class="ts-box"></span><span>Verify you are human</span>'
    else:
        box = f'<span class="ts-ok">{ic("check")}</span><span>Success!</span>'
    return (
        f'<div class="ts">{box}<span class="ts-brand"><b>Cloudflare</b><small>Turnstile</small></span></div>'
    )


def captcha_page():
    return (
        f'<div class="pc">{band(small=True)}<div class="mp"><div class="mp-ic plum">{ic("shield")}</div>'
        '<div class="mp-title">Quick check</div><p class="mp-text">Please confirm you\'re not a robot to open this card.</p>'
        f'{turnstile()}</div></div>'
    )


# ---------------------------------------------------------------- sharing

def wa_chat(kind="card"):
    if kind == "card":
        img = (
            f'<div class="wa-img"><div class="wi-band">{mark(16, "#fff", "#96487F")}<span>Minmed</span></div>'
            f'<div class="wi-body"><div class="wi-av">{P["initials"]}</div><div><div class="wi-n">{E(P["name"])}</div>'
            f'<div class="wi-d">{E(P["desig"])}</div></div></div></div>'
        )
        title = f'{E(P["name"])} · Minmed'
        desc = E(P["desig"])
    else:
        img = f'<div class="wa-img gen">{mark(46)}<span>Minmed digital name card</span></div>'
        title = "Minmed digital name card"
        desc = "Open the link to see the card."
    return (
        '<div class="wa"><div class="wa-head"><span class="wa-av">CL</span><span>Client</span></div>'
        '<div class="wa-msgs"><div class="wa-b">'
        f'<div class="wa-card">{img}<div class="wa-tx"><div class="wa-t">{title}</div><div class="wa-d">{desc}</div>'
        '<div class="wa-dom">me.minmed.sg</div></div></div>'
        f'<div class="wa-link">https://{E(LINK_ALIAS)}</div><div class="wa-time">10:42 ✓✓</div></div></div></div>'
    )


def gwallet_pass():
    return (
        '<div class="gpass"><div class="gp-top">'
        f'{mark(26, "#fff", "#96487F")}<span>Minmed</span></div>'
        f'<div class="gp-sub">{E(P["desig"])}</div><div class="gp-h">{E(P["name"])}</div>'
        f'<div class="gp-row"><div><small>Work email</small>{E(P["email"])}</div></div>'
        f'<div class="gp-qr">{qr(11)}<small>me.minmed.sg</small></div></div>'
    )


def apple_pass():
    return (
        '<div class="apass"><div class="ap-top"><span class="ap-name">Minmed name card</span></div>'
        f'<div class="ap-f"><small>NAME</small>{E(P["name"])}</div>'
        f'<div class="ap-qr">{qr(11)}</div></div>'
    )


# ---------------------------------------------------------------- emails

def mail(subject, frm, to, body, extra=""):
    return (
        f'<div class="mail"><div class="mail-h"><div class="mail-s">{subject}</div>'
        f'<div class="mail-m"><span><b>From</b> {frm}</span><span><b>To</b> {to}</span>{extra}</div></div>'
        f'<div class="mail-b">{body}</div></div>'
    )


def email_card():
    body = (
        f'<div class="ml-logo">{mark(26)}<span>Minmed</span></div>'
        f'<p>Hi {P["first"]},</p><p>Your digital name card is ready.</p>'
        f'<div class="ml-cta"><span class="btn-p sm">Open my card</span></div>'
        f'<p class="ml-url">{E(LINK)}</p>'
        f'<div class="ml-qr">{qr(11)}</div>'
        '<div class="ml-wallets"><span class="gw-btn"><span class="gw-ic"></span>Add to Google Wallet</span></div>'
        '<div class="ml-steps"><b>iPhone (iOS 27)</b><ol><li>Take a screenshot of the QR code.</li>'
        '<li>In Wallet, tap + then Create a Pass.</li><li>Choose the screenshot.</li></ol>'
        '<p>No Apple Intelligence? Choose Create Pass Manually and scan the QR code from a computer screen.</p></div>'
        '<p class="ml-foot">Want your name in your link? Sign in at me.minmed.sg/my-card.</p>'
        '<p class="ml-foot">Need another change? Reply to this email.</p>'
    )
    return mail(
        "Your Minmed digital name card",
        "Minmed Name Cards",
        E(P["email"]),
        body,
        '<span><b>Reply-to</b> manage@minmed.sg</span>',
    )


def email_admin(kind="edit"):
    if kind == "alias":
        body = (
            '<table class="ml-tab"><tr><th>Card</th><td>Alex Tan</td></tr>'
            f'<tr><th>Change</th><td>Link: <s>{E(LINK)}</s> → {E(LINK_ALIAS)}</td></tr>'
            '<tr><th>By</th><td>Alex Tan (staff)</td></tr><tr><th>When</th><td>16 Oct 2026, 11:05 am</td></tr></table>'
            '<div class="ml-cta left"><span class="ad-btn">Open in admin console</span></div>'
        )
        return mail("Alias changed: Alex Tan", "Minmed Name Cards", "manage@minmed.sg", body)
    body = (
        '<table class="ml-tab"><tr><th>Card</th><td>Alex Tan</td></tr>'
        f'<tr><th>Change</th><td>Designation: <s>{E(P["desig"])}</s> → {E(P["desig_new"])}</td></tr>'
        '<tr><th>By</th><td>Siti Rahman (Admin)</td></tr><tr><th>When</th><td>16 Oct 2026, 10:42 am</td></tr></table>'
        '<div class="ml-cta left"><span class="ad-btn">Open in admin console</span></div>'
    )
    return mail("Card edited: Alex Tan", "Minmed Name Cards", "manage@minmed.sg", body)


# ---------------------------------------------------------------- admin console

ADMIN = {"name": "Priya Nair", "initials": "PN", "role": "Super admin"}


def ad_top(active="Cards", role="Super admin", name="Priya Nair", initials="PN", menu=False):
    items = ["Cards", "Activity log"] + (["Admins", "Settings"] if role == "Super admin" else [])
    nav = "".join(f'<span class="{"on" if i == active else ""}">{i}</span>' for i in items)
    dd = f'<span class="ad-dd"><span>{ic("out", "ic sm")}Sign out</span></span>' if menu else ""
    return (
        f'<div class="ad-top"><div class="ad-brand">{mark(24)}<span>Minmed</span><small>Name cards admin</small></div>'
        f'<div class="ad-nav">{nav}</div><div class="ad-user"><span class="ad-av">{initials}</span>'
        f'<span class="ad-un">{name}<small>{role}</small></span>{ic("chev", "ic sm")}{dd}</div></div>'
    )


def ad_page(active, inner, role="Super admin", name="Priya Nair", initials="PN"):
    return f'<div class="ad">{ad_top(active, role, name, initials)}<div class="ad-main">{inner}</div></div>'


CARDS = [
    ("AT", "Alex Tan", "alex.tan@minmed.sg", "Corporate Sales Manager", True, 48, "15 Oct 2026"),
    ("PN", "Priya Nair", "priya.nair@minmed.sg", "HR Manager", True, 12, "14 Oct 2026"),
    ("NA", "Nur Aisyah", "nur.aisyah@minmed.sg", "Clinic Operations Executive", True, 19, "16 Oct 2026"),
    ("SR", "Siti Rahman", "siti.rahman@minmed.sg", "HR Executive", True, 7, "12 Oct 2026"),
    ("MG", "Marcus Goh", "marcus.goh@minmed.sg", "Corporate Health Consultant", True, 31, "15 Oct 2026"),
]


def status_pill(active):
    return '<span class="pill on">Active</span>' if active else '<span class="pill offp">Inactive</span>'


def ad_cards():
    rows = "".join(
        f'<tr><td><div class="who"><span class="ad-av">{i}</span><span>{n}<small>{e}</small></span></div></td>'
        f"<td>{d}</td><td>{status_pill(a)}</td><td class=\"num\">{v}</td><td>{u}</td></tr>"
        for i, n, e, d, a, v, u in CARDS
    )
    return ad_page(
        "Cards",
        '<div class="ad-h"><div class="ad-title">Cards<small>128 cards</small></div><div class="sp"></div>'
        f'<span class="ad-btn">{ic("upload", "ic sm")}Import</span><span class="ad-btn p">{ic("plus", "ic sm")}Add card</span></div>'
        f'<div class="ad-tools"><span class="ad-input ph grow">{ic("search", "ic sm")}Search name or email</span>'
        '<span class="ad-seg"><span class="on">Active</span><span>Deactivated</span></span></div>'
        '<div class="ad-panel"><table class="ad-table"><thead><tr><th>Name</th><th>Designation</th><th>Status</th>'
        f'<th class="num">Views, 30 days</th><th>Last updated</th></tr></thead><tbody>{rows}</tbody></table>'
        '<div class="ad-pg"><span>1–5 of 128</span><span class="ad-btn sm">Next</span></div></div>',
    )


def ad_mobile_cards():
    rows = "".join(
        f'<div class="amc-row"><span class="ad-av">{i}</span><span class="amc-t">{n}<small>{d}</small></span>{status_pill(a)}</div>'
        for i, n, e, d, a, v, u in CARDS[:4]
    )
    return (
        f'<div class="ad amc"><div class="amc-top">{mark(22)}<span>Cards</span><span class="amc-menu">{ic("list", "ic")}</span></div>'
        f'<div class="amc-tools"><span class="ad-input ph">{ic("search", "ic sm")}Search name or email</span>'
        '<span class="ad-seg"><span class="on">Active</span><span>Deactivated</span></span>'
        f'<span class="ad-btn p full">{ic("plus", "ic sm")}Add card</span></div>{rows}</div>'
    )


def field(label, value, ph=False, cls="", note="", changed=False):
    c = " ph" if ph else ""
    ch = " changed" if changed else ""
    n = f'<small class="fnote">{note}</small>' if note else ""
    return f'<div class="ad-field {cls}"><label>{label}</label><span class="ad-input{c}{ch}">{value}</span>{n}</div>'


def card_form(edit=False):
    if edit:
        vals = dict(first="Alex", last="Tan", desig=P["desig_new"], email="alex.tan", mob="8000 1234", bio=P["bio"],
                    langs=P["langs"], li="https://" + P["linkedin"])
    else:
        vals = dict(first="", last="", desig="", email="", mob="", bio="", langs="", li="")

    def v(key, placeholder):
        return (vals[key], False) if vals[key] else (placeholder, True)

    first, f_ph = v("first", "Alex")
    last, l_ph = v("last", "Tan")
    desig, d_ph = v("desig", "Corporate Sales Manager")
    email, e_ph = v("email", "alex.tan")
    mob, m_ph = v("mob", "8000 1234")
    bio, b_ph = v("bio", "Optional")
    langs, g_ph = v("langs", "Optional")
    li, i_ph = v("li", "Optional")
    toggle = '<span class="toggle"></span>' if edit else '<span class="toggle offt"></span>'
    photo = (
        f'<div class="ad-photo"><span class="ad-av lg">AT</span><span class="ad-btn sm">Replace</span><span class="ad-btn sm">Remove</span></div>'
        if edit
        else f'<div class="ad-drop">{ic("image", "ic")}<span>Upload photo (optional)</span></div>'
    )
    return (
        '<div class="ad-form">'
        f'<div class="ad-grid2">{field("First name", first, f_ph)}{field("Last name", last, l_ph)}</div>'
        f'{field("Designation", desig, d_ph, changed=edit)}'
        f'<div class="ad-field"><label>Work email</label><span class="ad-input{" ph" if e_ph else ""}">{email}<span class="suffix">@minmed.sg</span></span></div>'
        f'<div class="ad-field"><label>Mobile</label><div class="ad-mob"><span class="ad-input{" ph" if m_ph else ""}"><span class="pre">+65</span>{mob}</span>'
        f'<span class="ad-sw">{toggle}Show on card</span></div></div>'
        f'<div class="ad-field"><label>Photo</label>{photo}</div>'
        f"{logo_locked()}"
        f'<div class="ad-field"><label>Biography</label><span class="ad-input area{" ph" if b_ph else ""}">{bio}</span></div>'
        f'<div class="ad-grid2">{field("Languages", langs, g_ph)}{field("LinkedIn", li, i_ph)}</div>'
        "</div>"
    )


PV_BAND = f'<div class="pv-band"><span class="pv-logo">{mark(14, "#fff", "#96487F")}Minmed</span></div>'


def logo_locked():
    """The company logo as a card form shows it: locked, set only in Settings."""
    return (
        '<div class="ad-field"><label>Company logo</label>'
        f'<div class="ro-logo">{mark(26)}<span>Same on every card. Only a Super admin can change it, in Settings.</span>'
        f'{ic("lock", "ic sm")}</div></div>'
    )


def mini_card(desig=None, empty=False):
    if empty:
        return (
            f'<div class="pv">{PV_BAND}<div class="pv-av">?</div><div class="pv-n ph">Name</div>'
            '<div class="pv-d ph">Designation</div><div class="pv-btn">Save contact</div></div>'
        )
    return (
        f'<div class="pv">{PV_BAND}<div class="pv-av">{P["initials"]}</div><div class="pv-n">{E(P["name"])}</div>'
        f'<div class="pv-d">{E(desig or P["desig"])}</div><div class="pv-c">Minmed</div><div class="pv-btn">Save contact</div></div>'
    )


def ad_add():
    return ad_page(
        "Cards",
        '<div class="ad-crumb">Cards › <b>Add card</b></div>'
        '<div class="ad-h"><div class="ad-title">Add card</div></div>'
        f'<div class="ad-split"><div class="ad-panel pad">{card_form()}</div>'
        f'<div class="ad-side"><div class="ad-lbl">Preview</div>{mini_card(empty=True)}</div></div>'
        '<div class="ad-foot"><span class="ad-btn">Cancel</span><div class="sp"></div><span class="ad-btn">Save</span>'
        f'<span class="ad-btn p">{ic("send", "ic sm")}Save and send card email</span></div>',
    )


def ad_edit():
    return ad_page(
        "Cards",
        '<div class="ad-crumb">Cards › Alex Tan › <b>Edit</b></div>'
        '<div class="ad-h"><div class="ad-title">Edit card</div></div>'
        f'<div class="ad-split"><div class="ad-panel pad">{card_form(edit=True)}</div>'
        f'<div class="ad-side"><div class="ad-lbl">Preview</div>{mini_card(P["desig_new"])}'
        f'<div class="ad-hint">{ic("link", "ic sm")}Same link and QR code</div></div></div>'
        '<div class="ad-foot"><span class="ad-btn">Cancel</span><div class="sp"></div><span class="ad-btn p">Save changes</span></div>',
        role="Admin", name="Siti Rahman", initials="SR",
    )


def ad_import():
    steps = [("Download template", "done"), ("Upload", "done"), ("Check", "on"), ("Create", "")]
    stepper = "".join(
        f'<span class="st {s}"><i>{ic("check", "ic sm") if s == "done" else n + 1}</i>{t}</span>'
        for n, (t, s) in enumerate(steps)
    )
    rows = [
        ("2", "Alex Tan", "alex.tan@minmed.sg", "Corporate Sales Manager", None),
        ("3", "Priya Nair", "priya.nair@minmed.sg", "HR Manager", None),
        ("7", "Grace Koh", "grace.koh@gmail.com", "Clinic Manager", "Work email must end with @minmed.sg"),
        ("8", "Marcus Goh", "marcus.goh@minmed.sg", "Corporate Health Consultant", None),
        ("12", "Siti Rahman", "siti.rahman@minmed.sg", "HR Executive", "Already has a card"),
    ]
    body = "".join(
        f'<tr class="{"bad" if err else ""}"><td class="num">{r}</td><td>{n}</td><td>{e}</td><td>{d}</td>'
        + (f'<td><span class="imp-err">{ic("alert", "ic sm")}{err}</span></td>' if err else f'<td><span class="imp-ok">{ic("check", "ic sm")}Ready</span></td>')
        + "</tr>"
        for r, n, e, d, err in rows
    )
    return ad_page(
        "Cards",
        '<div class="ad-crumb">Cards › <b>Import cards</b></div>'
        f'<div class="ad-h"><div class="ad-title">Import cards</div></div><div class="ad-steps">{stepper}</div>'
        '<div class="ad-panel"><div class="ad-ph"><b>staff-cards.xlsx</b><span>43 rows · <b class="g">41 ready</b> · <b class="r">2 need fixing</b></span></div>'
        '<table class="ad-table"><thead><tr><th class="num">Row</th><th>Name</th><th>Work email</th><th>Designation</th><th>Check</th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
        '<div class="ad-foot"><span class="ad-btn">Upload again</span><div class="sp"></div>'
        '<span class="ad-ck"><span class="cb on">✓</span>Send card emails now</span><span class="ad-btn p">Create 41 cards</span></div>',
    )


def ad_details():
    hist = [
        ("16 Oct 2026, 11:05", f"Alias set to {P['alias']} by Alex Tan"),
        ("15 Oct 2026, 16:05", "Photo added by Siti Rahman"),
        ("12 Oct 2026, 09:16", "Card email sent by Priya Nair"),
        ("12 Oct 2026, 09:15", "Card created by Priya Nair (import)"),
    ]
    hist_html = "".join(f'<li><span>{t}</span>{d}</li>' for t, d in hist)
    bars = "".join(f'<i style="height:{h}%"></i>' for h in (20, 35, 15, 50, 40, 70, 30, 55, 90, 45, 60, 35, 80, 65))
    return ad_page(
        "Cards",
        '<div class="ad-crumb">Cards › <b>Alex Tan</b></div>'
        f'<div class="ad-h"><span class="ad-av lg">AT</span><div class="ad-title">Alex Tan<small>{E(P["desig"])} · alex.tan@minmed.sg</small></div>'
        f'{status_pill(True)}<div class="sp"></div><span class="ad-btn">{ic("edit", "ic sm")}Edit</span>'
        f'<span class="ad-btn">{ic("send", "ic sm")}Send card email</span><span class="ad-btn d">Deactivate</span>'
        f'<span class="ad-more"><span class="ad-btn">{ic("more", "ic sm")}</span><span class="ad-menu"><span>New link code</span><span class="r">Delete card</span><small>Super admin only</small></span></span></div>'
        '<div class="ad-det">'
        f'<div class="ad-side"><div class="ad-lbl">Live card</div>{mini_card()}</div>'
        '<div class="ad-cards">'
        f'<div class="ad-panel pad"><div class="ad-lbl">Link</div><div class="ad-link"><code>{E(LINK_ALIAS)}</code><span class="ad-btn sm">{ic("copy", "ic sm")}Copy</span></div>'
        f'<div class="ad-alias"><span>Alias <b>{E(P["alias"])}</b>, set by Alex Tan</span><span class="ad-btn sm">Clear alias</span></div></div>'
        f'<div class="ad-panel pad row"><div class="ad-qr">{qr(11)}</div><div><div class="ad-lbl">QR code and card image</div>'
        f'<span class="ad-btn sm">{ic("download", "ic sm")}QR code</span> <span class="ad-btn sm">{ic("download", "ic sm")}Card image</span></div></div>'
        f'<div class="ad-panel pad"><div class="ad-lbl">Google Wallet pass</div><div class="ad-gw"><span class="pill on">Active</span>Updates when the card changes</div></div>'
        f'<div class="ad-panel pad"><div class="ad-lbl">Views, last 30 days</div><div class="ad-views"><b>48</b><span class="spark">{bars}</span></div></div>'
        f'<div class="ad-panel pad span2"><div class="ad-lbl">History</div><ul class="ad-hist">{hist_html}</ul></div>'
        "</div></div>",
    )


def dialog(title, text, confirm, danger=True, extra=""):
    btn = "ad-btn dp" if danger else "ad-btn p"
    return (
        f'<div class="modal-wrap"><div class="modal"><div class="md-t">{title}</div><p>{text}</p>{extra}'
        f'<div class="md-a"><span class="ad-btn">Cancel</span><span class="{btn}">{confirm}</span></div></div></div>'
    )


def ad_dialogs():
    return (
        '<div class="dialogs">'
        + dialog("Deactivate Alex Tan's card?", "The link will show “This card is no longer active.” Save contact stops working and Alex can't sign in. The card is soft-deleted: it leaves the Cards list, and a Super admin can restore it.", "Deactivate")
        + dialog("Clear Alex Tan's alias?", f"The link goes back to {E(LINK)}. The link with the alias stops working, and Alex gets a new card email.", "Clear alias")
        + dialog(
            "Give Alex Tan's card a new link?",
            "The old link and QR code will stop working.",
            "New link code",
            extra='<div class="ad-ck"><span class="cb on">✓</span>Send Alex the new card email</div>',
        )
        + dialog("Delete Alex Tan's card permanently?", "This can't be undone. The link will show “No card found”.", "Delete permanently")
        + "</div>"
    )


def ad_activity():
    rows = [
        ("16 Oct 2026, 11:05", "Alex Tan (staff)", "Alias changed", "Alex Tan", f"{P['alias']} · new card email sent"),
        ("16 Oct 2026, 10:42", "Siti Rahman", "Edited", "Alex Tan", "Designation"),
        ("16 Oct 2026, 09:05", "Siti Rahman", "Deactivated", "Daniel Lim", "Last day 15 Oct"),
        ("15 Oct 2026, 17:20", "Priya Nair", "New link code", "Marcus Goh", "Old link stopped"),
        ("12 Oct 2026, 09:16", "Priya Nair", "Card emails sent", "41 cards", ""),
        ("12 Oct 2026, 09:15", "Priya Nair", "Imported", "41 cards", "staff-cards.xlsx"),
        ("10 Oct 2026, 14:02", "Priya Nair", "Admin added", "Siti Rahman", "Role: Admin"),
    ]
    body = "".join(
        f"<tr><td>{w}</td><td>{a}</td><td><b>{act}</b></td><td>{c}</td><td class=\"mut\">{d}</td></tr>" for w, a, act, c, d in rows
    )
    return ad_page(
        "Activity log",
        '<div class="ad-h"><div class="ad-title">Activity log</div></div>'
        '<div class="ad-tools"><span class="ad-input">Card: All' + ic("chev", "ic sm") + '</span>'
        '<span class="ad-input">By: All' + ic("chev", "ic sm") + '</span><span class="ad-input">Action: All' + ic("chev", "ic sm") + "</span></div>"
        '<div class="ad-panel"><table class="ad-table"><thead><tr><th>When</th><th>By</th><th>Action</th><th>Card</th><th>Details</th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>",
    )


def ad_admins():
    rows = [
        ("PN", "Priya Nair", "priya.nair@minmed.sg", "Super admin", "1 Oct 2026"),
        ("IT", "IT Support", "it.support@minmed.sg", "Super admin", "1 Oct 2026"),
        ("SR", "Siti Rahman", "siti.rahman@minmed.sg", "Admin", "10 Oct 2026"),
        ("JO", "Jason Ong", "jason.ong@minmed.sg", "Admin", "10 Oct 2026"),
    ]
    body = "".join(
        f'<tr><td><div class="who"><span class="ad-av">{i}</span><span>{n}<small>{e}</small></span></div></td>'
        f'<td><span class="ad-input sel">{r}{ic("chev", "ic sm")}</span></td><td>{d}</td><td class="r"><span class="lnk-r">Remove</span></td></tr>'
        for i, n, e, r, d in rows
    )
    return ad_page(
        "Admins",
        f'<div class="ad-h"><div class="ad-title">Admins</div><div class="sp"></div><span class="ad-btn p">{ic("plus", "ic sm")}Add admin</span></div>'
        '<div class="ad-panel"><table class="ad-table"><thead><tr><th>Admin</th><th>Role</th><th>Added</th><th></th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
        '<div class="ad-panel pad addrow"><span class="ad-input ph grow">name@minmed.sg</span>'
        f'<span class="ad-input sel">Admin{ic("chev", "ic sm")}</span><span class="ad-btn p">Add</span></div>',
    )


def ad_settings():
    return ad_page(
        "Settings",
        '<div class="ad-h"><div class="ad-title">Settings</div></div>'
        '<div class="ad-set"><div class="ad-snav"><span class="on">Card design</span><span>Company details</span>'
        '<span>Notifications</span><span>Google Wallet</span></div>'
        '<div class="ad-sbody">'
        f'<div class="ad-panel pad"><div class="ad-lbl">Card design</div><div class="ad-design"><div>'
        f'<div class="ad-field"><label>Logo</label><div class="ad-photo">{mark(36)}<span class="ad-btn sm">Replace</span></div>'
        '<small class="fnote">Shown on every card. Only Super admins can change it.</small></div>'
        '<div class="ad-field"><label>Brand colour</label><div class="sw"><i style="background:#96487f"></i><i style="background:#ad5e99"></i>'
        '<i style="background:#192637"></i><i style="background:#efdfeb"></i></div></div></div>'
        f"<div>{mini_card()}</div></div></div>"
        '<div class="ad-panel pad"><div class="ad-lbl">Company details</div>'
        f'{field("Website link (About Minmed)", "https://minmed.sg")}</div>'
        '<div class="ad-panel pad"><div class="ad-lbl">Notifications</div>'
        f'{field("Send admin notifications to", "manage@minmed.sg")}</div>'
        '<div class="ad-panel pad"><div class="ad-lbl">Google Wallet</div><div class="ad-gw"><span class="pill on">Publishing approved</span>'
        "Pass design follows the card design</div></div>"
        "</div></div>",
    )


def staff_signin(state="ask"):
    if state == "ask":
        inner = (
            '<div class="si-msg">Please sign in with your Minmed registered email address.</div>'
            '<span class="g-btn"><span class="g-ic">G</span>Sign in with Google</span>'
        )
    else:
        inner = (
            f'<div class="si-err">{ic("lock", "ic sm")}There\'s no name card for this account.</div>'
            '<span class="g-btn"><span class="g-ic">G</span>Use another account</span>'
        )
    return f'<div class="ad si mob"><div class="si-box">{mark(40)}<div class="si-t">My name card</div>{inner}</div></div>'


MC_HELP = "Your name or an alias: letters, numbers and hyphens, 2 to 30 characters. Leave it empty for a link without a name."
MC_WARN = (
    "Saving gives you a new link. Your old link, printed QR codes and Apple Wallet passes will show “No card found”. "
    "Your Google Wallet pass updates itself, and we'll email you the new card."
)
MC_NOTE = '<div class="mc-note">Only admins can change these. Reply to your card email to ask for a change.</div>'


def link_box(state):
    """The staff member's link with the one box they can type in: empty, typing, saved or error."""
    box = {
        "empty": '<span class="mc-in ph">your-name</span>',
        "typing": f'<span class="mc-in">{E(P["alias"])}<i></i></span>',
        "saved": f'<span class="mc-in done">{E(P["alias"])}</span>',
        "error": '<span class="mc-in bad">Alex Tan!<i></i></span>',
    }[state]
    return f'<div class="mc-link"><span>me.minmed.sg/card/</span>{box}<span>/{P["code"]}</span></div>'


def link_section(state):
    if state == "saved":
        after = (
            f'<div class="mc-ok">{ic("check", "ic sm")}<span>Your new link is ready. We\'ve emailed you the new card.</span></div>'
            f'<span class="ad-btn sm">{ic("copy", "ic sm")}Copy link</span>'
        )
    elif state == "error":
        after = (
            f'<div class="mc-err">{ic("alert", "ic sm")}<span>Use only letters, numbers and hyphens, 2 to 30 characters.</span></div>'
            '<div class="btn-p off">Save link</div>'
        )
    else:
        after = (
            f'<div class="mc-help">{MC_HELP}</div>'
            f'<div class="mc-warn">{ic("alert", "ic sm")}<span>{MC_WARN}</span></div><div class="btn-p">Save link</div>'
        )
    return f'<div class="mc-sec"><div class="mc-h">Your link</div>{link_box(state)}{after}</div>'


def ro_details(phone=False):
    """Every card field, read-only, as the staff member sees it."""
    langs = field("Languages", E(P["langs"]), cls="ro")
    li = field("LinkedIn", E(P["linkedin"]), cls="ro")
    return (
        '<div class="ad-form">'
        f'<div class="ad-grid2">{field("First name", "Alex", cls="ro")}{field("Last name", "Tan", cls="ro")}</div>'
        f'{field("Designation", E(P["desig"]), cls="ro")}{field("Work email", E(P["email"]), cls="ro")}'
        f'{field("Mobile", E(P["mobile"]) + "<span class=suffix>Shown on card</span>", cls="ro")}'
        f'<div class="ad-field ro"><label>Photo</label><span class="ad-av lg">{P["initials"]}</span></div>'
        f'<div class="ad-field ro"><label>Biography</label><span class="ad-input area auto">{E(P["bio"])}</span></div>'
        + (f"{langs}{li}" if phone else f'<div class="ad-grid2">{langs}{li}</div>')
        + f"{logo_locked()}</div>"
    )


def mc_top():
    return (
        f'<div class="mc-top">{mark(22, "#fff", "#96487F")}<span>My name card</span>'
        f'<span class="mc-out">{ic("out", "ic sm")}Sign out</span></div>'
    )


def mc_qr(title="Your QR code", seed=11):
    return (
        f'<div class="mc-sec mc-qrrow"><div class="mc-qr">{qr(seed)}</div><div><div class="mc-h">{title}</div>'
        f'<span class="ad-btn sm">{ic("download", "ic sm")}Download QR code</span></div></div>'
    )


def my_card():
    """My card on a phone, before the staff member has added a name."""
    return (
        f'<div class="mc">{mc_top()}{link_section("empty")}{mc_qr()}'
        f'<div class="mc-sec"><div class="mc-h">Your card details{ic("lock", "ic sm")}</div>{ro_details(phone=True)}{MC_NOTE}</div></div>'
    )


def my_card_step(state):
    """One step of changing the link on a phone: typing, saved or error."""
    extra = mc_qr("Your new QR code", 12) if state == "saved" else ""
    return f'<div class="mc">{mc_top()}{link_section(state)}{extra}</div>'


def my_card_desktop():
    """My card on a computer: the staff member's card details page."""
    top = (
        f'<div class="ad-top"><div class="ad-brand">{mark(24)}<span>Minmed</span><small>My name card</small></div>'
        f'<div class="ad-user"><span class="ad-av">{P["initials"]}</span><span class="ad-un">{E(P["name"])}<small>Staff</small></span>'
        f'<span class="ad-btn sm">{ic("out", "ic sm")}Sign out</span></div></div>'
    )
    link = (
        f'<div class="ad-panel pad"><div class="ad-lbl">Your link</div>{link_box("saved")}'
        f'<div class="mc-help">{MC_HELP}</div><div class="mc-warn">{ic("alert", "ic sm")}<span>{MC_WARN}</span></div>'
        f'<div class="ad-foot"><span class="ad-btn sm">{ic("copy", "ic sm")}Copy link</span><div class="sp"></div>'
        '<span class="ad-btn p off">Save link</span></div></div>'
    )
    qrp = (
        f'<div class="ad-panel pad row"><div class="ad-qr">{qr(12)}</div><div><div class="ad-lbl">Your QR code</div>'
        f'<span class="ad-btn sm">{ic("download", "ic sm")}Download QR code</span></div></div>'
    )
    det = (
        f'<div class="ad-panel pad"><div class="ad-lbl withic">Your card details{ic("lock", "ic sm")}</div>{ro_details()}{MC_NOTE}</div>'
    )
    return (
        f'<div class="ad">{top}<div class="ad-main">'
        f'<div class="ad-h"><span class="ad-av lg">{P["initials"]}</span><div class="ad-title">{E(P["name"])}'
        f'<small>{E(P["desig"])} · {E(P["email"])}</small></div>{status_pill(True)}</div>'
        f'<div class="ad-det"><div class="ad-side"><div class="ad-lbl">Your card</div>{mini_card()}</div>'
        f'<div class="ad-stack">{link}{qrp}{det}</div></div></div></div>'
    )


def my_card_confirm():
    return (
        '<div class="mc dim"><div class="modal"><div class="md-t">Change your link?</div>'
        f'<p>Your new link: <b class="mc-new">{E(LINK_ALIAS)}</b></p>'
        '<p>Your old link and QR code will stop working, including any Apple Wallet pass made from them. '
        'Your Google Wallet pass updates itself, and we\'ll email you the new card.</p>'
        '<div class="md-a"><span class="ad-btn">Cancel</span><span class="ad-btn p">Change link</span></div></div></div>'
    )


def ad_signin(state="ask"):
    if state == "ask":
        inner = (
            '<div class="si-msg">Please sign in with your Minmed registered email address.</div>'
            '<span class="g-btn"><span class="g-ic">G</span>Sign in with Google</span>'
        )
    else:
        inner = (
            f'<div class="si-err">{ic("lock", "ic sm")}You don\'t have access.</div>'
            '<span class="g-btn"><span class="g-ic">G</span>Use another account</span>'
        )
    return (
        f'<div class="ad si"><div class="si-box">{mark(40)}<div class="si-t">Name cards admin</div>{inner}</div></div>'
    )
