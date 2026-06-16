/**
 * home.js — Portfolio animations & interactions
 * Dependencies: GSAP + ScrollTrigger (loaded before this script)
 *
 * Sections:
 *  1. GSAP setup
 *  2. Hero entrance timeline
 *  3. Scroll-reveal for [data-reveal] elements
 *  4. Stat counters
 *  5. Skill bar fills
 *  6. Resume tab switcher
 *  7. Project filter
 *  8. Contact form (fetch + CSRF)
 *  9. Role cycling
 */

(function () {
  "use strict";

  /* ── 1. GSAP setup ─────────────────────────────────────────── */
  if (typeof gsap === "undefined") {
    console.warn("home.js: GSAP not loaded — animations disabled.");
    document.querySelectorAll("[data-reveal]").forEach((el) => {
      el.style.opacity = 1;
      el.style.transform = "none";
    });
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  /* ── 2. Hero entrance ──────────────────────────────────────── */
  const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

  heroTl
    .to(".hero-eyebrow", { opacity: 1, y: 0, duration: 0.6 }, 0.2)
    .to(".name-char", {
      opacity: 1,
      y: 0,
      duration: 0.55,
      stagger: 0.03,
      ease: "power4.out",
    }, 0.5)
    .to(".hero-roles", { opacity: 1, y: 0, duration: 0.5 }, 0.9)
    .to(".hero-tagline", { opacity: 1, y: 0, duration: 0.5 }, 1.0)
    .to(".hero-stats",   { opacity: 1, y: 0, duration: 0.5 }, 1.1)
    .to(".hero-ctas",    { opacity: 1, y: 0, duration: 0.5 }, 1.2)
    .to(".hero-social",  { opacity: 1, y: 0, duration: 0.5 }, 1.3);

  /* ── 3. Scroll-reveal ──────────────────────────────────────── */
  document.querySelectorAll("[data-reveal]").forEach((el) => {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.7,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 88%",
        once: true,
      },
    });
  });

  /* ── 4. Stat counters ──────────────────────────────────────── */
  document.querySelectorAll(".stat-value[data-target]").forEach((el) => {
    const target = parseInt(el.dataset.target, 10);
    ScrollTrigger.create({
      trigger: el,
      start: "top 90%",
      once: true,
      onEnter() {
        gsap.to({ val: 0 }, {
          val: target,
          duration: 1.4,
          ease: "power2.out",
          onUpdate() {
            el.textContent = Math.round(this.targets()[0].val);
          },
          onComplete() {
            el.textContent = target;
          },
        });
      },
    });
  });

  /* ── 5. Skill bar fills ────────────────────────────────────── */
  document.querySelectorAll(".skill-fill[data-percent]").forEach((bar) => {
    const pct = bar.dataset.percent + "%";
    ScrollTrigger.create({
      trigger: bar,
      start: "top 92%",
      once: true,
      onEnter() {
        gsap.to(bar, { width: pct, duration: 1.2, ease: "power2.out" });
      },
    });
  });

  /* ── 6. Resume tab switcher ─────────────────────────────────── */
  const tabs    = document.querySelectorAll(".resume-tab");
  const panels  = document.querySelectorAll(".resume-panel");
  const ink     = document.querySelector(".tab-ink");

  function moveInk(tab) {
    if (!ink) return;
    ink.style.left  = tab.offsetLeft + "px";
    ink.style.width = tab.offsetWidth + "px";
  }

  function activateTab(tab) {
    tabs.forEach((t) => {
      t.classList.remove("active");
      t.setAttribute("aria-selected", "false");
    });
    panels.forEach((p) => p.classList.remove("active"));

    tab.classList.add("active");
    tab.setAttribute("aria-selected", "true");
    const panel = document.getElementById(tab.dataset.target);
    if (panel) {
      panel.classList.add("active");
      // Trigger skill bars in newly revealed panel
      panel.querySelectorAll(".skill-fill[data-percent]").forEach((bar) => {
        if (bar.style.width === "0%" || bar.style.width === "") {
          gsap.to(bar, { width: bar.dataset.percent + "%", duration: 1.2, ease: "power2.out" });
        }
      });
    }
    moveInk(tab);
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => activateTab(tab));
  });

  // Init ink position
  const activeTab = document.querySelector(".resume-tab.active");
  if (activeTab) requestAnimationFrame(() => moveInk(activeTab));

  /* ── 7. Project filter ─────────────────────────────────────── */
  const filterChips = document.querySelectorAll(".filter-chip");
  const projectRows = document.querySelectorAll(".project-row");

  filterChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      filterChips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");

      const filter = chip.dataset.filter;
      projectRows.forEach((row) => {
        const tags = (row.dataset.tags || "").split(",");
        const show = filter === "all" || tags.includes(filter);
        if (show) {
          row.classList.remove("hidden");
          gsap.fromTo(row, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" });
        } else {
          gsap.to(row, {
            opacity: 0, y: -6, duration: 0.25, ease: "power2.in",
            onComplete() { row.classList.add("hidden"); },
          });
        }
      });
    });
  });

  /* ── 8. Contact form ───────────────────────────────────────── */
  const submitBtn  = document.getElementById("contact-submit");
  const successEl  = document.getElementById("contact-success");
  const errorEl    = document.getElementById("contact-error");
  const errorMsg   = document.getElementById("contact-error-msg");
  const formInner  = document.getElementById("contact-form-inner");

  if (submitBtn) {
    submitBtn.addEventListener("click", async () => {
      const name    = document.getElementById("contact-name")?.value.trim();
      const email   = document.getElementById("contact-email")?.value.trim();
      const subject = document.getElementById("contact-subject")?.value.trim();
      const message = document.getElementById("contact-message")?.value.trim();

      if (!name || !email || !subject || !message) {
        showError("Please fill out all required fields.");
        return;
      }

      setLoading(true);

      const formData = new FormData();
      formData.append("name", name);
      formData.append("email", email);
      formData.append("subject", subject);
      formData.append("message", message);

      const csrf = document.querySelector("[name=csrfmiddlewaretoken]");
      if (csrf) formData.append("csrfmiddlewaretoken", csrf.value);

      try {
        const res  = await fetch("/contact/", { method: "POST", body: formData });
        const data = await res.json();

        if (res.ok && data.status === "ok") {
          formInner.hidden = true;
          successEl.hidden = false;
          gsap.fromTo(successEl, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.4 });
        } else {
          showError(data.message || "Something went wrong. Please try again.");
        }
      } catch (err) {
        showError("Network error. Please check your connection.");
      } finally {
        setLoading(false);
      }
    });
  }

  function setLoading(on) {
    if (!submitBtn) return;
    const text    = submitBtn.querySelector(".btn-text");
    const spinner = submitBtn.querySelector(".btn-spinner");
    const arrow   = submitBtn.querySelector(".btn-arrow");
    submitBtn.disabled = on;
    if (text)    text.textContent = on ? "Sending…" : "Send Message";
    if (spinner) spinner.hidden = !on;
    if (arrow)   arrow.hidden = on;
  }

  function showError(msg) {
    if (!errorEl || !errorMsg) return;
    errorMsg.textContent = msg;
    errorEl.hidden = false;
    gsap.fromTo(errorEl, { opacity: 0, y: -4 }, { opacity: 1, y: 0, duration: 0.3 });
    setTimeout(() => { if (errorEl) errorEl.hidden = true; }, 5000);
  }

  /* ── 9. Role cycling ───────────────────────────────────────── */
  const roleChips = document.querySelectorAll(".role-chip");
  if (roleChips.length > 1) {
    let current = 0;
    setInterval(() => {
      roleChips[current].classList.remove("active");
      current = (current + 1) % roleChips.length;
      roleChips[current].classList.add("active");
    }, 2800);
  }

})();
