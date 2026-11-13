/* The kit selector on the Bill of materials page (owner, 2026-11-11): "I buy everything myself", "I have the
   partial kit", "I have the full kit". The data is docs/includes/bom-kits.yml, which tools/sync_bom.py writes into
   the page's .bom-kits element. With a kit chosen, each row's link cell says "Included" with a green check, or
   "Not included" beside its links; a row a kit builder does not need says "Not needed". A line under the buttons
   lists what is still to buy. The choice is remembered in this browser only. Without JavaScript, and in print, the
   page is the plain BOM. */
(function () {
  var KEY = "parol6-bom-kit";
  var CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2m-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8z"/></svg>';

  function remembered() { try { return localStorage.getItem(KEY) || ""; } catch (e) { return ""; } }
  function remember(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* private window: not remembered */ } }
  function text(el) {
    var c = el.cloneNode(true);
    c.querySelectorAll(".headerlink").forEach(function (a) { a.remove(); });
    return c.textContent.replace(/\s+/g, " ").trim();
  }
  function span(cls, words) { var s = document.createElement("span"); s.className = cls; s.textContent = words; return s; }

  function setup() {
    var box = document.querySelector(".bom-kits[data-kits]");
    if (!box || box.dataset.ready) return;
    var data;
    try { data = JSON.parse(box.dataset.kits); } catch (e) { return; }
    box.dataset.ready = "1";

    // every row of every table after the box, with its section and its entry in the data
    var rows = [], optional = [], section = "";
    for (var el = box.nextElementSibling; el; el = el.nextElementSibling) {
      if (el.tagName === "H2") {
        section = text(el);
        var sec = data.sections[section];
        if (sec && sec.optional) optional.push(section);
        continue;
      }
      var table = el.tagName === "TABLE" ? el : el.querySelector("table");
      if (!table || !table.tHead) continue;
      var heads = Array.prototype.map.call(table.tHead.rows[0].cells, text);
      var linkCol = heads.indexOf("Link"), altCol = heads.indexOf("ALT link"), qtyCol = heads.indexOf("Quantity");
      Array.prototype.forEach.call(table.tBodies[0].rows, function (tr) {
        var s = data.sections[section] || {};
        var name = text(tr.cells[0]);
        var entry = (s.rows && s.rows[name]) || (s.kits ? s : null);
        if (!entry) return;
        var target = tr.cells[linkCol >= 0 ? linkCol : tr.cells.length - 1];
        var alt = altCol >= 0 ? tr.cells[altCol] : null;
        rows.push({
          entry: entry, optional: !!s.optional, target: target, alt: alt, own: linkCol >= 0,
          html: target.innerHTML, altHtml: alt ? alt.innerHTML : "",
          name: name + (qtyCol >= 0 && text(tr.cells[qtyCol]) ? " (" + text(tr.cells[qtyCol]) + ")" : "")
        });
      });
    }

    // the buttons and the summary line
    var bar = document.createElement("div");
    bar.className = "bom-kits__choose";
    bar.setAttribute("role", "group");
    bar.setAttribute("aria-label", "What do you have?");
    bar.appendChild(span("bom-kits__q", "What do you have?"));
    var choices = [["", "I buy everything myself"]];
    Object.keys(data.kits).forEach(function (k) { choices.push([k, data.kits[k].label]); });
    var buttons = choices.map(function (c) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "md-button";
      b.dataset.kit = c[0];
      b.textContent = c[1];
      b.addEventListener("click", function () { apply(c[0]); remember(c[0]); });
      bar.appendChild(b);
      return b;
    });
    var summary = document.createElement("p");
    summary.className = "bom-kits__summary";
    summary.hidden = true;
    box.appendChild(bar);
    box.appendChild(summary);

    function apply(kit) {
      if (kit && !data.kits[kit]) kit = "";
      buttons.forEach(function (b) {
        var on = b.dataset.kit === kit;
        b.classList.toggle("md-button--primary", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      var toBuy = [];
      rows.forEach(function (r) {
        r.target.innerHTML = r.html;
        if (r.alt) r.alt.innerHTML = r.altHtml;
        if (!kit) return;
        var e = r.entry, mark;
        if ((e.kits || []).indexOf(kit) >= 0) {
          mark = span("bom-kits__in", "Included");
          mark.insertAdjacentHTML("afterbegin", CHECK);
          if (e.note) mark.appendChild(span("bom-kits__note", " (" + e.note + ")"));
          if (r.own) { r.target.innerHTML = ""; if (r.alt) r.alt.innerHTML = ""; }
          else r.target.appendChild(document.createTextNode(" "));
          r.target.appendChild(mark);
        } else if (e.needed === false) {
          mark = span("bom-kits__skip", "Not needed");
          if (e.note) mark.appendChild(span("bom-kits__note", ": " + e.note));
          if (r.own) { r.target.innerHTML = ""; if (r.alt) r.alt.innerHTML = ""; }
          r.target.insertBefore(mark, r.target.firstChild);
        } else {
          r.target.insertBefore(document.createTextNode(" "), r.target.firstChild);
          r.target.insertBefore(span("bom-kits__out", "Not included"), r.target.firstChild);
          if (!r.optional) toBuy.push(r.name);
        }
      });
      summary.hidden = !kit;
      summary.innerHTML = "";
      if (!kit) return;
      var k = data.kits[kit], a = document.createElement("a");
      a.href = k.url;
      a.textContent = k.name;
      summary.appendChild(document.createTextNode("With "));
      summary.appendChild(a);
      summary.appendChild(document.createTextNode(toBuy.length ? ", you still buy: " + toBuy.join(", ") + "." : ", you buy nothing else."));
      if (optional.length) summary.appendChild(document.createTextNode(" Optional, and in no kit: " + optional.join(", ").toLowerCase() + "."));
      if (data.extras) summary.appendChild(document.createTextNode(" The kits also carry " + data.extras + "."));
    }
    // ?kit=partial or ?kit=full in the address (a link from the shop's kit page) wins over the remembered choice
    var asked = null;
    try { asked = new URLSearchParams(window.location.search).get("kit"); } catch (e) { asked = null; }
    if (asked !== null && (asked === "" || data.kits[asked])) remember(asked);
    apply(asked !== null && (asked === "" || data.kits[asked]) ? asked : remembered());
  }

  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(setup); }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", setup); }
  else { setup(); }
})();
