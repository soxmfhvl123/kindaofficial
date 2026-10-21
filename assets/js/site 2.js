/* Kinda Official — live embed toggle, newsletter form, footer year. */
(function () {
  document.querySelectorAll("[data-interact]").forEach(function (b) {
    b.addEventListener("click", function () {
      b.textContent = b.parentNode.classList.toggle("on") ? "Done" : "Interact";
    });
  });

  var signup = document.querySelector(".signup");
  if (signup) {
    signup.querySelector("form").addEventListener("submit", function (e) {
      // If a newsletter service URL is set as the form action, let the browser submit it there.
      if (this.getAttribute("action")) return;
      e.preventDefault();
      signup.classList.add("done");
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
