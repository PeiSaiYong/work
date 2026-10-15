"""Build the name-card mockup pages.

    python3 name-card-mockups/src/build.py

Writes self-contained HTML files to name-card-mockups/.
"""

from pathlib import Path

from parts import (
    E, P, addr, apphead, badge, chathead, diff_table, email_phone, legend, mark, ncard, not_found,
    page, ph, phi, phone, public_page, section, st_active, st_error, st_unavail, staff_status,
    staff_view, step, wa_bubble,
)
from security import security_page

OUT = Path(__file__).resolve().parent.parent


def howto_sheet(under):
    sheet = (
        '<div class="sheet"><div class="grab"></div>'
        + ph("Panel title and final wording not defined. Lines below are the checks in spec §5.3 and meanings in §5.2.")
        + "<ol>"
        "<li>The address bar reads exactly <b>me.minmed.sg</b>.</li>"
        "<li>The status shows ✓ Active staff profile with a check time from when you opened the page.</li>"
        "<li>The details match what you were given. If they differ, trust the live page.</li>"
        "<li>Open the link or scan the QR yourself rather than trusting an image of the card.</li>"
        "<li>For payments or personal data, confirm through a Minmed contact you already know. Active confirms the card, not the person who sent it.</li>"
        "</ol><ul>"
        "<li><b>Card unavailable</b>: the card has been deactivated.</li>"
        "<li><b>Temporary verification error</b>: the card couldn't be checked right now. It does not mean the person has left.</li>"
        "</ul></div>"
    )
    return f'<div class="sheet-wrap"><div class="under">{under}</div>{sheet}</div>'


def staff_cap():
    return "Staff view (only the signed-in officer)"


def pub_cap():
    return "Recipient view (public page, no sign-in)"


# ======================================================================== index

def index_page():
    ref_steps = "".join([
        step(1, "Staff view: Approved and Active", "Signed-in officer",
             phone(staff_view("approved"), top=apphead(), cap=staff_cap()),
             [
                 "Only the signed-in officer sees this view.",
                 "The card shows name, designation, work email, published mobile and QR.",
                 "The link (me.minmed.sg/first-last) and the QR never change, even when details change.",
                 f"Who may use <b>Download image</b> is {badge('pending')}.",
             ], "§2"),
        step(2, "Shared on WhatsApp", "The chat the officer sends",
             phone(wa_bubble(text=""), top=chathead(phi("recipient")), kind="chat", cap="WhatsApp link preview"),
             [
                 "The preview is a snapshot from when the link was sent. It never updates.",
                 "It never carries a tick and doesn't show whether the card is still valid.",
                 f"\"Open link for current details.\" {badge('proposed')}",
                 "Some people turn off link previews, so not everyone sees it.",
             ], "§3, §6"),
        step(3, "Recipient opens the link", "Anyone with the link",
             phone(public_page(), top=addr(), cap=pub_cap()),
             [
                 "The address bar should read exactly <b>me.minmed.sg</b>. This is the main sign the page is genuine.",
                 "✓ <b>Active staff profile</b> appears only after a successful live check, always with the check time.",
                 "The check time is when this page was opened, not when the link was sent.",
                 "Call and WhatsApp appear only if a personal mobile is published.",
                 "Recipients see no sharing tools, downloads, editing or approval status.",
                 f"Whether recipients can download the card image is {badge('pending')}.",
             ], "§4, §6"),
        step(4, "How to verify panel", "Recipient taps How to verify",
             phone(howto_sheet(public_page(extras=False)), top=addr(), cap=pub_cap()),
             [
                 f"The whole panel is {badge('proposed')}. It opens on the same page.",
                 "Its wording isn't defined yet, so the lines shown are the checks listed in the spec.",
             ], "§4, §5.3"),
    ])

    hub = "".join(
        f'<a href="{h}"><h3>{t}</h3><p>{d}</p></a>'
        for h, t, d in [
            ("1-not-verified.html", "1 · Card not verified",
             "Four separate cases: sign-in or directory failure, new card waiting for approval, change not approved, live check failed. Plus how the three recipient results differ."),
            ("2-pending-change.html", "2 · Changed details pending",
             "From Edit my details to approval: what staff see, what recipients keep seeing, editing again during review, and the exact-version rule."),
            ("3-left-minmed.html", "3 · No longer with Minmed",
             "Deactivation: what changes at once, what the recipient sees, and what can't be erased (old WhatsApp messages, saved contacts, images)."),
            ("4-security.html", "4 · Security measures",
             "Every scenario in §7, with a request-path diagram, a CAPTCHA simulator, a token checker, look-alike addresses and the public-field filter."),
        ]
    )

    questions = [
        "Wording listed in §8 as still to decide: sign-in failure, held application, CAPTCHA and blocked messages.",
        "Wording that isn't defined but isn't listed in §8 either: the departure notice under Card unavailable, the text under Temporary verification error, the retry or status-unavailable message, the warning when editing during review, the approval and rejection emails, the download-failure message, the deactivation email to manage@minmed.sg.",
        "Button labels the spec doesn't name: the sign-in button, the submit button on the change form, and any Try again button.",
        "Card unavailable page: is the person's name, photo or designation still shown? Is a check time shown?",
        "Temporary verification error page: §7.12 says no protected response is released, so these mockups show no details. Please confirm.",
        "New card waiting for approval: what does the staff card preview show before first approval?",
        "Where the staff view lives (which address) isn't specified.",
        "Can someone whose card is deactivated still sign in and see Card deactivated?",
        "The reviewer's and administrator's screens aren't described anywhere.",
        "Format of the Checked time (these mockups use \"10:42 am, 15 Oct 2026\" as sample data).",
    ]

    body = f"""
<div class="eyebrow">Mockups · Spec draft 0.2</div>
<h1>Minmed Digital Name Cards: flows and security</h1>
<p class="lede">Phone mockups of what staff and recipients see in each flow, and visual explanations of each security measure. Everything comes from Technical Specification draft 0.2 (15/10/2026). Where the spec doesn't define something, the mockup says so instead of guessing.</p>

<h2 style="margin-top:28px">How to read these mockups</h2>
{legend()}
<div class="callout"><h3>Rule used in every phone</h3><p>Text inside a phone is either wording quoted from the spec or a dashed placeholder. Explanations sit outside the phone, with the spec section they come from.</p><p>Icons, colours and layout are illustrative. The spec fixes the wording and behaviour, not the visual design.</p></div>

<h2 style="margin-top:28px">Pages</h2>
<div class="hub">{hub}</div>

{section("reference", "Baseline", "Reference: a normal, active card",
         "<p>The starting point every other flow is compared with.</p>", f'<div class="steps">{ref_steps}</div>')}

{section("questions", "For you to decide", "Open questions found while building these",
         "<p>The mockups show each of these as a placeholder or a note. Answering them would let the placeholders be filled in.</p>",
         '<ol class="small" style="max-width:900px">' + "".join(f"<li>{q}</li>" for q in questions) + "</ol>")}
"""
    return page("index.html", "Name Card Mockups",
                "Phone mockups and security explanations for Minmed Digital Name Cards, from spec draft 0.2.", body)


# ======================================================================== 1 not verified

def not_verified_page():
    # ---- A: sign-in or directory failure
    signin = (
        '<div style="text-align:center;margin-top:30px">' + mark("mark").replace('class="mark"', 'class="mark" style="width:52px;height:52px"') + "</div>"
        + ph("Sign-in screen layout and wording not defined. Spec §1: staff sign in with their Minmed Google account.")
        + f'<div class="btn primary">{phi("sign-in button label")}</div><div class="blank"></div>'
    )
    refused = (
        '<div class="field"><label>' + phi("account shown") + '</label><div class="in">alex.personal@example.com</div></div>'
        + ph("Sign-in message asking you to use your Minmed Google account. Wording not yet defined (§8).")
        + '<div class="btn ghost">' + phi("button, if any") + '</div><div class="blank"></div>'
    )
    held = (
        '<div class="field"><label>' + phi("account shown") + f'</label><div class="in">{E(P["email"])}</div></div>'
        + ph("Message saying your application is held. Wording not yet defined (§8).")
        + '<div class="blank"></div>'
    )
    diagram = (
        '<div class="panel vlist small">'
        '<div class="node"><b>1. Google sign-in</b>Company Google account</div>'
        '<div class="arrow">↓</div>'
        '<div class="node"><b>2. Server: identity check</b>Every request, on the server. A typed email address is never accepted as proof.</div>'
        '<div class="flowdia"><div class="node no"><b>Fails or not Minmed</b>Refused (step A2)</div>'
        '<div class="node ok"><b>Minmed account</b>Continue ↓</div></div>'
        '<div class="node"><b>3. Server: staff directory match</b></div>'
        '<div class="flowdia"><div class="node warn"><b>Not found or unclear</b>Held for an administrator (step A3). Never picks a similar name.</div>'
        '<div class="node ok"><b>Clear match</b>Can create a card and submit it for approval (flow B)</div></div>'
        "</div>"
    )
    a = "".join([
        step("A1", "Sign-in", "Staff member",
             phone(signin, top=apphead(), cap="Sign-in screen"),
             ["Staff sign in with their Minmed Google account.",
              f"The sign-in screen itself is {badge('notspec')}: no layout or wording yet."],
             "§1, §5.1"),
        step("A2", "Signed in with a non-Minmed account", "Staff member",
             phone(refused, top=apphead(), cap=staff_cap()),
             ["Also shown when the identity check itself fails.",
              "They can't create, edit or manage a card.",
              "Typing a Minmed email address is not accepted as proof.",
              "The server checks identity on every request, not only by hiding buttons."],
             "§5.1, §7.6"),
        step("A3", "Not found in the staff directory", "Staff member with a Minmed account",
             phone(held, top=apphead(), cap=staff_cap()),
             ["Also applies when the directory match is unclear.",
              "An administrator resolves it. The system never picks a similar name and never publishes a card automatically.",
              f"How the administrator resolves it, and on what screen, is {badge('notspec')}."],
             "§5.1"),
        step("A4", "What the server checks", "Behind the scenes", diagram,
             ["These checks run before a card can be approved.",
              "Identity, directory match and ownership are checked on the server for every request."],
             "§7.1, §7.6"),
    ])

    # ---- B: new card not approved yet
    b_staff = staff_view(
        "pending",
        card=ph("What the card area shows before the first approval is not specified."),
        share_on=False,
    )
    b_compare = (
        '<div class="panel small"><div class="vlist">'
        '<div class="node"><b>me.minmed.sg/alex-tan</b>Card exists but isn\'t approved yet</div>'
        '<div class="node"><b>me.minmed.sg/alex-tann</b>Typo: no such card</div>'
        '<div class="arrow">↓ both return ↓</div>'
        '<div class="node"><b>The same response</b>"No card found at this address. Check the link or visit minmed.sg."</div>'
        "</div><p class=\"small\" style=\"margin-bottom:0\">Nobody can tell from the response whether a card is waiting for approval, so the link can't be used to discover new staff.</p></div>"
    )
    b = "".join([
        step("B1", "Officer submits a new card", "Staff member",
             phone(b_staff, top=apphead(), cap=staff_cap()),
             ["Status shows <b>Pending review</b>.",
              f"Sharing, QR and downloads stay off until approval {badge('proposed')}.",
              "The officer's public link shows \"No card found\" (step B2)."],
             "§5.1"),
        step("B2", "Someone opens the link anyway", "Recipient",
             phone(not_found(), top=addr(), cap=pub_cap()),
             ["Same message as a link that doesn't exist, on purpose.",
              "No status, no tick and no details are shown."],
             "§5.2, §7.7"),
        step("B3", "Why the message is the same", "Behind the scenes", b_compare,
             ["Unapproved cards return the same not-found response as links that don't exist."],
             "§7.7"),
        step("B4", "Card approved", "Staff member",
             phone(staff_view("approved"), top=apphead(), cap=staff_cap()),
             ["Status changes to <b>Approved and Active</b>.",
              "Sharing, QR and downloads turn on. The link now opens the live page (see the baseline on the Overview)."],
             "§2, §5.1"),
    ])

    # ---- C: change not approved
    c_pending = staff_view("pending", between=diff_table([("Designation", P["desig"], P["desig_new"])]))
    reason = (
        '<div class="panel" style="padding:8px 10px;font-size:12px">'
        f'{phi("label for reviewer reason")}<div style="margin-top:4px">"Please use your designation as it appears in HR records."</div>'
        f'<div style="margin-top:4px">{badge("sample", "Sample reason", mini=True)}</div></div>'
        '<div class="btn primary">Edit and resubmit</div>'
    )
    c_rejected = staff_view("rejected", between=reason)
    c_email = email_phone(
        P["email"], "subject not defined",
        ph("Email wording not defined. Spec: it includes the reviewer's reason and a link to your staff view.")
        + '<div class="panel" style="padding:8px 10px;font-size:12px">"Please use your designation as it appears in HR records."</div>'
        + f'<div class="linktext" style="font-size:12px">{phi("link to staff view")}</div>',
        cap="Email to the officer's work address",
    )
    c = "".join([
        step("C1", "Officer submits a change", "Staff member",
             phone(c_pending, top=apphead(), cap=staff_cap()),
             [f"Each changed field is listed with its current public value, the submitted value and the date {badge('proposed')}.",
              f"The card keeps showing the approved details {badge('proposed')}."],
             "§2, §5.1"),
        step("C2", "Reviewer doesn't approve it", "Staff member",
             phone(c_rejected, top=apphead(), cap=staff_cap()),
             ["Status shows <b>Changes not approved</b>, the reviewer's reason and <b>Edit and resubmit</b>.",
              "The approved card stays live, so sharing still works.",
              "Edit and resubmit starts a new review (see page 2)."],
             "§2, §5.1"),
        step("C3", "Email to the officer", "Staff member's inbox",
             c_email,
             [f"The email is {badge('proposed')}.",
              "It goes to the officer's work address with the reviewer's reason and a link to the staff view."],
             "§2, §5.1"),
        step("C4", "What recipients see meanwhile", "Recipient",
             phone(public_page(), top=addr(), cap=pub_cap()),
             ["Nothing changes for recipients: the last approved details, still ✓ Active.",
              "The rejected designation never appears anywhere public."],
             "§5.1, §7.5"),
    ])

    # ---- D: live check failed
    d_pub = (
        '<div class="avatar" style="opacity:.4">—</div>'
        + st_error()
        + ph("Explanation under the error not defined. Spec §5.2 meaning: the card couldn't be checked right now; it does not mean the person has left.")
        + f'<div class="btn ghost">{phi("Try again button, if any")}</div>'
        + f'<span class="howto">How to verify {badge("proposed", mini=True)}</span>'
        + '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )
    d_staff = (
        '<div class="status st-error"><span class="ic">!</span><span class="t">' + phi("temporary error, wording not defined") + "</span></div>"
        + ph("Spec §5.1: try again later. Nothing about your card changes.")
        + '<div class="blank"></div>'
    )
    d_lookup = (
        ph("Retry or status-unavailable message. Wording not defined. Shown when the CAPTCHA check or the card lookup fails.")
        + f'<div class="btn ghost">{phi("retry control, if any")}</div><div class="blank"></div>'
    )
    d = "".join([
        step("D1", "Recipient opens the link during an outage", "Recipient",
             phone(d_pub, top=addr(), cap=pub_cap()),
             ["Shows <b>Temporary verification error</b>, never the tick.",
              "It never shows a fresh Active result and never claims the person has left.",
              "No protected response is released, so this mockup shows no card details.",
              f"Whether the name or photo is still shown is {badge('notspec')}."],
             "§5.2, §6, §7.12"),
        step("D2", "Recipient checks what it means", "Recipient taps How to verify",
             phone(howto_sheet(d_pub), top=addr(), cap=pub_cap()),
             [f"The panel {badge('proposed')} explains Card unavailable and the verification error."],
             "§5.3"),
        step("D3", "Officer's status can't be checked", "Staff member",
             phone(d_staff, top=apphead(), cap=staff_cap()),
             ["A temporary error. Try again later.", "Nothing about the card changes."],
             "§5.1"),
        step("D4", "CAPTCHA check or card lookup fails", "Recipient",
             phone(d_lookup, top=addr(), cap=pub_cap()),
             ["This is the closest thing in the spec to a \"gateway error\".",
              "No protected data is released. The user tries again.",
              "More on page 4 (Security)."],
             "§5.2, §7.8"),
    ])

    # ---- E: compare recipient results
    unavail_body = (
        '<div class="avatar" style="opacity:.4">—</div>' + st_unavail()
        + ph("Notice that the person is no longer with Minmed. Wording not defined.")
        + '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )
    e = "".join([
        step("✓", "Active", "Live check succeeded", phone(public_page(extras=False), top=addr(), cap="Tick + check time"),
             ["The only result with a tick, and only on the live page."], "§5.2, §6"),
        step("⊘", "Card unavailable", "Card deactivated", phone(unavail_body, top=addr(), cap="Different icon, never the tick"),
             ["The person is no longer with Minmed. See page 3."], "§5.2, §6"),
        step("!", "Temporary verification error", "Live check failed", phone(d_pub, top=addr(), cap="Different icon, never the tick"),
             ["Does <b>not</b> mean the person has left."], "§5.2, §6, §7.12"),
        step("?", "No card found", "Bad link or not approved yet", phone(not_found(), top=addr(), cap="No status at all"),
             ["Same message for both causes, on purpose."], "§5.2, §7.7"),
    ])

    body = f"""
<div class="eyebrow">Page 1</div>
<h1>When a card is not verified</h1>
<p class="lede">"Not verified" covers four different situations in the spec. They look different and mean different things, so each has its own flow.</p>
{legend()}
<ul class="jump">
<li><a href="#a">A · Sign-in or directory failure</a></li>
<li><a href="#b">B · New card waiting for approval</a></li>
<li><a href="#c">C · Change not approved</a></li>
<li><a href="#d">D · Live check failed</a></li>
<li><a href="#e">Compare the recipient results</a></li>
</ul>
{section("a", "Flow A · staff", "Sign-in or directory failure", "<p>Someone tries to get a card but can't prove they're current Minmed staff.</p>", f'<div class="steps">{a}</div>')}
{section("b", "Flow B · staff and recipient", "New card waiting for approval", "<p>The officer has submitted a first card. Until it is approved, nothing is public.</p>", f'<div class="steps">{b}</div>')}
{section("c", "Flow C · staff and recipient", "Change not approved", "<p>The officer already has an approved card and submits a change that the reviewer doesn't approve.</p>", f'<div class="steps">{c}</div>')}
{section("d", "Flow D · recipient and staff", "Live check failed", "<p>Every time the link is opened, Minmed's server checks the card. If that check fails (for example an outage), the page must not guess.</p>", f'<div class="steps">{d}</div>')}
{section("e", "Side by side", "The four results a recipient can see", '<p>Tick rules ' + badge("proposed") + ': a ✓ appears only on the live page, only after a successful live check, always with the check time. The page never uses the word "Verified", so it doesn\'t suggest the sender\'s identity has been checked.</p>', f'<div class="steps">{e}</div>')}
"""
    return page("1-not-verified.html", "Card Not Verified",
                "Four flows where a Minmed name card is not verified, from spec draft 0.2.", body)


# ======================================================================== 2 pending change

def pending_page():
    form_fields = (
        f'<div class="small muted" style="font-size:11px">Which fields staff can edit, and which need approval: {badge("pending", mini=True)}</div>'
        + f'<div class="field"><label>Name</label><div class="in">{E(P["name"])}</div></div>'
        + '<div class="field"><label>Designation</label><div class="in changed">Senior Sales Manager</div></div>'
        + f'<div class="field"><label>Mobile</label><div class="in">{E(P["mobile"])}</div></div>'
        + '<div class="field"><label>Photo</label><div class="in locked">—</div></div>'
        + '<div class="field"><label>Biography</label><div class="in locked">—</div></div>'
        + f'<div class="field"><label>Languages</label><div class="in">{E(P["langs"])}</div></div>'
        + '<div class="field"><label>LinkedIn</label><div class="in">linkedin.com/in/…</div></div>'
        + f'<div class="btn primary">{phi("submit button label")}</div>'
    )
    pend = staff_view("pending", between=diff_table([("Designation", P["desig"], "Senior Sales Manager")]))
    warn_form = (
        ph("Warning that a change is already pending and this edit will replace it. Wording not defined.")
        + f'<div class="field"><label>Designation</label><div class="in changed">{E(P["desig_new"])}</div></div>'
        + f'<div class="field"><label>Mobile</label><div class="in">{E(P["mobile"])}</div></div>'
        + f'<div class="btn primary">{phi("submit button label")}</div><div class="blank"></div>'
    )
    version = (
        '<div class="panel small"><ol class="timeline" style="margin-left:4px">'
        '<li>Officer submits <b>version 2</b>: "Senior Sales Manager".</li>'
        '<li>Reviewer opens version 2.</li>'
        '<li class="amber">Officer corrects it: <b>version 3</b>, "Senior Corporate Sales Manager", replaces version 2 and review restarts.</li>'
        '<li class="red">Reviewer approves version 2. The server sees it isn\'t the current version: <b>nothing is published</b>.</li>'
        '<li>Version 3 goes back for review.</li>'
        '<li class="green">Only the exact version the reviewer approved can go live.</li>'
        f'</ol><p style="margin:0">The reviewer\'s screen is {badge("notspec")}.</p></div>'
    )
    approved_staff = staff_view("approved", card=ncard(desig=P["desig_new"], hl=("desig",)))
    approved_email = email_phone(
        P["email"], "subject not defined",
        ph("Email wording not defined. Spec: tells you the change is approved and your new details are live."),
        cap="Email to the officer's work address",
    )
    wa = (
        wa_bubble(time="Mon 9:14 am", open_line=True)
        + '<div class="small muted" style="text-align:center;font-size:11px">— change approved —</div>'
        + wa_bubble(desig=P["desig_new"], time="Thu 4:02 pm")
    )
    steps = "".join([
        step(1, "Officer opens Edit my details", "Staff member",
             phone(form_fields, top=apphead(), cap=staff_cap()),
             ["The form covers name, designation, mobile, photo, biography, languages and LinkedIn.",
              "Name, designation and mobile changes need approval.",
              f"Whether photo, biography, languages and LinkedIn changes need approval is {badge('pending')}. Spec proposal: review all public changes."],
             "§2, §7.5"),
        step(2, "Change waiting for review", "Staff member",
             phone(pend, top=apphead(), cap=staff_cap()),
             ["Status shows <b>Pending review</b>.",
              f"Each changed field is listed with the current public value, the submitted value and the date {badge('proposed')}.",
              f"The card keeps showing the approved details, so the officer never shares details still under review {badge('proposed')}."],
             "§2, §5.1"),
        step(3, "Recipients meanwhile", "Recipient",
             phone(public_page(), top=addr(), cap=pub_cap()),
             ["Still the approved designation, still ✓ Active.",
              "Pending edits are never public: not on the page, the preview, the contact file or the card image."],
             "§5.1, §7.5, §7.10"),
        step(4, "Officer edits again during review", "Staff member",
             phone(warn_form, top=apphead(), cap=staff_cap()),
             [f"The form warns before submitting {badge('proposed')}.",
              f"The new edit replaces the pending one and review starts again {badge('proposed')}."],
             "§2, §5.1"),
        step(5, "The exact-version rule", "Behind the scenes", version,
             ["If the submission changed after the reviewer opened it, it stays pending and the current version goes back for review.",
              "Approval applies only to the exact version reviewed."],
             "§5.1, §7.5"),
        step(6, "Change approved", "Staff member",
             phone(approved_staff, top=apphead(), cap=staff_cap()),
             ["Status returns to <b>Approved and Active</b>.",
              "The new details go live on the same link and QR. The QR image is identical."],
             "§5.1"),
        step(7, "Approval email", "Staff member's inbox", approved_email,
             [f"The email is {badge('proposed')}."], "§2, §5.1"),
        step(8, "Recipients see the new details", "Recipient",
             phone(public_page(desig=P["desig_new"], hl=("desig",), time="4:05 pm, 18 Oct 2026"), top=addr(), cap=pub_cap()),
             ["Same link, new details, fresh check time.",
              "Contacts saved earlier don't update. They are snapshots."],
             "§4, §5.1"),
        step(9, "WhatsApp previews: old and new", "Recipient's chat",
             phone(wa, top=chathead(phi("recipient")), kind="chat", cap="Old message keeps the old preview"),
             ["The preview image updates on approval, so new shares show the new designation.",
              "Messages sent before keep the old snapshot. Third-party caches may too.",
              "That's why the preview never claims to be verified."],
             "§3, §7.13"),
    ])
    body = f"""
<div class="eyebrow">Page 2</div>
<h1>When changed details are pending</h1>
<p class="lede">An officer with an approved card changes their designation, then corrects the change while it's still under review. Sample: "{E(P['desig'])}" to "Senior Sales Manager", corrected to "{E(P['desig_new'])}" {badge('sample')}.</p>
{legend()}
{section("flow", "Flow", "From edit to live", "<p>The approved card stays live the whole time. Recipients never see unapproved details.</p>", f'<div class="steps">{steps}</div>')}
"""
    return page("2-pending-change.html", "Pending Change Flow",
                "What staff and recipients see while a name card change is pending, from spec draft 0.2.", body)


# ======================================================================== 3 left minmed

def left_page():
    deact = (
        '<div class="panel small"><div class="vlist">'
        f'<div class="node tbd"><b>Offboarding trigger</b>Who triggers it and how quickly it takes effect: {badge("pending")}</div>'
        '<div class="arrow">↓</div>'
        '<div class="node"><b>Card deactivated</b>Immediate and central.</div>'
        '<div class="arrow">↓ at the same time ↓</div>'
        f'<div class="node">New contact and card downloads stop {badge("proposed", mini=True)}</div>'
        f'<div class="node">New WhatsApp preview images are refused {badge("proposed", mini=True)}</div>'
        f'<div class="node">Controlled caches are cleared {badge("proposed", mini=True)}</div>'
        '<div class="node">Every download re-checks status</div>'
        '<div class="node">manage@minmed.sg is emailed, and an audit record is kept</div>'
        "</div></div>"
    )
    staff = staff_view("deactivated", card=ncard(dim=True), share_on=False, edit_on=False)
    staff = staff.replace("Sharing, QR and downloads off until approval", "Sharing and new downloads stop")
    unavail = (
        '<div class="avatar" style="opacity:.4">—</div>' + st_unavail()
        + ph("Notice that the person is no longer with Minmed. Wording not defined.")
        + ph("Whether name, photo, designation or a check time are still shown is not specified.")
        + '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )
    old_chat = (
        wa_bubble(time="12 Aug", me=False, text="")
        + '<div class="small muted" style="text-align:center;font-size:11px">— weeks later, recipient taps the link —</div>'
    )
    leftovers = (
        '<div class="panel small">'
        "<b>Saved contact</b><div class=\"muted\">Alex Tan · Corporate Sales Manager · Minmed · +65 8000 1234</div>"
        '<hr style="border:0;border-top:1px solid var(--border)">'
        "<b>Screenshot or downloaded card image</b>" + ncard()
        + '<p style="margin:8px 0 0">These copies keep looking normal. None of them carries a tick, so none of them looks verified. Only opening the link shows the current status.</p></div>'
    )
    audit = email_phone(
        "manage@minmed.sg", "subject not defined",
        ph("Email wording not defined. Spec: includes the responsible account, the card and the time.")
        + '<dl class="kv"><div><dt>Account</dt><dd style="margin:0">' + phi("administrator") + "</dd></div>"
        + f'<div><dt>Card</dt><dd style="margin:0">me.minmed.sg/{P["slug"]}</dd></div>'
        + '<div><dt>Time</dt><dd style="margin:0">' + phi("time") + "</dd></div></dl>",
        cap="Notification to manage@minmed.sg",
    )
    dl_fail = (
        staff_status("deactivated")
        + ph("Message when a download is refused because the card is deactivated. Wording not defined.")
        + '<div class="blank"></div>'
    )
    steps = "".join([
        step(1, "Before: card is active", "Recipient",
             phone(public_page(), top=addr(), cap=pub_cap()),
             ["Normal ✓ Active page while the officer works at Minmed."], "§4"),
        step(2, "Officer leaves: card deactivated", "Behind the scenes", deact,
             [f"The administrator's screen is {badge('notspec')}.",
              "An email failure never reverses a saved deactivation."],
             "§7.4, §7.14"),
        step(3, "Staff view after deactivation", "Former officer",
             phone(staff, top=apphead(), cap=staff_cap()),
             ["Shows <b>Card deactivated</b>.",
              f"Sharing and new downloads stop {badge('proposed')}.",
              f"Whether a former officer can still sign in to see this is {badge('notspec')}."],
             "§5.1"),
        step(4, "Recipient opens the link", "Recipient",
             phone(unavail, top=addr(), cap=pub_cap()),
             ["Shows <b>Card unavailable</b> with a notice that the person is no longer with Minmed.",
              "A different icon, never the tick.",
              "Save contact is gone: new contact downloads stop."],
             "§5.2, §6, §7.4"),
        step(5, "An old WhatsApp message", "Recipient's chat",
             phone(old_chat, top=chathead(P["name"]), kind="chat", cap="Old preview still shows old details"),
             ["Old messages can't be changed remotely. The preview still shows the old snapshot.",
              "Tapping it opens the live page, which shows Card unavailable (step 4)."],
             "§3, §7.4, §7.13"),
        step(6, "Copies that can't be erased", "Recipient's phone", leftovers,
             ["Saved contacts, screenshots and downloaded images can't be erased remotely.",
              "Don't rely on old copies, screenshots or saved contacts."],
             "§5.2, §6, §7.4"),
        step(7, "Download attempt after deactivation", "Former officer",
             phone(dl_fail, top=apphead(), cap=staff_cap()),
             ["Every download re-checks status, so nothing new is produced."],
             "§7.4"),
        step(8, "Notification and audit", "manage@minmed.sg", audit,
             ["Deactivations and administrator edits are emailed with the responsible account, the card and the time.",
              "An audit record is kept."],
             "§7.4, §7.14"),
    ])
    body = f"""
<div class="eyebrow">Page 3</div>
<h1>When the person is no longer with Minmed</h1>
<p class="lede">The officer's card is deactivated. The link and QR keep working, but now they show that the card is unavailable.</p>
{legend()}
{section("flow", "Flow", "From deactivation to what recipients see", "", f'<div class="steps">{steps}</div>')}
<div class="callout warn"><h3>Still to decide {badge("pending")}</h3><p>Who triggers offboarding, and how quickly a departure takes effect.</p></div>
"""
    return page("3-left-minmed.html", "Left Minmed Flow",
                "What happens to a Minmed name card when the person leaves, from spec draft 0.2.", body)


def main():
    pages = {
        "index.html": index_page(),
        "1-not-verified.html": not_verified_page(),
        "2-pending-change.html": pending_page(),
        "3-left-minmed.html": left_page(),
        "4-security.html": security_page(),
    }
    for name, text in pages.items():
        (OUT / name).write_text(text)
        print(f"wrote {name} ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
