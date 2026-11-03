/* Loads MathJax only on a page that has a formula: the library is a quarter of a megabyte compressed and a
   handful of pages use it. The configuration in mathjax.js is read when the library starts; the browser keeps
   the library cached for the next page with a formula. */
(function () {
  var SRC = "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js";
  function load() {
    if (!document.querySelector(".arithmatex")) return;
    if (window.MathJax && window.MathJax.startup) { window.MathJax.typesetPromise(); return; }
    if (document.getElementById("mathjax-lib")) return;
    var s = document.createElement("script");
    s.id = "mathjax-lib";
    s.src = SRC;
    s.async = true;
    document.head.appendChild(s);
  }
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(load); }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", load); }
  else { load(); }
})();
