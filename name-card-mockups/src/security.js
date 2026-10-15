(function () {
  // ---------------- CAPTCHA simulator (spec 7.7). Threshold of 4 is the spec's example only.
  var sim = document.getElementById("captcha-sim");
  if (sim) {
    var CARDS = ["alex-tan", "bea-lim", "chen-wei", "dina-rahman", "evan-ng", "farah-ali", "gopal-k", "hui-min", "ivan-ong", "jia-hui"];
    var EXAMPLE_LIMIT = 4;
    var s;

    function fresh() {
      return { clock: 0, opens: [], next: 0, last: null, held: null, state: "idle", passed: 0 };
    }
    function fmt(t) {
      var m = Math.floor(t / 60), sec = t % 60;
      return m + ":" + (sec < 10 ? "0" : "") + sec;
    }
    function title(slug) {
      return slug.split("-").map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(" ");
    }
    function distinct(extra) {
      var seen = {};
      s.opens.forEach(function (o) { if (o.t > s.clock - 60) seen[o.c] = 1; });
      if (extra) seen[extra] = 1;
      return Object.keys(seen).length;
    }
    function log(msg, cls) {
      var box = document.getElementById("simLog");
      var d = document.createElement("div");
      if (cls) d.className = cls;
      d.textContent = fmt(s.clock) + "  " + msg;
      box.prepend(d);
    }
    function show(state, slug) {
      s.state = state;
      sim.querySelectorAll("[data-state]").forEach(function (el) {
        el.classList.toggle("hidden", el.getAttribute("data-state") !== state);
      });
      sim.querySelector('[data-sim="path"]').textContent = slug ? "/" + slug : "/";
      if (slug) {
        sim.querySelector('[data-sim="name"]').textContent = title(slug) + " (sample)";
        sim.querySelector('[data-sim="time"]').textContent = fmt(s.clock);
      }
      render();
    }
    function render() {
      var n = distinct(s.state === "challenge" ? s.held : null);
      document.getElementById("simCount").textContent = n;
      document.getElementById("simClock").textContent = fmt(s.clock);
      var m = document.getElementById("simMeter");
      m.style.width = Math.min(100, (n / EXAMPLE_LIMIT) * 100) + "%";
      m.style.background = n >= EXAMPLE_LIMIT ? "var(--red)" : n >= EXAMPLE_LIMIT - 1 ? "var(--amber)" : "var(--green)";
      var st = s.state;
      sim.querySelector('[data-act="pass"]').disabled = st !== "challenge";
      sim.querySelector('[data-act="fail"]').disabled = st !== "challenge";
      sim.querySelector('[data-act="keep"]').disabled = s.passed === 0 || st === "blocked";
      sim.querySelector('[data-act="open"]').disabled = st === "challenge" || st === "blocked";
      sim.querySelector('[data-act="same"]').disabled = !s.last || st === "challenge" || st === "blocked";
    }
    function openCard(slug) {
      s.opens.push({ c: slug, t: s.clock });
      s.last = slug;
      show("card", slug);
    }

    var actions = {
      open: function () {
        s.clock += 5;
        var slug = CARDS[s.next % CARDS.length];
        s.next++;
        var n = distinct(slug);
        if (s.passed === 0 && n >= EXAMPLE_LIMIT) {
          s.held = slug;
          log("Request for /" + slug + " is card number " + n + " in 60 s: CAPTCHA check shown (example threshold)", "warn");
          show("challenge", slug);
          return;
        }
        log("Opened /" + slug + ". Different cards in the last 60 s: " + n + (s.passed ? ". Still counted after the pass." : ""), "ok");
        openCard(slug);
      },
      same: function () {
        s.clock += 5;
        log("Reopened /" + s.last + ". Same card, so the count stays at " + distinct(), "ok");
        openCard(s.last);
      },
      wait: function () {
        s.clock += 60;
        if (s.state === "blocked") {
          log("Waited. Real cooldown length is Pending; this demo lifts it here.", "warn");
          s.passed = 0;
          show("idle");
          return;
        }
        log("Waited 60 s. Older openings drop out of the window.");
        render();
      },
      pass: function () {
        s.passed++;
        log("Check passed. Token validated on the server, /" + s.held + " released. Limits still apply.", "ok");
        var slug = s.held;
        s.held = null;
        openCard(slug);
      },
      fail: function () {
        log("Check failed. Failed challenges are one of the signals the server weighs. Nothing released.", "no");
        s.held = null;
        show("retry");
      },
      keep: function () {
        s.clock += 5;
        log("Repeated suspicious activity: slowed down or blocked. Thresholds and cooldown are Pending.", "no");
        show("blocked");
      },
      reset: function () {
        s = fresh();
        document.getElementById("simLog").innerHTML = "";
        show("idle");
      },
    };
    sim.querySelectorAll("[data-act]").forEach(function (b) {
      b.addEventListener("click", function () { actions[b.getAttribute("data-act")](); });
    });
    s = fresh();
    show("idle");
  }

  // ---------------- token checker (spec 7.8). Turnstile is a candidate only.
  var tok = document.getElementById("token-check");
  if (tok) {
    // Each check: [text, result] where result is "ok", "no" or "info".
    var SCEN = {
      fresh: { checks: [["Token present", "ok"], ["Server validation: genuine, not used before, issued 40 s ago (under 5 minutes)", "ok"], ["Hostname check: issued for me.minmed.sg", "ok"], ["Action check: issued for the expected action", "ok"]], ok: true, end: "Accepted. Card data released, still subject to rate limits." },
      reuse: { checks: [["Token present", "ok"], ["Server validation: tokens are single-use and this one was already used", "no"]], end: "Rejected: token already used." },
      expired: { checks: [["Token present", "ok"], ["Server validation: issued 6 min 10 s ago, over 5 minutes", "no"]], end: "Rejected: token expired." },
      host: { checks: [["Token present", "ok"], ["Server validation: genuine and unused", "ok"], ["Hostname check: issued for a different site, not me.minmed.sg", "no"]], end: "Rejected: wrong hostname." },
      action: { checks: [["Token present", "ok"], ["Server validation: genuine and unused", "ok"], ["Hostname check: issued for me.minmed.sg", "ok"], ["Action check: issued for a different action", "no"]], end: "Rejected: wrong action." },
      direct: { checks: [["Request goes straight to the Base44 or origin API, skipping the public address", "info"], ["The Base44 and origin APIs must be protected as well as the public domain", "ok"], ["How that protection is deployed is Pending (Base44 needs DNS-only records, so it isn't automatic)", "info"]], end: "Intended result: rejected. Mechanism Pending." },
      ua: { checks: [["User-Agent says it is a trusted search crawler", "info"], ["A User-Agent string is not taken as proof", "ok"], ["Normal checks apply: no valid token", "no"]], end: "Rejected: no special treatment for a claimed crawler." },
      ip: { checks: [["Client sends its own client-IP header", "info"], ["Client IP is trusted only from the chosen gateway, so the header is ignored", "ok"], ["Rate limits use the IP the gateway reports", "ok"]], end: "No effect: faking the header doesn't reset limits.", neutral: true },
    };
    var logBox = document.getElementById("tokLog");
    function showTok(state) {
      tok.querySelectorAll("[data-tok-state]").forEach(function (el) {
        el.classList.toggle("hidden", el.getAttribute("data-tok-state") !== state);
      });
    }
    tok.querySelectorAll("[data-tok]").forEach(function (b) {
      b.addEventListener("click", function () {
        var sc = SCEN[b.getAttribute("data-tok")];
        logBox.innerHTML = "";
        var head = document.createElement("div");
        head.textContent = "> " + b.textContent;
        head.style.fontWeight = "700";
        logBox.appendChild(head);
        sc.checks.forEach(function (c) {
          var d = document.createElement("div");
          d.className = c[1] === "info" ? "" : c[1];
          d.textContent = (c[1] === "ok" ? "PASS  " : c[1] === "no" ? "FAIL  " : "NOTE  ") + c[0];
          logBox.appendChild(d);
        });
        var end = document.createElement("div");
        end.className = sc.ok ? "ok" : sc.neutral ? "warn" : "no";
        end.style.fontWeight = "700";
        end.textContent = "= " + sc.end;
        logBox.appendChild(end);
        if (!sc.neutral) showTok(sc.ok ? "ok" : "no");
      });
    });
  }
})();
