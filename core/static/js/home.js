(function () {
  "use strict";

  if (typeof gsap === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Hero boot-up sequence ---------- */
  var heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });
  heroTl
    .from(".hero__status", { opacity: 0, y: -10, duration: 0.5 })
    .from(".eyebrow", { opacity: 0, y: -10, duration: 0.5 }, "-=0.3")
    .from(".hero__line", {
      opacity: 0,
      y: reduceMotion ? 0 : 40,
      clipPath: "inset(0 0 100% 0)",
      duration: 0.9,
    }, "-=0.2")
    .from(".hero__tagline", { opacity: 0, y: 16, duration: 0.6 }, "-=0.4")
    .from(".hero__meta-item", { opacity: 0, y: 14, duration: 0.5, stagger: 0.08 }, "-=0.3")
    .from(".hero__actions .btn", { opacity: 0, y: 14, duration: 0.5, stagger: 0.1 }, "-=0.3")
    .from(".corner", { opacity: 0, duration: 0.4, stagger: 0.05 }, "-=0.6");

  gsap.to(".hero__scroll-cue", {
    y: 8,
    duration: 1.2,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
  });

  /* ---------- Generic scroll reveal ---------- */
  gsap.utils.toArray("[data-reveal]").forEach(function (el) {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.8,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        toggleActions: "play none none reverse",
      },
    });
  });

  /* ---------- Skill bar fill ---------- */
  gsap.utils.toArray(".skill-bar__fill").forEach(function (bar) {
    var level = bar.getAttribute("data-level") || 0;
    gsap.to(bar, {
      width: level + "%",
      duration: 1.1,
      ease: "power2.out",
      scrollTrigger: {
        trigger: bar,
        start: "top 90%",
        toggleActions: "play none none reverse",
      },
    });
  });

  /* ---------- Animated counters (about section) ---------- */
  gsap.utils.toArray(".fact__value").forEach(function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    var counter = { val: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: "top 90%",
      once: true,
      onEnter: function () {
        gsap.to(counter, {
          val: target,
          duration: 1.4,
          ease: "power1.out",
          onUpdate: function () {
            el.textContent = Math.round(counter.val);
          },
        });
      },
    });
  });

  /* ---------- Section title / card entrance on scroll (subtle parallax) ---------- */
  gsap.utils.toArray(".skill-card, .service-card, .project-card, .timeline__item").forEach(function (el) {
    gsap.from(el, {
      opacity: 0,
      y: 30,
      duration: 0.7,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 92%",
        toggleActions: "play none none reverse",
      },
    });
  });

  /* ---------- Contact form ---------- */
  var form = document.getElementById("contact-form");
  var note = document.getElementById("form-note");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var submitBtn = form.querySelector("button[type=submit]");
      var originalText = submitBtn.textContent;
      submitBtn.disabled = true;

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          note.textContent = data.message || "";
          note.className = "form-note mono-tag " + (data.success ? "is-success" : "is-error");
          if (data.success) form.reset();
        })
        .catch(function () {
          note.textContent = "Something went wrong. Please try again.";
          note.className = "form-note mono-tag is-error";
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        });
    });
  }
})();
