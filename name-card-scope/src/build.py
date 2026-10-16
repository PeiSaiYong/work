"""Builds ../minmed-name-card-scope.html, a single self-contained file.

Run: python3 build.py
"""

from pathlib import Path

import html
import re

import mocks as M
import preview as PV
from mocks import E, LINK, chip, mark, thumb

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "minmed-name-card-scope.html"

# Figures are numbered in this order; build() checks the document uses the same order.
FIG_ORDER = [
    "overview", "sitemap", "nav", "journey",
    "pg-card", "pg-captcha", "pg-inactive", "pg-notfound", "pg-error", "pg-whatsapp", "pg-desktop",
    "pg-email", "pg-gpass", "pg-apass", "pg-staffsignin", "pg-mycard", "pg-mycardflow", "pg-mycarddesk",
    "pg-signin", "pg-cards", "pg-add", "pg-import", "pg-details", "pg-edit", "pg-dialogs",
    "pg-activity", "pg-admins", "pg-settings", "pg-adminphone", "pg-notify",
    "bot-flow", "bot-outcome",
]
USED = []


def fnum(key):
    return FIG_ORDER.index(key) + 1


def fref(key):
    return f'<a href="#{key}">Figure {fnum(key)}</a>'


def fig(key, inner, title, sub="", alt="", wide=False, img=True):
    USED.append(key)
    cls = "fig wide" if wide else "fig"
    role = f' role="img" aria-label="{E(alt or title)}"' if img else ""
    sub_html = f"<span>{sub}</span>" if sub else ""
    return (
        f'<figure class="{cls}" id="{key}"><div class="fstage"{role}>{inner}</div>'
        f"<figcaption><b>Figure {fnum(key)}. {title}</b>{sub_html}</figcaption></figure>"
    )


def shot(inner):
    return f'<div class="shot">{inner}</div>'


def admin_shot(path, page):
    return shot(M.browser("me.minmed.sg" + path, page))


# ------------------------------------------------------------------ rules (section 8)

RULES = [
    # (number, name, counted, limit, then, status)
    ("1", "Same IP", "Card opens, contact downloads and wrong card addresses from one IP address",
     "More than 3 in a rolling minute", "CAPTCHA before anything is sent", chip("Confirmed", "dec")),
    ("2", "Pass", "A browser that has passed the CAPTCHA", "30 minutes", "No new CAPTCHA for that browser",
     chip("Confirmed", "dec")),
    ("3", "Busy card", "Opens and downloads of one card, from all IP addresses together",
     "More than 20 in a rolling 10 minutes", "Everyone opening that card gets the CAPTCHA for the next 30 minutes",
     chip("Confirmed", "dec") + "<br><small>Replaces “every 5th visitor”</small>"),
    ("4", "Limit after a pass", "Opens and downloads by a browser holding a pass", "More than 20 in 5 minutes",
     "The pass ends and the CAPTCHA comes back", chip("Confirmed", "dec")),
]


# ------------------------------------------------------------------ card preview (dialog)

PREVIEW_CSS = """
.pv-cta { display: flex; align-items: center; gap: 8px 14px; flex-wrap: wrap; margin: 14px 0 0; }
.pv-open { display: inline-flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 16px; border: 0; border-radius: 10px; background: var(--plum); color: #fff; font: 700 0.9rem/1.2 "Open Sans", sans-serif; cursor: pointer; }
.pv-open:hover { background: #84396e; }
.pv-open:focus-visible { outline: 3px solid var(--brand); outline-offset: 2px; }
.pv-open .ic { width: 16px; height: 16px; }
.pv-cta span { color: var(--muted); font-size: 0.86rem; }
.pvd { padding: 0; border: 0; background: transparent; overflow: visible; max-width: none; max-height: none; }
.pvd::backdrop { background: rgba(25, 38, 55, 0.62); }
.pvd form { position: absolute; top: 0; right: -56px; margin: 0; z-index: 2; }
.pvd-x { width: 40px; height: 40px; border-radius: 50%; border: 0; background: #fff; color: var(--navy); font: 400 26px/1 "Open Sans", sans-serif; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
.pvd-x:focus-visible { outline: 3px solid var(--brand); outline-offset: 2px; }
@media (max-width: 520px) {
  .pvd { width: 100vw; height: 100vh; height: 100dvh; margin: 0; }
  .pvd .pvw { height: 100%; }
  .pvd .pvw .pv-dev { width: 100%; height: 100%; border: 0; border-radius: 0; box-shadow: none; }
  .pvd .pvw .pv-sb, .pvd .pvw .pv-bar { display: none; }
  .pvd form { top: 10px; right: 10px; }
}
"""


def preview_button():
    return (
        '<div class="pv-cta"><button type="button" class="pv-open" data-preview="card-preview">'
        f'{M.ic("phone")}Preview the card at full size</button>'
        "<span>What a visitor sees after scanning a QR code, with made-up details.</span></div>"
    )


def preview_dialog():
    return (
        '<dialog id="card-preview" class="pvd" aria-label="Card preview at full size">'
        '<form method="dialog"><button class="pvd-x" aria-label="Close preview">×</button></form>'
        f"{PV.device()}</dialog>"
    )


# ------------------------------------------------------------------ sections

def head():
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="description" content="Product scope for Minmed Digital Name Cards: decisions, users, permissions, site map, page mockups, bot protection, privacy, feasibility and spec changes.">
<title>Name Card Scope</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
{(SRC / "scope.css").read_text()}
{PV.card_css()}
{PV.FRAME_CSS}
{PREVIEW_CSS}
</style>
</head>
<body>
<header class="top"><div class="top-inner">
  <div class="brand">{mark(28)}<span>Name Card Scope</span></div>
  <nav class="toc" aria-label="Sections">
    <a href="#how">How it works</a><a href="#confirmed">Confirmed</a><a href="#features">Features</a><a href="#users">Users</a><a href="#matrix">Permissions</a><a href="#map">Site map</a><a href="#pages">Pages</a><a href="#bots">Bot protection</a><a href="#links">Links &amp; privacy</a><a href="#feasibility">Feasibility</a><a href="#pending">Open items</a>
  </nav>
</div></header>
<main>
"""


def intro():
    return f"""
<div class="eyebrow">Product scope · input to spec 0.3</div>
<h1>Minmed Digital Name Cards</h1>
<p class="lede">A digital name card for every Minmed staff member, managed centrally. Admins create and change every card. Staff sign in only to see their card, add a name or alias to their link and download their QR code. Anyone with a card's link can open it, but nobody can find it on Google.</p>
<p class="meta">Based on Technical Specification draft 0.2 (15/10/2026) and your decisions on 16/10/2026. Names, numbers, codes and QR codes in the examples are made up. Updated 16/10/2026.</p>
<div class="legend">
  <span>{chip("Confirmed", "dec")} you decided it</span>
  <span>{chip("Proposed", "rec")} my recommendation, waiting for your OK (section 11)</span>
  <span>{chip("Test", "test")} try on a test app before the build</span>
</div>
{preview_button()}
"""


def s_how():
    steps = [
        ("Admin adds the card", "In the admin console, one at a time or from a spreadsheet."),
        ("Staff member gets an email", "Their link and QR code, an Add to Google Wallet button, and steps for Apple Wallet."),
        ("Staff member can add a name to the link", "Optional. They sign in with their Minmed Google account and type a name or alias. They get a new link and a new card email; the old link stops working."),
        ("Staff member shares it", "Sends the link on WhatsApp or email, or shows the QR code from Wallet."),
        ("Visitor opens the link", "Sees the card, then saves the contact, emails, calls or WhatsApps. Unusual traffic gets a CAPTCHA."),
        ("Details change", "The staff member replies to the card email. An admin edits the card, and the same link shows the new details."),
        ("Staff member leaves", "HR tells an admin. On the last day the card is deactivated and soft-deleted, and the staff member can't sign in. The link shows “This card is no longer active.”"),
    ]
    boxes = "".join(f"<div><b>{t}</b>{d}</div>" for t, d in steps)
    return f"""
<section id="how">
<div class="eyebrow">1</div>
<h2>How it works</h2>
{fig("overview", f'<div class="flow">{boxes}</div>', "The life of a card, from creation to deactivation.",
     alt="Seven numbered steps: admin adds the card; staff member gets an email; staff member can add a name to the link; staff member shares it; visitor opens the link; details change; staff member leaves.", wide=True)}
</section>
"""


def s_confirmed():
    def row(text, src, status=""):
        st = f" {status}" if status else ""
        return f'<tr><td>{text}{st}</td><td class="src">{src}</td></tr>'

    def grp(t):
        return f'<tr class="group"><th colspan="2">{t}</th></tr>'

    you = "You, 16/10"
    rows = [
        grp("Product"),
        row("One central place to manage every staff card. Staff can't change their card details, so there's no approval process. The only thing they can change is the name or alias in their link.", you),
        row("Cards are public to anyone with the link, but can't be found through Google.", you),
        row(f"Each link ends in a random code of 22 letters and numbers, so nobody can guess it: <code>{E(LINK)}</code>. Staff can put a name or alias in front of the code: <code>{E(M.LINK_ALIAS)}</code>.", "You, 16/10; industry standards"),
        row("Staff sign in with their Minmed Google account to a My card page at <code>me.minmed.sg/my-card</code>. There they can only read their card details, set or change the name or alias in their link, and download their QR code. They keep their link on their phone, or in Apple Wallet or Google Wallet.", you),
        row("Built on Base44. Phone-first public card. Admins and staff sign in with company Google accounts.", "Spec 0.2 §1.1; you, 16/10"),
        grp("The card"),
        row("Fields: name, designation, Minmed, work email, optional mobile and photo, optional biography, languages and LinkedIn. Company information is a link to minmed.sg; no social links.", "Spec 0.2 §3.1; you, 16/10"),
        row("Actions: Save contact and Email, plus Call and WhatsApp when a mobile is published. No visitor app.", "Spec 0.2 §1.1; you, 16/10"),
        row("Every card shows the Minmed logo. A Super admin sets it once in Settings; it's the same on every card and can't be changed for a single card. The card forms and My card show it as locked.", you),
        row("On a computer, the card also shows a QR code to move it to a phone.", you),
        row("No “Active staff profile ✓ Checked” line and no How to verify panel.", you),
        row("Sharing the link on WhatsApp shows a preview of the card.", "Spec 0.2 §4.4",
            chip("At risk", "risk") + ' <span class="note">Base44 can\'t make a per-card preview as is. See section 10 and open item 1.</span>'),
        grp("Wallet"),
        row("Minmed issues a Google Wallet pass. iPhone staff add their QR code to Apple Wallet themselves with iOS 27's Create a Pass. No Apple Developer Program, fee or D-U-N-S number.", you),
        grp("Name or alias in the link"),
        row("Optional. Letters, numbers and hyphens, 2 to 30 characters.", you),
        row("Until an alias is set, the plain link without a name works.", you),
        row("Setting or changing the alias gives a new link. The old link, printed QR codes and Apple Wallet passes made from it show “No card found”. The Google Wallet pass updates itself, and a new card email goes out automatically.", you),
        row("Staff can change their alias as often as they like. Each change ends the previous link, and My card asks them to confirm before saving.", you),
        row("Clearing an alias, by the staff member or an admin, brings back the plain link without a name.", you),
        row("Before saving, staff can preview their card at the new link. Nothing changes until they save: the new link doesn't work yet and the old one keeps working.", you),
        row("Admins can clear an alias that's offensive or copies someone else's name. Every alias change is logged and emailed to manage@minmed.sg.", you),
        grp("Admins"),
        row("Two roles: Super admin and Admin.", you),
        row("Only a Super admin can reactivate (restore) a card, give it a new link code or delete it.", you),
        row("Cards can be imported from a spreadsheet at launch.", you),
        row("Admins see view counts. No monthly report emails.", you),
        row("Every admin change is logged and emailed to manage@minmed.sg.", "Spec 0.2 §1.1"),
        grp("Leavers and records"),
        row("HR tells an admin as part of offboarding. On the person's last day their card is deactivated and soft-deleted, and they can no longer sign in.", you),
        row("Soft-deleted cards are kept but hidden. A Super admin can restore one or delete it permanently.", "You, 16/10 (PDPA)"),
        row("Soft-deleted cards are listed under a Deactivated tab on the Cards page, which only Super admins see.", you),
        grp("Bot protection"),
        row("One IP address making more than 3 card opens or contact downloads within 1 minute must pass a CAPTCHA.", you),
        row("After passing, that browser isn't asked again for 30 minutes.", you),
        row("A busy card is checked: more than 20 opens of one card in 10 minutes means everyone opening it gets the CAPTCHA for the next 30 minutes. This replaces “every 5th visitor”.", "You, 16/10; industry standards"),
        row("A pass ends early after 20 opens in 5 minutes.", "You, 16/10; industry standards"),
        row("For the first 2 weeks the rules only record. Then they switch on.", "You, 16/10; industry standards"),
    ]
    return f"""
<section id="confirmed">
<div class="eyebrow">2</div>
<h2>What's confirmed</h2>
<p>On 16/10/2026 you approved the proposals in this document. Open items are in section 11.</p>
<div class="tablewrap"><table class="decisions">
<thead><tr><th>Decision</th><th>Source</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>
</section>
"""


def s_features():
    return """
<section id="features">
<div class="eyebrow">3</div>
<h2>Features</h2>
<p>Everything in the first version. Anything not listed here isn't being built.</p>
<div class="feat">
  <div><h3>Public card</h3><div class="host">me.minmed.sg</div><ul>
    <li>Card page: photo, name, designation, contacts and About</li>
    <li>Save contact, Email, Call and WhatsApp</li>
    <li>QR code when opened on a computer</li>
    <li>WhatsApp link preview</li>
    <li>No longer active, not found and temporary error pages</li>
    <li>CAPTCHA check against bots</li>
    <li>Hidden from search engines</li>
  </ul></div>
  <div><h3>Staff</h3><div class="host">me.minmed.sg/my-card</div><ul>
    <li>Minmed Google sign-in, own card only</li>
    <li>My card: read-only details, a name or alias for the link, a preview before saving, QR code download</li>
    <li>Card email with link, QR code and Wallet options</li>
    <li>Google Wallet pass that updates itself</li>
    <li>Apple Wallet pass they make themselves</li>
    <li>Ask for changes by replying to the card email</li>
  </ul></div>
  <div><h3>Admin console</h3><div class="host">me.minmed.sg/admin</div><ul>
    <li>Google sign-in, admin list only</li>
    <li>Cards: list, search, add, import, edit</li>
    <li>Card details: link, alias (clear it if needed), QR code, card image, views, history</li>
    <li>Deactivate (soft delete); Super admin also restores, re-codes and deletes permanently</li>
    <li>Activity log</li>
    <li>Admins and Settings, including the company logo (Super admin)</li>
    <li>Email to manage@minmed.sg on every change, alias changes included</li>
  </ul></div>
</div>
</section>
"""


def s_users():
    return """
<section id="users">
<div class="eyebrow">4</div>
<h2>Users</h2>
<div class="tablewrap"><table>
<thead><tr><th>User</th><th>Signs in?</th><th>Who they are</th><th>What they do</th></tr></thead>
<tbody>
<tr><td><b>Visitor</b></td><td>No</td><td>Anyone who has a card's link or scans its QR code.</td><td>Views the card, saves the contact, gets in touch. May be asked to pass a CAPTCHA.</td></tr>
<tr><td><b>Staff member</b> (card holder)</td><td>Yes, company Google account, to their own My card page only</td><td>Minmed staff with a card.</td><td>Gets their card by email, keeps it in Wallet or on their phone, shares it. Can add a name or alias to their link and download their QR code. Asks an admin for other changes.</td></tr>
<tr><td><b>Admin</b></td><td>Yes, company Google account</td><td>For example HR, added by a Super admin.</td><td>Adds, edits, sends and deactivates cards.</td></tr>
<tr><td><b>Super admin</b></td><td>Yes, company Google account</td><td>One or two owners, for example manage@minmed.sg's owner and IT.</td><td>Everything an Admin does, plus admins, settings, and reactivating, re-coding or deleting cards.</td></tr>
</tbody></table></div>
<p class="note">manage@minmed.sg receives admin notifications automatically. It's a mailbox, not a user.</p>
</section>
"""


def s_matrix():
    Y, N, O = '<td class="y">✓</td>', '<td class="n">—</td>', '<td class="o">Own</td>'

    def r(text, *cells):
        return f"<tr><td>{text}</td>{''.join(cells)}</tr>"

    def g(t):
        return f'<tr class="group"><th colspan="5">{t}</th></tr>'

    def auto(text):
        return f'<tr><td>{text}</td><td class="a" colspan="4">Auto</td></tr>'

    rows = [
        g("Public card"),
        r("Open a card from its link or QR code", Y, Y, Y, Y),
        r("Save contact, email, call, WhatsApp", Y, Y, Y, Y),
        r("Forward the link to someone else", Y, Y, Y, Y),
        r("Find a card without its link (search, browse, guess)", N, N, N, N),
        g("Getting and keeping a card"),
        r("Receive the card email (link, QR code, Wallet options)", N, O, N, N),
        r("Add the card to Google Wallet or Apple Wallet", N, O, N, N),
        r("Sign in to My card and see their own card details", N, O, N, N),
        r("Set or change the name or alias in their own link", N, O, N, N),
        r("Preview their card at a new link before saving", N, O, N, N),
        r("Clear their own alias, going back to the plain link", N, O, N, N),
        r("Download their own QR code", N, O, N, N),
        r("Change their own card details", N, N, N, N),
        r("Ask for a change by replying to the card email", N, O, N, N),
        g("Admin console"),
        r("Sign in to the admin console", N, N, Y, Y),
        r("See and search all cards", N, N, Y, Y),
        r("Add a card", N, N, Y, Y),
        r("Import cards from a spreadsheet", N, N, Y, Y),
        r("Edit a card's details and photo, and choose whether the mobile is shown", N, N, Y, Y),
        r("Clear a staff member's alias", N, N, Y, Y),
        r("Send or re-send the card email", N, N, Y, Y),
        r("Download a card's QR code and card image", N, N, Y, Y),
        r("Deactivate a card (soft delete)", N, N, Y, Y),
        r("Restore a deactivated card", N, N, N, Y),
        r("Issue a new link code (the old link stops working)", N, N, N, Y),
        r("Delete a card permanently", N, N, N, Y),
        r("See view counts", N, N, Y, Y),
        r("See the activity log", N, N, Y, Y),
        r("Add or remove admins and change roles", N, N, N, Y),
        r("Change the company logo shown on every card (in Settings)", N, N, N, Y),
        r("Use a different logo on one card", N, N, N, N),
        r("Change the brand colours, company details, notifications and Google Wallet settings", N, N, N, Y),
        g("Automatic"),
        auto("Record every admin action and alias change in the activity log"),
        auto("Email manage@minmed.sg when a card is added, edited, given a new alias, deactivated, restored, re-coded or deleted"),
        auto("Send a new card email and update the Google Wallet pass when an alias changes"),
        auto("Update the Google Wallet pass when its card changes, and expire it when the card is deactivated"),
        auto("Ask for a CAPTCHA when a bot-protection rule is met (section 8)"),
    ]
    return f"""
<section id="matrix">
<div class="eyebrow">5</div>
<h2>Roles and permissions</h2>
<p>✓ allowed · — not allowed · <b style="color:var(--blue)">Own</b> their own card only · <b style="color:var(--amber)">Auto</b> the system does it. Every rule is checked on the server, not only by hiding buttons.</p>
<div class="tablewrap"><table class="matrix">
<thead><tr><th>Action</th><th class="col">Visitor</th><th class="col">Staff member</th><th class="col">Admin</th><th class="col">Super admin</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>
</section>
"""


def node(key, thumb_html, title, sub="", code=""):
    c = f"<code>{E(code).replace('/', '/<wbr>')}</code>" if code else ""
    s = f"<small>{sub}</small>" if sub else ""
    href = f' href="#{key}"' if key else ""
    tag = "a" if key else "div"
    return f'<{tag} class="smn"{href}>{thumb_html}<span><b>{title}</b>{c}{s}</span></{tag}>'


def dot_node(title, sub="", code=""):
    c = f"<code>{E(code)}</code>" if code else ""
    s = f"<small>{sub}</small>" if sub else ""
    return f'<div class="smn"><span class="dot"></span><span><b>{title}</b>{c}{s}</span></div>'


def s_map():
    tp = lambda h: thumb(h, "phone")  # noqa: E731
    tw = lambda h: thumb(h, "wide")  # noqa: E731
    public = f"""
<div class="smz z-pub"><div class="smz-h"><b>Public</b><code>me.minmed.sg</code><span>No sign-in · hidden from search engines · no menu</span></div>
<ul class="smt">
  <li>{node("pg-card", tp(M.card_body()), "Card page", "or /card/{alias}/{code}", code="/card/{code}")}
    <ul class="smt">
      <li>{node("pg-desktop", tw(M.card_desktop()), "On a computer", "adds a QR code")}</li>
      <li>{node("pg-captcha", tp(M.captcha_page()), "CAPTCHA check", "when a rule in section 8 is met")}</li>
      <li>{node("pg-inactive", tp(M.inactive_page()), "No longer active", "after deactivation")}</li>
      <li>{node("pg-error", tp(M.error_page()), "Temporary error", "card can't be checked")}</li>
    </ul>
  </li>
  <li>{node("pg-notfound", tp(M.notfound_page()), "Card not found", "any wrong address")}</li>
  <li>{dot_node("Files behind the same code", "contact file, card image, Google Wallet link; served by backend functions", "/functions/…?code={code}")}</li>
  <li>{dot_node("Home", "redirects to minmed.sg; no staff list", "/")}</li>
</ul></div>"""

    staff = f"""
<div class="smz z-stf"><div class="smz-h"><b>Staff</b><code>me.minmed.sg/my-card</code><span>Minmed Google sign-in · own card only</span></div>
<ul class="smt">
  <li>{node("pg-staffsignin", tp(M.staff_signin()), "Sign in", code="/my-card")}</li>
  <li>{node("pg-mycard", tp(M.my_card()), "My card", "every field read-only, one box for the link, QR code download")}
    <ul class="smt">
      <li>{node("pg-mycardflow", tp(M.my_card_step("typing")), "Changing the link", "type, preview, confirm, done")}</li>
      <li>{node("pg-mycarddesk", tw(M.my_card_desktop()), "On a computer", "same page, wider")}</li>
    </ul>
  </li>
</ul></div>"""

    admin = f"""
<div class="smz z-adm"><div class="smz-h"><b>Admin console</b><code>me.minmed.sg/admin</code><span>Company Google sign-in · admin list only</span></div>
<ul class="smt">
  <li>{node("pg-signin", tw(M.ad_signin()), "Sign in", code="/admin")}</li>
  <li>{node("pg-cards", tw(M.ad_cards()), "Cards", code="/admin/cards")}
    <ul class="smt">
      <li>{node("pg-add", tw(M.ad_add()), "Add card", code="/admin/cards/new")}</li>
      <li>{node("pg-import", tw(M.ad_import()), "Import cards", code="/admin/cards/import")}</li>
      <li>{node("pg-details", tw(M.ad_details()), "Card details", code="/admin/cards/{id}")}
        <ul class="smt">
          <li>{node("pg-edit", tw(M.ad_edit()), "Edit card", code="/admin/cards/{id}/edit")}</li>
          <li>{node("pg-dialogs", "", "Confirm dialogs", "deactivate, clear alias, new link code, delete")}</li>
        </ul>
      </li>
    </ul>
  </li>
  <li>{node("pg-activity", tw(M.ad_activity()), "Activity log", code="/admin/activity")}</li>
  <li>{node("pg-admins", tw(M.ad_admins()), "Admins", "Super admin only", code="/admin/admins")}</li>
  <li>{node("pg-settings", tw(M.ad_settings()), "Settings", "Super admin only", code="/admin/settings")}</li>
</ul></div>"""

    tm = lambda h: thumb(h, "mail")  # noqa: E731
    tpass = lambda h: thumb(h, "pass")  # noqa: E731
    msgs = f"""
<div class="smz z-msg"><div class="smz-h"><b>Emails, Wallet and sharing</b><code>outside the website</code><span>How cards reach staff, admins and visitors</span></div>
<ul class="smt">
  <li>{node("pg-email", tm(M.email_card()), "Card email", "to the staff member")}</li>
  <li>{node("pg-gpass", tpass(M.gwallet_pass()), "Google Wallet pass", "issued by Minmed")}</li>
  <li>{node("pg-apass", tpass(M.apple_pass()), "Apple Wallet pass", "made by the staff member")}</li>
  <li>{node("pg-whatsapp", tp(M.wa_chat()), "WhatsApp link preview", "when a link is shared")}</li>
  <li>{node("pg-notify", tm(M.email_admin()), "Admin notification", "to manage@minmed.sg")}</li>
</ul></div>"""

    nav_inner = (
        '<div class="navdemo">'
        f'<div><div class="navlbl">Super admin</div><div class="shot navs">{M.browser("me.minmed.sg/admin/cards", M.ad_top("Cards", "Super admin", menu=True) + "<div style=height:64px></div>")}</div></div>'
        f'<div><div class="navlbl">Admin</div><div class="shot navs">{M.browser("me.minmed.sg/admin/cards/AT29/edit", M.ad_top("Cards", "Admin", "Siti Rahman", "SR") + "<div class=ad-main><div class=ad-crumb>Cards › Alex Tan › <b>Edit</b></div></div>")}</div></div>'
        "</div>"
    )

    journey = f"""
<div class="dg">
  <div class="dg-row"><div class="dg-n"><b>Link</b><small>in WhatsApp, email or anywhere</small></div><div class="dg-n"><b>QR code</b><small>scanned from Wallet, a screen or print</small></div></div>
  <div class="dg-ar"></div>
  <div class="dg-n cond"><b>CAPTCHA check</b><small>only when a rule in section 8 is met</small></div>
  <div class="dg-ar"></div>
  <div class="dg-n main"><b>Card page</b><small>on a computer, a QR code moves it to a phone</small></div>
  <div class="dg-ar"></div>
  <div class="dg-acts">
    <div class="dg-n"><b>Save contact</b><small>contact file</small></div>
    <div class="dg-n"><b>Email</b><small>mail app</small></div>
    <div class="dg-n"><b>Call</b><small>phone app</small></div>
    <div class="dg-n"><b>WhatsApp</b><small>chat</small></div>
    <div class="dg-n"><b>About Minmed</b><small>minmed.sg</small></div>
  </div>
</div>"""

    return f"""
<section id="map">
<div class="eyebrow">6</div>
<h2>Site map and navigation</h2>
<p>Four parts: the public card, the staff's My card page, the admin console, and the emails and passes that connect them. Select a page to see its mockup in section 7.</p>
{fig("sitemap", f'<div class="smap">{public}{staff}{admin}{msgs}</div>', "Site map. Each entry is a page or message, with its address.", wide=True, img=False)}
<div class="figs">
{fig("nav", nav_inner, "Admin console navigation.",
     "Admins see Cards and Activity log; Super admins also see Admins and Settings. The account menu holds Sign out. Inside a card, the breadcrumb leads back to Cards.",
     alt="Two admin top bars. Super admin: Cards, Activity log, Admins, Settings, with the account menu open showing Sign out. Admin: Cards and Activity log only, with the breadcrumb Cards, Alex Tan, Edit.", wide=True)}
{fig("journey", journey, "How a visitor moves through the public card.",
     "There's no menu and no way to reach another person's card. Call and WhatsApp appear only when a mobile is published.",
     alt="Link or QR code leads to an optional CAPTCHA check, then the card page, which offers Save contact, Email, Call, WhatsApp and About Minmed.", wide=True)}
</div>
</section>
"""


def s_pages():
    phone_figs = (
        fig("pg-card", M.phone(M.card_body()), "Card page.",
            f"<code>{E(M.LINK_ALIAS)}</code>, or <code>{E(LINK)}</code> until a name or alias is added · anyone with the link. Call and WhatsApp only with a published mobile; About only when filled in.",
            alt="Phone showing Alex Tan's card: photo initials, name, designation, Minmed, Save contact button, Email, Call and WhatsApp buttons, work email, mobile, About with biography, languages and LinkedIn, and an About Minmed link.")
        + fig("pg-captcha", M.phone(M.captcha_page()), "CAPTCHA check.",
              "Same address, shown instead of the card when a rule in section 8 is met. Most people pass without clicking; this is what a flagged visitor sees.",
              alt="Phone showing a Quick check page with a Cloudflare Turnstile checkbox labelled Verify you are human.")
        + fig("pg-inactive", M.phone(M.inactive_page()), "No longer active.",
              "Same address after deactivation. No details, photo, Save contact or contact buttons.",
              alt="Phone showing: This card is no longer active, and an About Minmed link.")
        + fig("pg-notfound", M.phone(M.notfound_page()), "Card not found.",
              "Any wrong code, old alias, deleted card or mistyped link. The same answer every time, so nobody learns which codes exist.",
              alt="Phone showing: No card found at this address. Check the link or visit minmed.sg.")
        + fig("pg-error", M.phone(M.error_page()), "Temporary error.",
              "The card can't be checked, for example during an outage or when Base44 credits run out. Never shows old details.",
              alt="Phone showing: Can't load this card right now. Please try again in a few minutes, with a Try again button.")
        + fig("pg-whatsapp",
              '<div><span class="variant">Per-card preview · options B, C</span>' + M.wa_chat("card") + "</div>"
              + '<div><span class="variant">Same for every card · option A</span>' + M.wa_chat("generic") + "</div>",
              "WhatsApp link preview. " + chip("Test", "test"),
              "Which one depends on the WhatsApp test (open item 1).",
              alt="Two WhatsApp messages with link previews: one shows Alex Tan's card image and name; the other shows the Minmed logo and Minmed digital name card.")
    )
    desktop = fig("pg-desktop", shot(M.browser(M.LINK_ALIAS, M.card_desktop())), "Card page on a computer.",
                  "The same card in a narrow column, plus a QR code to move it to a phone.",
                  alt="Browser window showing the card in a centred column and a QR code panel: Scan to save to your phone.", wide=True)

    staff_figs = (
        fig("pg-email", M.email_card(), "Card email to the staff member.",
            "Sent when an admin chooses Save and send card email or Send card email, and again after every alias change. Replies go to manage@minmed.sg.",
            alt="Email: Your Minmed digital name card. Open my card button, link, QR code, Add to Google Wallet button, three iPhone steps for Create a Pass, a pointer to me.minmed.sg/my-card for adding a name to the link, and Need another change? Reply to this email.")
        + fig("pg-gpass", M.gwallet_pass(), "Google Wallet pass.",
              "Issued by Minmed. Updates when the card changes and shows as expired when it's deactivated.",
              alt="Plum Google Wallet pass with the Minmed logo, designation, name, work email and a QR code.")
        + fig("pg-apass", M.apple_pass(), "Apple Wallet pass, made by the staff member.",
              "Made with iOS 27's Create a Pass, so its look may vary. Minmed can't update or remove it, but its QR code always opens the live card.",
              alt="Dark Apple Wallet pass named Minmed name card with the name Alex Tan and a QR code.")
    )

    def step(n, label, body, cls=""):
        return f'<div><div class="stepl"><i>{n}</i>{label}</div>{M.phone(body, url="me.minmed.sg/my-card", cls=cls)}</div>'

    steps = (
        '<div class="steps">'
        + step(1, "Type a name or alias", M.my_card_step("typing"))
        + step(2, "Preview the card before saving", M.my_card_preview(), cls="cut")
        + step(3, "Save and confirm the new link", M.my_card_confirm())
        + step(4, "Done: new link, QR code and email", M.my_card_step("saved"))
        + step(5, "If the alias breaks the rule", M.my_card_step("error"))
        + "</div>"
    )
    mycard_figs = (
        '<div class="figs two">'
        + fig("pg-staffsignin", M.phone(M.staff_signin(), url="me.minmed.sg/my-card"), "My card sign-in.",
              "<code>me.minmed.sg/my-card</code>. A Minmed account without an active card sees “There's no name card for this account.”",
              alt="Phone showing My name card, Please sign in with your Minmed registered email address, and a Sign in with Google button.")
        + fig("pg-mycard", M.phone(M.my_card(), url="me.minmed.sg/my-card", cls="cut"), "My card.",
              f"Top of the page after signing in. The only box staff can type in is the name or alias in their link. Preview shows the card at the new link before saving, and they can download their QR code. Below that, every field is read-only, including the company logo (whole page in {fref('pg-mycarddesk')}).",
              alt="Phone showing the top of My name card: the link me.minmed.sg/card/ with an empty box marked alias and the code after it, the alias rules, a warning that saving gives a new link, Preview and Save link buttons, the QR code with Download QR code, and the start of the read-only card details.")
        + "</div>"
        + '<div class="figs">'
        + fig("pg-mycardflow", steps, "How a staff member changes their link.",
              "1. They type a name or alias in the box. 2. Preview shows their card at the new link; nothing is saved yet. 3. They save and confirm. 4. The new link works at once and a new card email goes out; the old link shows “No card found”. 5. An alias that breaks the rule can't be previewed or saved.",
              alt="Five phone screens. One: Alex-Tan typed into the box in the link, with Preview and Save link buttons. Two: the preview, with the note Not saved yet. This is how your card will look at your new link., the new link me.minmed.sg/card/Alex-Tan/ followed by the code, Alex Tan's card, and Back and Save link buttons. Three: the Change your link? dialog with Cancel and Change link. Four: the saved link with Alex-Tan, a message that the new link is ready and the new card was emailed, Copy link, and the new QR code with Download. Five: Alex Tan! typed in, a red message to use only letters, numbers and hyphens, 2 to 30 characters, and Preview and Save link greyed out.",
              wide=True)
        + fig("pg-mycarddesk", shot(M.browser("me.minmed.sg/my-card", M.my_card_desktop())), "My card on a computer.",
              "The same page, laid out like the admin card details page: the card on the left, then the link box, the QR code and every field read-only.",
              alt="Browser at me.minmed.sg/my-card for Alex Tan, Staff, with Sign out. Left: the card with the company logo. Right: the link me.minmed.sg/card/ with Alex-Tan in a box and the code, the alias rules and warning, Copy link, Preview and a greyed Save link; the QR code with Download QR code; and read-only fields for first and last name, designation, work email, mobile shown on card, photo, biography, languages, LinkedIn and the locked company logo.",
              wide=True)
        + "</div>"
    )

    signin = (
        '<div class="pair">'
        + M.browser("me.minmed.sg/admin", M.ad_signin("ask"))
        + M.browser("me.minmed.sg/admin", M.ad_signin("denied"))
        + "</div>"
    )
    admin_figs = (
        fig("pg-signin", signin, "Admin sign-in.",
            "Left: <code>me.minmed.sg/admin</code>. Right: a company account that isn't on the admin list.",
            alt="Two sign-in screens. Left: Name cards admin, Please sign in with your Minmed registered email address, Sign in with Google. Right: You don't have access, Use another account.", wide=True)
        + fig("pg-cards", admin_shot("/admin/cards", M.ad_cards()), "Cards.",
              "<code>/admin/cards</code>. Search by name or email. Deactivated cards are soft-deleted: they leave this list and appear under Deactivated, for Super admins. Views count card page openings in the last 30 days.",
              alt="Admin Cards page: search box, Active and Deactivated tabs, Import and Add card buttons, and a table of five active cards with designation, status, views and last updated.", wide=True)
        + fig("pg-add", admin_shot("/admin/cards/new", M.ad_add()), "Add card.",
              "<code>/admin/cards/new</code>. Work email must end with @minmed.sg. The mobile shows on the card only when switched on. The company logo is locked: it's the same on every card.",
              alt="Add card form with first and last name, designation, work email, mobile with Show on card switch, photo upload, the company logo shown as locked, biography, languages, LinkedIn, and an empty preview with the logo. Buttons: Cancel, Save, Save and send card email.", wide=True)
        + fig("pg-import", admin_shot("/admin/cards/import", M.ad_import()), "Import cards.",
              "<code>/admin/cards/import</code>. Rows with problems are skipped until fixed. The card emails can go out in the same step.",
              alt="Import cards page at the Check step: 43 rows, 41 ready, 2 need fixing, with two rows flagged. Send card emails now is ticked; Create 41 cards button.", wide=True)
        + fig("pg-details", admin_shot("/admin/cards/AT29", M.ad_details()), "Card details.",
              "<code>/admin/cards/{id}</code>. Admins can clear an alias. The ⋯ menu (New link code, Delete card) appears only for Super admins. On a deactivated card, Restore replaces Deactivate.",
              alt="Card details for Alex Tan: Edit, Send card email, Deactivate and an open menu with New link code and Delete card. Panels for the live card with the company logo, the link with the alias Alex-Tan, Copy and Clear alias, QR code and card image downloads, Google Wallet pass Active, 48 views, and history.", wide=True)
        + fig("pg-edit", admin_shot("/admin/cards/AT29/edit", M.ad_edit()), "Edit card.",
              "<code>/admin/cards/{id}/edit</code>, seen by an Admin, who has no Settings tab. Saving changes the live card at once, on the same link and QR code, and emails manage@minmed.sg. The company logo is locked here for everyone.",
              alt="Edit card form, signed in as Siti Rahman, Admin, with only Cards and Activity log in the menu. The designation is changed to Senior Corporate Sales Manager and highlighted, the company logo is shown as locked, and the preview shows the logo and the new designation, with the note Same link and QR code.", wide=True)
        + fig("pg-dialogs", M.ad_dialogs(), "Confirm dialogs.",
              "Deactivate and Clear alias are for Admins and Super admins. New link code and Delete are for Super admins only.",
              alt="Four dialogs: Deactivate Alex Tan's card, which also soft-deletes it; Clear Alex Tan's alias; Give Alex Tan's card a new link, with Send Alex the new card email ticked; Delete Alex Tan's card permanently.", wide=True)
        + fig("pg-activity", admin_shot("/admin/activity", M.ad_activity()), "Activity log.",
              "<code>/admin/activity</code>. Every admin action and alias change: who, what, which card and when.",
              alt="Activity log with filters for card, person and action, and seven entries such as Alias changed by Alex Tan (staff), Edited, Deactivated, New link code and Imported.", wide=True)
        + fig("pg-admins", admin_shot("/admin/admins", M.ad_admins()), "Admins (Super admin only).",
              "<code>/admin/admins</code>. Admins are added by company email.",
              alt="Admins page listing four admins with role selectors and Remove links, plus a row to add an admin by email and role.", wide=True)
        + fig("pg-settings", admin_shot("/admin/settings", M.ad_settings()), "Settings (Super admin only).",
              "<code>/admin/settings</code>. Card design: the company logo on every card, which only Super admins can change. Also company details, notifications and Google Wallet.",
              alt="Settings page with sections for card design (logo with Replace and the note Shown on every card. Only Super admins can change it., brand colours and a card preview with the logo), company details, notifications to manage@minmed.sg and Google Wallet status.", wide=True)
    )
    last_pair = (
        '<div class="figs two">'
        + fig("pg-adminphone", M.phone(M.ad_mobile_cards(), url="me.minmed.sg/admin/cards"), "Admin console on a phone.",
              "The same Cards page on a phone: the table becomes a list, with the same Active and Deactivated tabs.",
              alt="Phone showing the admin Cards list with search, Active and Deactivated tabs, Add card and four cards with their status.")
        + fig("pg-notify", f'<div class="mails">{M.email_admin()}{M.email_admin("alias")}</div>', "Admin notification.",
              "Sent to manage@minmed.sg for every add, edit, alias change, deactivation, restore, new link code and deletion. Two examples: an admin's edit and a staff member's alias change.",
              alt="Two emails to manage@minmed.sg. Card edited: Alex Tan, designation changed by Siti Rahman (Admin), 16 Oct 2026, 10:42 am. Alias changed: Alex Tan, link changed from the plain link to the one with Alex-Tan, by Alex Tan (staff), 16 Oct 2026, 11:05 am. Each has an Open in admin console button.")
        + "</div>"
    )
    return f"""
<section id="pages">
<div class="eyebrow">7</div>
<h2>Pages</h2>
<p>High-fidelity mockups of every page and message. You approved the wording on 16/10/2026, except the preview screen's (open item 2). The “mm” logo stands in for the real one, and the QR codes can't be scanned.</p>
<h3>Public card</h3>
{preview_button()}
<div class="figs">{phone_figs}{desktop}</div>
<h3>Staff</h3>
<div class="figs">{staff_figs}</div>
<h3>My card (staff view)</h3>
{mycard_figs}
<h3>Admin console</h3>
<div class="figs">{admin_figs}</div>
{last_pair}
</section>
"""


def s_bots():
    rule_rows = "".join(
        f'<tr><td><span class="rule-n">Rule {n}</span><br><b>{name}</b></td><td>{counted}</td><td>{limit}</td><td>{then}</td><td>{status}</td></tr>'
        for n, name, counted, limit, then, status in RULES
    )
    flow = f"""
<div class="fc">
  <div class="dg-n"><b>A card is opened, a contact file is requested, or a card address is tried</b></div><div></div><div></div>
  <div class="fc-down"></div><div class="fc-gap"></div>
  <div class="dg-n main"><span class="rule-n">Rules 2, 4</span><br>Browser holds a valid pass?</div><div class="fc-yes"><span>Yes</span></div><div class="dg-n ok"><b>Send the page</b></div>
  <div class="fc-down"><span>No</span></div><div class="fc-gap"></div>
  <div class="dg-n main"><span class="rule-n">Rule 1</span><br>This IP: more than 3 in the last minute?</div><div class="fc-yes"><span>Yes</span></div><div class="dg-n stop"><b>CAPTCHA</b></div>
  <div class="fc-down"><span>No</span></div><div class="fc-gap"></div>
  <div class="dg-n main"><span class="rule-n">Rule 3</span><br>This card: more than 20 in the last 10 minutes?</div><div class="fc-yes"><span>Yes</span></div><div class="dg-n stop"><b>CAPTCHA</b></div>
  <div class="fc-down"><span>No</span></div><div class="fc-gap"></div>
  <div class="dg-n ok"><b>Send the page</b><small>the card, or “No card found”</small></div><div></div><div></div>
</div>"""
    outcome = """
<div class="dg">
  <div class="dg-n stop"><b>CAPTCHA</b><small>Turnstile, Managed mode</small></div>
  <div class="dg-ar"></div>
  <div class="dg-row">
    <div class="dg-n ok"><b>Passed</b><small>most people, without clicking</small>The card is sent. The browser gets a 30-minute pass.</div>
    <div class="dg-n end"><b>Not passed</b><small>or the check can't load</small>No card details are sent. The visitor can try again.</div>
  </div>
</div>"""
    return f"""
<section id="bots">
<div class="eyebrow">8</div>
<h2>Bot protection (CAPTCHA)</h2>
<p>Purpose: slow down bots that copy cards in bulk. Random links and hiding from search stop people finding cards; these rules limit how fast anyone can open them. A CAPTCHA can't stop a person, or a bot that pays a solving service, from copying a card they can already open.</p>
<div class="tablewrap"><table>
<thead><tr><th>Rule</th><th>What's counted</th><th>Limit</th><th>Then</th><th>Status</th></tr></thead>
<tbody>
{rule_rows}
<tr><td><b>Never checked</b></td><td colspan="4">WhatsApp and other link-preview fetches (they only see the preview), the admin console and My card (Google sign-in), and images, styles and scripts.</td></tr>
</tbody></table></div>
<div class="figs two">
{fig("bot-flow", flow, "How each request is checked.",
     "Counting happens on the server, in rolling windows.",
     alt="Decision flow. A request first checks for a valid pass (rules 2 and 4): if yes, send the page. If not, rule 1: more than 3 from this IP in the last minute leads to the CAPTCHA. If not, rule 3: more than 20 for this card in the last 10 minutes leads to the CAPTCHA. Otherwise send the page.")}
{fig("bot-outcome", outcome, "What happens at the CAPTCHA.",
     f"The page is in {fref('pg-captcha')}. A Turnstile token is checked by a backend function; it works once and expires after 5 minutes.",
     alt="CAPTCHA leads to two outcomes: passed, where the card is sent and the browser gets a 30-minute pass; or not passed, where no card details are sent and the visitor can try again.")}
</div>
<h3>Based on industry standards and research</h3>
<p>Each rule follows published guidance from OWASP (a web security nonprofit), Cloudflare and Google.</p>
<div class="tablewrap"><table>
<thead><tr><th>Industry practice</th><th>Source</th><th>Used in</th></tr></thead>
<tbody>
<tr><td>Use a CAPTCHA only as a step-up for suspicious traffic, not as the main defence. None of the sources suggests checking every Nth visitor: that would interrupt 1 in 5 real people, while a bot just tries again.</td><td>OWASP</td><td>Rules 1 and 3, instead of “every 5th visitor”</td></tr>
<tr><td>Limit by more than the IP address. For example, count all requests to one page, whoever sends them.</td><td>OWASP, Cloudflare</td><td>Rule 3</td></tr>
<tr><td>Count in rolling windows, not fixed ones, so bursts can't hide at the edges.</td><td>OWASP</td><td>All rules</td></tr>
<tr><td>A pass lasts 30 minutes by default; 15 to 45 minutes is recommended.</td><td>Cloudflare</td><td>Rule 2</td></tr>
<tr><td>Keep limits in place after a CAPTCHA is passed.</td><td>OWASP</td><td>Rule 4</td></tr>
<tr><td>Against scraping, use two limits per IP: 10 requests in 2 minutes, then 20 in 5 minutes.</td><td>Cloudflare</td><td>Rule 4's limit</td></tr>
<tr><td>Prefer managed checks that only ask a person to click when needed.</td><td>Cloudflare</td><td>Turnstile in Managed mode</td></tr>
<tr><td>Run the checks without acting first, then set the limits from real traffic.</td><td>Google, Cloudflare</td><td>The first 2 weeks record only</td></tr>
</tbody></table></div>
<p class="note">The numbers are starting points. Rule 4's limit matches Cloudflare's example; rule 3's is our estimate for a name card. Both get checked during the record-only weeks.</p>
<ul>
  <li><b>Managed mode:</b> Turnstile decides whether to show a checkbox. Most people never see it, and there are no picture puzzles.</li>
  <li><b>Shared networks:</b> office Wi-Fi, events and mobile data put many people behind one IP address, so they meet rule 1 sooner. So does one person who opens a card, saves it and reloads twice. In Managed mode, most still pass without clicking.</li>
  <li><b>Server-side:</b> the card page asks a backend function for the card. When a check is needed, no card details are sent until Cloudflare confirms the token.</li>
  <li><b>Launch</b> {chip("Confirmed", "dec")}: for the first 2 weeks the rules only record. Compare them with real traffic, then switch them on.</li>
</ul>
<p class="note">Sources: <a href="https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html">OWASP bot management</a>, <a href="https://developers.cloudflare.com/waf/rate-limiting-rules/best-practices/">Cloudflare rate limiting best practices</a>, <a href="https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/challenge-passage/">Cloudflare challenge passage</a>, <a href="https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/">Cloudflare challenge types</a>, <a href="https://developers.google.com/recaptcha/docs/v3">Google reCAPTCHA v3</a>, <a href="https://developers.cloudflare.com/turnstile/concepts/widget/">Turnstile widget modes</a> and <a href="https://developers.cloudflare.com/turnstile/get-started/server-side-validation/">server-side validation</a>.</p>
</section>
"""


def s_links():
    return f"""
<section id="links">
<div class="eyebrow">9</div>
<h2>Links and privacy</h2>
<ul>
  <li><b>Link format:</b> <code>me.minmed.sg/card/{{code}}</code>, or <code>me.minmed.sg/card/{{alias}}/{{code}}</code> once the staff member adds a name or alias. For example <code>{E(LINK)}</code> and <code>{E(M.LINK_ALIAS)}</code>. The code has no name, initials or counting numbers. The <code>/card/</code> prefix keeps clear of Base44's own addresses.</li>
  <li><b>The code</b> {chip("Confirmed", "dec")}: 22 random letters and numbers, made by the server with a secure random generator (CSPRNG) and never reused. That's about 131 bits of randomness, above the 128-bit minimum in the standard below.</li>
  <li><b>The alias:</b> optional and chosen by the staff member: letters, numbers and hyphens, 2 to 30 characters. It adds no security; the code alone keeps the link unguessable. A link with an alias can be found by searching for that alias.</li>
  <li><b>Both parts are checked:</b> the code must belong to a card, and the alias must be the card's current one, or absent when none is set. Anything else shows “No card found” and counts towards rule 1.</li>
  <li><b>The link changes only</b> when the alias is set, changed or cleared, or a Super admin issues a new code. Name and designation edits keep the same link.</li>
  <li><b>An alias change ends the old link:</b> links already sent, printed QR codes and Apple Wallet passes made from it show “No card found”. The Google Wallet pass updates itself and a new card email goes out.</li>
  <li><b>Every public address uses the same random code:</b> the card page, contact file, card image and Google Wallet pass. Never a counting number, so nobody can fetch cards by counting.</li>
  <li><b>Hidden from Google, twice over:</b> no list of cards anywhere (no sitemap entries, no staff directory, the home address redirects to minmed.sg), and every card page, image and contact file tells search engines not to index it. On Base44 that means the page's “Search visibility” switch plus a noindex header on files from backend functions, checked after every publish. Don't block card addresses in robots.txt: Google then can't see the “don't index” instruction and may still list a link someone posted elsewhere.</li>
  <li><b>If a link is misused:</b> a Super admin issues a new code. The old link then shows “No card found”. An admin can also clear an offensive alias.</li>
  <li><b>Bots:</b> see section 8.</li>
</ul>
<h3>Based on industry standards and research</h3>
<div class="tablewrap"><table>
<thead><tr><th>Industry practice</th><th>Source</th><th>Used in</th></tr></thead>
<tbody>
<tr><td>A link that is the only key to a page must be unguessable: a random identifier, never a counting number.</td><td>W3C</td><td>Random code</td></tr>
<tr><td>Random strings meant to be unguessable need a secure random generator and at least 128 bits of randomness. Each bit doubles the number of possible codes.</td><td>OWASP ASVS 5.0</td><td>22 characters</td></tr>
<tr><td>A fixed or predictable part, such as a name or initials, adds no strength.</td><td>OWASP</td><td>The alias adds none; the code alone keeps links unguessable</td></tr>
<tr><td>Researchers scanned every possible 5- and 6-character short-link code. They found shared OneDrive files and Google Maps directions that revealed people's home addresses.</td><td>Georgiev and Shmatikov, 2016</td><td>Long codes; rule 1 counts wrong addresses</td></tr>
</tbody></table></div>
<p class="note">Sources: <a href="https://www.w3.org/TR/capability-urls/">W3C Good Practices for Capability URLs</a> (2014 draft), <a href="https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md">OWASP ASVS 5.0 requirement 11.5.1</a>, <a href="https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html">OWASP session management</a> and <a href="https://arxiv.org/abs/1604.02734">Gone in Six Characters: Short URLs Considered Harmful for Cloud Services</a>.</p>
</section>
"""


def s_failures(n):
    return f"""
<section id="failures">
<div class="eyebrow">{n}</div>
<h2>When things go wrong</h2>
<div class="tablewrap"><table>
<thead><tr><th>Situation</th><th>Visitor sees</th><th>Behind it</th></tr></thead>
<tbody>
<tr><td>Wrong, mistyped or deleted link, or one with an old alias</td><td>“No card found” ({fref("pg-notfound")})</td><td>Counts towards rule 1.</td></tr>
<tr><td>Card deactivated (soft-deleted)</td><td>“This card is no longer active.” ({fref("pg-inactive")})</td><td>The contact file and card image stop at once. The Google Wallet pass shows as expired. The staff member can't sign in to My card.</td></tr>
<tr><td>A staff member changes their alias after sharing their link</td><td>People with the old link see “No card found”</td><td>Expected. My card warned before saving, and the staff member got a new card email.</td></tr>
<tr><td>An alias with other characters or the wrong length</td><td>My card explains the rule; nothing is saved ({fref("pg-mycardflow")})</td><td>The link doesn't change.</td></tr>
<tr><td>A Minmed account with no active card signs in to My card</td><td>“There's no name card for this account.” ({fref("pg-staffsignin")})</td><td>No card details are shown.</td></tr>
<tr><td>Apple Wallet pass of someone who has left</td><td>The pass stays on their phone</td><td>Its QR code opens the “no longer active” page. Minmed can't remove the pass.</td></tr>
<tr><td>Outage, or Base44 credits run out</td><td>Temporary error ({fref("pg-error")})</td><td>No old or cached details are shown.</td></tr>
<tr><td>The CAPTCHA can't load or isn't passed</td><td>The check again, with a way to retry</td><td>No card details are sent until a check passes.</td></tr>
<tr><td>A chat shows an old WhatsApp preview</td><td>The preview from when the link was first shared</td><td>WhatsApp keeps previews it already fetched. Opening the link shows the current card.</td></tr>
</tbody></table></div>
</section>
"""


def s_feasibility():
    def r(cap, status, text):
        return f"<tr><td>{cap}</td><td>{status}</td><td>{text}</td></tr>"

    works = chip("Works", "dec")
    rows = [
        r("Custom domain me.minmed.sg", works,
          "One DNS record pointing to Base44, on the Starter plan or higher. If minmed.sg's DNS is on Cloudflare, the record must be “DNS only”, so Cloudflare's own protection can't sit in front."),
        r("Card address with optional alias", chip("Test", "test"),
          "Base44 keeps addresses at the root for sign-in and system pages, so card links need a prefix: <code>/card/{code}</code> and <code>/card/{alias}/{code}</code>. Two-part addresses aren't documented."),
        r("Hidden from Google", chip("Test", "test"),
          "A per-page “Search visibility” switch (added 28/09/2026) marks pages noindex and removes them from the sitemap. Files served by backend functions can carry their own noindex header. Check what the live site serves after every publish."),
        r("Per-card WhatsApp preview", chip("Not supported as is", "risk"),
          "Base44 sets preview tags per page template, not per card, so every card would share one Minmed preview. Plan below."),
        r("CAPTCHA (Cloudflare Turnstile)", chip("Test", "test"),
          "Free plan: unlimited checks, up to 20 widgets, and no need to route traffic through Cloudflare. The page loads Turnstile (Cloudflare suggests a React component); a backend function verifies each token using a secret key kept in Base44's secrets. Base44's security policy can't be changed per app, so check that Turnstile loads."),
        r("Visitor IP address", chip("Test", "test"),
          "Rule 1 needs the visitor's real IP address inside a backend function. Base44 passes the request headers on, but doesn't document which one holds the visitor's IP. Log the headers on a test app. If none does, rule 1 needs option C's separate host."),
        r("Counting for the CAPTCHA rules", chip("Ours to build", "rec"),
          "Cloudflare can't sit in front of a Base44 domain, so the rules are counted in backend functions with a database table, in rolling windows."),
        r("Contact file and Google Wallet link", chip("Test", "test"),
          "Backend functions can return files of the right type and use code libraries. Their addresses look like <code>me.minmed.sg/functions/contact?code=…</code>, still behind the random code."),
        r("Sign-in limited to minmed.sg (admins and staff)", chip("Works, with setup", "dec"),
          "Needs Minmed's own Google sign-in set to “Internal” (Builder plan or higher). Base44 only has “admin” and “user” roles, so Super admin and Admin are our own list, editable only by Super admins. Staff sign in as ordinary users. Base44's plans don't charge per user."),
        r("Staff limited to their own card and alias", chip("Test", "test"),
          "Base44's row-level rules can limit a signed-in user to the card with their email, and field-level rules can limit which fields they write. Saving goes through a backend function that checks the alias, then updates the link, the Google Wallet pass, the activity log and the emails. Check that the field rule can be tied to the person's own card."),
        r("Soft delete for leavers", works,
          "Base44 records carry a soft-delete flag and date, so a deactivated card can be hidden but kept, and restored by a Super admin."),
        r("Visitors can't list cards", chip("Ours to build", "rec"),
          "A public Base44 app lets anyone register. Visitors must only get one card's public fields, by its code, through a backend function. One wrong rule could expose every card."),
        r("Emails to staff and manage@minmed.sg", chip("Works, with setup", "dec"),
          "Needs a paid plan and a verified sending domain. One recipient per email, about 1–2 credits each."),
        r("View counts", works,
          "Record card openings ourselves; Base44's own analytics keeps 60 days. A view is a card page opening, not a person. Link previews and admin previews don't count."),
        r("Rate limits and credits", chip("Built in", "dec"),
          "Base44 rate-limits public endpoints by default; the limits aren't published or adjustable. Function calls, counting and emails use credits. If credits run out, those actions pause and visitors see the temporary error page. Watch usage."),
        r("Google Wallet", chip("Test", "test"),
          "Free issuer account, but Google must approve publishing (needs a business profile). Passes can be updated and set to expired."),
        r("Apple Wallet", chip("Test", "test"),
          "iOS 27's Create a Pass: from a screenshot of the QR code on iPhone 15 Pro or newer with Apple Intelligence; on other iOS 27 iPhones (iPhone 11 or newer), Create Pass Manually and scan the QR code. No Apple fee. Minmed can't update or remove these passes."),
    ]
    return f"""
<section id="feasibility">
<div class="eyebrow">10</div>
<h2>Feasibility on Base44 and Wallet</h2>
<p>Checked against Base44, Apple, Google and Cloudflare documentation on 16/10/2026. Base44's settings are new and its docs contradict each other in places, so anything marked {chip("Test", "test")} needs trying on a throwaway app before the build starts. The tests are listed in the build notes, a separate file.</p>
<div class="tablewrap"><table>
<thead><tr><th style="width:24%">Capability</th><th style="width:130px">Status</th><th>What it means for the scope</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>

<h3>WhatsApp previews</h3>
<div class="tablewrap"><table>
<thead><tr><th style="width:24%">Option</th><th>What you get</th><th>Cost</th></tr></thead>
<tbody>
<tr><td><b>A. One Minmed preview</b></td><td>Every shared link shows the same preview: Minmed logo and “Minmed digital name card”. Everything stays on Base44.</td><td>Simplest. Drops the spec's per-card preview.</td></tr>
<tr><td><b>B. Card served by a backend function</b></td><td>Per-card preview on Base44, but links look like <code>me.minmed.sg/functions/card?code=…</code>.</td><td>Untested. Uglier links.</td></tr>
<tr><td><b>C. Public card pages on a small separate host</b></td><td>Per-card previews, clean links, and full control of noindex, contact files and the visitor's IP address. The admin console stays on Base44.</td><td>An extra service, its cost, and more build work.</td></tr>
</tbody></table></div>
<p><b>Plan</b> {chip("Confirmed", "dec")}: test option B on a throwaway app first, which takes a day or two. If it doesn't work cleanly, choose C if per-card previews are a must, otherwise A (open item 1).</p>
<p class="note">Sources: Base44 docs on <a href="https://docs.base44.com/Setting-up-your-app/Connecting-an-external-domain">external domains</a>, <a href="https://docs.base44.com/Performance-and-SEO/checking-your-seo-and-geo">search visibility</a>, <a href="https://docs.base44.com/Performance-and-SEO/SEO-and-search-visibility">SEO and sharing</a>, <a href="https://docs.base44.com/developers/backend/resources/backend-functions/overview">backend functions</a>, <a href="https://docs.base44.com/developers/backend/resources/entities/security">data security</a>, <a href="https://docs.base44.com/documentation/building-your-app/sending-emails">sending emails</a>, <a href="https://docs.base44.com/Setting-up-your-app/security-overview">security</a>, <a href="https://docs.base44.com/Community-and-support/Troubleshooting">troubleshooting</a> and <a href="https://docs.base44.com/Account-and-billing/Credits">credits</a>; Apple's <a href="https://support.apple.com/en-sg/guide/iphone/el8l5r9jnhyv/ios">Create passes in Wallet</a>; Google's <a href="https://developers.google.com/wallet/generic/web">Generic pass</a>, <a href="https://developers.google.com/wallet/generic/test-and-go-live/request-publishing-access">publishing access</a> and <a href="https://developers.google.com/wallet/generic/use-cases/expired-passes">expired passes</a>; Cloudflare's <a href="https://developers.cloudflare.com/turnstile/plans/">Turnstile plans</a> and <a href="https://developers.cloudflare.com/turnstile/">Turnstile overview</a>.</p>
</section>
"""


def s_tests(n):
    return f"""
<section id="tests">
<div class="eyebrow">{n}</div>
<h2>Test before the build</h2>
<p>On a throwaway app on a test subdomain, before the build starts.</p>
<ol>
  <li>Open a card link as WhatsApp and as Google's crawler. Check the preview tags, the noindex instruction and the sitemap, then share the link in a real WhatsApp chat.</li>
  <li>Show Turnstile on the card page, verify its token in a backend function, and log the request headers to find the visitor's IP address. Then try rule 1 and the 30-minute pass from one phone, and from two phones on the same Wi-Fi.</li>
  <li>Download a contact file and open the Google Wallet link from a backend function in iPhone Safari, Android Chrome, WhatsApp and Gmail. Add the pass, edit the card and check the pass updates, then deactivate the card and check the pass shows as expired.</li>
  <li>Add a card's QR code to Apple Wallet with Create a Pass on two iPhones: one with Apple Intelligence and one without.</li>
  <li>Check that a non-minmed Google account is refused, an Admin can't make themselves Super admin, a staff member can't open another card or the admin console, and an anonymous visitor can't list cards.</li>
  <li>Sign in to My card as a staff member on a phone. Check they can change only the alias, that Preview changes nothing until they save, that the old link then shows “No card found”, and that the Google Wallet pass updates and a new card email arrives.</li>
  <li>Check that emails reach staff and manage@minmed.sg.</li>
</ol>
</section>
"""


def s_spec(n):
    rm, ch, keep, add = chip("Remove", "out"), chip("Change", "rec"), chip("Keep", "in"), chip("Add", "dec")
    rows = [
        (rm, "Staff creating cards (<code>me.minmed.sg/create</code>); the approval process (pending review, reviewers, rejections, exact-version rule, held applications); approval emails to staff", "§1.2, §3, Fig. 2, §5.1, §5.3, §6.1, §7"),
        (ch, "The staff view becomes a read-only My card page, with one box for a name or alias in the link and a QR code download", "§5, §5.1"),
        (rm, "Signed links; watermark and reference labels", "§4, §4.1, §4.3, §8, §8.1"),
        (rm, "“Active staff profile ✓ Checked [time]” and the How to verify panel", "§4.1, §5.2"),
        (ch, "CAPTCHA options become four set rules (section 8): more than 3 card opens or contact downloads per IP in 1 minute; a busy-card check; a 30-minute pass that ends after 20 opens in 5 minutes; Turnstile checked on the server. Rules record only for the first 2 weeks", "§4.5, §4.6, §8.1"),
        (ch, "Public address from <code>me.minmed.sg/first-last</code> to a random code, with an optional name or alias chosen by the staff member", "§1.2, §4.3"),
        (ch, "Actors table becomes four users with a full permissions matrix", "§3"),
        (ch, "Field rules: “changes require approval” becomes “maintained by admins”; staff change only their alias", "§3.1"),
        (ch, "Monthly email reports become view counts in the admin console", "§6"),
        (ch, "UI: the staff and recipient views become the public card and admin console in section 7", "§5"),
        (ch, "Launch checks: replace ownership and approval checks with admin-only, random-code, CAPTCHA and “don't index” checks", "§9"),
        (keep, "Base44; public card fields and actions; Save contact; WhatsApp preview; deactivation; public-field filtering on the server; search exclusion; admin notifications and audit", "§1.1, §3.2, §4.2, §4.4, §7.1"),
        (add, "Admin console pages; Super admin and Admin roles; spreadsheet import; card email to staff with Google Wallet and Apple Wallet steps, and replies used for change requests; QR code for computer visitors; new link code; soft delete for leavers; offboarding owner and timing; failure handling", "new sections"),
        (add, "The WhatsApp preview approach; the tests to run before the build", "§7.1, new section"),
    ]
    body = "".join(f"<tr><td>{c}</td><td>{w}</td><td>{s}</td></tr>" for c, w, s in rows)
    return f"""
<section id="spec">
<div class="eyebrow">{n}</div>
<h2>What changes in the spec (draft 0.2 to 0.3)</h2>
<div class="tablewrap"><table>
<thead><tr><th style="width:110px">Change</th><th>What</th><th style="width:170px">Spec 0.2 sections</th></tr></thead>
<tbody>
{body}
</tbody></table></div>
</section>
"""


def s_pending():
    return f"""
<section id="pending">
<div class="eyebrow">11</div>
<h2>Open items</h2>
<p>The only open items. Everything else is confirmed.</p>
<ol class="qs">
  <li><b>WhatsApp previews: option A, B or C.</b> {chip("Test", "test")}<span class="def">Plan confirmed: test B first. Then C if per-card previews are a must, otherwise A. Affects {fref("pg-whatsapp")}, section 10 and the file addresses in section 6. Needs the test result.</span></li>
  <li><b>Wording on the preview screen.</b> {chip("Proposed", "rec")}<span class="def">Step 2 of {fref("pg-mycardflow")}: the title Preview, the note “Not saved yet. This is how your card will look at your new link.”, the new link shown above the card, and Back and Save link buttons. The Preview button sits next to Save link ({fref("pg-mycard")}, {fref("pg-mycarddesk")}). Needs your OK.</span></li>
</ol>
</section>
"""


def foot():
    return f"""
<div class="footer">
  <p><b>Sources.</b> Minmed Digital Name Cards Technical Specification draft 0.2 (15/10/2026). Your decisions in this conversation on 16/10/2026. Standards, research, platform and vendor documentation linked in sections 8, 9 and 10.</p>
</div>
</main>
{preview_dialog()}
<script>
document.documentElement.classList.add("js");
function fitShots() {{
  document.querySelectorAll(".shot").forEach(function (s) {{
    var c = s.firstElementChild;
    if (!c) return;
    c.style.zoom = "";
    if (s.classList.contains("zoomed")) {{ s.classList.remove("fit"); return; }}
    var need = c.scrollWidth, have = s.clientWidth - 4;
    if (need > have + 1) {{ c.style.zoom = (have / need).toFixed(4); s.classList.add("fit"); }}
    else {{ s.classList.remove("fit"); }}
  }});
}}
document.addEventListener("click", function (e) {{
  var s = e.target.closest && e.target.closest(".shot");
  if (!s || !(s.classList.contains("fit") || s.classList.contains("zoomed"))) return;
  s.classList.toggle("zoomed");
  fitShots();
}});
window.addEventListener("resize", fitShots);
window.addEventListener("load", fitShots);
fitShots();
document.addEventListener("click", function (e) {{
  var b = e.target.closest && e.target.closest("[data-preview]");
  if (b) {{
    var d = document.getElementById(b.getAttribute("data-preview"));
    if (d && d.showModal) d.showModal();
    else if (d) d.setAttribute("open", "");
    return;
  }}
  if (e.target.classList && e.target.classList.contains("pvd")) e.target.close();
}});
document.addEventListener("click", function (e) {{
  var a = e.target.closest && e.target.closest('a[href^="#"]');
  if (!a) return;
  var id = decodeURIComponent(a.getAttribute("href").slice(1));
  var el = id && document.getElementById(id);
  if (!el) return;
  e.preventDefault();
  el.scrollIntoView({{ behavior: "smooth", block: "start" }});
  if (/^(https?|file|blob):$/.test(location.protocol)) {{
    try {{ history.replaceState(null, "", "#" + id); }} catch (err) {{}}
  }}
}});
</script>
</body>
</html>
"""


TABLE_RE = re.compile(r'(<div class="tablewrap"><table[^>]*>)(.*?)(</table></div>)', re.S)


def label_cells(doc):
    """Adds data-label (the column heading) to each data cell, so tables can stack on phones."""
    def table(m):
        start, inner, end = m.groups()
        head = re.search(r"<thead>(.*?)</thead>", inner, re.S)
        if not head:
            return m.group(0)
        labels = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", head.group(1), re.S)]

        def row(rm):
            col = 0

            def cell(cm):
                nonlocal col
                tag, attrs = cm.groups()
                span = re.search(r'colspan="(\d+)"', attrs)
                width = int(span.group(1)) if span else 1
                label = labels[col] if col < len(labels) and width == 1 else ""
                col += width
                if tag == "td" and label:
                    return f'<td{attrs} data-label="{html.escape(label)}">'
                return cm.group(0)

            return re.sub(r"<(td|th)(\b[^>]*)>", cell, rm.group(0))

        body = inner[head.end():]
        body = re.sub(r"<tr[^>]*>.*?</tr>", row, body, flags=re.S)
        return start + inner[:head.end()] + body + end

    return TABLE_RE.sub(table, doc)


def build():
    parts = [
        head(), intro(), s_how(), s_confirmed(), s_features(), s_users(), s_matrix(), s_map(), s_pages(),
        s_bots(), s_links(), s_feasibility(), s_pending(), foot(),
    ]
    doc = label_cells("".join(parts))
    assert USED == FIG_ORDER, f"figure order mismatch:\n{USED}\n{FIG_ORDER}"
    assert "zapkad" not in doc.lower(), "Zapkad must not appear in the scope"
    OUT.write_text(doc)
    print(f"wrote {OUT} ({len(doc):,} bytes, {len(USED)} figures)")
    PV.write()
    notes()


NOTES_OUT = SRC.parent / "minmed-name-card-build-notes.html"


def notes():
    """Build notes moved out of the scope. Figure links become plain text, as the figures are in the scope."""
    doc = f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="description" content="Build notes for Minmed Digital Name Cards: what happens when things go wrong, the tests to run before the build, and what changes in the technical specification.">
<title>Name Card Build Notes</title>
{PV.FONTS}
<style>
{(SRC / "scope.css").read_text()}
</style>
</head>
<body>
<header class="top"><div class="top-inner">
  <div class="brand">{mark(28)}<span>Name Card Build Notes</span></div>
  <nav class="toc" aria-label="Sections">
    <a href="#failures">When things go wrong</a><a href="#tests">Tests</a><a href="#spec">Spec changes</a>
  </nav>
</div></header>
<main>
<div class="eyebrow">Build notes · go with the product scope</div>
<h1>Minmed Digital Name Cards: build notes</h1>
<p class="lede">Moved out of the product scope on 16/10/2026: what happens when things go wrong, the tests to run before the build, and what changes in the technical specification.</p>
<p class="meta">Figure, section and rule numbers refer to the product scope. Updated 16/10/2026.</p>
{s_failures(1)}{s_tests(2)}{s_spec(3)}
<div class="footer">
  <p><b>Sources.</b> Minmed Digital Name Cards Technical Specification draft 0.2 (15/10/2026). Your decisions in this conversation on 16/10/2026.</p>
</div>
</main>
</body>
</html>
"""
    doc = label_cells(doc)
    doc = re.sub(r'<a href="#[\w-]+">(Figure \d+)</a>', r"\1", doc)
    assert 'href="#pg-' not in doc and "zapkad" not in doc.lower()
    NOTES_OUT.write_text(doc)
    print(f"wrote {NOTES_OUT} ({len(doc):,} bytes)")


if __name__ == "__main__":
    build()
