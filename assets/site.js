// Copy buttons, theme switch and contents highlighting. No dependencies.
(function () {
  "use strict";

  var data = JSON.parse(document.getElementById("thread-data").textContent);
  var toast = document.getElementById("toast");
  var toastTimer;

  function say(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 1600);
  }

  function legacyCopy(text) {
    var t = document.createElement("textarea");
    t.value = text;
    t.setAttribute("readonly", "");
    t.style.position = "fixed";
    t.style.opacity = "0";
    document.body.appendChild(t);
    t.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    t.remove();
    return ok;
  }

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; },
        function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }

  function flash(btn, ok) {
    var label = btn.querySelector(".label") || btn;
    var original = label.textContent;
    label.textContent = ok ? "Copied" : "Press Ctrl+C";
    btn.classList.add("done");
    setTimeout(function () { label.textContent = original; btn.classList.remove("done"); }, 1500);
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    var kind = btn.getAttribute("data-copy");
    var text, msg;
    if (kind === "all") {
      text = data.map(function (p, i) { return (i + 1) + "/" + data.length + "\n\n" + p.text; }).join("\n\n\n");
      msg = "Whole thread copied";
    } else {
      var i = Number(btn.getAttribute("data-index"));
      text = data[i][kind];
      msg = (kind === "alt" ? "Alt text for post " : "Post ") + (i + 1) + " copied";
    }
    copy(text).then(function (ok) {
      flash(btn, ok);
      say(ok ? msg : "Copy blocked by the browser. Select the text instead.");
    });
  });

  // Theme: follows the system until the reader picks one.
  var root = document.documentElement;
  var themeBtn = document.getElementById("theme-btn");
  function current() {
    var set = root.getAttribute("data-theme");
    if (set) return set;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }
  function label() {
    var light = current() === "light";
    var text = light ? "Switch to dark theme" : "Switch to light theme";
    themeBtn.classList.toggle("is-light", light);
    themeBtn.setAttribute("aria-label", text);
    themeBtn.setAttribute("title", text);
  }
  try {
    var saved = localStorage.getItem("rb-theme");
    if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  } catch (e) { /* storage blocked: keep the system theme */ }
  label();
  themeBtn.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("rb-theme", next); } catch (e) { /* ignore */ }
    label();
  });

  // Back to top: shows once the reader has scrolled past the hero.
  var toTop = document.getElementById("to-top");
  function onScroll() { toTop.classList.toggle("show", window.scrollY > 600); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  toTop.addEventListener("click", function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
    document.querySelector(".logo").focus({ preventScroll: true });
  });

  // Highlight the contents entry for the section in view.
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    targets.forEach(function (t) { if (t) io.observe(t); });
  }
})();
