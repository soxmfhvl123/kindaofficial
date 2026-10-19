/* Kinda Official — hover video, live embed toggle, newsletter form, footer year. */
(function () {
  var calm = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Thumbnails play their video on hover: add data-video="path/to/clip.mp4" to an .item. */
  if (!calm) {
    document.querySelectorAll("[data-video]").forEach(function (el) {
      var box = el.querySelector(".thumb") || el, v;
      el.addEventListener("mouseenter", function () {
        if (!v) {
          v = document.createElement("video");
          v.src = el.getAttribute("data-video");
          v.muted = true; v.loop = true; v.playsInline = true;
          box.appendChild(v);
        }
        v.play().catch(function () {});
      });
      el.addEventListener("mouseleave", function () { if (v) { v.pause(); v.currentTime = 0; } });
    });
  }

  document.querySelectorAll("[data-interact]").forEach(function (b) {
    b.addEventListener("click", function () {
      b.textContent = b.parentNode.classList.toggle("on") ? "Done" : "Interact";
    });
  });

  document.querySelectorAll(".signup").forEach(function (box) {
    box.querySelector("form").addEventListener("submit", function (e) {
      // If a newsletter service URL is set as the form action, let the browser submit it there.
      if (this.getAttribute("action")) return;
      e.preventDefault();
      box.classList.add("done");
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
