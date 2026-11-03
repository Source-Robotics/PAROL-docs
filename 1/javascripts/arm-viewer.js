/* The arm viewer: a three.js view of the robot that tools/build_model.py writes from the URDFs (one GLB per arm
   link, one per tool, viewer.json with the kinematic chain and the list of tools). The reader turns and zooms the
   robot, moves every joint with a slider within its limits, chooses the tool on the flange (loaded the first time
   it is chosen) and picks the colour of the printed parts: the meshes under a node named <part>__body. Motors,
   jaws and the rest keep the model's colours. Loaded as a module by arm-viewer-loader.js only on a page that has
   an .arm-viewer element; three.js comes from the import map in overrides/main.html. */
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";   // the models are meshopt-compressed (gltfpack)

async function mount(el) {
  if (el.dataset.ready) return;
  el.dataset.ready = "1";
  const base = new URL(el.dataset.base, window.location.href).href;
  const cfg = await (await fetch(base + "viewer.json")).json();
  const q = (n) => el.querySelector("[name=" + n + "]");
  const canvas = el.querySelector("canvas");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(35, 1, 0.005, 20);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 1.0;
  controls.addEventListener("start", () => { controls.autoRotate = false; });
  const root = new THREE.Group();
  if (cfg.up === "z") root.rotation.x = -Math.PI / 2;      // the URDF is Z-up, three.js Y-up
  scene.add(root);
  const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
  const load = (file) => new Promise((ok, err) => loader.load(base + file, (g) => ok(g.scene), undefined, err));

  // the chain: a frame per joint (its origin in the parent link) holding the child link, which turns about the axis
  const frames = { [cfg.root]: new THREE.Group() };
  root.add(frames[cfg.root]);
  const joints = cfg.joints.map((j) => {
    const frame = new THREE.Group();
    frame.position.fromArray(j.xyz);
    frame.quaternion.setFromEuler(new THREE.Euler(j.rpy[0], j.rpy[1], j.rpy[2], "ZYX"));   // URDF roll, pitch, yaw
    const link = new THREE.Group();
    frame.add(link);
    frames[j.parent].add(frame);
    frames[j.child] = link;
    return { cfg: j, node: link, axis: new THREE.Vector3().fromArray(j.axis).normalize(), deg: 0 };
  });
  const tools = cfg.tools || [];
  const defaultTool = tools.length ? (cfg.default.tool || tools[0].id) : null;
  const toolFrame = frames[cfg.tool_link] || frames[cfg.joints[cfg.joints.length - 1].child];
  const suffix = cfg.body_suffix || "__body";
  const state = { color: cfg.default.body, bodies: [], tool: null, wanted: null };

  // a printed part is a mesh under a node named <part>__body; it gets a material of its own, so that the new
  // colour reaches the printed parts only (the arm's and every tool's loaded so far)
  function adopt(obj) {
    obj.traverse((o) => {
      if (!o.isMesh) return;
      let body = false;
      for (let n = o; n && !body; n = n.parent) body = n.name.endsWith(suffix);
      if (body) {
        o.material = o.material.clone();
        o.material.color.set(state.color);
        state.bodies.push(o);
      }
    });
    return obj;
  }
  function paint(hex) {
    state.color = hex;
    for (const o of state.bodies) o.material.color.set(hex);
  }
  function setJoint(i, deg) {
    const j = joints[i];
    j.deg = deg;
    j.node.quaternion.setFromAxisAngle(j.axis, (deg * Math.PI) / 180);
  }

  // the tools: each file is fetched the first time it is chosen and kept
  const select = q("tool");
  const toolCache = new Map();
  function loadTool(id) {
    if (!toolCache.has(id)) {
      const t = tools.find((x) => x.id === id);
      const p = t ? load(t.file).then(adopt) : Promise.reject(new Error("no tool " + id));
      p.catch(() => toolCache.delete(id));     // a failed load is tried again on the next choice
      toolCache.set(id, p);
    }
    return toolCache.get(id);
  }
  async function setTool(id) {
    state.wanted = id;
    if (select) select.value = id;
    let obj = null;
    try { obj = await loadTool(id); } catch (e) { console.error("arm viewer: tool " + id, e); }
    if (state.wanted !== id) return;           // the reader chose another tool while this one loaded
    if (!obj) {                                // keep the tool on the flange, and say so in the list
      state.wanted = state.tool ? state.tool.id : null;
      if (select && state.tool) select.value = state.tool.id;
      return;
    }
    if (state.tool) toolFrame.remove(state.tool.obj);
    toolFrame.add(obj);
    state.tool = { id, obj };
  }
  if (select) {
    for (const t of tools) {
      const option = document.createElement("option");
      option.value = t.id;
      option.textContent = t.label;
      select.appendChild(option);
    }
    if (!tools.length) select.closest("label").hidden = true;
    select.addEventListener("change", () => setTool(select.value));
  }

  function frame() {
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3()).length();
    const centre = box.getCenter(new THREE.Vector3());
    const dist = (size / 2) / Math.tan((camera.fov * Math.PI) / 360) * (cfg.camera.fill || 1.2);
    const az = (cfg.camera.azimuth_deg * Math.PI) / 180, po = (cfg.camera.polar_deg * Math.PI) / 180;
    camera.position.set(centre.x + dist * Math.sin(po) * Math.sin(az), centre.y + dist * Math.cos(po), centre.z + dist * Math.sin(po) * Math.cos(az));
    controls.target.copy(centre);
    controls.update();
  }

  await Promise.all([
    ...cfg.links.map(async (l) => { frames[l.name].add(adopt(await load(l.file))); }),
    defaultTool ? setTool(defaultTool) : null,
  ]);
  joints.forEach((j, i) => setJoint(i, cfg.default.q_deg[i] || 0));
  frame();

  // the joint sliders, the colours, Reset
  const box = el.querySelector(".arm-viewer__joints");
  const sliders = [];
  if (box) {
    joints.forEach((j, i) => {
      const label = document.createElement("label");
      label.className = "arm-viewer__joint";
      const text = document.createElement("span");
      text.textContent = "J" + (i + 1) + " ";
      const value = document.createElement("output");
      value.textContent = j.deg.toFixed(0) + "°";
      const input = document.createElement("input");
      // whole degrees inside the limits, so that every step and 0 fall on the slider's grid
      input.type = "range"; input.min = Math.ceil(j.cfg.lower_deg); input.max = Math.floor(j.cfg.upper_deg); input.step = 1; input.value = j.deg;
      input.setAttribute("aria-label", "Joint " + (i + 1));
      input.addEventListener("input", () => { setJoint(i, parseFloat(input.value)); value.textContent = input.value + "°"; });
      label.append(text, value, input);
      box.appendChild(label);
      sliders.push({ input, value });
    });
  }
  const input = q("body");
  const swatches = el.querySelector(".arm-viewer__swatches[data-target=body]");
  const apply = (hex) => { paint(hex); if (input) input.value = hex; };
  if (swatches) {
    for (const [name, hex] of Object.entries(cfg.colors.body)) {
      const b = document.createElement("button");
      b.type = "button"; b.title = name; b.setAttribute("aria-label", name);
      b.style.background = hex;
      b.addEventListener("click", () => apply(hex));
      swatches.appendChild(b);
    }
  }
  if (input) { input.value = state.color; input.addEventListener("input", () => apply(input.value)); }
  const reset = q("reset");
  if (reset) reset.addEventListener("click", async () => {
    joints.forEach((j, i) => { setJoint(i, cfg.default.q_deg[i] || 0); if (sliders[i]) { sliders[i].input.value = j.deg; sliders[i].value.textContent = j.deg.toFixed(0) + "°"; } });
    apply(cfg.default.body);
    if (defaultTool) await setTool(defaultTool);
    frame();
    controls.autoRotate = true;
  });

  // size, visibility, render
  const resize = () => {
    const w = el.clientWidth || canvas.clientWidth, h = canvas.clientHeight || Math.round(w * 0.7);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(el);
  resize();
  let visible = true;
  new IntersectionObserver((e) => { visible = e[0].isIntersecting; }).observe(el);
  renderer.setAnimationLoop(() => { if (!visible) return; controls.update(); renderer.render(scene, camera); });
}

document.querySelectorAll(".arm-viewer").forEach((el) => mount(el).catch((e) => {
  console.error("arm viewer:", e);
  const hint = el.querySelector(".arm-viewer__hint");
  if (hint) hint.textContent = "The 3D view could not load in this browser.";
}));
