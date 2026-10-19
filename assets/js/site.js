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

  /* Language: press L to switch between English and 한국어. */
  var root = document.documentElement, toast = document.querySelector(".lang-toast"), toastT;
  function setLang(lang, announce) {
    root.setAttribute("data-lang", lang);
    root.lang = lang;
    try { localStorage.setItem("ko-lang", lang); } catch (e) {}
    document.querySelectorAll("[data-ph-" + lang + "]").forEach(function (el) {
      el.placeholder = el.getAttribute("data-ph-" + lang);
    });
    if (announce && toast) {
      toast.textContent = lang === "ko" ? "한국어" : "English";
      toast.classList.add("on");
      clearTimeout(toastT);
      toastT = setTimeout(function () { toast.classList.remove("on"); }, 900);
    }
  }
  setLang(root.getAttribute("data-lang") === "ko" ? "ko" : "en", false);
  document.addEventListener("keydown", function (e) {
    if (e.key !== "l" && e.key !== "L" && e.key !== "ㅣ") return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable) return;
    setLang(root.getAttribute("data-lang") === "ko" ? "en" : "ko", true);
  });

  document.querySelectorAll("[data-interact]").forEach(function (b) {
    var en = b.querySelector(".en"), ko = b.querySelector(".ko");
    b.addEventListener("click", function () {
      var on = b.parentNode.classList.toggle("on");
      en.textContent = on ? "Done" : "Interact";
      ko.textContent = on ? "완료" : "조작하기";
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
