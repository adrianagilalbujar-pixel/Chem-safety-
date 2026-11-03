/* CHEM SAFE — generador de etiquetas con QR (se ejecuta en el navegador).
   Solo genera QR cuando hay una URL base https verificada por la persona usuaria. */
(function () {
  "use strict";
  var SLUGS = ["acido-sulfurico", "hidroxido-de-sodio", "cloruro-de-sodio"];
  var input = document.getElementById("base-url");
  var applyBtn = document.getElementById("apply");
  var confirmBox = document.getElementById("confirm");
  var printBtn = document.getElementById("print");
  var status = document.getElementById("status");
  var linkList = document.getElementById("links");

  function normalize(u) {
    u = (u || "").trim();
    if (!u) return "";
    if (!/^https:\/\//i.test(u)) return "";
    if (u.charAt(u.length - 1) !== "/") u += "/";
    return u;
  }

  function qrSvg(text) {
    var qr = qrcode(0, "M");           // corrección de errores M (15 %)
    qr.addData(text);
    qr.make();
    return qr.createSvgTag({ cellSize: 4, margin: 4, scalable: true, alt: "Código QR de la ficha", title: "QR" });
  }

  function render(base) {
    linkList.innerHTML = "";
    SLUGS.forEach(function (slug) {
      var box = document.querySelector('[data-qr="' + slug + '"]');
      if (!box) return;
      if (!base) {
        box.innerHTML = '<div class="qr-pending">QR pendiente<br><small>Publica el sitio y escribe la URL</small></div>';
        return;
      }
      var url = base + "fichas/" + slug + ".html";
      box.innerHTML = qrSvg(url);
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = url; a.target = "_blank"; a.rel = "noopener"; a.textContent = url;
      li.appendChild(a);
      linkList.appendChild(li);
    });
  }

  function update() {
    var base = normalize(input.value);
    if (!input.value.trim()) {
      status.textContent = "Sin URL: los QR aún no son definitivos.";
    } else if (!base) {
      status.textContent = "La URL debe comenzar con https:// (GitHub Pages la usa por defecto).";
    } else {
      status.textContent = "Abre cada enlace de abajo. Si todos cargan la ficha correcta, marca la casilla para imprimir.";
    }
    render(base);
    confirmBox.checked = false;
    confirmBox.disabled = !base;
    printBtn.disabled = true;
  }

  applyBtn.addEventListener("click", update);
  input.addEventListener("keydown", function (e) { if (e.key === "Enter") update(); });
  confirmBox.addEventListener("change", function () { printBtn.disabled = !confirmBox.checked; });
  printBtn.addEventListener("click", function () { window.print(); });

  // Vista previa adaptable: reduce la etiqueta (100 mm) cuando la pantalla es más angosta.
  document.querySelectorAll(".sheet .label").forEach(function (lb) {
    var w = document.createElement("div"); w.className = "label-wrap";
    lb.parentNode.insertBefore(w, lb); w.appendChild(lb);
  });
  function fit() {
    document.querySelectorAll(".label-wrap").forEach(function (w) {
      var lb = w.firstElementChild; lb.style.transform = "none"; w.style.height = "";
      var avail = document.querySelector(".sheet").clientWidth, full = lb.offsetWidth, hh = lb.offsetHeight;
      var k = Math.min(1, avail / full);
      lb.style.transform = k < 1 ? "scale(" + k + ")" : "none";
      w.style.height = Math.ceil(hh * k) + "px";
    });
  }
  window.addEventListener("resize", fit); window.addEventListener("orientationchange", fit);
  fit();

  var fromQuery = new URLSearchParams(location.search).get("base");
  input.value = fromQuery || window.CHEMSAFE_BASE_URL || "";
  update();
})();
