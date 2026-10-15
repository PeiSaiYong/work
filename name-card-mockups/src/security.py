"""Page 4: security measures (spec §7), with visual and interactive explanations."""

from parts import (
    E, P, SRC, addr, apphead, badge, chathead, email_phone, legend, ncard, not_found, page, ph, phi,
    phone, public_page, st_active, st_error, st_unavail, wa_bubble,
)


def sec(sid, num, title, happens, reduce, cant, visual):
    def col(cls, head, items):
        if not items:
            return ""
        lis = "".join(f"<li>{i}</li>" for i in items)
        return f'<div><h4 class="{cls}">{head}</h4><ul>{lis}</ul></div>'

    what = col("h-n", "What happens", happens) + col("h-ok", "How we reduce it", reduce) + col("h-no", "What we can't prevent", cant)
    return (
        f'<section class="section sec" id="{sid}"><div class="eyebrow">§{num}</div><h2>{title}</h2>'
        f'<div class="what">{what}</div>{visual}</section>'
    )


def gateway_explainer():
    rows = [
        ("Temporary verification error", "The live check fails, for example during an outage.", "Heading defined. Explanation text not defined."),
        ("Retry or status-unavailable message", "The CAPTCHA check or the card lookup fails.", "Not defined."),
        ("CAPTCHA check", "Browsing looks automated, for example many different cards very quickly.", "Not defined (§8)."),
        ("Slowed down or blocked for a while", "Repeated suspicious activity.", "Wording and duration not defined (§8)."),
        ('"No card found at this address. Check the link or visit minmed.sg."', "The link doesn't exist, or the card isn't approved yet.", "Defined."),
    ]
    trs = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f"""
<div class="callout info"><h3>Is there a "gateway error"?</h3>
<p>Not as such. The spec has no message called a gateway error, and the gateway itself is {badge("pending")}: the spec says the CAPTCHA provider, the gateway design and how they're deployed are still to decide.</p>
<p>One fact shapes that decision: <b>Base44 requires DNS-only records, so Cloudflare's firewall isn't automatically in front of the app.</b> Protection has to be added on purpose, and the Base44 and origin APIs need it too, not only the public address.</p>
<p>These are the error-type messages the spec does define:</p></div>
<div class="tablewrap"><table class="t"><tr><th>Message</th><th>When it appears</th><th>Wording status</th></tr>{trs}</table></div>
"""


def request_path():
    return f"""
<div class="panel">
<h3>How a card request travels</h3>
<p class="small muted" style="margin-top:0">Boxes with a dashed blue border are {badge("pending")}. Nothing here says which product will do the job, only what the spec requires.</p>
<div class="pathdia">
  <div class="node"><b>Recipient's phone</b>Opens me.minmed.sg/alex-tan or scans the QR. The link carries only the card ID.</div>
  <div class="arrow">→</div>
  <div class="node tbd"><b>Gateway and CAPTCHA layer</b>{badge("pending", mini=True)}
    <ul><li>Shows a CAPTCHA only to suspicious traffic</li><li>{badge("candidate", "Candidate", mini=True)} Cloudflare Turnstile</li><li>Client IP is trusted only from this gateway</li></ul></div>
  <div class="arrow">→</div>
  <div class="node ok"><b>Minmed app on Base44 (server checks)</b>
    <ul><li>Validates any CAPTCHA token on the server</li><li>Counts every profile-data and download request</li><li>Weighs session limits, IP activity, distinct cards and failed challenges</li><li>Live status lookup on every opening</li><li>Returns only the explicit list of public fields</li></ul></div>
  <div class="arrow">→</div>
  <div class="node"><b>Card records</b>Only the approved version is ever public. Pending edits, unpublished mobiles and admin logs stay private.</div>
</div>
<p class="small" style="margin:16px 0 6px"><b>The route around the gateway</b></p>
<div class="bypass">
  <div class="node no"><b>Script calling the Base44 or origin API directly</b>Tries to skip the public address and its checks.</div>
  <div class="arrow red">→</div>
  <div class="node tbd"><b>Must be protected too</b>The spec requires the Base44 and origin APIs to be protected as well as the public domain. How: {badge("pending", mini=True)}. Because Base44 needs DNS-only records, this protection isn't automatic.</div>
</div>
</div>"""


def captcha_sim():
    card_state = (
        '<div class="avatar">Photo<br>(optional)</div>'
        '<p class="pname" data-sim="name">—</p><p class="pco">Minmed</p>'
        '<div class="status st-active"><span class="ic">✓</span><span class="t">Active staff profile'
        '<span class="s">Checked <span data-sim="time">0:00</span> (simulated)</span></span></div>'
        '<div class="btn primary">Save contact</div><div class="blank"></div>'
    )
    states = {
        "idle": '<div class="blank"></div><p class="small muted" style="text-align:center">Use the buttons to open cards.</p><div class="blank"></div>',
        "card": card_state,
        "challenge": (
            ph("CAPTCHA check message. Wording not defined (§8).")
            + '<div class="captcha"><span class="box" aria-hidden="true"></span><span class="small">'
            + phi("challenge widget")
            + f'<br>{badge("candidate", "Candidate: Cloudflare Turnstile", mini=True)}</span></div>'
            + '<p class="small muted" style="font-size:11px">Provider is Pending. A real widget looks different.</p><div class="blank"></div>'
        ),
        "retry": ph("Retry or status-unavailable message. Wording not defined.") + '<div class="blank"></div>',
        "blocked": ph("Slowed down or blocked for a while. Wording and duration not defined (§8).") + '<div class="blank"></div>',
    }
    screens = "".join(
        f'<div data-state="{k}" class="{"" if k == "idle" else "hidden"}" style="display:flex;flex-direction:column;gap:10px;flex:1">{v}</div>'
        for k, v in states.items()
    )
    sim_phone = (
        '<div class="phone"><div class="sbar"></div>'
        '<div class="addr"><span class="url"><b>me.minmed.sg</b><span class="path" data-sim="path">/</span></span></div>'
        f'<div class="screen" id="simScreen">{screens}</div></div>'
    )
    return f"""
<div class="panel" id="captcha-sim">
<h3>Try it: what a scraper runs into</h3>
<p class="small" style="margin-top:0">The spec's own example: a CAPTCHA on the <b>fourth different card within 60 seconds</b> {badge("example")}. Real thresholds, time windows and cooldowns are {badge("pending")}, so after the first challenge this demo only shows <i>which</i> outcomes exist, not when they trigger.</p>
<div class="sim">
  <div>{sim_phone}</div>
  <div>
    <div class="small"><b>Different cards opened in the last 60 s:</b> <span id="simCount">0</span> / 4 {badge("example", mini=True)}</div>
    <div class="meter" style="margin:6px 0 4px"><i id="simMeter"></i></div>
    <div class="small muted">Simulated clock: <span id="simClock">0:00</span></div>
    <div class="ctrls">
      <button class="act primary" data-act="open">Open a different card</button>
      <button class="act" data-act="same">Reopen the same card</button>
      <button class="act" data-act="wait">Wait 60 seconds</button>
    </div>
    <div class="ctrls">
      <button class="act" data-act="pass">Pass the check</button>
      <button class="act" data-act="fail">Fail the check</button>
      <button class="act" data-act="keep">Keep scraping after passing</button>
      <button class="act" data-act="reset">Reset</button>
    </div>
    <div class="log" id="simLog" aria-live="polite"></div>
    <ul class="small" style="margin-top:10px">
      <li>Ordinary visitors pass straight through. Opening the same card again doesn't add to the count.</li>
      <li>Limits still apply after a pass, so one pass doesn't unlock the directory.</li>
      <li>Failed challenges are one of the signals the server weighs.</li>
      <li>There is no public staff list or bulk endpoint to scrape instead.</li>
    </ul>
  </div>
</div>
</div>"""


def token_checker():
    buttons = [
        ("fresh", "Fresh token"),
        ("reuse", "Reuse a token"),
        ("expired", "Token over 5 minutes old"),
        ("host", "Token from another site"),
        ("action", "Token for a different action"),
        ("direct", "Call the API directly"),
        ("ua", "Claim to be a search crawler"),
        ("ip", "Fake the client IP header"),
    ]
    btns = "".join(f'<button class="act" data-tok="{k}">{v}</button>' for k, v in buttons)
    ok_state = (
        '<div class="avatar">Photo<br>(optional)</div>'
        f'<p class="pname">{E(P["name"])}</p><p class="pco">Minmed</p>{st_active()}'
        '<div class="btn primary">Save contact</div><div class="blank"></div>'
    )
    no_state = (
        ph("Retry or status-unavailable message. Wording not defined.")
        + '<p class="small muted" style="font-size:11px;text-align:center">No protected data is released.</p><div class="blank"></div>'
    )
    tok_phone = (
        f'<div class="phone"><div class="sbar"></div>{addr()}<div class="screen" id="tokScreen">'
        '<div data-tok-state="idle" style="display:flex;flex-direction:column;gap:10px;flex:1"><div class="blank"></div><p class="small muted" style="text-align:center">Pick a request to send.</p><div class="blank"></div></div>'
        f'<div data-tok-state="ok" class="hidden" style="display:flex;flex-direction:column;gap:10px;flex:1">{ok_state}</div>'
        f'<div data-tok-state="no" class="hidden" style="display:flex;flex-direction:column;gap:10px;flex:1">{no_state}</div>'
        "</div></div>"
    )
    return f"""
<div class="panel" id="token-check">
<h3>Try it: how the server treats a CAPTCHA token</h3>
<p class="small" style="margin-top:0">When someone passes a challenge, their browser gets a token to send with the next request. Using the spec's {badge("candidate")} Cloudflare Turnstile, the server checks that the token is valid, single-use, under five minutes old and issued for the expected hostname and action.</p>
<div class="sim">
  <div>{tok_phone}</div>
  <div>
    <div class="ctrls">{btns}</div>
    <div class="log" id="tokLog" aria-live="polite"><div class="muted">Server checks appear here.</div></div>
  </div>
</div>
</div>"""


def shared_wifi():
    ppl = "".join(f'<span class="person">{c}</span>' for c in "ABCDE")
    return f"""
<div class="cmp">
  <div class="ipbox"><b>If the rule counted only by IP address</b> <span class="verdict no">Not preferred</span>
    <div class="people">{ppl}</div>
    <p class="small" style="margin:0">Five colleagues on the same office Wi-Fi each open one different card. To the server that's one IP address opening five different cards in a minute, which could look like scraping.</p></div>
  <div class="ipbox"><b>Counting per session, with IP as one signal</b> <span class="verdict ok">Preferred</span>
    <div class="people">{ppl}</div>
    <p class="small" style="margin:0">Each person has their own session that opened one card. Nobody looks automated. IP activity still counts, but as one signal, not as a person.</p></div>
</div>
<p class="small">If someone is caught anyway, the first response is a challenge, not a block. Shared-network complaints are tracked before thresholds are set.</p>"""


def impersonation():
    chat = (
        f'<div class="bubble"><div>Hi, it\'s Alex from Minmed. Here\'s my card.</div><div class="time">2:10 pm</div></div>'
        + wa_bubble(me=False, time="2:10 pm")
        + '<div class="bubble"><div>Please transfer the deposit to this account today so we can confirm your booking.</div><div class="time">2:11 pm</div></div>'
    )
    return f"""
<div class="cmp">
  <div>{phone(chat, top=chathead(phi("unknown number")), kind="chat", cap="An impersonator forwards a genuine link " + badge("sample", mini=True))}</div>
  <div>{phone(public_page(), top=addr(), cap="The genuine page still shows ✓ Active")}</div>
  <div class="panel small"><h3>What this shows</h3>
    <p>The link is genuine, so the page shows the real officer's details and official contacts on the Minmed domain.</p>
    <p><b>Active confirms the card, not the sender.</b> Anyone can forward a genuine link.</p>
    <p>For payments or personal data, confirm through a Minmed contact you already know. The How to verify panel {badge("proposed", mini=True)} says this.</p></div>
</div>"""


def altered_card():
    fake = ncard(desig="Director, Group Finance", mobile="+65 8999 0000", hl=("desig", "mobile"), hl_cls="hl-red", seed=7)
    return f"""
<div class="cmp">
  <div class="panel"><h3>Copied card image, altered</h3>{fake}
    <p class="small">Title and phone number changed in an image editor {badge("sample", mini=True)}. The genuine QR has been kept so it still looks real.</p></div>
  <div>{phone(public_page(), top=addr(), cap="The live page, when the recipient opens the link")}</div>
  <div class="panel small"><h3>Why the difference shows</h3>
    <p>The link and QR carry only the card ID:</p>
    <pre class="req">me.minmed.sg/<span class="ok">alex-tan</span>
<span class="c">no title, no phone number</span></pre>
    <p>Every opening triggers a live lookup, so the page always shows the real approved details. The tick appears only on the live page.</p>
    <p><b>Can't prevent:</b> a genuine QR pasted onto an altered image. It only helps if the recipient opens the link and compares.</p></div>
</div>"""


def lookalike():
    rows = [
        ("me.minmed.sg/alex-tan", True, "Exactly me.minmed.sg."),
        ("me-minmed.sg.example/alex-tan", False, "A hyphen instead of a dot makes it a different site."),
        ("me.minmed.sg.card-check.example/alex-tan", False, "Starts with me.minmed.sg but the real site is card-check.example."),
        ("minmed-namecards.example/alex-tan", False, "Mentions Minmed but isn't me.minmed.sg."),
        ("me.minmed.sg.example/alex-tan", False, "Extra ending after .sg. Different site."),
    ]
    out = "".join(
        f'<div class="row"><span class="verdict {"ok" if ok else "no"}">{"Genuine" if ok else "Not genuine"}</span>'
        f'<span class="u">{E(u)}</span><span class="small muted">{E(why)}</span></div>'
        for u, ok, why in rows
    )
    fake_page = phone(public_page(), top=addr("me-minmed.sg.example", fake=True), cap="Copied design, wrong address")
    return f"""
<div class="cmp">
  <div>{fake_page}</div>
  <div><div class="addr-test">{out}</div>
  <p class="small muted">Look-alike addresses here are made up and use the reserved <code>.example</code> ending.</p>
  <p class="small">Branding can be copied, so the design proves nothing. <b>me.minmed.sg</b> is the only verification reference, and the How to verify panel {badge("proposed", mini=True)} tells recipients to check the address bar.</p></div>
</div>"""


def edit_other():
    return f"""
<div class="cmp">
<pre class="req"><span class="c"># Illustrative request, not the real API</span>
Change card:   bea-lim
Signed in as:  alex.tan@minmed.sg

Server checks
  Identity (Google, company account)  <span class="ok">pass</span>
  Staff directory match              <span class="ok">pass</span>
  Owns card bea-lim?                 <span class="no">fail</span>

Result: <span class="no">refused</span></pre>
<pre class="req"><span class="c"># Illustrative request, not the real API</span>
Sign in with:  someone@example.com
Typed email:   bea.lim@minmed.sg

Server checks
  Identity (Google, company account)  <span class="no">fail</span>
  Typed email address                <span class="c">not proof</span>

Result: <span class="no">refused</span></pre>
<div class="panel small"><h3>Why hiding buttons isn't enough</h3><p>Anyone can send a request without using the app's buttons. So identity, directory match and ownership are checked on the server for every request.</p></div>
</div>"""


def field_filter():
    stored = [
        ("Name", True), ("Designation", True), ("Work email", True), ("Mobile, if published", True),
        ("Photo, if added", True), ("Biography, languages, LinkedIn, if added", True),
        ("Mobile the officer chose not to publish", False), ("Pending edits", False), ("Admin logs", False),
    ]
    chips = "".join(f'<span class="chip {"pub" if ok else "priv"}">{E(n)}</span>' for n, ok in stored)
    outs = "".join(f'<span class="chip pub">{o}</span>' for o in ["Live web page", "WhatsApp preview", "Contact file (Save contact)", "Card image"])
    return f"""
<div class="panel"><div class="fields">
  <div><b>Stored for the card</b><div>{chips}</div></div>
  <div class="arrow">→</div>
  <div><div class="node ok"><b>Explicit list of public fields (on the server)</b>Only approved public fields pass. All outputs are generated from the same approved version.</div>
  <div style="margin-top:8px"><b>Outputs</b><div>{outs}</div></div></div>
</div>
<p class="small" style="margin-bottom:0">A withheld mobile is absent from every output, its metadata and its image files. A launch check confirms this. The field list shown is the one in §4; the full stored record isn't described in the spec.</p></div>"""


def search_vis():
    return f"""
<div class="cmp">
  <div class="panel small"><h3>What's done</h3><ul>
    <li>Each staff page is set to <b>noindex</b>.</li>
    <li>Staff pages are left out of the sitemap.</li>
    <li>Every staff page, image and alternate address is checked before launch.</li></ul></div>
  <div class="panel small"><h3>What it isn't</h3><ul>
    <li>noindex is an instruction to search engines. Well-behaved ones follow it.</li>
    <li>It isn't access control: anyone with the link can still open the page.</li>
    <li>It doesn't stop scraping. That's what the measures in §7.7 are for.</li></ul></div>
</div>"""


def outage_vis():
    err = (
        '<div class="avatar" style="opacity:.4">—</div>' + st_error()
        + ph("Explanation under the error not defined.") + '<div class="blank"></div>'
    )
    return f"""
<div class="cmp">
  <div>{phone(err, top=addr(), cap="Live check failed")}</div>
  <div class="panel small"><h3>The page never</h3><ul>
    <li>shows a fresh ✓ Active when the check didn't succeed</li>
    <li>claims the person has left</li>
    <li>releases a protected response</li></ul>
    <p>The recipient is told to try again later. For staff, nothing about the card changes.</p></div>
</div>"""


def preview_timeline():
    return f"""
<div class="cmp">
<div class="panel"><ol class="timeline">
  <li><b>Day 1.</b> Officer shares the link. WhatsApp stores a preview snapshot.</li>
  <li class="amber"><b>Day 10.</b> A change is approved. The preview image updates, so <i>new</i> shares show the new details. The Day 1 message still shows the old snapshot.</li>
  <li class="red"><b>Day 40.</b> Officer leaves. New preview images are refused {badge("proposed", mini=True)}. Old messages still show the Day 1 snapshot.</li>
  <li class="green"><b>Any day.</b> Tapping the link opens the live page, which always shows the current state.</li>
</ol></div>
<div>{phone(wa_bubble(me=False, time="Day 1"), top=chathead(P["name"]), kind="chat", cap="Old preview: no tick, never claims to be verified")}</div>
</div>"""


def admin_vis():
    mail = email_phone(
        "manage@minmed.sg", "subject not defined",
        ph("Email wording not defined.")
        + '<dl class="kv"><div><dt>Account</dt><dd style="margin:0">' + phi("responsible administrator") + "</dd></div>"
        + '<div><dt>Card</dt><dd style="margin:0">me.minmed.sg/' + P["slug"] + "</dd></div>"
        + '<div><dt>Time</dt><dd style="margin:0">' + phi("time") + "</dd></div></dl>",
        cap="Sent for every deactivation and administrator edit",
    )
    return f"""
<div class="cmp">
  <div>{mail}</div>
  <div class="panel small"><h3>If the email fails</h3>
    <p style="margin:0">The saved approval or deactivation stands. A failed email never reverses it.</p></div>
</div>"""


def tick_rules():
    items = [
        ("Live page after a successful check", True, "✓ with the check time"),
        ("Card image (downloaded)", False, "No tick, stamp or seal"),
        ("QR download", False, "No tick, stamp or seal"),
        ("WhatsApp preview", False, "No tick, stamp or seal"),
        ("Card unavailable / verification error", False, "Different icons, never the tick"),
    ]
    rows = "".join(
        f'<div class="row"><span class="verdict {"ok" if ok else "no"}">{"Tick" if ok else "No tick"}</span>'
        f'<span class="u" style="font-family:inherit">{E(a)}</span><span class="small muted">{E(b)}</span></div>'
        for a, ok, b in items
    )
    return f"""
<div class="cmp">
  <div class="addr-test">{rows}</div>
  <div class="panel small"><p>Copies can be shared after the person has left, and they'd still look valid. That's why only the live page ever carries a tick.</p>
  <p>The page never uses the word <b>"Verified"</b>, so it doesn't suggest the sender's identity has been checked.</p></div>
</div>"""


def checks_vis():
    return """
<div class="cmp">
  <div class="panel small"><h3>Ways to check a card is genuine</h3><ol>
    <li><b>Address bar</b> reads exactly me.minmed.sg.</li>
    <li><b>Status</b> shows ✓ Active staff profile with a check time from when you opened the page.</li>
    <li><b>Details</b> match what you were given. If they differ, trust the live page.</li>
    <li><b>How to verify panel</b> (Proposed) lists these checks.</li>
    <li><b>Open it yourself</b>: tap the link or scan the QR rather than trusting an image.</li>
    <li><b>Sensitive requests</b>: confirm through a Minmed contact you already know.</li></ol></div>
  <div class="panel small"><h3>Not proof on their own</h3><ul>
    <li>The WhatsApp preview</li><li>A screenshot</li><li>A downloaded card image</li><li>A saved contact</li><li>A QR code</li><li>A page that looks like Minmed's</li></ul>
    <p>Pending: signed links, and watermark, reference or date labels on downloads.</p></div>
</div>"""


def security_page():
    toc = [
        ("gateway", "Gateway and error messages"), ("path", "How a request travels"),
        ("s1", "7.1 Impersonation"), ("s2", "7.2 Altered card"), ("s3", "7.3 Look-alike website"),
        ("s4", "7.4 Staff member leaves"), ("s5", "7.5 Unauthorised details"), ("s6", "7.6 Editing someone else's card"),
        ("s7", "7.7 Bots and CAPTCHA (simulator)"), ("s8", "7.8 Getting around the checks (token checker)"),
        ("s9", "7.9 Shared office Wi-Fi"), ("s10", "7.10 Private information"), ("s11", "7.11 Search results"),
        ("s12", "7.12 Outage"), ("s13", "7.13 Outdated WhatsApp preview"), ("s14", "7.14 Administrator misuse"),
        ("ticks", "Tick rules and checks"),
    ]
    toc_html = '<ol class="toc">' + "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc) + "</ol>"

    sections = [
        sec("s1", "7.1", "Someone pretends to be a Minmed staff member",
            ["An impersonator forwards a genuine card link or makes a fake card.", "A genuine link still shows the real officer's details and official contacts."],
            ["Before approval, the server checks the officer's company Google account against the staff directory.",
             "The live page shows official contact details on the Minmed domain.",
             f"The How to verify panel {badge('proposed', mini=True)} tells recipients to confirm sensitive requests through a contact they already know."],
            ["Anyone can forward a genuine link. Active confirms the card, not the sender."],
            impersonation()),
        sec("s2", "7.2", "A copied card is altered",
            ["When the recipient opens the link, the live page shows the real approved details, and the difference is visible."],
            ["The link carries only a card ID, never the editable title or number.", "Every opening triggers a live lookup.",
             "The official URL and QR are on the card, and the tick appears only on the live page."],
            ["A genuine QR can be pasted onto an altered image. It only helps if the recipient opens the link and compares."],
            altered_card()),
        sec("s3", "7.3", "A fake look-alike website",
            ["A fake site copies Minmed's design to collect details or payments."],
            ["me.minmed.sg is the only verification reference.", f"The How to verify panel {badge('proposed', mini=True)} tells recipients to check the address bar."],
            ["Branding can be copied. Recipients still have to check the address."],
            lookalike()),
        sec("s4", "7.4", "A staff member leaves",
            ["The live link shows Card unavailable and the departure notice.", "The officer can no longer share the card."],
            ["Deactivation is immediate and central.",
             f"New contact and card downloads stop, new WhatsApp preview images are refused, controlled caches are cleared {badge('proposed', mini=True)}.",
             "Every download re-checks status.", "manage@minmed.sg is notified and an audit record is kept."],
            ["Old WhatsApp messages, saved images and saved contacts can't be erased remotely.",
             f"Who triggers offboarding and how quickly: {badge('pending', mini=True)}"],
            '<p><a href="3-left-minmed.html">See the full flow on page 3 →</a></p>'),
        sec("s5", "7.5", "A staff member publishes unauthorised or wrong details",
            ["The change stays pending and is not public until approved."],
            ["Name, designation and contact changes need approval.", "The server checks ownership and reviewer permissions.",
             "Approval applies only to the exact version reviewed, and editing during review restarts it.", "Pending edits are never public."],
            [f"Whether photo, biography, languages and LinkedIn changes need approval: {badge('pending', mini=True)}. Proposed: review all public changes."],
            '<p><a href="2-pending-change.html">See the full flow on page 2 →</a></p>'),
        sec("s6", "7.6", "Someone edits another officer's card, or signs in with a non-Minmed account",
            ["The request is refused."],
            ["Identity, directory match and ownership are checked on the server for every request, not only by hiding buttons.",
             "A typed email address is never accepted as proof."],
            [], edit_other()),
        sec("s7", "7.7", "Bots harvesting the staff list or guessing names",
            ["Ordinary visitors pass straight through.", "Suspicious traffic gets a CAPTCHA.", "Repeated abuse is throttled or blocked for a cooldown period."],
            ["No public staff list or bulk endpoint.", "The server counts every profile-data and download request.",
             "Each request is assessed on per-session limits, IP activity, how many different cards are requested and failed challenges.",
             "Limits still apply after a CAPTCHA pass.", "Unapproved cards return the same not-found response as links that don't exist."],
            ["The WhatsApp preview is public by design and can be read by scrapers.",
             "CAPTCHA-solving services and slow, spread-out scraping can still copy public details. No promise of zero scraping.",
             f"Thresholds, time windows and cooldowns: {badge('pending', mini=True)}"],
            captcha_sim()),
        sec("s8", "7.8", "Attempts to get around the checks",
            ["Reused tokens, direct API calls and fake crawler identities are rejected, or the user gets a retry message.", "No protected data is released."],
            [f"{badge('candidate', mini=True)} Cloudflare Turnstile, validated on the server. Tokens are single-use, expire after five minutes, and are checked against the expected hostname and action.",
             "Invalid, expired and reused tokens are rejected.", "The Base44 and origin APIs are protected as well as the public domain.",
             "Client IP information is trusted only from the chosen gateway.", "A User-Agent claiming to be a trusted crawler is not taken as proof."],
            ["Base44 requires DNS-only records, so Cloudflare's firewall isn't automatically in front of the app.",
             f"CAPTCHA provider, gateway design and deployment: {badge('pending', mini=True)}"],
            token_checker()),
        sec("s9", "7.9", "Genuine visitors on shared office Wi-Fi get challenged",
            ["Several real people behind one IP could trigger checks."],
            ["Per-session limits are preferred over IP-only rules. IP is one signal, not a person.",
             "The first response is a challenge, not a block.", "Shared-network complaints are tracked before thresholds are set."],
            ["Some friction is possible until thresholds are tuned."],
            shared_wifi()),
        sec("s10", "7.10", "Private information leaks",
            ["Only approved public fields are ever returned to the public."],
            ["An explicit list of public fields.", "The website, WhatsApp preview, contact file and card image are all generated from the same approved version.",
             "A withheld mobile is absent from every output, its metadata and its image files.", "The server filters fields, and a launch check confirms this."],
            [], field_filter()),
        sec("s11", "7.11", "Profiles appear in search results",
            [], ["Each page is set to noindex and excluded from the sitemap.", "Every staff page, image and alternate address is checked before launch."],
            ["This is an instruction to search engines, not access control or protection from scraping."],
            search_vis()),
        sec("s12", "7.12", "The live check fails (outage)",
            ["Recipients see a temporary verification error."],
            ["The page never shows a fresh Active result or claims the person has left when the check fails.", "No protected response is released."],
            [], outage_vis()),
        sec("s13", "7.13", "An outdated WhatsApp preview after an update or departure",
            ["Old messages may still show old details."],
            ["The preview never claims to be verified.", f'It says "Open link for current details." {badge("proposed", mini=True)}',
             "The preview image updates on approval.", "New images are refused after deactivation."],
            ["Previously sent messages and third-party caches may keep the old image."],
            preview_timeline()),
        sec("s14", "7.14", "Administrator misuse or mistakes",
            [], ["Deactivations and administrator edits are emailed to manage@minmed.sg with the responsible account, the card and the time.",
                 "An audit record is kept.", "An email failure never reverses a saved approval or deactivation."],
            [f"Extra reviewers, and whether administrator edits need independent approval: {badge('pending', mini=True)}"],
            admin_vis()),
    ]

    body = f"""
<div class="eyebrow">Page 4</div>
<h1>Security measures, explained</h1>
<p class="lede">Each scenario from spec §7: what happens, how it's reduced, what can't be prevented, and a picture or a hands-on demo of the measure.</p>
{legend()}
<div class="panel" style="margin-top:16px"><h3>On this page</h3>{toc_html}</div>
<section class="section" id="gateway"><div class="eyebrow">Read first</div><h2>Gateway and error messages</h2>{gateway_explainer()}</section>
<section class="section" id="path"><div class="eyebrow">Overview</div><h2>Where each check happens</h2>{request_path()}</section>
{"".join(sections)}
<section class="section sec" id="ticks"><div class="eyebrow">§5.3 and §6</div><h2>Tick rules {badge("proposed")} and how recipients check a card</h2>{tick_rules()}<div style="height:14px"></div>{checks_vis()}</section>
"""
    js = (SRC / "security.js").read_text()
    return page("4-security.html", "Name Card Security",
                "Security measures for Minmed Digital Name Cards with visual explanations, from spec draft 0.2.", body, js)
