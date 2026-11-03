/* The joint units calculator on Drives, ratios and resolution: degrees and degrees per second at a joint to
   motor steps, steps per second and motor rpm, through the joint's ratio chosen in the select. The microsteps
   per motor turn come from the element's data attribute. */
(function () {
  function setup() {
    document.querySelectorAll(".calc[data-steps-per-motor-turn]").forEach(function (el) {
      if (el.dataset.ready) return;
      el.dataset.ready = "1";
      var perTurn = parseFloat(el.dataset.stepsPerMotorTurn);
      var q = function (n) { return el.querySelector("[name=" + n + "]"); };
      var out = function (n, v) { var o = el.querySelector("[data-out=" + n + "]"); if (o) o.textContent = v; };
      var group = function (n) { return Math.round(n).toLocaleString("en-US").replace(/,/g, "\u2009"); };
      var joint = q("joint"), deg = q("degrees"), speed = q("degps");
      function update() {
        var ratio = parseFloat(joint.value), perJointTurn = perTurn * ratio;
        out("steps", group(parseFloat(deg.value || 0) / 360 * perJointTurn));
        out("stepdeg", (360 / perJointTurn).toFixed(5) + "\u00b0");
        var sps = parseFloat(speed.value || 0) / 360 * perJointTurn;
        out("stepsps", group(sps));
        out("rpm", (parseFloat(speed.value || 0) * ratio / 6).toFixed(0));
      }
      [joint, deg, speed].forEach(function (x) { x.addEventListener("input", update); x.addEventListener("change", update); });
      update();
    });
  }
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(setup); }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", setup); }
  else { setup(); }
})();
