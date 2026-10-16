"""Builds the figures for the technical specification as PNG files.

Diagrams are drawn as SVG in Carlito (metrically identical to Calibri, the document font).
Wireframes reuse the approved high-fidelity mockups from ../../name-card-scope/src.

Run: python3 figures.py   (then node shoot.js renders build/*.html to ../figures/*.png)
"""

import html
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
SCOPE_SRC = SRC.parent.parent / "name-card-scope" / "src"
BUILD = SRC / "build"
sys.path.insert(0, str(SCOPE_SRC))

import mocks as M  # noqa: E402

E = html.escape
W = 700  # design width of every diagram, in CSS pixels

STYLES = {
    "plain": ("#ffffff", "#9aa5b1"),
    "main": ("#e7eff4", "#8fa9bc"),
    "ok": ("#e8f3ec", "#8dbf9e"),
    "warn": ("#fff4e0", "#d9a94e"),
    "end": ("#f1f2f4", "#b8bdc4"),
    "err": ("#fbeaea", "#d99a9a"),
    "note": ("#ffffff", "#b8bdc4"),
}


def box(x, y, w, h, title, lines=(), kind="plain"):
    fill, stroke = STYLES[kind]
    dash = ' stroke-dasharray="5 4"' if kind == "note" else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>']
    rows = ([("t", title)] if title else []) + [("l", s) for s in lines]
    height = sum(18 if k == "t" else 16.5 for k, _ in rows)
    cy = y + (h - height) / 2 + 13
    for k, s in rows:
        cls = "t" if k == "t" else "l"
        out.append(f'<text class="{cls}" x="{x + w / 2}" y="{cy:.1f}" text-anchor="middle">{E(s)}</text>')
        cy += 18 if k == "t" else 16.5
    return "".join(out)


def note(x, y, w, lines, anchor="start"):
    tx = x if anchor == "start" else x + w / 2 if anchor == "middle" else x + w
    return "".join(
        f'<text class="n" x="{tx}" y="{y + i * 16:.1f}" text-anchor="{anchor}">{E(s)}</text>' for i, s in enumerate(lines)
    )


def arrow(points, label=None, at=None, anchor="start", lines=None):
    d = "M " + " L ".join(f"{px} {py}" for px, py in points)
    out = f'<path d="{d}" fill="none" stroke="#5b6470" stroke-width="1.6" marker-end="url(#ah)"/>'
    labels = lines or ([label] if label else [])
    if labels and at:
        lx, ly = at
        out += "".join(
            f'<text class="a" x="{lx}" y="{ly + i * 15}" text-anchor="{anchor}">{E(s)}</text>' for i, s in enumerate(labels)
        )
    return out


def zone(x, y, w, h, label, lx=14):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="#9aa5b1" stroke-width="1.3" stroke-dasharray="6 5"/>'
        f'<text class="z" x="{x + lx}" y="{y + 20}">{E(label)}</text>'
    )


def svg(height, body):
    return (
        f'<svg id="fig" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}">'
        '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="#5b6470"/></marker></defs>'
        '<rect width="100%" height="100%" fill="#ffffff"/>'
        f"{body}</svg>"
    )


DIAGRAM_CSS = """
body { margin: 0; background: #fff; }
svg text { font-family: Carlito, Calibri, sans-serif; fill: #1f1f1f; }
svg .t { font-size: 15px; font-weight: 700; }
svg .l { font-size: 13.5px; }
svg .n { font-size: 13px; fill: #3f454d; }
svg .a { font-size: 12.5px; fill: #3f454d; paint-order: stroke; stroke: #fff; stroke-width: 4px; stroke-linejoin: round; }
svg .z { font-size: 13px; font-weight: 700; fill: #4a4f57; }
"""


def page(body, css=DIAGRAM_CSS, head_extra=""):
    return f'<!doctype html><html><head><meta charset="utf-8">{head_extra}<style>{css}</style></head><body>{body}</body></html>'


# ---------------------------------------------------------------- diagrams

def fig_system():
    b = []
    b.append(box(10, 10, 240, 58, "Visitor", ["phone or computer, no sign-in"]))
    b.append(box(450, 10, 240, 58, "Admin or Super admin", ["company Google account"]))
    b.append(zone(10, 132, 680, 300, "Base44 app on me.minmed.sg", lx=262))
    b.append(note(30, 176, 200, ["Public, no sign-in"]))
    b.append(note(470, 176, 200, ["Private, admins only"]))
    b.append(box(30, 186, 210, 58, "Card pages", ["me.minmed.sg/card/{code}"], "main"))
    b.append(box(470, 186, 200, 58, "Admin console", ["me.minmed.sg/admin"], "main"))
    b.append(box(30, 292, 290, 120, "Backend functions", ["one card's public fields, by its code", "bot checks, counting, CAPTCHA check", "contact file, card image, Wallet link"], "main"))
    b.append(box(400, 292, 270, 120, "Database", ["cards, admin list, settings", "activity log, view counts", "bot counters and passes"], "plain"))
    b.append(box(10, 476, 210, 64, "Cloudflare Turnstile", ["verifies CAPTCHA tokens"]))
    b.append(box(245, 476, 210, 64, "Google Wallet", ["issues, updates and", "expires passes"]))
    b.append(box(480, 476, 210, 64, "Email sending", ["card emails; notices to", "manage@minmed.sg"]))
    b.append(box(330, 596, 270, 58, "Staff member", ["no sign-in; shares the link or QR code"]))
    b.append(arrow([(130, 68), (130, 184)], lines=["opens a link", "or QR code"], at=(140, 92)))
    b.append(arrow([(640, 68), (640, 184)], lines=["signs in", "with Google"], at=(630, 92), anchor="end"))
    b.append(arrow([(135, 244), (135, 290)], "asks for one card", at=(145, 272)))
    b.append(arrow([(570, 244), (570, 290)], "reads and writes", at=(580, 272)))
    b.append(arrow([(320, 352), (398, 352)]))
    b.append(note(359, 342, 0, ["reads, counts"], anchor="middle"))
    b.append(arrow([(115, 412), (115, 474)], "verify token", at=(125, 458)))
    b.append(arrow([(300, 412), (300, 474)], "pass link, updates", at=(310, 458)))
    b.append(arrow([(585, 412), (585, 474)], "on admin actions", at=(595, 458)))
    b.append(arrow([(395, 540), (395, 594)], "Wallet pass", at=(405, 572)))
    b.append(arrow([(585, 540), (585, 594)], "card email", at=(595, 572)))
    return svg(664, "".join(b))


def fig_lifecycle():
    b = []
    b.append(box(10, 10, 205, 74, "", ["New link code (Super admin),", "in either state: the old link", "shows “No card found”."], "note"))
    b.append(box(235, 10, 230, 58, "Admin adds the card", ["one at a time or by import"]))
    b.append(box(40, 170, 230, 64, "Active", ["the link shows the card"], "ok"))
    b.append(box(430, 170, 230, 64, "Inactive", ["“This card is no longer active.”"], "end"))
    b.append(box(235, 380, 230, 64, "Deleted", ["the link shows “No card found”"], "err"))
    b.append(arrow([(350, 68), (350, 112), (155, 112), (155, 168)], "creates a random link code", at=(165, 104)))
    b.append(arrow([(270, 190), (428, 190)], lines=["Admin deactivates", "on the last day"], at=(349, 160), anchor="middle"))
    b.append(arrow([(430, 218), (272, 218)], "Super admin reactivates", at=(351, 241), anchor="middle"))
    b.append(arrow([(200, 234), (300, 378)], "Super admin deletes", at=(152, 318), anchor="middle"))
    b.append(arrow([(500, 234), (400, 378)], "Super admin deletes", at=(548, 318), anchor="middle"))
    b.append(box(10, 470, 330, 58, "", ["Edits: an admin changes details and the card", "updates at once, on the same link and QR code."], "note"))
    b.append(box(360, 470, 330, 58, "", ["Inactive cards are kept and deleted on request.", "Retention period: Pending confirmation."], "note"))
    return svg(540, "".join(b))


def fig_open():
    b = []
    b.append(box(165, 10, 370, 50, "Visitor opens the link or scans the QR code"))
    b.append(box(165, 96, 370, 58, "Bot checks (section 7)", ["valid pass, rule 1, rule 3"], "main"))
    b.append(box(565, 96, 125, 116, "CAPTCHA", ["not passed:", "no card details;", "can try again"], "warn"))
    b.append(box(165, 236, 370, 58, "Backend function looks up the code", ["live, on every opening"], "main"))
    b.append(arrow([(350, 60), (350, 94)]))
    b.append(arrow([(535, 118), (563, 118)]))
    b.append(note(549, 92, 0, ["rule met"], anchor="middle"))
    b.append(arrow([(350, 154), (350, 234)], lines=["no rule met"], at=(360, 196)))
    b.append(arrow([(627, 212), (627, 265), (537, 265)], "passed", at=(637, 244)))
    xs = [10, 185, 360, 535]
    b.append('<path d="M 350 294 L 350 322 M 90 322 L 615 322" fill="none" stroke="#5b6470" stroke-width="1.6"/>')
    for x in xs:
        b.append(arrow([(x + 80, 322), (x + 80, 352)]))
    b.append(box(10, 354, 160, 132, "Active", ["Card page with the", "current details.", "On a computer, it adds", "a QR code."], "ok"))
    b.append(box(185, 354, 160, 132, "Inactive", ["“This card is no", "longer active.”", "No details or", "contact actions."], "end"))
    b.append(box(360, 354, 160, 132, "No card with this code", ["“No card found at", "this address. Check the", "link or visit minmed.sg.”", "Counts towards rule 1."], "end"))
    b.append(box(535, 354, 160, 132, "Can't be checked", ["“Can't load this card", "right now. Please try", "again in a few minutes.”", "Never shows old details."], "err"))
    return svg(496, "".join(b))


def fig_bots():
    b = []
    b.append(box(10, 10, 420, 58, "A card is opened, a contact file is requested,", ["or a card address is tried"]))
    b.append(box(10, 110, 420, 56, "Rules 2 and 4", ["Does the browser hold a valid pass?"], "main"))
    b.append(box(10, 210, 420, 56, "Rule 1", ["More than 3 from this IP address in the last minute?"], "main"))
    b.append(box(10, 310, 420, 56, "Rule 3", ["More than 20 for this card in the last 10 minutes?"], "main"))
    b.append(box(10, 410, 420, 56, "Send the page", ["the card, or “No card found”"], "ok"))
    b.append(box(470, 110, 220, 56, "Send the page", ["the card"], "ok"))
    b.append(box(470, 210, 220, 156, "CAPTCHA", ["Cloudflare Turnstile,", "Managed mode: most people", "pass without clicking"], "warn"))
    b.append(box(470, 410, 105, 96, "Passed", ["card sent;", "30-minute", "pass"], "ok"))
    b.append(box(585, 410, 105, 96, "Not passed", ["or can't load:", "no card details;", "try again"], "end"))
    b.append(arrow([(220, 68), (220, 108)]))
    for y in (166, 266, 366):
        b.append(arrow([(220, y), (220, y + 42)], "No", at=(230, y + 26)))
    for y in (138, 238, 338):
        b.append(arrow([(430, y), (468, y)]))
        b.append(note(449, y - 8, 0, ["Yes"], anchor="middle"))
    b.append('<path d="M 580 366 L 580 386 M 522 386 L 637 386" fill="none" stroke="#5b6470" stroke-width="1.6"/>')
    b.append(arrow([(522, 386), (522, 408)]))
    b.append(arrow([(637, 386), (637, 408)]))
    b.append(note(10, 498, 440, ["Never checked: link-preview fetches, the admin console,", "and images, styles and scripts.", "First 2 weeks: the rules only record."]))
    return svg(540, "".join(b))


SITEMAP_CSS = DIAGRAM_CSS + """
#fig { width: 700px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; font-family: Carlito, Calibri, sans-serif; color: #1f1f1f; padding: 2px; box-sizing: border-box; }
.col { border: 1.5px solid #9aa5b1; border-radius: 10px; padding: 10px 10px 8px; background: #fff; }
.col h3 { margin: 0; font-size: 16px; }
.col .host { font-size: 13px; color: #3f454d; margin: 1px 0 2px; }
.col .sub { font-size: 12.5px; color: #3f454d; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #d9d9d9; }
ul { list-style: none; margin: 0; padding: 0; }
ul ul { margin-left: 9px; padding-left: 10px; border-left: 1.5px solid #c9ced4; }
li { margin: 5px 0; }
.it { display: block; background: #e7eff4; border: 1px solid #8fa9bc; border-radius: 6px; padding: 4px 7px; font-size: 13.5px; line-height: 1.25; }
.it.plain { background: #fff; border-color: #b8bdc4; }
.it b { font-weight: 700; }
.it code { display: block; font-family: Carlito, Calibri, sans-serif; font-size: 12.5px; color: #3f454d; }
.it small { display: block; font-size: 12.5px; color: #3f454d; }
"""


def it(title, code="", sub="", plain=False):
    c = f"<code>{E(code)}</code>" if code else ""
    s = f"<small>{E(sub)}</small>" if sub else ""
    return f'<span class="it{" plain" if plain else ""}"><b>{E(title)}</b>{c}{s}</span>'


def fig_sitemap():
    public = f"""<div class="col"><h3>Public</h3><div class="host">me.minmed.sg</div>
<div class="sub">No sign-in, hidden from search engines, no menu</div><ul>
<li>{it("Card page", "/card/{code}")}<ul>
  <li>{it("On a computer", sub="adds a QR code", plain=True)}</li>
  <li>{it("CAPTCHA check", sub="when a rule is met", plain=True)}</li>
  <li>{it("No longer active", sub="after deactivation", plain=True)}</li>
  <li>{it("Temporary error", sub="card can't be checked", plain=True)}</li></ul></li>
<li>{it("Card not found", sub="any wrong address")}</li>
<li>{it("Files behind the same code", "/functions/…?code={code}", "contact file, card image, Google Wallet link")}</li>
<li>{it("Home", "/", "redirects to minmed.sg")}</li></ul></div>"""
    admin = f"""<div class="col"><h3>Admin console</h3><div class="host">me.minmed.sg/admin</div>
<div class="sub">Company Google sign-in, admin list only</div><ul>
<li>{it("Sign in", "/admin")}</li>
<li>{it("Cards", "/admin/cards")}<ul>
  <li>{it("Add card", "/admin/cards/new")}</li>
  <li>{it("Import cards", "/admin/cards/import")}</li>
  <li>{it("Card details", "/admin/cards/{id}")}<ul>
    <li>{it("Edit card", "/admin/cards/{id}/edit")}</li>
    <li>{it("Confirm dialogs", sub="deactivate, new link code, delete", plain=True)}</li></ul></li></ul></li>
<li>{it("Activity log", "/admin/activity")}</li>
<li>{it("Admins", "/admin/admins", "Super admin only")}</li>
<li>{it("Settings", "/admin/settings", "Super admin only")}</li></ul></div>"""
    msgs = f"""<div class="col"><h3>Emails, Wallet and sharing</h3><div class="host">outside the website</div>
<div class="sub">How cards reach staff, admins and visitors</div><ul>
<li>{it("Card email", sub="to the staff member")}</li>
<li>{it("Google Wallet pass", sub="issued by Minmed")}</li>
<li>{it("Apple Wallet pass", sub="made by the staff member")}</li>
<li>{it("WhatsApp link preview", sub="when a link is shared")}</li>
<li>{it("Admin notification", sub="to manage@minmed.sg")}</li></ul></div>"""
    return page(f'<div id="fig">{public}{admin}{msgs}</div>', SITEMAP_CSS)


# ---------------------------------------------------------------- wireframes

MOCK_HEAD = (
    '<link href="https://fonts.googleapis.com/css2?family=Lato:wght@700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">'
)
MOCK_CSS = (SCOPE_SRC / "scope.css").read_text() + """
body { margin: 0; background: #fff; }
#fig { display: inline-block; padding: 14px; background: #fff; }
.row { display: flex; gap: 22px; align-items: flex-start; }
.row.grow > div { flex: 1; min-width: 0; }
.col { display: flex; flex-direction: column; gap: 18px; }
.lbl { font: 900 13px/1 Lato, sans-serif; letter-spacing: .05em; text-transform: uppercase; color: #5f6673; margin: 0 0 8px; }
.shot { overflow: visible; padding: 0; }
.browser { box-shadow: none; }
.phone { box-shadow: none; }
"""


def mock(inner, width=None):
    style = f' style="width:{width}px"' if width else ""
    return page(f'<div id="fig"{style}>{inner}</div>', MOCK_CSS, MOCK_HEAD)


def labelled(label, inner):
    return f'<div><div class="lbl">{E(label)}</div>{inner}</div>'


def admin(path, body):
    return M.browser("me.minmed.sg" + path, body)


def wireframes():
    return {
        "fig06-card-captcha": mock('<div class="row">' + labelled("Card page", M.phone(M.card_body()))
                                   + labelled("CAPTCHA check", M.phone(M.captcha_page())) + "</div>"),
        "fig07-computer": mock(M.browser(M.LINK, M.card_desktop()), 900),
        "fig08-states": mock('<div class="row">' + labelled("No longer active", M.phone(M.inactive_page()))
                             + labelled("Card not found", M.phone(M.notfound_page()))
                             + labelled("Temporary error", M.phone(M.error_page())) + "</div>"),
        "fig09-whatsapp": mock('<div class="row">' + labelled("Per-card preview (options B, C)", M.wa_chat("card"))
                               + labelled("Same for every card (option A)", M.wa_chat("generic")) + "</div>"),
        "fig10-email": mock(M.email_card(), 400),
        "fig11-passes": mock('<div class="row">' + labelled("Google Wallet, issued by Minmed", M.gwallet_pass())
                             + labelled("Apple Wallet, made by the staff member", M.apple_pass()) + "</div>"),
        "fig12-signin": mock('<div class="row grow">' + labelled("Sign-in", admin("/admin", M.ad_signin("ask")))
                             + labelled("Account not on the admin list", admin("/admin", M.ad_signin("denied"))) + "</div>", 1000),
        "fig13-cards": mock(admin("/admin/cards", M.ad_cards()), 860),
        "fig14-details": mock(admin("/admin/cards/AT29", M.ad_details()), 1000),
        "fig15-add": mock(admin("/admin/cards/new", M.ad_add()), 860),
        "fig16-import": mock(admin("/admin/cards/import", M.ad_import()), 860),
        "fig17-dialogs": mock(M.ad_dialogs(), 860),
        "fig18-activity": mock('<div class="col">' + labelled("Activity log", admin("/admin/activity", M.ad_activity()))
                               + labelled("Admin notification email", f'<div style="width:420px">{M.email_admin()}</div>') + "</div>", 860),
        "fig19-admins-settings": mock('<div class="col">' + labelled("Admins", admin("/admin/admins", M.ad_admins()))
                                      + labelled("Settings", admin("/admin/settings", M.ad_settings())) + "</div>", 860),
    }


def main():
    BUILD.mkdir(exist_ok=True)
    pages = {
        "fig01-system": page(fig_system()),
        "fig02-lifecycle": page(fig_lifecycle()),
        "fig03-open": page(fig_open()),
        "fig04-bots": page(fig_bots()),
        "fig05-sitemap": fig_sitemap(),
        **wireframes(),
    }
    for name, doc in pages.items():
        (BUILD / f"{name}.html").write_text(doc)
    print(f"wrote {len(pages)} figure pages to {BUILD}")


if __name__ == "__main__":
    main()
