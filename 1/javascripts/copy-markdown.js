/* "Copy this page as Markdown": a button next to the page's edit and view buttons that copies the page's Markdown
   twin (…/index.md, written by hooks/llms.py) to the clipboard, for pasting into a chat with an AI assistant or
   into a note. A browser that refuses the clipboard opens the twin instead. */
(function () {
  var ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12z"/></svg>';
  var DONE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21 7 9 19l-5.5-5.5 1.41-1.41L9 16.17 19.59 5.59z"/></svg>';
  var TITLE = "Copy this page as Markdown";

  function add() {
    var inner = document.querySelector(".md-content__inner");
    if (!inner || inner.querySelector(".md-copy-md")) return;
    var a = document.createElement("a");
    a.className = "md-content__button md-icon md-copy-md";
    a.href = new URL("index.md", window.location.href).href;
    a.title = TITLE;
    a.setAttribute("aria-label", TITLE);
    a.innerHTML = ICON;
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      fetch(a.href).then(function (r) { return r.text(); }).then(function (text) {
        return navigator.clipboard.writeText(text);
      }).then(function () {
        a.innerHTML = DONE;
        a.title = "Copied";
        setTimeout(function () { a.innerHTML = ICON; a.title = TITLE; }, 1600);
      }).catch(function () {
        window.location.href = a.href;
      });
    });
    var first = inner.querySelector(".md-content__button");
    inner.insertBefore(a, first || inner.firstChild);
  }

  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(add);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", add);
  } else {
    add();
  }
})();
