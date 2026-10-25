// Sorty: SaveSort's mascot, an original bookmark-ribbon character.
// createMascot(parent) returns {el, draw(t, opts)}; opts = {x, y, w, mood, talk (0..1), wave, look (-1..1), enter (0..1)}.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const INK = "#10121C";
  const MOODS = {
    // brows: inner = how far the inner ends rise (+ worried/sad, - cross), curve = arch, lift = raise both, raiseR = raise right brow only
    happy:      { inner: 0,  curve: 7, lift: 4,  raiseR: 0,  eye: 1.0,  pup: 11, mouth: "smile" },
    shocked:    { inner: 0,  curve: 9, lift: 14, raiseR: 0,  eye: 1.25, pup: 7,  mouth: "o" },
    suspicious: { inner: -9, curve: 0, lift: -2, raiseR: 0,  eye: 0.45, pup: 11, mouth: "flat" },
    smug:       { inner: 0,  curve: 3, lift: 0,  raiseR: 10, eye: 0.6,  pup: 11, mouth: "smirk" },
    sad:        { inner: 9,  curve: 2, lift: 2,  raiseR: 0,  eye: 0.9,  pup: 10, mouth: "frown" },
  };
  const svgEl = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  window.createMascot = function (parent) {
    const wrap = document.createElement("div");
    wrap.style.cssText = "position:absolute;left:0;top:0;z-index:15;display:none;transform-origin:50% 100%";
    const svg = svgEl("svg", { viewBox: "-40 -20 280 300", width: "100%" });
    svg.style.overflow = "visible";
    const defs = svgEl("defs", {}, svg);
    const g1 = svgEl("linearGradient", { id: "sortyBody", x1: "0", y1: "0", x2: "0", y2: "1" }, defs);
    svgEl("stop", { offset: "0", "stop-color": "#4C5CFF" }, g1);
    svgEl("stop", { offset: "1", "stop-color": "#2433D0" }, g1);
    const shadow = svgEl("ellipse", { cx: 100, cy: 268, rx: 78, ry: 11, fill: "#000", opacity: 0.25 }, svg);
    const rig = svgEl("g", {}, svg);
    // arms (behind body)
    const armL = svgEl("g", {}, rig), armR = svgEl("g", {}, rig);
    svgEl("path", { d: "M30 150 Q0 165 -14 196", stroke: "#1C27A8", "stroke-width": 13, fill: "none", "stroke-linecap": "round" }, armL);
    svgEl("circle", { cx: -14, cy: 198, r: 13, fill: "#FFE14A", stroke: "#1C27A8", "stroke-width": 5 }, armL);
    svgEl("path", { d: "M170 150 Q200 165 214 196", stroke: "#1C27A8", "stroke-width": 13, fill: "none", "stroke-linecap": "round" }, armR);
    svgEl("circle", { cx: 214, cy: 198, r: 13, fill: "#FFE14A", stroke: "#1C27A8", "stroke-width": 5 }, armR);
    // body: a bookmark ribbon with rounded top
    svgEl("path", { d: "M24 22 Q24 6 40 6 H160 Q176 6 176 22 V252 L100 204 L24 252 Z", fill: "url(#sortyBody)", stroke: "#1C27A8", "stroke-width": 6, "stroke-linejoin": "round" }, rig);
    svgEl("ellipse", { cx: 58, cy: 36, rx: 20, ry: 9, fill: "#fff", opacity: 0.22, transform: "rotate(-18 58 36)" }, rig);
    // yellow tag stripe (brand accent)
    svgEl("rect", { x: 24, y: 214, width: 0, height: 0, fill: "none" }, rig);
    // cheeks
    svgEl("circle", { cx: 50, cy: 130, r: 12, fill: "#FF8FA3", opacity: 0.45 }, rig);
    svgEl("circle", { cx: 150, cy: 130, r: 12, fill: "#FF8FA3", opacity: 0.45 }, rig);
    // eyes
    const eyes = [72, 128].map(cx => {
      const g = svgEl("g", {}, rig);
      const white = svgEl("ellipse", { cx, cy: 92, rx: 23, ry: 27, fill: "#fff", stroke: INK, "stroke-width": 4 }, g);
      const pupil = svgEl("circle", { cx, cy: 96, r: 11, fill: INK }, g);
      const glint = svgEl("circle", { cx: cx + 4, cy: 91, r: 3.5, fill: "#fff" }, g);
      return { cx, white, pupil, glint };
    });
    const brows = [72, 128].map(cx => svgEl("path", { d: `M${cx - 18} 56 L${cx + 18} 56`, stroke: INK, "stroke-width": 8, "stroke-linecap": "round", fill: "none" }, rig));
    const mouth = svgEl("path", { d: "", stroke: INK, "stroke-width": 7, "stroke-linecap": "round", "stroke-linejoin": "round", fill: "none" }, rig);
    const tongue = svgEl("ellipse", { cx: 100, cy: 160, rx: 0, ry: 0, fill: "#FF6B81" }, rig);
    wrap.appendChild(svg);
    parent.appendChild(wrap);

    function draw(t, o) {
      if (!o) { wrap.style.display = "none"; return; }
      wrap.style.display = "block";
      const m = MOODS[o.mood] || MOODS.happy;
      const w = o.w || 300, scale = w / 280;
      const enter = o.enter == null ? 1 : o.enter;
      const pop = enter < 1 ? 0.4 + 0.6 * (1 + 2.9 * Math.pow(enter - 1, 3) + 1.9 * Math.pow(enter - 1, 2)) : 1;
      const bob = Math.sin(t * 2.4) * 7 * scale;
      const tilt = Math.sin(t * 1.3) * 2.2 + (o.talk || 0) * Math.sin(t * 9) * 1.5;
      wrap.style.width = w + "px";
      wrap.style.left = o.x + "px";
      wrap.style.top = (o.y + bob) + "px";
      wrap.style.transform = `rotate(${tilt}deg) scale(${pop}) scaleY(${1 + Math.sin(t * 4.8) * 0.012})`;
      shadow.setAttribute("rx", 78 - Math.sin(t * 2.4) * 6);
      // blink every ~3.3s (and right after entering)
      const ph = (t + (o.seed || 0)) % 3.3;
      const blink = ph < 0.13 ? Math.abs(Math.sin(ph / 0.13 * Math.PI)) : 0;
      const open = Math.max(0.08, m.eye * (1 - blink));
      const look = (o.look || 0) * 7;
      eyes.forEach(e => {
        e.white.setAttribute("ry", 27 * open);
        e.white.setAttribute("rx", 23 * (m.eye > 1 ? 1.1 : 1));
        e.pupil.setAttribute("r", Math.min(m.pup, 27 * open * 0.8));
        e.pupil.setAttribute("cx", e.cx + look);
        e.pupil.setAttribute("cy", 96 - (1 - open) * 4);
        e.glint.setAttribute("cx", e.cx + look + 4);
        e.glint.setAttribute("opacity", open > 0.3 ? 1 : 0);
      });
      brows.forEach((b, i) => {
        const cx = eyes[i].cx, y = 58 - m.lift - (i === 1 ? m.raiseR : 0) - (o.talk || 0) * 3;
        const inX = i === 0 ? cx + 18 : cx - 18, outX = i === 0 ? cx - 18 : cx + 18;
        b.setAttribute("d", `M${outX} ${y + m.inner * 0.3} Q${cx} ${y - m.curve - 4} ${inX} ${y - m.inner}`);
      });
      const talk = o.talk || 0;
      if (talk > 0.06) {
        const h = 6 + 26 * talk, wd = 20 + 6 * talk;
        mouth.setAttribute("d", `M${100 - wd} 150 Q100 ${150 + h * 2} ${100 + wd} 150 Q100 ${150 - 4} ${100 - wd} 150 Z`);
        mouth.setAttribute("fill", "#5A0E1E"); tongue.setAttribute("rx", wd * 0.55); tongue.setAttribute("ry", h * 0.35); tongue.setAttribute("cy", 150 + h * 0.75);
      } else {
        tongue.setAttribute("rx", 0); tongue.setAttribute("ry", 0);
        const d = { smile: "M76 146 Q100 172 124 146", o: "M100 140 a10 13 0 1 0 0.1 0 Z", flat: "M82 152 L118 152", smirk: "M80 154 Q102 160 124 142", frown: "M80 160 Q100 140 120 160" }[m.mouth];
        mouth.setAttribute("d", d); mouth.setAttribute("fill", m.mouth === "o" ? "#5A0E1E" : "none");
      }
      // arms: wave on entrance (or when asked), otherwise gentle swing
      const wave = o.wave ? Math.sin(t * 14) * 28 - 40 : Math.sin(t * 2.4 + 1) * 6;
      armR.setAttribute("transform", `rotate(${wave} 170 150)`);
      armL.setAttribute("transform", `rotate(${-Math.sin(t * 2.4) * 6 + (m.mouth === "o" ? 30 : 0)} 30 150)`);
    }
    return { el: wrap, draw };
  };
})();
