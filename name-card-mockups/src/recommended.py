"""Page 5: one mockup with a recommended answer to every open question.

Inside phones: plain text is quoted from the spec; text wrapped in rec() is a
recommendation (shown highlighted). Nothing here is in the spec yet.
"""

from parts import (
    E, P, addr, apphead, badge, diff_table, mark, ncard, page, phi, phone, staff_buttons, staff_status,
)

TIME = P["time"]


def rec(text):
    return f'<span class="rec">{E(text)}</span>'


def rec_html(html):
    return f'<span class="rec">{html}</span>'


def pub_cap():
    return "Recipient view (public page)"


def staff_cap():
    return "Staff view (signed-in officer)"


# ======================================================================== recipient screens

def r_unavailable():
    return (
        f'<p class="pname" style="margin-top:22px">{rec(P["name"])}</p>'
        '<div class="status st-unavail"><span class="ic" aria-hidden="true">⊘</span><span class="t">Card unavailable'
        f'<span class="s">{rec("Checked " + TIME)}</span></span></div>'
        f'<p class="ptext">{rec(P["name"] + " is no longer with Minmed.")}</p>'
        f'<span class="howto">How to verify {badge("proposed", mini=True)}</span>'
        '<div class="blank"></div>'
        '<div class="foot-link">About Minmed</div>'
    )


def r_temp_error():
    return (
        '<div style="height:18px"></div>'
        '<div class="status st-error"><span class="ic" aria-hidden="true">!</span><span class="t">Temporary verification error</span></div>'
        f'<p class="ptext">{rec("We couldn’t check this card.")}</p>'
        f'<div class="btn primary">{rec("Try again")}</div>'
        f'<span class="howto">How to verify {badge("proposed", mini=True)}</span>'
        '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )


def r_captcha():
    return (
        '<div style="height:18px"></div>'
        f'<p class="ptitle">{rec("Quick check")}</p>'
        f'<p class="ptext">{rec("Please confirm you’re a person to continue.")}</p>'
        '<div class="captcha"><span class="box" aria-hidden="true"></span><span class="small">'
        + phi("challenge widget")
        + f'<br>{badge("candidate", "Candidate: Cloudflare Turnstile", mini=True)}</span></div>'
        '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )


def r_captcha_failed():
    return (
        '<div style="height:18px"></div>'
        f'<p class="ptitle">{rec("Check failed")}</p>'
        f'<div class="btn primary">{rec("Try again")}</div>'
        '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )


def r_blocked():
    return (
        '<div style="height:18px"></div>'
        f'<p class="ptitle">{rec("Too many cards opened")}</p>'
        f'<p class="ptext">{rec("Please try again after 10:57 am.")}</p>'
        f'<p class="psmall">{badge("sample", "Sample time", mini=True)} Real cooldown {badge("pending", mini=True)}</p>'
        '<div class="blank"></div><div class="foot-link">About Minmed</div>'
    )


def r_howto():
    under = (
        f'<p class="pname" style="margin-top:22px">{E(P["name"])}</p><p class="pdesig">{E(P["desig"])}</p>'
        '<div class="status st-active"><span class="ic">✓</span><span class="t">Active staff profile'
        f'<span class="s">Checked {E(TIME)}</span></span></div><div class="btn primary">Save contact</div>'
    )
    sheet = (
        '<div class="sheet"><div class="grab"></div>'
        f'<p class="ptitle" style="font-size:14px">{rec("How to check this card")}</p>'
        "<ol>"
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


# ======================================================================== staff screens

def s_signin():
    big = mark("mark").replace('class="mark"', 'class="mark" style="width:52px;height:52px"')
    return (
        f'<div style="text-align:center;margin-top:34px">{big}</div>'
        f'<p class="ptext" style="text-align:center">{rec("Please sign in with your Minmed registered email address.")}</p>'
        f'<div class="btn primary">{rec("Sign in with Google")}</div>'
        '<div class="blank"></div>'
    )


def s_wrong_account():
    return (
        '<div style="height:10px"></div>'
        f'<p class="ptext">{rec("Please sign in with your Minmed registered email address.")}</p>'
        f'<div class="btn primary">{rec("Try again")}</div>'
        '<div class="blank"></div>'
    )


def s_held():
    return (
        '<div style="height:10px"></div>'
        f'<p class="ptitle">{rec("Your application is on hold")}</p>'
        '<div class="blank"></div>'
    )


def s_new_pending():
    return (
        staff_status("pending")
        + f'<p class="ptext">{rec("You can share your card once it’s approved.")}</p>'
        + f'<p class="prevlabel">{rec("Preview · not public yet")}</p>'
        + ncard()
        + staff_buttons(share_on=False, note=False)
    )


def s_form():
    return (
        f'<div class="field"><label>Name</label><div class="in">{E(P["name"])}</div></div>'
        '<div class="field"><label>Designation</label><div class="in changed">Senior Sales Manager</div></div>'
        f'<div class="field"><label>Mobile</label><div class="in">{E(P["mobile"])}</div></div>'
        f'<div class="field"><label>Languages</label><div class="in">{E(P["langs"])}</div></div>'
        '<div class="field"><label>LinkedIn</label><div class="in">linkedin.com/in/…</div></div>'
    )


def s_edit_again():
    under = (
        s_form().replace("Senior Sales Manager", E(P["desig_new"]))
        + f'<div class="btn primary">{rec("Submit for review")}</div>'
    )
    dialog = (
        '<div class="dialog">'
        f'<p class="ptitle">{rec("Replace your pending change?")}</p>'
        f'<p class="ptext">{rec("Review will start again.")}</p>'
        f'<div class="btn primary">{rec("Replace and submit")}</div>'
        f'<div class="btn ghost">{rec("Cancel")}</div></div>'
    )
    return f'<div class="modal-wrap"><div class="under">{under}</div>{dialog}</div>'


def s_submit():
    return s_form() + f'<div class="btn primary">{rec("Submit for review")}</div><div class="blank"></div>'


def s_deactivated():
    return (
        staff_status("deactivated")
        + f'<p class="ptext">{rec("Contact HR if this is a mistake.")}</p>'
        + '<div class="blank"></div>'
    )


def s_temp_error():
    return (
        f'<div class="status st-error"><span class="ic" aria-hidden="true">!</span><span class="t">{rec("Couldn’t check your card")}</span></div>'
        f'<p class="ptext">{rec("Please try again later.")}</p>'
        f'<div class="btn primary">{rec("Try again")}</div><div class="blank"></div>'
    )


def s_download_failed():
    return (
        staff_status("approved") + ncard()
        + f'<div class="toast"><span style="flex:1">{rec("Download failed.")}</span>'
        f'<span class="btn sm">{rec("Try again")}</span></div>'
        + staff_buttons()
    )


# ======================================================================== emails

SENDER = "Minmed Name Cards <no-reply@minmed.sg>"


def email(to, subject, body, cap):
    head = (
        '<div class="mailhead">'
        f'<div><span class="k">From</span>{rec(SENDER)}</div>'
        f'<div><span class="k">To</span>{E(to)}</div>'
        f'<div><span class="k">Subject</span>{rec(subject)}</div></div>'
    )
    return phone(head + body, top=apphead("Email"), cap=cap)


def e_approved():
    body = (
        f'<p class="ptext">{rec("Hi Alex,")}</p>'
        f'<p class="ptext">{rec("Your change is now live.")}</p>'
        f'<dl class="kv"><div><dt>Designation</dt><dd style="margin:0">{E(P["desig_new"])}</dd></div></dl>'
    )
    return email(P["email"], "Name card change approved", body, "Change approved")


def e_rejected():
    body = (
        f'<p class="ptext">{rec("Hi Alex,")}</p>'
        f'<p class="ptext">{rec("Your change wasn’t approved.")}</p>'
        f'<div class="panel" style="padding:8px 10px;font-size:12px"><b>{rec("Reason from reviewer")}</b>'
        '<div>"Please use your designation as it appears in HR records."</div></div>'
        f'<p class="ptext">{rec("To edit, open")} <span class="linktext">me.minmed.sg/staff</span></p>'
    )
    return email(P["email"], "Name card change not approved", body, "Change not approved")


def e_deactivated():
    body = (
        f'<dl class="kv"><div><dt>Card</dt><dd style="margin:0">me.minmed.sg/{P["slug"]}</dd></div>'
        f'<div><dt>{rec("Action")}</dt><dd style="margin:0">{rec("Deactivated")}</dd></div>'
        f'<div><dt>{rec("By")}</dt><dd style="margin:0">hr.admin@minmed.sg</dd></div>'
        f'<div><dt>{rec("Time")}</dt><dd style="margin:0">{E(TIME)}</dd></div></dl>'
    )
    return email("manage@minmed.sg", "Name card deactivated: Alex Tan", body, "To manage@minmed.sg")


# ======================================================================== reviewer + admin

def rv_queue():
    rows = [
        ("Chen Wei", "Mobile", "Yesterday"),
        ("Bea Lim", "New card", "9:12 am"),
        ("Alex Tan", "Designation", "10:40 am"),
    ]
    items = "".join(
        f'<div class="listrow"><span class="grow"><b>{n}</b><span class="sub">{f}</span></span><span class="psmall">{t}</span></div>'
        for n, f, t in rows
    )
    return f'<p class="ptitle">{rec("Waiting for review (3)")}</p>{items}<div class="blank"></div>'


def rv_review():
    return (
        f'<p class="ptitle">{E(P["name"])}</p>'
        f'<p class="psmall">{rec("Version 3 · submitted 10:40 am, 15 Oct 2026")}</p>'
        + diff_table([("Designation", P["desig"], P["desig_new"])], labels=("Current public value", rec("Submitted")))
        + f'<p class="psmall">{rec("Recipients will see:")}</p>'
        + ncard(desig=P["desig_new"], hl=("desig",))
        + f'<div class="btn primary">{rec("Approve")}</div>'
        f'<div class="btn danger">{rec("Don’t approve")}</div>'
    )


def rv_reason():
    under = rv_review()
    dialog = (
        '<div class="dialog">'
        f'<p class="ptitle">{rec("Don’t approve this change?")}</p>'
        f'<div class="field"><label>{rec("Reason (sent to Alex)")}</label>'
        '<div class="textarea">Please use your designation as it appears in HR records.</div></div>'
        f'<div class="btn danger primary">{rec("Don’t approve")}</div>'
        f'<div class="btn ghost">{rec("Cancel")}</div></div>'
    )
    return f'<div class="modal-wrap"><div class="under">{under}</div>{dialog}</div>'


def rv_changed():
    return (
        f'<p class="ptitle">{E(P["name"])}</p>'
        f'<div class="status st-error"><span class="ic" aria-hidden="true">!</span><span class="t">{rec("This change was updated")}</span></div>'
        f'<p class="ptext">{rec("Please review the latest version.")}</p>'
        f'<div class="btn primary">{rec("Load latest version")}</div><div class="blank"></div>'
    )


def ad_held():
    rows = [("Alex Tan", "Corporate Sales"), ("Alex Tan", "Clinic Operations")]
    items = "".join(
        f'<div class="listrow"><span class="grow"><b>{n}</b><span class="sub">{d}</span></span><span class="btn sm">{rec("Link")}</span></div>'
        for n, d in rows
    )
    return (
        f'<p class="ptitle">{rec("Application on hold")}</p>'
        f'<dl class="kv"><div><dt>{rec("Signed in as")}</dt><dd style="margin:0">alex.t@minmed.sg</dd></div>'
        f'<div><dt>{rec("Google name")}</dt><dd style="margin:0">Alex Tan</dd></div></dl>'
        f'<div class="field"><label>{rec("Search the staff directory")}</label><div class="in">Alex Tan</div></div>'
        f'{items}<div class="blank"></div><div class="btn danger">{rec("Reject application")}</div>'
    )


def ad_deactivate():
    under = (
        f'<p class="ptitle">{E(P["name"])}</p>' + staff_status("approved") + ncard()
        + f'<div class="btn danger">{rec("Deactivate card")}</div>'
    )
    dialog = (
        '<div class="dialog">'
        f'<p class="ptitle">{rec("Deactivate Alex Tan’s card?")}</p>'
        f'<p class="ptext">{rec("This takes effect immediately and is recorded.")}</p>'
        f'<div class="btn danger primary">{rec("Deactivate")}</div>'
        f'<div class="btn ghost">{rec("Cancel")}</div></div>'
    )
    return f'<div class="modal-wrap"><div class="under">{under}</div>{dialog}</div>'


# ======================================================================== layout

def qa(qid, n, question, answer, why, visuals, side=False):
    lis = "".join(f"<li>{w}</li>" for w in why)
    text = f'<div class="answer"><div class="lbl">Recommendation</div><p>{answer}</p></div><ul class="why">{lis}</ul>'
    if side:
        inner = f'<div class="qa-split"><div>{text}</div><div>{visuals}</div></div>'
    else:
        inner = text + (f'<div class="steps">{visuals}</div>' if visuals else "")
    return (
        f'<section class="section sec" id="{qid}"><div class="eyebrow">Question {n}</div>'
        f'<h2>{question}</h2>{inner}</section>'
    )


def card(title, who, visual, notes):
    """A step without a number or spec reference."""
    lis = "".join(f"<li>{n}</li>" for n in notes)
    return (
        f'<div class="step"><div class="step-head"><div><h3>{title}</h3><div class="who">{who}</div></div></div>'
        f'{visual}<ul class="notes">{lis}</ul></div>'
    )


QUESTIONS = [
    ("q1", "Card unavailable page", "Show the name, the status and the check time. Hide the photo, designation, contacts and Save contact."),
    ("q2", "Temporary verification error page", "Show no card details at all. One line and a Try again button."),
    ("q3", "New card before first approval", "Show the submitted card in the staff view, labelled \"Preview · not public yet\"."),
    ("q4", "Signing in after deactivation", "Allow it, but show only the status and who to contact. No card, no buttons."),
    ("q5", "Reviewer and administrator screens", "Yes. Six screens below: review queue, review, reason, changed version, held application, deactivate."),
    ("q6", "Where the staff view lives", "me.minmed.sg/staff, with \"staff\" reserved so no card can use that address."),
    ("q7", "Undefined wording and button labels", "One short line per screen, collected in one table at the end of this tab."),
    ("q8", "Format of the check time", "An exact date and time, such as \"Checked 10:42 am, 15 Oct 2026\". Never \"just now\"."),
]


def summary():
    rows = "".join(
        f'<tr><td><a href="#{qid}">{i}</a></td><td><b>{q}</b></td><td>{E(a)}</td></tr>'
        for i, (qid, q, a) in enumerate(QUESTIONS, 1)
    )
    return f'<div class="tablewrap"><table class="t"><tr><th>#</th><th>Question</th><th>Recommendation</th></tr>{rows}</table></div>'


WORDING = [
    ("Staff · sign-in screen", "Please sign in with your Minmed registered email address. [Sign in with Google]"),
    ("Staff · sign-in or access fails, e.g. non-Minmed account or failed identity check (§8)", "Please sign in with your Minmed registered email address. [Try again]"),
    ("Staff · application held (§8)", "Your application is on hold."),
    ("Staff · new card waiting for approval", "You can share your card once it's approved. Card label: Preview · not public yet."),
    ("Staff · change form button", "[Submit for review]"),
    ("Staff · editing during review", "Replace your pending change? Review will start again. [Replace and submit] [Cancel]"),
    ("Staff · status can't be checked", "Couldn't check your card. Please try again later. [Try again]"),
    ("Staff · download fails", "Download failed. [Try again]"),
    ("Staff · card deactivated", "Contact HR if this is a mistake. (Below the Card deactivated status.)"),
    ("Recipient · Card unavailable notice", "{name} is no longer with Minmed."),
    ("Recipient · Temporary verification error", "We couldn't check this card. [Try again]"),
    ("Recipient · CAPTCHA (§8)", "Quick check. Please confirm you're a person to continue."),
    ("Recipient · CAPTCHA failed", "Check failed. [Try again]"),
    ("Recipient · slowed down or blocked (§8)", "Too many cards opened. Please try again after {time}."),
    ("Recipient · How to verify panel title", "How to check this card"),
    ("Reviewer · change edited during review", "This change was updated. Please review the latest version. [Load latest version]"),
    ("Administrator · confirm deactivation", "Deactivate {name}'s card? This takes effect immediately and is recorded. [Deactivate] [Cancel]"),
    ("Email · change approved", "Subject: Name card change approved. Hi {first name}, your change is now live. {changed fields}"),
    ("Email · change not approved", "Subject: Name card change not approved. Hi {first name}, your change wasn't approved. Reason from reviewer: {reason}. To edit, open me.minmed.sg/staff."),
    ("Email · deactivation to manage@minmed.sg", "Subject: Name card deactivated: {name}. Card, Action, By, Time."),
    ("All emails · sender", "Minmed Name Cards <no-reply@minmed.sg> (sample address)"),
]


def wording_table():
    rows = "".join(f"<tr><td><b>{E(w)}</b></td><td>{E(t)}</td></tr>" for w, t in WORDING)
    return (
        '<section class="section sec" id="wording"><div class="eyebrow">Summary</div>'
        '<h2>All recommended wording in one place</h2>'
        '<p class="small muted" style="margin-top:0">Square brackets are buttons. Curly brackets are filled in by the system.</p>'
        f'<div class="tablewrap"><table class="t"><tr><th style="width:30%">Where</th><th>Recommended wording</th></tr>{rows}</table></div>'
        '</section>'
    )


def address_visual():
    rows = [
        (f"me.minmed.sg/{P['slug']}", "Public card", "Anyone with the link. No sign-in."),
        ("me.minmed.sg/staff", "Staff sign-in and staff view", "Minmed Google account required."),
        ("me.minmed.sg/staff/review", "Reviewers", "Reviewer permission required."),
        ("me.minmed.sg/staff/admin", "Administrators", "Administrator permission required."),
    ]
    out = "".join(
        f'<div class="row"><span class="u">{E(u)}</span><span class="verdict ok">{E(w)}</span><span class="small muted">{E(n)}</span></div>'
        for u, w, n in rows
    )
    return f'<div class="panel"><div class="addr-test">{out}</div></div>'


def time_visual():
    def shot(label, status_s, verdict_ok, verdict):
        body = (
            f'<p class="pname" style="margin-top:22px">{E(P["name"])}</p><p class="pdesig">{E(P["desig"])}</p><p class="pco">Minmed</p>'
            '<div class="status st-active"><span class="ic">✓</span><span class="t">Active staff profile'
            f'<span class="s">{status_s}</span></span></div><div class="btn primary">Save contact</div><div class="blank"></div>'
        )
        v = f'<span class="verdict {"ok" if verdict_ok else "no"}">{verdict}</span>'
        return f'<div class="shot" data-label="{E(label)}">{phone(body, top=addr(), cap=v)}</div>'

    a = shot("Screenshot taken 15 Oct, forwarded 20 Nov", "Checked just now", False, "Looks fresh forever")
    b = shot("Screenshot taken 15 Oct, forwarded 20 Nov", rec("Checked 10:42 am, 15 Oct 2026"), True, "Shows how old it is")
    return a, b


def recommended_page():
    q1 = qa("q1", 1, "What does the Card unavailable page show?", QUESTIONS[0][2], [
        "Show only what this check just confirmed: whose card it is and that it's unavailable. The name is already in the link, so showing it reveals nothing new and confirms the recipient opened the right card.",
        "Hide the photo, designation and contact details. They're out of date, and the person has left.",
        "No Save contact. New contact downloads stop after deactivation (§7.4, Proposed).",
        "Show the check time, as with Active, so a screenshot of this page also shows when it was taken.",
        "One line: the person is no longer with Minmed. The About Minmed link still leads to minmed.sg.",
    ], card("Recommended Card unavailable page", "Recipient", phone(r_unavailable(), top=addr(), cap=pub_cap()),
            ["Compare with page 3, step 4."]), side=True)

    q2 = qa("q2", 2, "What does the Temporary verification error page show?", QUESTIONS[1][2], [
        "Nothing was confirmed, so nothing is shown: no name, no photo and no check time (§7.12: no protected response is released).",
        "The heading already says the error is temporary. The How to verify panel explains that it doesn't mean the person has left (§5.2).",
        "Offer Try again, since most outages are short.",
        "Use this same screen when the card lookup fails. Only a failed CAPTCHA gets its own short message (see question 7). That's one fewer screen meaning the same thing.",
    ], card("Recommended verification error page", "Recipient", phone(r_temp_error(), top=addr(), cap=pub_cap()),
            ["Compare with page 1, step D1."]), side=True)

    q3 = qa("q3", 3, "What does the staff card show before the first approval?", QUESTIONS[2][2], [
        "The officer can check their details before anyone else sees them.",
        "The label makes it clear the card isn't live. The public link still shows \"No card found\".",
        "Sharing, QR and downloads stay off (Proposed in the spec), so the preview can't leave the staff view. The label only appears here and never on a download.",
    ], card("Recommended staff view, new card", "Signed-in officer", phone(s_new_pending(), top=apphead(), cap=staff_cap()),
            ["Compare with page 1, step B1."]), side=True)

    q4 = qa("q4", 4, "Can someone whose card is deactivated still sign in?", QUESTIONS[3][2], [
        "If Minmed suspends a leaver's Google account, they can't sign in at all. This screen covers the cases where they still can, for example a card deactivated during a notice period or by mistake.",
        "Show no card. A fresh-looking card in the app invites screenshots after the person has left.",
        "Say who to contact if it's a mistake. \"HR\" is a suggestion: §8 still has to decide who owns offboarding.",
    ], card("Recommended staff view, deactivated", "Signed-in former officer", phone(s_deactivated(), top=apphead(), cap=staff_cap()),
            ["Compare with page 3, step 3."]), side=True)

    q5_visuals = "".join([
        card("Review queue", "Reviewer", phone(rv_queue(), top=apphead("Reviewer"), cap="Reviewer view"),
             ["Oldest first, so nothing waits too long.",
              f"Reviewers can't approve their own card {badge('rec')}. The spec doesn't say this, but it stops anyone approving their own title."]),
        card("Review a change", "Reviewer", phone(rv_review(), top=apphead("Reviewer"), cap="Reviewer view"),
             ["Shows the version number, so the approval is tied to this exact version (§7.5).",
              "Shows the card as recipients will see it."]),
        card("Not approving needs a reason", "Reviewer", phone(rv_reason(), top=apphead("Reviewer"), cap="Reviewer view"),
             ["The reason is required. It goes to the officer's staff view and email."]),
        card("The change was edited during review", "Reviewer", phone(rv_changed(), top=apphead("Reviewer"), cap="Reviewer view"),
             ["What the reviewer sees if they approve a version that's no longer current. Nothing is published (§5.1)."]),
        card("Resolve a held application", "Administrator", phone(ad_held(), top=apphead("Administrator"), cap="Administrator view"),
             ["The administrator searches and picks the exact directory record. The system never picks one itself (§5.1).",
              f"Directory fields shown are {badge('sample')}: the spec doesn't say what the directory holds."]),
        card("Deactivate a card", "Administrator", phone(ad_deactivate(), top=apphead("Administrator"), cap="Administrator view"),
             ["A confirmation step, because deactivation is immediate.",
              "Recorded and emailed to manage@minmed.sg (§7.14)."]),
    ])
    q5 = qa("q5", 5, "Should the reviewer and administrator screens be mocked up?", QUESTIONS[4][2], [
        "These screens enforce several key rules: approval of the exact version, a reason for not approving, no automatic directory match, and an audit trail for deactivation.",
        "Whether administrator edits need independent approval is still Pending in §8, so there's no admin edit screen here.",
    ], q5_visuals)

    q6 = qa("q6", 6, "Where does the staff view live?", QUESTIONS[5][2], [
        "One domain to protect and one Base44 app to run.",
        "Staff see the same address they share, which reinforces \"check for me.minmed.sg\".",
        "Reserve \"staff\" (and similar words such as \"admin\") so no card's address can ever clash.",
        "Every /staff page requires sign-in, and the server still checks identity and permission on every request (§7.6). These pages are also set to noindex.",
        "The alternative is a separate subdomain. It would keep staff sign-in cookies off public card pages, which is slightly safer, but only worth it if Base44 lets one app use two custom domains. That hasn't been checked yet.",
    ], "") .replace("</section>", address_visual() + "</section>")

    w_staff = "".join([
        card("Sign-in screen", "Staff", phone(s_signin(), top=apphead(), cap="Sign-in"),
             ["One line. Staff already know who the app is for.",
              "\"Sign in with Google\" is the label Google's own sign-in button uses."]),
        card("Sign-in or access fails", "Staff", phone(s_wrong_account(), top=apphead(), cap=staff_cap()),
             ["The same line covers every sign-in or access failure, such as a non-Minmed account or a failed identity check.",
              "It doesn't say which check failed, so it gives nothing away.",
              "Try again lets them sign in with a different account."]),
        card("Application on hold", "Staff", phone(s_held(), top=apphead(), cap=staff_cap()),
             ["Kept separate from the line above, because an administrator still has to act (§5.1)."]),
        card("Change form button", "Staff", phone(s_submit(), top=apphead(), cap=staff_cap()),
             ["\"Submit for review\" matches the status they'll see next: Pending review."]),
        card("Editing during review", "Staff", phone(s_edit_again(), top=apphead(), cap=staff_cap()),
             ["Asked as a question so they can back out."]),
        card("Status can't be checked", "Staff", phone(s_temp_error(), top=apphead(), cap=staff_cap()),
             ["Short. Nothing about the card changes when this happens (§5.1), so the screen doesn't need to say so."]),
        card("Download fails", "Staff", phone(s_download_failed(), top=apphead(), cap=staff_cap()),
             ["Short. The spec already rules out giving them an empty or partial file."]),
    ])
    w_recipient = "".join([
        card("CAPTCHA check", "Recipient", phone(r_captcha(), top=addr(), cap=pub_cap()),
             ["One line. Visitors don't need the reasons."]),
        card("CAPTCHA failed", "Recipient", phone(r_captcha_failed(), top=addr(), cap=pub_cap()),
             ["Short, with nothing that helps a bot tune its attempts."]),
        card("Slowed down or blocked", "Recipient", phone(r_blocked(), top=addr(), cap=pub_cap()),
             ["Gives a time rather than \"later\". The real cooldown is still Pending."]),
        card("How to verify panel", "Recipient", phone(r_howto(), top=addr(), cap=pub_cap()),
             ["Title says \"check\", not \"verify\", in line with the rule that the page never says \"Verified\"."]),
    ])
    w_email = "".join([
        card("Change approved", "Officer's inbox", e_approved(), ["Says the change is live and lists what changed."]),
        card("Change not approved", "Officer's inbox", e_rejected(), ["Gives the reason and where to edit."]),
        card("Deactivation notice", "manage@minmed.sg", e_deactivated(), ["The fields §7.14 asks for: account, card and time."]),
    ])
    q7 = qa("q7", 7, "What should the undefined messages and buttons say?", QUESTIONS[6][2], [
        "One short line per screen saying what to do next. Staff already know the rules, so screens don't explain them.",
        "The only exception is the two confirmation boxes. Each keeps one line saying what will happen, so it's more than \"Are you sure?\"",
        "No error codes, and nothing that tells a scraper which rule it tripped.",
        "Emails come from one fixed address on minmed.sg, set up with SPF, DKIM and DMARC so staff can trust them. Emails link to me.minmed.sg/staff and never ask for a password.",
    ], "").replace("</section>",
        '<h3 style="margin-top:22px">Staff screens</h3>' + f'<div class="steps">{w_staff}</div>'
        + '<h3 style="margin-top:34px">Recipient screens</h3>' + f'<div class="steps">{w_recipient}</div>'
        + '<h3 style="margin-top:34px">Emails</h3>' + f'<div class="steps">{w_email}</div>'
        + "</section>")

    a, b = time_visual()
    q8 = qa("q8", 8, "How should the check time be written?", QUESTIONS[7][2], [
        "Screenshots get forwarded. \"Checked just now\" in a screenshot looks fresh forever, while an exact date shows how old it is.",
        "Use the time the server ran the check, shown in the viewer's own time zone.",
        "Use Singapore's usual order: time, then day, month and year.",
    ], card("Relative time", "Screenshot of the live page", a, ["Misleading once it's copied."])
       + card("Exact time (recommended)", "Screenshot of the live page", b, ["Anyone can see it's weeks old."]))

    legend = (
        '<div class="legend">'
        f'<div>{badge("rec")}<br>A recommendation. Not in the spec yet.</div>'
        f'<div>{rec("Highlighted text")}<br>Recommended wording inside a phone. Plain text inside a phone is quoted from the spec.</div>'
        f'<div>{badge("proposed")} {badge("pending")} {badge("candidate")}<br>Same meaning as on the other pages.</div>'
        f'<div>{badge("sample")}<br>Fictional people, addresses and times.</div>'
        "</div>"
    )

    body = f"""
<div class="eyebrow">Page 5 · for review</div>
<h1>Recommended answers to the open questions</h1>
<p class="lede">One recommendation for each question raised while building pages 1 to 4, shown in place. Nothing on this page is in the spec yet. If you agree, these can be written into the spec and the placeholders on pages 1 to 4 replaced.</p>
{legend}
<h2 style="margin-top:28px">At a glance</h2>
{summary()}
{q1}{q2}{q3}{q4}{q5}{q6}{q7}{q8}{wording_table()}
"""
    return page("5-recommended.html", "Recommended Answers",
                "Mockups showing a recommended answer to each open question for Minmed Digital Name Cards.", body)
