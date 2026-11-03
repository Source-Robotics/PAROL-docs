/* Loads the arm viewer (arm-viewer.js, a module on three.js) only on a page that has one: the three.js library is
   a few hundred kilobytes, and most pages have no model. The import map in overrides/main.html says where
   three.js comes from. */
(function () {
  var me = document.currentScript;
  var url = me ? new URL("arm-viewer.js", me.src).href : null;
  function load() {
    if (!url || !document.querySelector(".arm-viewer")) return;
    import(url).catch(function (e) { console.error("arm viewer:", e); });
  }
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(load); }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", load); }
  else { load(); }
})();
