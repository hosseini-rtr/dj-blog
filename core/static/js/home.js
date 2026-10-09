(function () {
  "use strict";

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
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          note.textContent = data.message || "";
          note.className =
            "form-note mono-tag " + (data.success ? "is-success" : "is-error");
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
