(function () {
  "use strict";

  var header = document.getElementById("site-header");
  var nav = document.getElementById("main-nav");
  var navToggle = document.getElementById("nav-toggle");
  var toTop = document.getElementById("to-top");
  var clock = document.getElementById("hero-clock");

  // Header shadow / background on scroll
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile nav toggle
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Back to top
  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Live status clock in hero
  if (clock) {
    function tick() {
      var now = new Date();
      var pad = function (n) { return String(n).padStart(2, "0"); };
      clock.textContent = pad(now.getHours()) + ":" + pad(now.getMinutes()) + ":" + pad(now.getSeconds());
    }
    tick();
    setInterval(tick, 1000);
  }
})();
