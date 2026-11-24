/* Solar Installation Bahria Town Lahore — site interactions
   No backend: the contact form composes a WhatsApp message and
   opens wa.me so the visitor sends the enquiry themselves. */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Sticky header state ---------- */
  var header = $(".site-header");
  var backTop = $("#backTop");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 40);
    if (backTop) backTop.classList.toggle("show", y > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile drawer ---------- */
  var toggle = $("#menuToggle");
  var drawer = $("#mobileDrawer");
  var overlay = $("#drawerOverlay");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("open", open);
    if (overlay) overlay.classList.toggle("show", open);
    if (toggle) {
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (toggle) toggle.addEventListener("click", function () { setDrawer(!drawer.classList.contains("open")); });
  if (overlay) overlay.addEventListener("click", function () { setDrawer(false); });
  $$("#mobileDrawer a").forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { setDrawer(false); closeLightbox(); } });

  /* ---------- Back to top ---------- */
  if (backTop) backTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var revealEls = $$(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visible"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------- FAQ accordion ---------- */
  $$(".faq-item").forEach(function (item) {
    var q = $(".faq-q", item);
    var a = $(".faq-a", item);
    if (!q || !a) return;
    q.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      $$(".faq-item.open").forEach(function (other) {
        other.classList.remove("open");
        var oa = $(".faq-a", other);
        if (oa) oa.style.maxHeight = null;
        var oq = $(".faq-q", other);
        if (oq) oq.setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("open");
        a.style.maxHeight = a.scrollHeight + "px";
        q.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* ---------- Gallery: filters + lightbox ---------- */
  var lightbox = $("#lightbox");
  var lbImg = $("#lbImg");
  var lbCap = $("#lbCap");
  function closeLightbox() {
    if (lightbox) lightbox.classList.remove("open");
    document.body.style.overflow = "";
  }
  $$(".gallery figure").forEach(function (fig) {
    fig.addEventListener("click", function () {
      var img = $("img", fig);
      var cap = $("figcaption", fig);
      if (!img || !lightbox) return;
      lbImg.src = img.dataset.full || img.src;
      lbImg.alt = img.alt;
      lbCap.textContent = cap ? cap.textContent : img.alt;
      lightbox.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  });
  var lbClose = $("#lbClose");
  if (lbClose) lbClose.addEventListener("click", closeLightbox);
  if (lightbox) lightbox.addEventListener("click", function (e) { if (e.target === lightbox) closeLightbox(); });

  $$(".filter-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      $$(".filter-btn").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var cat = btn.getAttribute("data-filter");
      $$(".gallery figure").forEach(function (fig) {
        var show = cat === "all" || fig.getAttribute("data-cat") === cat;
        fig.style.display = show ? "" : "none";
      });
    });
  });

  /* ---------- Blog search ---------- */
  var searchInput = $("#blogSearch");
  var noResults = $("#noResults");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      var q = searchInput.value.trim().toLowerCase();
      var visible = 0;
      $$(".post-card").forEach(function (card) {
        var hay = (card.textContent || "").toLowerCase();
        var show = !q || hay.indexOf(q) !== -1;
        card.style.display = show ? "" : "none";
        if (show) visible++;
      });
      if (noResults) noResults.style.display = visible ? "none" : "block";
    });
  }

  /* ---------- Contact form: validate, then open WhatsApp ---------- */
  var form = $("#contactForm");
  if (form) {
    var WA_NUMBER = "923200147783";
    function setErr(input, bad) {
      var field = input.closest(".field");
      if (field) field.classList.toggle("invalid", !!bad);
      return !bad;
    }
    function validPhone(v) {
      var digits = v.replace(/[^0-9]/g, "");
      return digits.length >= 10 && digits.length <= 13;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      /* Honeypot: if filled, a bot filled it — silently stop. */
      var hp = $("#hpWebsite");
      if (hp && hp.value) return;

      var name = $("#fName"), phone = $("#fPhone"), email = $("#fEmail"),
          ptype = $("#fProperty"), system = $("#fSystem"), msg = $("#fMessage");
      var ok = true;
      ok = setErr(name, !name.value.trim()) && ok;
      ok = setErr(phone, !validPhone(phone.value)) && ok;
      ok = setErr(email, email.value.trim() !== "" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) && ok;
      ok = setErr(ptype, !ptype.value) && ok;
      ok = setErr(system, !system.value) && ok;
      ok = setErr(msg, !msg.value.trim()) && ok;
      if (!ok) {
        var firstBad = $(".field.invalid input, .field.invalid select, .field.invalid textarea");
        if (firstBad) firstBad.focus();
        return;
      }

      var lines = [
        "Hello Solar Installation Bahria Town Lahore,",
        "I would like a free solar consultation.",
        "",
        "Name: " + name.value.trim(),
        "Phone: " + phone.value.trim(),
        "Email: " + (email.value.trim() || "Not provided"),
        "Property type: " + ptype.value,
        "Solar system required: " + system.value,
        "",
        "Message:",
        msg.value.trim()
      ];
      var waUrl = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));
      var status = $("#formStatus");
      var opened = window.open(waUrl, "_blank", "noopener");
      if (status) {
        status.innerHTML = "Your enquiry is ready in WhatsApp — please press <strong>Send</strong> in WhatsApp to deliver it to Solar Installation Bahria Town Lahore. " +
          "If WhatsApp did not open, <a href=\"" + waUrl + "\" target=\"_blank\" rel=\"noopener\">tap here to open it</a>. " +
          "No details were sent anywhere else.";
        status.classList.add("show");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      if (!opened && status) {
        status.innerHTML = "WhatsApp did not open automatically (your browser may have blocked the pop-up). " +
          "Please <a href=\"" + waUrl + "\" target=\"_blank\" rel=\"noopener\">tap here to open WhatsApp</a> and send your enquiry. " +
          "No details were sent anywhere else.";
      }
    });
    /* Clear error state as the visitor types. */
    $$("#contactForm input, #contactForm select, #contactForm textarea").forEach(function (el) {
      el.addEventListener("input", function () { setErr(el, false); });
      el.addEventListener("change", function () { setErr(el, false); });
    });
  }

  /* ---------- Footer year ---------- */
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
