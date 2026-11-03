/* CHEM SAFE — comportamiento mínimo de las fichas */
(function () {
  "use strict";
  document.querySelectorAll("[data-print]").forEach(function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
  // Resalta brevemente la sección a la que se llega desde el menú
  function flash() {
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el || !el.classList.contains("sec")) return;
    el.animate([{ boxShadow: "0 0 0 4px var(--accent-soft)" }, { boxShadow: "0 0 0 0 transparent" }],
      { duration: 900, easing: "ease-out" });
  }
  window.addEventListener("hashchange", flash);
  flash();
})();
