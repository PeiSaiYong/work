"""Builds ../minmed-name-card-scope.html, a single self-contained file.

Run: python3 build.py
"""

from pathlib import Path

import mocks as M
from mocks import E, LINK, chip, mark, thumb

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "minmed-name-card-scope.html"

# Figures are numbered in this order; build() checks the document uses the same order.
FIG_ORDER = [
    "overview", "sitemap", "nav", "journey",
    "pg-card", "pg-captcha", "pg-inactive", "pg-notfound", "pg-error", "pg-whatsapp", "pg-desktop",
    "pg-email", "pg-gpass", "pg-apass",
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
</style>
</head>
<body>
<header class="top"><div class="top-inner">
  <div class="brand">{mark(28)}<span>Name Card Scope</span></div>
  <nav class="toc" aria-label="Sections">
    <a href="#how">How it works</a><a href="#confirmed">Confirmed</a><a href="#features">Features</a><a href="#users">Users</a><a href="#matrix">Permissions</a><a href="#map">Site map</a><a href="#pages">Pages</a><a href="#bots">Bot protection</a><a href="#links">Links &amp; privacy</a><a href="#failures">Failures</a><a href="#feasibility">Feasibility</a><a href="#benchmark">Other platforms</a><a href="#spec">Spec changes</a><a href="#pending">Pending</a>
  </nav>
</div></header>
<main>
"""


def intro():
    return f"""
<div class="eyebrow">Product scope · input to spec 0.3</div>
<h1>Minmed Digital Name Cards</h1>
<p class="lede">A digital name card for every Minmed staff member, managed centrally. Admins create and change every card. Staff never sign in. Anyone with a card's link can open it, but nobody can find it on Google.</p>
<p class="meta">Based on Technical Specification draft 0.2 (15/10/2026) and your decisions on 16/10/2026. Names, numbers, codes and QR codes in the examples are made up. Updated 16/10/2026.</p>
<div class="legend">
  <span>{chip("Confirmed", "dec")} you decided it</span>
  <span>{chip("Proposed", "rec")} my recommendation, waiting for your OK</span>
  <span>{chip("Test", "test")} try on a test app before the build</span>
  <span>{chip("Pending confirmation", "pend")} still to decide (section 14)</span>
</div>
"""


def s_how():
    steps = [
        ("Admin adds the card", "In the admin console, one at a time or from a spreadsheet."),
        ("Staff member gets an email", "Their link and QR code, an Add to Google Wallet button, and steps for Apple Wallet."),
        ("Staff member shares it", "Sends the link on WhatsApp or email, or shows the QR code from Wallet."),
        ("Visitor opens the link", "Sees the card, then saves the contact, emails, calls or WhatsApps. Unusual traffic gets a CAPTCHA."),
        ("Details change", "The staff member replies to the card email. An admin edits the card, and the same link shows the new details."),
        ("Staff member leaves", "HR tells an admin. On the last day the card is deactivated and the link shows “This card is no longer active.”"),
    ]
    boxes = "".join(f"<div><b>{t}</b>{d}</div>" for t, d in steps)
    return f"""
<section id="how">
<div class="eyebrow">1</div>
<h2>How it works</h2>
{fig("overview", f'<div class="flow">{boxes}</div>', "The life of a card, from creation to deactivation.",
     alt="Six numbered steps: admin adds the card; staff member gets an email; staff member shares it; visitor opens the link; details change; staff member leaves.", wide=True)}
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
        row("One central place to manage every staff card. Staff can't edit their own card, so there's no approval process.", you),
        row("Cards are public to anyone with the link, but can't be found through Google.", you),
        row(f"Each link has the person's name and a random code: <code>{E(LINK)}</code>.", you),
        row("Staff never sign in. They keep their link on their phone, or in Apple Wallet or Google Wallet.", you),
        row("Built on Base44. Phone-first public card. Admins sign in with company Google accounts.", "Spec 0.2 §1.1"),
        grp("The card"),
        row("Fields: name, designation, Minmed, work email, optional mobile and photo, optional biography, languages and LinkedIn. Company information is a link to minmed.sg; no social links.", "Spec 0.2 §3.1; you, 16/10"),
        row("Actions: Save contact and Email, plus Call and WhatsApp when a mobile is published. No visitor app.", "Spec 0.2 §1.1; you, 16/10"),
        row("On a computer, the card also shows a QR code to move it to a phone.", you),
        row("No “Active staff profile ✓ Checked” line and no How to verify panel.", you),
        row("Sharing the link on WhatsApp shows a preview of the card.", "Spec 0.2 §4.4",
            chip("At risk", "risk") + ' <span class="note">Base44 can\'t make a per-card preview as is. See section 11 and pending item 1.</span>'),
        grp("Wallet"),
        row("Minmed issues a Google Wallet pass. iPhone staff add their QR code to Apple Wallet themselves with iOS 27's Create a Pass. No Apple Developer Program, fee or D-U-N-S number.", you),
        grp("Admins"),
        row("Two roles: Super admin and Admin.", you),
        row("Only a Super admin can reactivate a card, give it a new link code or delete it.", you),
        row("Cards can be imported from a spreadsheet at launch.", you),
        row("Admins see view counts. No monthly report emails.", you),
        row("Every admin change is logged and emailed to manage@minmed.sg.", "Spec 0.2 §1.1"),
        grp("Leavers and records"),
        row("HR tells an admin as part of offboarding. The card is deactivated on the person's last day.", you),
        row("Deactivated cards are kept and deleted on request.", you,
            chip("Pending confirmation", "pend") + ' <span class="note">Retention period, pending item 2.</span>'),
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
<div class="tablewrap"><table>
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
  <div><h3>Staff</h3><div class="host">no sign-in</div><ul>
    <li>Card email with link, QR code and Wallet options</li>
    <li>Google Wallet pass that updates itself</li>
    <li>Apple Wallet pass they make themselves</li>
    <li>Ask for changes by replying to the card email</li>
  </ul></div>
  <div><h3>Admin console</h3><div class="host">me.minmed.sg/admin</div><ul>
    <li>Google sign-in, admin list only</li>
    <li>Cards: list, search, add, import, edit</li>
    <li>Card details: link, QR code, card image, views, history</li>
    <li>Deactivate; Super admin also reactivates, re-codes and deletes</li>
    <li>Activity log</li>
    <li>Admins and Settings (Super admin)</li>
    <li>Email to manage@minmed.sg on every change</li>
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
<tr><td><b>Staff member</b> (card holder)</td><td>No</td><td>Minmed staff with a card.</td><td>Gets their card by email, keeps it in Wallet or on their phone, shares it. Asks an admin for changes.</td></tr>
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
        r("Change their own details", N, N, N, N),
        r("Ask for a change by replying to the card email", N, O, N, N),
        g("Admin console"),
        r("Sign in to the admin console", N, N, Y, Y),
        r("See and search all cards", N, N, Y, Y),
        r("Add a card", N, N, Y, Y),
        r("Import cards from a spreadsheet", N, N, Y, Y),
        r("Edit a card's details and photo, and choose whether the mobile is shown", N, N, Y, Y),
        r("Send or re-send the card email", N, N, Y, Y),
        r("Download a card's QR code and card image", N, N, Y, Y),
        r("Deactivate a card", N, N, Y, Y),
        r("Reactivate a card", N, N, N, Y),
        r("Issue a new link code (the old link stops working)", N, N, N, Y),
        r("Delete a card permanently", N, N, N, Y),
        r("See view counts", N, N, Y, Y),
        r("See the activity log", N, N, Y, Y),
        r("Add or remove admins and change roles", N, N, N, Y),
        r("Change the card design, company details, notifications and Google Wallet settings", N, N, N, Y),
        g("Automatic"),
        auto("Record every admin action in the activity log"),
        auto("Email manage@minmed.sg when a card is added, edited, deactivated, reactivated, re-coded or deleted"),
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
    c = f"<code>{E(code)}</code>" if code else ""
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
<div class="smz"><div class="smz-h"><b>Public</b><code>me.minmed.sg</code><span>No sign-in · hidden from search engines · no menu</span></div>
<ul class="smt">
  <li>{node("pg-card", tp(M.card_body()), "Card page", code="/card/{Name}/{code}")}
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

    admin = f"""
<div class="smz"><div class="smz-h"><b>Admin console</b><code>me.minmed.sg/admin</code><span>Company Google sign-in · admin list only</span></div>
<ul class="smt">
  <li>{node("pg-signin", tw(M.ad_signin()), "Sign in", code="/admin")}</li>
  <li>{node("pg-cards", tw(M.ad_cards()), "Cards", code="/admin/cards")}
    <ul class="smt">
      <li>{node("pg-add", tw(M.ad_add()), "Add card", code="/admin/cards/new")}</li>
      <li>{node("pg-import", tw(M.ad_import()), "Import cards", code="/admin/cards/import")}</li>
      <li>{node("pg-details", tw(M.ad_details()), "Card details", code="/admin/cards/{id}")}
        <ul class="smt">
          <li>{node("pg-edit", tw(M.ad_edit()), "Edit card", code="/admin/cards/{id}/edit")}</li>
          <li>{node("pg-dialogs", "", "Confirm dialogs", "deactivate, new link code, delete")}</li>
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
<div class="smz"><div class="smz-h"><b>Emails, Wallet and sharing</b><code>outside the website</code><span>How cards reach staff, admins and visitors</span></div>
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
<p>Three parts: the public card, the admin console, and the emails and passes that connect them. Select a page to see its mockup in section 7.</p>
{fig("sitemap", f'<div class="smap">{public}{admin}{msgs}</div>', "Site map. Each entry is a page or message, with its address.", wide=True, img=False)}
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
            f"<code>{E(LINK)}</code> · anyone with the link. Call and WhatsApp only with a published mobile; About only when filled in.",
            alt="Phone showing Alex Tan's card: photo initials, name, designation, Minmed, Save contact button, Email, Call and WhatsApp buttons, work email, mobile, About with biography, languages and LinkedIn, and an About Minmed link.")
        + fig("pg-captcha", M.phone(M.captcha_page()), "CAPTCHA check.",
              "Same address, shown instead of the card when a rule in section 8 is met. Most people pass without clicking; this is what a flagged visitor sees.",
              alt="Phone showing a Quick check page with a Cloudflare Turnstile checkbox labelled Verify you are human.")
        + fig("pg-inactive", M.phone(M.inactive_page()), "No longer active.",
              "Same address after deactivation. No details, photo, Save contact or contact buttons.",
              alt="Phone showing: This card is no longer active, and an About Minmed link.")
        + fig("pg-notfound", M.phone(M.notfound_page()), "Card not found.",
              "Any wrong code, deleted card or mistyped link. The same answer every time, so nobody learns which codes exist.",
              alt="Phone showing: No card found at this address. Check the link or visit minmed.sg.")
        + fig("pg-error", M.phone(M.error_page()), "Temporary error.",
              "The card can't be checked, for example during an outage or when Base44 credits run out. Never shows old details.",
              alt="Phone showing: Can't load this card right now. Please try again in a few minutes, with a Try again button.")
        + fig("pg-whatsapp",
              '<div><span class="variant">Per-card preview · options B, C</span>' + M.wa_chat("card") + "</div>"
              + '<div><span class="variant">Same for every card · option A</span>' + M.wa_chat("generic") + "</div>",
              "WhatsApp link preview. " + chip("Pending confirmation", "pend"),
              "Which one depends on the WhatsApp test (pending item 1).",
              alt="Two WhatsApp messages with link previews: one shows Alex Tan's card image and name; the other shows the Minmed logo and Minmed digital name card.")
    )
    desktop = fig("pg-desktop", shot(M.browser(LINK, M.card_desktop())), "Card page on a computer.",
                  "The same card in a narrow column, plus a QR code to move it to a phone.",
                  alt="Browser window showing the card in a centred column and a QR code panel: Scan to save to your phone.", wide=True)

    staff_figs = (
        fig("pg-email", M.email_card(), "Card email to the staff member.",
            "Sent when an admin chooses Save and send card email, or Send card email. Replies go to manage@minmed.sg.",
            alt="Email: Your Minmed digital name card. Open my card button, link, QR code, Add to Google Wallet button, three iPhone steps for Create a Pass, and Need a change? Reply to this email.")
        + fig("pg-gpass", M.gwallet_pass(), "Google Wallet pass.",
              "Issued by Minmed. Updates when the card changes and shows as expired when it's deactivated.",
              alt="Plum Google Wallet pass with the Minmed logo, designation, name, work email and a QR code.")
        + fig("pg-apass", M.apple_pass(), "Apple Wallet pass, made by the staff member.",
              "Made with iOS 27's Create a Pass, so its look may vary. Minmed can't update or remove it, but its QR code always opens the live card.",
              alt="Dark Apple Wallet pass named Minmed name card with the name Alex Tan and a QR code.")
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
              "<code>/admin/cards</code>. Search by name or email, filter by status. Views count card page openings in the last 30 days.",
              alt="Admin Cards page: search box, All/Active/Inactive filter, Import and Add card buttons, and a table of five cards with designation, status, views and last updated.", wide=True)
        + fig("pg-add", admin_shot("/admin/cards/new", M.ad_add()), "Add card.",
              "<code>/admin/cards/new</code>. Work email must end with @minmed.sg. The mobile shows on the card only when switched on.",
              alt="Add card form with first and last name, designation, work email, mobile with Show on card switch, photo upload, biography, languages, LinkedIn, and an empty preview. Buttons: Cancel, Save, Save and send card email.", wide=True)
        + fig("pg-import", admin_shot("/admin/cards/import", M.ad_import()), "Import cards.",
              "<code>/admin/cards/import</code>. Rows with problems are skipped until fixed. The card emails can go out in the same step.",
              alt="Import cards page at the Check step: 43 rows, 41 ready, 2 need fixing, with two rows flagged. Send card emails now is ticked; Create 41 cards button.", wide=True)
        + fig("pg-details", admin_shot("/admin/cards/AT29", M.ad_details()), "Card details.",
              "<code>/admin/cards/{id}</code>. The ⋯ menu (New link code, Delete card) appears only for Super admins. On an inactive card, Reactivate replaces Deactivate.",
              alt="Card details for Alex Tan: Edit, Send card email, Deactivate and an open menu with New link code and Delete card. Panels for live card preview, link with Copy, QR code and card image downloads, Google Wallet pass Active, 48 views, and history.", wide=True)
        + fig("pg-edit", admin_shot("/admin/cards/AT29/edit", M.ad_edit()), "Edit card.",
              "<code>/admin/cards/{id}/edit</code>. Saving changes the live card at once, on the same link and QR code, and emails manage@minmed.sg.",
              alt="Edit card form with the designation changed to Senior Corporate Sales Manager and highlighted, a preview showing the new designation, and the note Same link and QR code.", wide=True)
        + fig("pg-dialogs", M.ad_dialogs(), "Confirm dialogs.",
              "Deactivate is for Admins and Super admins. New link code and Delete are for Super admins only.",
              alt="Three dialogs: Deactivate Alex Tan's card; Give Alex Tan's card a new link, with Send Alex the new card email ticked; Delete Alex Tan's card permanently.", wide=True)
        + fig("pg-activity", admin_shot("/admin/activity", M.ad_activity()), "Activity log.",
              "<code>/admin/activity</code>. Every admin action: who, what, which card and when.",
              alt="Activity log with filters for card, admin and action, and six entries such as Edited, Deactivated, New link code and Imported.", wide=True)
        + fig("pg-admins", admin_shot("/admin/admins", M.ad_admins()), "Admins (Super admin only).",
              "<code>/admin/admins</code>. Admins are added by company email.",
              alt="Admins page listing four admins with role selectors and Remove links, plus a row to add an admin by email and role.", wide=True)
        + fig("pg-settings", admin_shot("/admin/settings", M.ad_settings()), "Settings (Super admin only).",
              "<code>/admin/settings</code>. Card design, company details, notifications and Google Wallet.",
              alt="Settings page with sections for card design (logo and brand colours with a card preview), company details, notifications to manage@minmed.sg and Google Wallet status.", wide=True)
    )
    last_pair = (
        '<div class="figs two">'
        + fig("pg-adminphone", M.phone(M.ad_mobile_cards(), url="me.minmed.sg/admin/cards"), "Admin console on a phone.",
              "The same Cards page on a phone: the table becomes a list.",
              alt="Phone showing the admin Cards list with search, Add card and four cards with their status.")
        + fig("pg-notify", M.email_admin(), "Admin notification.",
              "Sent to manage@minmed.sg for every add, edit, deactivation, reactivation, new link code and deletion.",
              alt="Email: Card edited: Alex Tan. Designation changed, by Siti Rahman (Admin), 16 Oct 2026, 10:42 am, with an Open in admin console button.")
        + "</div>"
    )
    return f"""
<section id="pages">
<div class="eyebrow">7</div>
<h2>Pages</h2>
<p>High-fidelity mockups of every page and message. Wording you confirmed: “This card is no longer active.” and “Please sign in with your Minmed registered email address.” “No card found at this address. Check the link or visit minmed.sg.” comes from spec 0.2. All other wording is Proposed. The “mm” logo stands in for the real one, and the QR codes can't be scanned.</p>
<h3>Public card</h3>
<div class="figs">{phone_figs}{desktop}</div>
<h3>Staff</h3>
<div class="figs">{staff_figs}</div>
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
<tr><td><b>Never checked</b></td><td colspan="4">WhatsApp and other link-preview fetches (they only see the preview), the admin console (Google sign-in), and images, styles and scripts.</td></tr>
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
  <li><b>Link format:</b> <code>me.minmed.sg/card/{{FirstLast}}/{{code}}</code>, for example <code>{E(LINK)}</code>. The code is random, at least 10 letters and numbers, made by the server and never reused. The <code>/card/</code> prefix keeps clear of Base44's own addresses.</li>
  <li><b>The name part is only for people:</b> the server finds the card by its code alone. If someone's name changes, old links and printed QR codes keep working.</li>
  <li><b>Every public address uses the same random code:</b> the card page, contact file, card image and Google Wallet pass. Never a counting number, so nobody can fetch cards by counting.</li>
  <li><b>Hidden from Google, twice over:</b> no list of cards anywhere (no sitemap entries, no staff directory, the home address redirects to minmed.sg), and every card page, image and contact file tells search engines not to index it. On Base44 that means the page's “Search visibility” switch plus a noindex header on files from backend functions, checked after every publish. Don't block card addresses in robots.txt: Google then can't see the “don't index” instruction and may still list a link someone posted elsewhere.</li>
  <li><b>If a link is misused:</b> a Super admin issues a new code. The old link then shows “No card found”.</li>
  <li><b>Bots:</b> see section 8.</li>
</ul>
</section>
"""


def s_failures():
    return f"""
<section id="failures">
<div class="eyebrow">10</div>
<h2>When things go wrong</h2>
<div class="tablewrap"><table>
<thead><tr><th>Situation</th><th>Visitor sees</th><th>Behind it</th></tr></thead>
<tbody>
<tr><td>Wrong, mistyped or deleted link</td><td>“No card found” ({fref("pg-notfound")})</td><td>Counts towards rule 1.</td></tr>
<tr><td>Card deactivated</td><td>“This card is no longer active.” ({fref("pg-inactive")})</td><td>The contact file and card image stop at once. The Google Wallet pass shows as expired.</td></tr>
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
        r("Card address with name and code", chip("Test", "test"),
          f"Base44 keeps addresses at the root for sign-in and system pages, so card links need a prefix: <code>{E(LINK)}</code>. Not documented."),
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
        r("Admin sign-in limited to minmed.sg", chip("Works, with setup", "dec"),
          "Needs Minmed's own Google sign-in set to “Internal” (Builder plan or higher). Base44 only has “admin” and “user” roles, so Super admin and Admin are our own list, editable only by Super admins."),
        r("Visitors can't list cards", chip("Ours to build", "rec"),
          "A public Base44 app lets anyone register. Visitors must only get one card's public fields, by its code, through a backend function. One wrong rule could expose every card."),
        r("Emails to staff and manage@minmed.sg", chip("Works, with setup", "dec"),
          "Needs a paid plan and a verified sending domain. One recipient per email, about 1–2 credits each."),
        r("View counts", works,
          "Record card openings ourselves; Base44's own analytics keeps 60 days. A view is a card page opening, not a person. Link previews and admin previews don't count."),
        r("Rate limits and credits", chip("Built in", "dec"),
          "Base44 rate-limits public endpoints by default; the limits aren't published or adjustable. Function calls, counting and emails use credits. If credits run out, those actions pause and visitors see the temporary error page. Watch usage."),
        r("Google Wallet", works,
          "Free issuer account, but Google must approve publishing (needs a business profile). Passes can be updated and set to expired."),
        r("Apple Wallet", chip("Works, staff-made", "dec"),
          "iOS 27's Create a Pass: from a screenshot of the QR code on iPhone 15 Pro or newer with Apple Intelligence; on other iOS 27 iPhones (iPhone 11 or newer), Create Pass Manually and scan the QR code. No Apple fee. Minmed can't update or remove these passes."),
    ]
    return f"""
<section id="feasibility">
<div class="eyebrow">11</div>
<h2>Feasibility on Base44 and Wallet</h2>
<p>Checked against Base44, Apple, Google and Cloudflare documentation on 16/10/2026. Base44's settings are new and its docs contradict each other in places, so anything marked {chip("Test", "test")} needs trying on a throwaway app before the build starts.</p>
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
<p><b>Plan</b> {chip("Confirmed", "dec")}: test option B on a throwaway app first, which takes a day or two. If it doesn't work cleanly, choose C if per-card previews are a must, otherwise A (pending item 1).</p>

<h3>Test before the build (throwaway app on a test subdomain)</h3>
<ol>
  <li>Open a card link as WhatsApp and as Google's crawler. Check the preview tags, the noindex instruction and the sitemap, then share the link in a real WhatsApp chat.</li>
  <li>Show Turnstile on the card page, verify its token in a backend function, and log the request headers to find the visitor's IP address. Then try rule 1 and the 30-minute pass from one phone, and from two phones on the same Wi-Fi.</li>
  <li>Download a contact file and open the Google Wallet link from a backend function in iPhone Safari, Android Chrome, WhatsApp and Gmail.</li>
  <li>Add a card's QR code to Apple Wallet with Create a Pass on two iPhones: one with Apple Intelligence and one without.</li>
  <li>Check that a non-minmed Google account is refused, an Admin can't make themselves Super admin, and an anonymous visitor can't list cards.</li>
  <li>Check that emails reach staff and manage@minmed.sg.</li>
</ol>

<h3>Accounts and costs to arrange</h3>
<ul>
  <li>Base44 Builder plan or higher (own Google sign-in, backend functions, workflows), plus credits.</li>
  <li>A verified email sending domain, set up by IT.</li>
  <li>Google Wallet issuer account with a business profile (free, needs Google's approval).</li>
  <li>Cloudflare account for Turnstile (free plan).</li>
  <li>Option C only: hosting for the public card pages.</li>
</ul>
<p class="note">Sources: Base44 docs on <a href="https://docs.base44.com/Setting-up-your-app/Connecting-an-external-domain">external domains</a>, <a href="https://docs.base44.com/Performance-and-SEO/checking-your-seo-and-geo">search visibility</a>, <a href="https://docs.base44.com/Performance-and-SEO/SEO-and-search-visibility">SEO and sharing</a>, <a href="https://docs.base44.com/developers/backend/resources/backend-functions/overview">backend functions</a>, <a href="https://docs.base44.com/developers/backend/resources/entities/security">data security</a>, <a href="https://docs.base44.com/documentation/building-your-app/sending-emails">sending emails</a>, <a href="https://docs.base44.com/Setting-up-your-app/security-overview">security</a>, <a href="https://docs.base44.com/Community-and-support/Troubleshooting">troubleshooting</a> and <a href="https://docs.base44.com/Account-and-billing/Credits">credits</a>; Apple's <a href="https://support.apple.com/en-sg/guide/iphone/el8l5r9jnhyv/ios">Create passes in Wallet</a>; Google's <a href="https://developers.google.com/wallet/generic/web">Generic pass</a>, <a href="https://developers.google.com/wallet/generic/test-and-go-live/request-publishing-access">publishing access</a> and <a href="https://developers.google.com/wallet/generic/use-cases/expired-passes">expired passes</a>; Cloudflare's <a href="https://developers.cloudflare.com/turnstile/plans/">Turnstile plans</a> and <a href="https://developers.cloudflare.com/turnstile/">Turnstile overview</a>.</p>
</section>
"""


def s_benchmark():
    return """
<section id="benchmark">
<div class="eyebrow">12</div>
<h2>Checked against other platforms</h2>
<p>How five company card platforms handle the admin side, taken from their public help pages. Those pages were read through search results, some are a few years old, and “Unclear” means nothing was documented.</p>
<div class="tablewrap"><table>
<thead><tr><th>Capability</th><th>Blinq</th><th>HiHello</th><th>Popl</th><th>Uniqode</th><th>Mobilo</th><th>Minmed plan</th></tr></thead>
<tbody>
<tr><td>Roles</td><td>Owner, Admin, Member</td><td>Owner, Admin, Member</td><td>Admin, Subteam admin, Member</td><td>Owner, Admin, Editor, Viewer</td><td>Super admin, Group admin, Member</td><td><b>Super admin, Admin</b></td></tr>
<tr><td>Admins create staff cards</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td><b>Yes</b></td></tr>
<tr><td>Staff must log in</td><td>Yes</td><td>Yes</td><td>Yes, except Company Pages</td><td>No</td><td>No</td><td><b>No</b></td></tr>
<tr><td>Wallet pass</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes, emailed to staff</td><td>Yes, emailed to staff</td><td><b>Google pass emailed; iPhone staff make their own</b></td></tr>
<tr><td>Import from a spreadsheet</td><td>Yes</td><td>Unclear</td><td>Yes</td><td>Yes</td><td>Yes</td><td><b>Yes</b></td></tr>
<tr><td>When someone leaves</td><td>Deactivate, keep record, reactivate on rehire</td><td>Pause</td><td>Remove or delete</td><td>Delete</td><td>Release or reassign</td><td><b>Deactivate, keep record, Super admin reactivates</b></td></tr>
<tr><td>Usage analytics</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td><b>View counts</b></td></tr>
<tr><td>Admin activity log</td><td>Unclear</td><td>Unclear</td><td>Unclear</td><td>Partly</td><td>Unclear</td><td><b>Yes</b></td></tr>
<tr><td>Hidden from search engines</td><td>Unclear</td><td>Only cards set to private</td><td>Unclear</td><td>Unclear</td><td>Unclear</td><td><b>Always</b></td></tr>
</tbody></table></div>
<h3>Patterns this scope copies</h3>
<ul>
  <li><b>No staff logins, Wallet pass by email</b> (Uniqode, Mobilo): the card email with a Google Wallet button.</li>
  <li><b>Deactivate and keep the record</b> (Blinq): a rehired person gets their old card back.</li>
  <li><b>Stable link and QR code, live content</b> (Blinq, Uniqode): edits never break shared links or printed QR codes.</li>
  <li><b>Spreadsheet import</b> (four of five): for loading every staff member at launch.</li>
  <li><b>Our own page for a departed card:</b> no platform documents what visitors see, so the scope defines it.</li>
  <li><b>An activity log and “don't index”:</b> platforms barely document them, so the scope makes both explicit requirements.</li>
</ul>
<p class="note">Sources: vendor help centres, including <a href="https://support.blinq.me/en/articles/73643-business-admin-onboarding-guide">Blinq admin onboarding</a>, <a href="https://support.hihello.com/hc/en-us/articles/14720204063771-Account-Roles">HiHello roles</a>, <a href="https://support.popl.co/en/articles/9142485-admin-subteam-admin-and-member-roles">Popl roles</a>, <a href="https://docs.uniqode.com/en/articles/7901549-create-apple-wallet-pass-for-your-digital-business-cards">Uniqode Wallet passes</a> and <a href="https://www.mobilocard.com/support-articles/new-admin-features-for-teams">Mobilo admin features</a>.</p>
</section>
"""


def s_spec():
    rm, ch, keep, add = chip("Remove", "out"), chip("Change", "rec"), chip("Keep", "in"), chip("Add", "dec")
    rows = [
        (rm, "Staff sign-in and the staff view; staff creating cards (<code>me.minmed.sg/create</code>); the approval process (pending review, reviewers, rejections, exact-version rule, held applications); approval emails to staff", "§1.2, §3, Fig. 2, §5.1, §5.3, §6.1, §7"),
        (rm, "Signed links; watermark and reference labels", "§4, §4.1, §4.3, §8, §8.1"),
        (rm, "“Active staff profile ✓ Checked [time]” and the How to verify panel", "§4.1, §5.2"),
        (ch, "CAPTCHA options become four set rules (section 8): more than 3 card opens or contact downloads per IP in 1 minute; a busy-card check; a 30-minute pass that ends after 20 opens in 5 minutes; Turnstile checked on the server. Rules record only for the first 2 weeks", "§4.5, §4.6, §8.1"),
        (ch, "Public address from <code>me.minmed.sg/first-last</code> to name plus random code", "§1.2, §4.3"),
        (ch, "Actors table becomes four users with a full permissions matrix", "§3"),
        (ch, "Field rules: “changes require approval” becomes “maintained by admins”", "§3.1"),
        (ch, "Monthly email reports become view counts in the admin console", "§6"),
        (ch, "UI: the staff and recipient views become the public card and admin console in section 7", "§5"),
        (ch, "Launch checks: replace ownership and approval checks with admin-only, random-code, CAPTCHA and “don't index” checks", "§9"),
        (keep, "Base44; public card fields and actions; Save contact; WhatsApp preview; deactivation; public-field filtering on the server; search exclusion; admin notifications and audit", "§1.1, §3.2, §4.2, §4.4, §7.1"),
        (add, "Admin console pages; Super admin and Admin roles; spreadsheet import; card email to staff with Google Wallet and Apple Wallet steps, and replies used for change requests; QR code for computer visitors; new link code; delete and retention rules; offboarding owner and timing; failure handling", "new sections"),
        (add, "Platform prerequisites: Base44 Builder plan, verified email sending domain, Google Wallet issuer account, Cloudflare Turnstile; the WhatsApp preview approach; the tests to run before the build", "§7.1, new section"),
    ]
    body = "".join(f"<tr><td>{c}</td><td>{w}</td><td>{s}</td></tr>" for c, w, s in rows)
    return f"""
<section id="spec">
<div class="eyebrow">13</div>
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
<div class="eyebrow">14</div>
<h2>Pending confirmation</h2>
<p>The only open items. Everything else is confirmed.</p>
<ol class="qs">
  <li><b>WhatsApp previews: option A, B or C.</b> {chip("Pending confirmation", "pend")}<span class="def">Plan confirmed: test B first. Then C if per-card previews are a must, otherwise A. Affects {fref("pg-whatsapp")}, section 11 and the file addresses in section 6. Needs the test result.</span></li>
  <li><b>How long deactivated cards are kept.</b> {chip("Pending confirmation", "pend")}<span class="def">Until then, they're kept and deleted on request. Needs whoever handles data protection (PDPA).</span></li>
</ol>
</section>
"""


def foot():
    return """
<div class="footer">
  <p><b>Sources.</b> Minmed Digital Name Cards Technical Specification draft 0.2 (15/10/2026). Your decisions in this conversation on 16/10/2026. Platform and vendor documentation linked in sections 8, 11 and 12.</p>
</div>
</main>
<script>
document.documentElement.classList.add("js");
document.addEventListener("click", function (e) {
  var a = e.target.closest && e.target.closest('a[href^="#"]');
  if (!a) return;
  var id = decodeURIComponent(a.getAttribute("href").slice(1));
  var el = id && document.getElementById(id);
  if (!el) return;
  e.preventDefault();
  el.scrollIntoView({ behavior: "smooth", block: "start" });
  if (/^(https?|file|blob):$/.test(location.protocol)) {
    try { history.replaceState(null, "", "#" + id); } catch (err) {}
  }
});
</script>
</body>
</html>
"""


def build():
    parts = [
        head(), intro(), s_how(), s_confirmed(), s_features(), s_users(), s_matrix(), s_map(), s_pages(),
        s_bots(), s_links(), s_failures(), s_feasibility(), s_benchmark(), s_spec(), s_pending(), foot(),
    ]
    doc = "".join(parts)
    assert USED == FIG_ORDER, f"figure order mismatch:\n{USED}\n{FIG_ORDER}"
    assert "zapkad" not in doc.lower(), "Zapkad must not appear in the scope"
    OUT.write_text(doc)
    print(f"wrote {OUT} ({len(doc):,} bytes, {len(USED)} figures)")


if __name__ == "__main__":
    build()
