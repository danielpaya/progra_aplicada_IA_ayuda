/* =====================================================================
   Alimenta Familia · Propuesta a la Junta
   Motor de la presentación: navegación con pasos (builds), anexo opcional,
   contadores, gráficos animados y efectos de collage. Sin dependencias.
   ===================================================================== */
(() => {
  const deck = document.getElementById('deck');
  const ALL = [...deck.querySelectorAll('.slide')];
  const D = window.DATA, K = D.kpi;
  const ORDER = ['Camilo', 'Daniel', 'Laura', 'Mateo', 'Valery'];
  const COLOR = { Camilo: 'var(--red)', Daniel: '#E8DFCB', Laura: 'var(--blue)', Mateo: 'var(--mustard)', Valery: 'var(--green)', Equipo: 'var(--blue)' };
  const BAR = { Camilo: '#E03A1E', Daniel: '#E03A1E', Laura: '#2442C9', Mateo: '#F2B705', Valery: '#2E7D4F', Equipo: '#2442C9' };
  const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } } };

  // ---------- utilidades ----------
  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, a = {}, text) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (text !== undefined) n.textContent = text; return n; };
  const add = (p, tag, a, text) => p.appendChild(el(tag, a, text));
  const nf = (v, d = 0) => Number(v).toLocaleString('es-CO', { minimumFractionDigits: d, maximumFractionDigits: d });
  const MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  const mes = m => MES[Number(m.slice(5, 7)) - 1];
  const row = m => K.find(r => r.mes === m);
  const txt = (p, x, y, s, o = {}) => add(p, 'text', { x, y, 'font-size': o.size || 20, 'font-weight': o.w || 600, 'text-anchor': o.a || 'start', style: `fill:${o.fill || 'var(--ink)'};${o.font ? 'font-family:' + o.font : ''}`, ...(o.anim ? { 'data-a': o.anim, style: `fill:${o.fill || 'var(--ink)'};--d:${o.d || 0}ms;${o.font ? 'font-family:' + o.font : ''}` } : {}) }, s);
  const anim = (node, a, d) => { node.setAttribute('data-a', a); node.style.setProperty('--d', `${d}ms`); if (a === 'pop' || a === 'stamp') { node.style.transformBox = 'fill-box'; node.style.transformOrigin = 'center'; } return node; };
  const size = svg => { const w = svg.clientWidth || 1000, h = svg.clientHeight || 400; svg.setAttribute('viewBox', `0 0 ${w} ${h}`); return [w, h]; };
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

  // ---------- estructura común de cada diapositiva ----------
  ALL.forEach(s => {
    const who = s.dataset.speaker;
    s.style.setProperty('--speaker', COLOR[who]);
    if (!s.classList.contains('cover') || s.dataset.title !== 'Portada') {
      const w = document.createElement('div'); w.className = 'who'; w.style.setProperty('--c', COLOR[who]); w.textContent = who; s.appendChild(w);
    }
    const f = document.createElement('div'); f.className = 'foot';
    f.innerHTML = `<span>Alimenta Familia · Propuesta a la Junta Directiva</span><span style="display:flex;gap:14px;align-items:center"><span class="sim">dato simulado</span><span class="pg"></span></span>`;
    s.appendChild(f);
    if (s.dataset.steps) { s.classList.add('has-steps'); const h = document.createElement('div'); h.className = 'build-hint'; h.textContent = `→ ${s.dataset.steps} PASOS`; s.appendChild(h); }
    s.querySelectorAll('[data-d]').forEach(n => n.style.setProperty('--d', `${n.dataset.d}ms`));
  });

  // ---------- letras recortadas («nota de rescate») ----------
  const RB = ['var(--white)', '#151311', '#E03A1E', '#F2B705', '#2442C9', '#2E7D4F', '#E8DFCB'];
  const RF = ['var(--display)', 'var(--serif)', 'var(--sans)'];
  document.querySelectorAll('[data-ransom]').forEach(n => {
    const words = n.textContent.trim().split(/\s+/); n.textContent = '';
    words.forEach(wd => {
      const w = document.createElement('span'); w.className = 'w';
      [...wd].forEach((c, i) => {
        const bg = RB[Math.floor(rnd() * RB.length)], dark = ['#151311', '#E03A1E', '#2442C9', '#2E7D4F'].includes(bg);
        const ch = document.createElement('span'); ch.className = 'ch'; ch.textContent = i === 0 || rnd() > .5 ? c.toUpperCase() : c.toLowerCase();
        ch.style.cssText = `background:${bg};color:${dark ? '#F2EBDC' : '#151311'};font-family:${RF[Math.floor(rnd() * 3)]};font-weight:${rnd() > .5 ? 800 : 500};transform:rotate(${(rnd() * 10 - 5).toFixed(1)}deg) translateY(${(rnd() * 8 - 4).toFixed(0)}px);font-size:${(0.85 + rnd() * 0.3).toFixed(2)}em`;
        w.appendChild(ch);
      });
      n.appendChild(w);
    });
  });

  // ---------- estallidos tipo sticker ----------
  document.querySelectorAll('svg[data-burst]').forEach(svg => {
    const n = Number(svg.dataset.burst), pts = [];
    for (let i = 0; i < n * 2; i++) { const r = i % 2 ? 62 : 96, a = Math.PI * i / n; pts.push(`${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`); }
    const p = el('polygon', { points: pts.join(' '), style: 'fill:#F2B705;stroke:#151311;stroke-width:5;stroke-linejoin:round' });
    svg.insertBefore(p, svg.firstChild);
    svg.classList.add('wobble');
  });

  // ---------- tiendas (4 de 10 se van) ----------
  document.querySelectorAll('[data-stores]').forEach(box => {
    for (let i = 0; i < 10; i++) {
      const gone = [1, 4, 6, 8].includes(i), d = 1100 + [1, 4, 6, 8].indexOf(i) * 220;
      const st = document.createElement('div'); st.className = 'st' + (gone ? ' gone' : ''); st.style.setProperty('--i', i);
      st.innerHTML = `<svg class="store ico" viewBox="-6 -6 112 112"><use href="#i-store"/></svg>` +
        (gone ? `<svg class="x" viewBox="0 0 100 100"><path d="M14 14 L86 86" pathLength="1" data-a="draw" style="--d:${d}ms"/><path d="M86 14 L14 86" pathLength="1" data-a="draw" style="--d:${d + 120}ms"/></svg>` : '');
      box.appendChild(st);
    }
  });

  // ---------- casillas 6/6 ----------
  document.querySelectorAll('[data-checks]').forEach(box => {
    for (let i = 0; i < 6; i++) box.insertAdjacentHTML('beforeend', `<div class="ck" data-a="pop" style="--d:${300 + i * 180}ms"><svg viewBox="0 0 100 100"><path d="M18 52 L42 76 L84 26" pathLength="1" data-a="draw" style="--d:${450 + i * 180}ms"/></svg></div>`);
  });

  // ---------- gráficos de puntos (waffle) ----------
  document.querySelectorAll('[data-waffle]').forEach(w => {
    const n = Number(w.dataset.waffle), on = Number(w.dataset.on || 0), red = Number(w.dataset.red || 0), gone = Number(w.dataset.gone || 0), step = w.dataset.goneStep;
    for (let i = 0; i < n; i++) {
      const c = document.createElement('i'); c.style.setProperty('--i', i);
      if (i < red) c.className = 'r';
      else if (i < on) { c.className = 'on'; if (i >= on - gone) c.dataset.bc = `${step}:gone`; }
      w.appendChild(c);
    }
  });

  // ---------- barras de avance frente a la meta ----------
  document.querySelectorAll('[data-progress]').forEach(box => {
    const items = [
      { f: 'tiempo_rastreo_lote_h', n: 'Rastrear un lote', u: 'h', goal: 4, down: true },
      { f: 'tiempo_respuesta_pqr_h', n: 'Responder a una familia', u: 'h', goal: 12, down: true },
      { f: 'pct_mensajes_auditados', n: 'Mensajes auditados', u: '%', goal: 100, down: false },
      { f: 'nps', n: 'NPS', u: '', goal: 40, down: false },
    ];
    items.forEach((it, i) => {
      const vals = K.filter(r => r.mes >= '2026-04' && r.mes <= '2026-09').map(r => r[it.f]);
      const worst = it.down ? Math.max(...vals) : Math.min(...vals), now = row('2026-09')[it.f];
      const p = Math.max(0.03, Math.min(1, (it.down ? worst - now : now - worst) / Math.abs(it.down ? worst - it.goal : it.goal - worst)));
      const ok = it.down ? now <= it.goal * 1.5 : now >= it.goal;
      box.insertAdjacentHTML('beforeend', `<div class="prog" data-a="up" style="--d:${250 + i * 200}ms"><div class="nm">${it.n}<small>peor en la crisis: ${nf(worst)}${it.u} · meta ${it.down ? '≤' : '≥'} ${it.goal}${it.u}</small></div><div class="bar"><b style="--w:${p * 100}%;--d:${450 + i * 200}ms;background:var(--${ok ? 'green' : 'mustard'})"></b></div><div class="val" style="color:var(--${ok ? 'green' : 'ink'})">${String(now).replace('-', '−')}${it.u}</div></div>`);
    });
  });

  // ---------- gráficos SVG ----------
  const charts = {
    caida(svg) {
      const [w, h] = size(svg), R = K.filter(r => r.mes >= '2025-12' && r.mes <= '2026-05');
      const x = i => 20 + i / (R.length - 1) * (w - 40), y = v => 20 + (1 - (v - 30) / 55) * (h - 40);
      const d = R.map((r, i) => `${i ? 'L' : 'M'}${x(i)} ${y(r.indice_confianza_0_100)}`).join('');
      add(svg, 'path', { d, fill: 'none', 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1, style: 'stroke:var(--red);--d:500ms', 'data-a': 'draw' });
      R.forEach((r, i) => { const c = add(svg, 'circle', { cx: x(i), cy: y(r.indice_confianza_0_100), r: 9, style: `fill:var(--paper);stroke:var(--ink);stroke-width:4` }); anim(c, 'pop', 450 + i * 160); });
    },

    escalera(svg) {
      const [w, h] = size(svg), L = ['Lote', 'Producto', 'Línea vegana', 'Marca', 'Organización'], gap = 18, bw = (w - gap * 4) / 5;
      L.forEach((l, i) => {
        const bh = (h - 20) * (0.2 + i * 0.2), x = i * (bw + gap);
        const r = add(svg, 'rect', { x, y: h - bh, width: bw, height: bh, style: `fill:url(#htR);stroke:#151311;stroke-width:4` }); anim(r, 'grow', 300 + i * 260);
        if (i === 4) { const r2 = add(svg, 'rect', { x, y: h - bh, width: bw, height: bh, style: 'fill:var(--red);stroke:#151311;stroke-width:4' }); anim(r2, 'grow', 300 + i * 260); }
        const t = txt(svg, x + bw / 2, h - bh - 16, l, { a: 'middle', size: 26, w: 800 }); anim(t, 'up', 500 + i * 260);
      });
    },

    gauge(svg) {
      const [w, h] = size(svg), v = 96.8, meta = 95, cx = w / 2, cy = h * .78, r = Math.min(w / 2 - 30, h * .66);
      const pt = (p, rr) => [cx + rr * Math.cos(Math.PI * (1 - p / 100)), cy - rr * Math.sin(Math.PI * (1 - p / 100))];
      const arc = (p0, p1, rr) => { const [x0, y0] = pt(p0, rr), [x1, y1] = pt(p1, rr); return `M${x0} ${y0}A${rr} ${rr} 0 0 1 ${x1} ${y1}`; };
      add(svg, 'path', { d: arc(0, 100, r), fill: 'none', 'stroke-width': 46, style: 'stroke:var(--paper-2)' });
      const a = add(svg, 'path', { d: arc(0, v, r), fill: 'none', 'stroke-width': 46, pathLength: 1, style: 'stroke:url(#htG);stroke:var(--green)' }); anim(a, 'draw', 300);
      const [mx1, my1] = pt(meta, r - 34), [mx2, my2] = pt(meta, r + 34);
      add(svg, 'line', { x1: mx1, y1: my1, x2: mx2, y2: my2, 'stroke-width': 5, style: 'stroke:var(--ink)' });
      txt(svg, mx2 + 6, my2 - 14, 'META 95 %', { a: 'middle', size: 17, w: 800 });
      const t = txt(svg, cx, cy - 34, '96,8 %', { a: 'middle', size: 88, w: 400, fill: 'var(--green)', font: 'var(--display)' }); anim(t, 'pop', 900);
      const s = txt(svg, cx, cy + 8, '✓ CUMPLE LA META', { a: 'middle', size: 22, w: 800, fill: 'var(--green)' }); anim(s, 'up', 1300);
    },

    heat(svg) {
      const [w, h] = size(svg), P = ['Chía', 'Funza', 'Rionegro'], T = ['Mañana', 'Tarde', 'Noche'];
      const x0 = 150, y0 = 40, cw = (w - x0) / 3, ch = (h - y0) / 3, mx = Math.max(...D.omision.map(r => r.pct));
      T.forEach((t, j) => txt(svg, x0 + j * cw + cw / 2, 24, t.toUpperCase(), { a: 'middle', size: 18, w: 800, fill: 'var(--ink-2)' }));
      P.forEach((p, i) => {
        txt(svg, x0 - 18, y0 + i * ch + ch / 2 + 9, p, { a: 'end', size: 28, w: 800 });
        T.forEach((t, j) => {
          const r = D.omision.find(o => o.planta === p && o.turno === t), hot = r.pct === mx, k = i * 3 + j;
          const g = add(svg, 'g', {});
          g.appendChild(el('rect', { x: x0 + j * cw + 5, y: y0 + i * ch + 5, width: cw - 10, height: ch - 10, style: hot ? 'fill:var(--red);stroke:#151311;stroke-width:5' : `fill:url(#htR);opacity:${0.25 + r.pct / 6 * 0.6};stroke:#151311;stroke-width:2` }));
          g.appendChild(el('text', { x: x0 + j * cw + cw / 2, y: y0 + i * ch + ch / 2 + (hot ? 12 : 12), 'text-anchor': 'middle', 'font-size': hot ? 74 : 32, style: `font-family:var(--display);fill:${hot ? '#fff' : 'var(--ink)'}` }, `${nf(r.pct, 1)}%`));
          if (hot) g.appendChild(el('text', { x: x0 + j * cw + cw / 2, y: y0 + i * ch + ch - 20, 'text-anchor': 'middle', 'font-size': 17, 'font-weight': 800, style: 'fill:#fff;letter-spacing:.06em' }, 'AQUÍ SALIÓ EL LOTE 047'));
          anim(g, 'pop', hot ? 1200 : 250 + k * 70);
        });
      });
    },

    semanas(svg) {
      const [w, h] = size(svg), R = D.semanas, x0 = 6, bot = h - 28, band = (w - x0) / R.length, bw = band * .72;
      const peak = Math.max(...R.map(r => r.total)), y = v => bot - v / peak * (bot - 20);
      const pr = R.filter(r => r.w < '2026-04-14'), avg = pr.reduce((s, r) => s + r.total, 0) / pr.length, pi = R.findIndex(r => r.total === peak);
      R.forEach((r, i) => {
        const b = add(svg, 'rect', { x: x0 + i * band, y: y(r.total), width: bw, height: bot - y(r.total), style: 'fill:var(--ink)' }); anim(b, 'grow', 200 + i * 25);
        b.appendChild(el('title', {}, `Semana al ${r.w}: ${r.total} reclamos, ${r.salud} de salud`));
        if (r.salud) { const s = add(svg, 'rect', { x: x0 + i * band, y: y(r.salud), width: bw, height: bot - y(r.salud), style: 'fill:var(--red)' }); anim(s, 'grow', 400 + i * 25); }
        if (i === 0 || r.w.slice(5, 7) !== R[i - 1].w.slice(5, 7)) txt(svg, x0 + i * band, bot + 24, mes(r.w), { size: 17, w: 700, fill: 'var(--ink-2)' });
      });
      add(svg, 'line', { x1: x0, x2: w, y1: y(avg), y2: y(avg), 'stroke-width': 3, 'stroke-dasharray': '8 6', style: 'stroke:var(--green)' });
      txt(svg, w, y(avg) - 12, `promedio previo: ${nf(avg, 0)} por semana`, { a: 'end', size: 18, w: 800, fill: 'var(--green)' });
      const t = txt(svg, x0 + pi * band + bw + 14, y(peak) + 40, '173', { size: 72, w: 400, font: 'var(--display)' }); anim(t, 'pop', 1200);
      const t2 = txt(svg, x0 + pi * band - 12, y(R[pi].salud) + 10, `${R[pi].salud} de salud`, { a: 'end', size: 22, w: 800, fill: 'var(--red)' }); anim(t2, 'up', 1400);
    },

    donut(svg) {
      const [w, h] = size(svg), E = Object.entries(D.contagio).sort((a, b) => (a[0] === 'Vegana') - (b[0] === 'Vegana') || b[1] - a[1]);
      const tot = E.reduce((s, e) => s + e[1], 0), sanas = E.filter(e => e[0] !== 'Vegana').reduce((s, e) => s + e[1], 0);
      const cx = w / 2, cy = h / 2, r = Math.min(w, h) / 2 - 95;
      add(svg, 'circle', { cx, cy, r, fill: 'none', 'stroke-width': 60, style: 'stroke:var(--paper-2)' });
      let acc = 0; const C = { Cereales: 'var(--red)', 'Lácteos': '#B62A12', 'Panadería': '#F07A5E', Vegana: 'var(--ink)' };
      E.forEach(([l, n], i) => {
        const frac = n / tot, c = add(svg, 'circle', { cx, cy, r, fill: 'none', 'stroke-width': 60, pathLength: 1, transform: `rotate(${-90 + acc * 360} ${cx} ${cy})`, style: `stroke:${C[l]};stroke-dasharray:${frac} ${1 - frac};--d:${300 + i * 350}ms`, 'data-a': 'fade' });
        c.appendChild(el('title', {}, `${l}: ${n}`));
        const mid = (acc + frac / 2) * Math.PI * 2 - Math.PI / 2, lx = cx + Math.cos(mid) * (r + 50), ly = cy + Math.sin(mid) * (r + 50);
        const t = txt(svg, lx, ly + 6, `${l} ${n}`, { a: Math.cos(mid) > 0.2 ? 'start' : Math.cos(mid) < -0.2 ? 'end' : 'middle', size: 18, w: 800, fill: l === 'Vegana' ? 'var(--ink)' : 'var(--red)' }); anim(t, 'up', 500 + i * 350);
        acc += frac;
      });
      const t = txt(svg, cx, cy + 22, `${Math.round(sanas / tot * 100)}%`, { a: 'middle', size: 84, w: 400, fill: 'var(--red)', font: 'var(--display)' }); anim(t, 'pop', 1700);
    },

    matriz(svg) {
      const [w, h] = size(svg), x0 = 40, top = 34, pw = w - x0, ph = h - 40, X = e => x0 + e / 10 * pw, Y = i => top + (1 - i / 10) * (ph - top);
      [['VICTORIAS RÁPIDAS', 0, 0, 'var(--green)'], ['PROYECTOS ESTRATÉGICOS', 1, 0, 'var(--blue)'], ['COMPLEMENTARIAS', 0, 1, 'var(--ink-2)'], ['EVITAR', 1, 1, 'var(--red)']].forEach(([l, cx, cy, c], k) => {
        const qh = (ph - top) / 2, r = add(svg, 'rect', { x: x0 + cx * pw / 2 + 4, y: top + cy * qh + 4, width: pw / 2 - 8, height: qh - 8, style: `fill:${c};fill-opacity:${cy ? .06 : .16}` }); anim(r, 'fade', 100 + k * 100);
        txt(svg, x0 + cx * pw / 2 + (cy ? 18 : 6), cy ? top + qh + 36 : 22, l, { size: 17, w: 800, fill: c });
      });
      txt(svg, x0 + pw / 2, h - 6, 'ESFUERZO →', { a: 'middle', size: 16, w: 800, fill: 'var(--ink-2)' });
      add(svg, 'text', { x: 14, y: top + (ph - top) / 2, 'font-size': 16, 'font-weight': 800, 'text-anchor': 'middle', transform: `rotate(-90 14 ${top + (ph - top) / 2})`, style: 'fill:var(--ink-2)' }, 'IMPACTO →');
      ACC.forEach((a, i) => {
        const g = add(svg, 'g', {}); g.appendChild(el('title', {}, `${a.n}. ${a.t}`));
        g.appendChild(el('circle', { cx: X(a.esf), cy: Y(a.imp), r: 26, style: `fill:${a.esf < 5 ? 'var(--green)' : 'var(--blue)'};stroke:#151311;stroke-width:4` }));
        g.appendChild(el('text', { x: X(a.esf), y: Y(a.imp) + 9, 'text-anchor': 'middle', 'font-size': 26, style: 'font-family:var(--display);fill:#fff' }, a.n));
        anim(g, 'pop', 500 + i * 150);
      });
    },

    gantt(svg) {
      const [w, h] = size(svg), x0 = 360, top = 34, pw = w - x0 - 10, rh = (h - top) / ACC.length, X = d => x0 + d / 90 * pw;
      [0, 30, 60, 90].forEach(d => { add(svg, 'line', { x1: X(d), x2: X(d), y1: top - 8, y2: h, 'stroke-width': 2, 'stroke-dasharray': d ? '6 6' : '0', style: 'stroke:var(--ink-2)' }); txt(svg, X(d), 20, d ? `DÍA ${d}` : 'HOY', { a: d === 90 ? 'end' : 'middle', size: 16, w: 800, fill: 'var(--ink-2)' }); });
      ACC.forEach((a, i) => {
        const y = top + i * rh;
        txt(svg, 0, y + rh / 2 + 1, `${a.n}. ${a.s}`, { size: 19, w: 800 });
        txt(svg, 0, y + rh / 2 + 22, a.o, { size: 15, w: 600, fill: 'var(--ink-2)' });
        const b = add(svg, 'rect', { x: X(a.d0), y: y + rh * .18, width: X(a.d1) - X(a.d0), height: rh * .64, style: `fill:${a.esf < 5 ? 'var(--green)' : 'var(--blue)'};stroke:#151311;stroke-width:3` }); anim(b, 'growx', 300 + i * 160);
        const t = txt(svg, X(a.d1) + 8, y + rh / 2 + 7, `${a.d1 - a.d0} d`, { size: 17, w: 800, fill: 'var(--ink-2)' }); anim(t, 'fade', 700 + i * 160);
      });
    },

    ruta(svg) {
      const [w, h] = size(svg), S = [
        ['Reporte', '15-ago · consumidor'], ['Planta Chía', '16-may · turno noche'], ['6/6 controles', 'todos conformes'],
        ['CEDI', 'Bucaramanga'], ['Tienda', 'recibe 27-may'], ['Compra', '15-ago · después'],
      ];
      const y = h * .42, x = i => 70 + i * (w - 140) / (S.length - 1);
      const d = `M${x(0)} ${y} ` + S.slice(1).map((_, i) => `C ${x(i) + 60} ${y + (i % 2 ? 70 : -70)}, ${x(i + 1) - 60} ${y + (i % 2 ? 70 : -70)}, ${x(i + 1)} ${y}`).join(' ');
      add(svg, 'path', { d, fill: 'none', 'stroke-width': 6, 'stroke-dasharray': '2 12', 'stroke-linecap': 'round', style: 'stroke:var(--ink-2)' });
      const p = add(svg, 'path', { id: 'rutaPath', d, fill: 'none', 'stroke-width': 8, 'stroke-linecap': 'round', pathLength: 1, style: 'stroke:var(--green)' }); anim(p, 'draw', 300);
      p.style.animationDuration = '3s';
      S.forEach((s, i) => {
        const g = add(svg, 'g', {});
        g.appendChild(el('circle', { cx: x(i), cy: y, r: 26, style: `fill:${i === 2 ? 'var(--green)' : 'var(--white)'};stroke:#151311;stroke-width:5` }));
        g.appendChild(el('text', { x: x(i), y: y + 9, 'text-anchor': 'middle', 'font-size': 24, style: `font-family:var(--display);fill:${i === 2 ? '#fff' : 'var(--ink)'}` }, i + 1));
        g.appendChild(el('text', { x: x(i), y: y + 84, 'text-anchor': 'middle', 'font-size': 23, 'font-weight': 800, style: 'fill:var(--ink)' }, s[0]));
        g.appendChild(el('text', { x: x(i), y: y + 112, 'text-anchor': 'middle', 'font-size': 18, 'font-weight': 600, style: 'fill:var(--ink-2)' }, s[1]));
        anim(g, 'pop', 300 + i * 520);
      });
      const truck = add(svg, 'g', { 'data-motion': '' });
      truck.appendChild(el('circle', { r: 16, style: 'fill:var(--mustard);stroke:#151311;stroke-width:4' }));
      const m = el('animateMotion', { dur: '3s', begin: 'indefinite', fill: 'freeze', rotate: '0' }); m.appendChild(el('mpath', { href: '#rutaPath' })); truck.appendChild(m);
      const st = txt(svg, w / 2, h - 18, 'Resultado: sin desviaciones · la empresa lo comunicó igual', { a: 'middle', size: 24, w: 800, fill: 'var(--green)' }); anim(st, 'up', 3300);
    },

    confianza(svg) {
      const [w, h] = size(svg), R = D.confianza, x0 = 44, top = 20, bot = h - 34, pw = w - x0 - 50;
      const step = pw / (R.length - 1), X = i => x0 + i * step, Y = v => bot - v / 100 * (bot - top);
      const cs = R.findIndex(r => r.fase === 'Crisis'), ce = R.map(r => r.fase).lastIndexOf('Crisis'), pj = R.findIndex(r => r.fase.includes('proyecc')), last = pj - 1;
      const band = add(svg, 'rect', { x: X(cs) - step / 2, y: top, width: (ce - cs + 1) * step, height: bot - top, style: 'fill:url(#htR);opacity:.35' }); anim(band, 'fade', 200);
      txt(svg, X(cs) - step / 2 + 8, top + 24, 'CRISIS', { size: 17, w: 800, fill: 'var(--red)' });
      [0, 50, 100].forEach(v => { add(svg, 'line', { x1: x0, x2: x0 + pw, y1: Y(v), y2: Y(v), style: 'stroke:var(--ink-2);opacity:.25' }); txt(svg, x0 - 10, Y(v) + 6, v, { a: 'end', size: 16, w: 700, fill: 'var(--ink-2)' }); });
      add(svg, 'line', { x1: x0, x2: x0 + pw, y1: Y(75), y2: Y(75), 'stroke-width': 3, 'stroke-dasharray': '8 6', style: 'stroke:#C99400' });
      txt(svg, x0 + 6, Y(75) + 26, 'META 75', { size: 17, w: 800, fill: '#C99400' });
      const path = idx => idx.map((i, k) => `${k ? 'L' : 'M'}${X(i)} ${Y(R[i].v)}`).join('');
      const a = add(svg, 'path', { d: path(R.slice(0, pj).map((_, i) => i)), fill: 'none', 'stroke-width': 8, 'stroke-linejoin': 'round', pathLength: 1, style: 'stroke:var(--green)' }); anim(a, 'draw', 300);
      const b = add(svg, 'path', { d: path(R.map((_, i) => i).slice(last)), fill: 'none', 'stroke-width': 6, 'stroke-dasharray': '3 12', 'stroke-linecap': 'round', style: 'stroke:var(--green)' }); anim(b, 'fade', 1500);
      R.forEach((r, i) => { const c = add(svg, 'circle', { cx: X(i), cy: Y(r.v), r: 7, style: i >= pj ? 'fill:var(--paper);stroke:var(--green);stroke-width:3' : 'fill:var(--green)' }); anim(c, 'pop', 300 + i * 70); if (i % 3 === 0) txt(svg, X(i), bot + 26, `${mes(r.m)} ${r.m.slice(2, 4)}`, { a: 'middle', size: 16, w: 700, fill: 'var(--ink-2)' }); });
      const low = R.reduce((m, r) => r.v < m.v ? r : m), li = R.indexOf(low);
      [[li, low.v, 'var(--red)', 52], [last, R[last].v, 'var(--ink)', -22], [R.length - 1, R.at(-1).v, 'var(--green)', -22]].forEach(([i, v, c, dy], k) => {
        const t = txt(svg, X(i), Y(v) + dy, v, { a: 'middle', size: 54, w: 400, fill: c, font: 'var(--display)' }); anim(t, 'pop', 900 + k * 500);
      });
    },

    ventas(svg) {
      const [w, h] = size(svg), R = K.filter(r => r.mes >= '2026-03'), base = row('2026-03').ventas_linea_vegana_mm_cop;
      const bot = h - 34, top = 30, band = w / R.length, bw = band * .66, y = v => bot - v / 460 * (bot - top);
      R.forEach((r, i) => {
        const v = r.ventas_linea_vegana_mm_cop, proj = r.fase.includes('proyecc'), x = i * band + (band - bw) / 2;
        const b = add(svg, 'rect', { x, y: y(v), width: bw, height: bot - y(v), style: proj ? 'fill:url(#htG);stroke:#151311;stroke-width:3' : r.mes >= '2026-04' ? 'fill:var(--ink)' : 'fill:var(--ink-2)' }); anim(b, 'grow', 200 + i * 90);
        b.appendChild(el('title', {}, `${r.mes}: ${v} MM COP${proj ? ' (proyección)' : ''}`));
        txt(svg, x + bw / 2, bot + 24, mes(r.mes), { a: 'middle', size: 16, w: 700, fill: 'var(--ink-2)' });
        if (['2026-05', '2026-09', '2027-03'].includes(r.mes)) { const t = txt(svg, x + bw / 2, y(v) - 12, v, { a: 'middle', size: 30, w: 400, font: 'var(--display)', fill: r.mes === '2027-03' ? 'var(--green)' : 'var(--ink)' }); anim(t, 'up', 600 + i * 90); }
      });
      add(svg, 'line', { x1: 0, x2: w, y1: y(base), y2: y(base), 'stroke-width': 3, 'stroke-dasharray': '8 6', style: 'stroke:var(--ink)' });
      txt(svg, 4, y(base) - 12, `nivel previo: ${base}`, { size: 17, w: 800 });
    },
  };

  // acciones críticas: una sola fuente para la matriz y la hoja de ruta
  const ACC = [
    { n: 1, s: 'Bloqueo de liberación 6/6', t: 'Bloqueo de liberación 6/6', o: 'Calidad', imp: 9.6, esf: 1.8, d0: 0, d1: 10 },
    { n: 2, s: 'Ficha de hechos + auditoría IA', t: 'Ficha de hechos + auditoría IA de mensajes', o: 'Comunicación y Jurídica', imp: 9, esf: 2.6, d0: 0, d1: 14 },
    { n: 3, s: 'Atención humana a afectados', t: 'Atención humana a afectados', o: 'Atención al Consumidor', imp: 8.2, esf: 4.2, d0: 0, d1: 30 },
    { n: 4, s: 'Auditoría turno noche, Chía', t: 'Auditoría del turno noche', o: 'Operaciones', imp: 8, esf: 3.4, d0: 7, d1: 45 },
    { n: 5, s: 'Escucha social y anti-rumor', t: 'Escucha social contra rumores', o: 'Comunicación', imp: 6.2, esf: 3, d0: 14, d1: 40 },
    { n: 6, s: 'Kit de evidencia distribuidores', t: 'Kit de evidencia para distribuidores', o: 'Comercial', imp: 7.4, esf: 5.6, d0: 30, d1: 60 },
    { n: 7, s: 'Trazabilidad lote → tienda', t: 'Trazabilidad lote → tienda', o: 'Operaciones y TI', imp: 8.8, esf: 7.6, d0: 20, d1: 80 },
    { n: 8, s: 'Verificación universitaria', t: 'Verificación universitaria', o: 'Dirección', imp: 7.8, esf: 6.6, d0: 45, d1: 90 },
  ];
  document.querySelectorAll('svg[data-chart]').forEach(svg => charts[svg.dataset.chart]?.(svg));

  // ---------- valores calculados desde los datos ----------
  const lost = K.filter(r => r.mes >= '2026-04' && r.mes <= '2026-09').reduce((s, r) => s + Math.max(0, row('2026-03').ventas_linea_vegana_mm_cop - r.ventas_linea_vegana_mm_cop), 0);
  document.querySelectorAll('[data-count-lost]').forEach(n => n.dataset.count = lost);
  document.querySelectorAll('[data-count-gain]').forEach(n => n.dataset.count = row('2027-03').ventas_linea_vegana_mm_cop - row('2026-09').ventas_linea_vegana_mm_cop);

  // ---------- efectos al entrar a una diapositiva ----------
  const timers = [];
  function playEffects(s) {
    timers.splice(0).forEach(clearTimeout);
    s.querySelectorAll('[data-count]').forEach(n => {
      const to = Number(n.dataset.count), from = Number(n.dataset.from || 0), dur = Number(n.dataset.dur || 1300);
      const hostD = parseInt(getComputedStyle(n.closest('[data-d]') || n).getPropertyValue('--d')) || 0;
      n.textContent = nf(from);
      timers.push(setTimeout(() => {
        const t0 = performance.now();
        const tick = now => { const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3); n.textContent = nf(Math.round(from + (to - from) * e)); if (p < 1) requestAnimationFrame(tick); };
        requestAnimationFrame(tick);
      }, hostD + 150));
    });
    s.querySelectorAll('animateMotion').forEach(m => { try { m.beginElement(); } catch (e) { /* SMIL no disponible */ } });
    s.querySelectorAll('[data-type]').forEach(term => {
      const L = [['$ ', 'pip install -r requirements.txt'], ['', '✓ pandas · numpy · openpyxl · matplotlib', 'ok'], ['$ ', 'python src/gen_datos.py datos'], ['', 'PQR 1025 | lotes 216 | controles 1307 | kpi 18', 'ok'], ['$ ', 'python src/aed_alimenta_familia.py datos resultados/figuras'], ['', '✓ 994 PQR válidas · 1296 controles · 7 figuras', 'ok'], ['', 'semilla 2026 → siempre los mismos datos', 'ok']];
      term.innerHTML = ''; let li = 0;
      const next = () => {
        if (li >= L.length) { term.insertAdjacentHTML('beforeend', '<span class="p">$ </span><span class="blink">▍</span>'); return; }
        const [pr, line, cls] = L[li++], div = document.createElement('div'); div.innerHTML = `<span class="p">${pr}</span><span class="${cls || ''}"></span>`; term.appendChild(div);
        const span = div.lastChild; let k = 0;
        const typeCh = () => { span.textContent = line.slice(0, ++k); if (k < line.length) timers.push(setTimeout(typeCh, cls ? 6 : 24)); else timers.push(setTimeout(next, cls ? 200 : 380)); };
        typeCh();
      };
      timers.push(setTimeout(next, 600));
    });
  }

  // ---------- anexo de datos simulados (oculto por defecto) ----------
  let annexOn = store.get('anexo') === '1';
  function applyAnnex() {
    ALL.forEach(s => s.classList.toggle('hidden-annex', s.hasAttribute('data-annex') && !annexOn));
    document.body.classList.toggle('annex-on', annexOn);
    document.getElementById('annexBtn').classList.toggle('on', annexOn);
    document.getElementById('annexBtn').textContent = annexOn ? '▤ Datos ✓' : '▤ Datos';
  }
  const slides = () => ALL.filter(s => annexOn || !s.hasAttribute('data-annex'));
  function toggleAnnex() {
    const curEl = slides()[cur]; annexOn = !annexOn; store.set('anexo', annexOn ? '1' : '0'); applyAnnex();
    const list = slides(); let i = list.indexOf(curEl); if (i < 0) i = list.length - 1;
    toast(annexOn ? 'Anexo de datos simulados activado · está al final' : 'Anexo de datos simulados oculto');
    go(i, true);
  }
  const goAnnex = () => { if (!annexOn) toggleAnnex(); go(slides().findIndex(s => s.hasAttribute('data-annex'))); };

  // ---------- navegación con pasos ----------
  let cur = 0, step = 0, prevEl = null;
  function setStep(s, n) {
    step = n;
    s.querySelectorAll('[data-b]').forEach(b => b.classList.toggle('on', Number(b.dataset.b) <= n));
    s.querySelectorAll('[data-bc]').forEach(b => { const [k, c] = b.dataset.bc.split(':'); b.classList.toggle(c, Number(k) <= n); });
    renderNotes();
  }
  function go(i, keep = false, atEnd = false) {
    const list = slides(); i = Math.max(0, Math.min(list.length - 1, i));
    const s = list[i];
    if (prevEl && prevEl !== s && !keep) { prevEl.classList.remove('active'); prevEl.classList.add('leaving'); const p = prevEl; setTimeout(() => p.classList.remove('leaving'), 450); }
    ALL.forEach(x => { if (x !== s) x.classList.remove('active', 'current'); });
    if (prevEl !== s || keep) { s.classList.remove('active'); void s.offsetWidth; s.classList.add('active'); if (prevEl !== s) playEffects(s); }
    s.classList.add('current');
    cur = i; prevEl = s;
    setStep(s, atEnd ? Number(s.dataset.steps || 0) : (keep ? step : 0));
    list.forEach((x, k) => { const pg = x.querySelector('.pg'); if (pg) pg.textContent = `${k + 1} / ${list.length}`; });
    document.getElementById('count').textContent = `${i + 1} / ${list.length}`;
    const pr = document.getElementById('progress'); pr.style.width = `${(i + 1) / list.length * 100}%`; pr.style.background = BAR[s.dataset.speaker];
    try { history.replaceState(null, '', `#${i + 1}`); } catch (e) { /* file:// */ }
  }
  const next = () => { const s = slides()[cur], n = Number(s.dataset.steps || 0); if (step < n) setStep(s, step + 1); else go(cur + 1); };
  const prev = () => { const s = slides()[cur]; if (step > 0) setStep(s, step - 1); else go(cur - 1, false, true); };

  function renderNotes() {
    const list = slides(), s = list[cur], n = list[cur + 1], note = s.querySelector('.notes'), total = Number(s.dataset.steps || 0);
    document.getElementById('notes-panel').innerHTML = `<div class="np-who" style="color:${BAR[s.dataset.speaker]}">${s.dataset.speaker}</div><div class="np-title">${s.dataset.title}</div>` +
      (total ? `<div class="np-step">Paso ${step} de ${total} · → para revelar</div>` : '') + `<div>${note ? note.innerHTML.replace(/\[→\]/g, '<b style="color:#F2B705">[→]</b>') : ''}</div>` +
      (n ? `<div class="np-next">Sigue: <b>${n.dataset.title}</b> · ${n.dataset.speaker}${n.dataset.speaker !== s.dataset.speaker ? ' (cambio de expositor)' : ''}</div>` : '<div class="np-next">Fin</div>');
  }
  function toast(m) { const t = document.getElementById('toast'); t.textContent = m; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 2200); }

  // ---------- escala, vistas y controles ----------
  function fit() {
    if (document.body.classList.contains('overview')) return;
    const st = document.getElementById('stage').getBoundingClientRect();
    deck.style.transform = `scale(${Math.min(st.width / 1280, st.height / 720)})`;
  }
  window.addEventListener('resize', fit);
  function toggle(cls) {
    const map = { notes: 'notes-open', help: 'help-open' };
    document.body.classList.toggle(map[cls] || cls);
    if (cls === 'overview' && document.body.classList.contains('overview')) { deck.style.transform = 'none'; slides()[cur].scrollIntoView({ block: 'center' }); }
    else setTimeout(fit, 260);
  }
  ALL.forEach(s => s.addEventListener('click', () => { if (document.body.classList.contains('overview')) { toggle('overview'); go(slides().indexOf(s)); } }));
  const theme = () => { document.body.classList.toggle('night'); store.set('tema', document.body.classList.contains('night') ? 'noche' : 'dia'); };
  let t0 = null, acc = 0, tick = null;
  const fmt = ms => { const s = Math.floor(ms / 1000); return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; };
  function timer() { if (tick) { acc += Date.now() - t0; clearInterval(tick); tick = null; return; } t0 = Date.now(); tick = setInterval(() => { document.getElementById('timer').textContent = fmt(acc + Date.now() - t0); }, 500); }
  const resetTimer = () => { acc = 0; t0 = Date.now(); document.getElementById('timer').textContent = '00:00'; };
  const full = () => (!document.fullscreenElement ? document.documentElement.requestFullscreen?.() : document.exitFullscreen?.());

  document.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); prev(); }
    else if (k === 'Home') go(0); else if (k === 'End') go(slides().length - 1);
    else if (/^[1-5]$/.test(k)) go(slides().findIndex(s => s.dataset.speaker === ORDER[Number(k) - 1] && !s.hasAttribute('data-annex')));
    else if (/^[dD]$/.test(k)) toggleAnnex();
    else if (/^[nN]$/.test(k)) toggle('notes'); else if (/^[oO]$/.test(k)) toggle('overview');
    else if (k === 'Escape') { document.body.classList.remove('help-open'); if (document.body.classList.contains('overview')) toggle('overview'); }
    else if (/^[fF]$/.test(k)) full(); else if (/^[lL]$/.test(k)) theme();
    else if (/^[tT]$/.test(k)) timer(); else if (/^[rR]$/.test(k)) resetTimer(); else if (k === '?') toggle('help');
  });
  document.getElementById('hud').addEventListener('click', e => {
    const a = e.target.closest('button')?.dataset.act; if (!a) return;
    ({ prev, next, notes: () => toggle('notes'), overview: () => toggle('overview'), theme, annex: toggleAnnex, goAnnex, timer, full, help: () => toggle('help') })[a]();
  });
  document.getElementById('help').addEventListener('click', () => toggle('help'));
  document.querySelectorAll('[data-annex-cta]').forEach(b => b.addEventListener('click', e => { e.stopPropagation(); goAnnex(); }));
  let hudT = null;
  document.addEventListener('mousemove', () => { document.body.classList.add('show-hud'); clearTimeout(hudT); hudT = setTimeout(() => document.body.classList.remove('show-hud'), 2400); });
  let sx = null;
  document.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) (dx < 0 ? next : prev)(); sx = null; });

  // ---------- inicio ----------
  if (store.get('tema') === 'noche' || new URLSearchParams(location.search).get('tema') === 'noche') document.body.classList.add('night');
  if (new URLSearchParams(location.search).get('anexo') === '1') annexOn = true;
  applyAnnex();
  document.body.classList.add('show-hud'); setTimeout(() => document.body.classList.remove('show-hud'), 5000);
  window.deckAPI = { go, count: () => slides().length, toggleAnnex, finish: () => { const sl = slides()[cur]; setStep(sl, Number(sl.dataset.steps || 0)); } };
  const h0 = parseInt(location.hash.slice(1), 10);
  go(Number.isFinite(h0) ? h0 - 1 : 0);
  fit();
})();
