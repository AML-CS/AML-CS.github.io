/* Mobile menu */
document.addEventListener('DOMContentLoaded', () => {
  const b = document.querySelector('.burger'), nav = document.querySelector('.nav');
  if (b && nav) b.addEventListener('click', () => { nav.classList.toggle('open'); b.setAttribute('aria-expanded', nav.classList.contains('open')); });
  // external links open in a new tab
  for (const a of document.links) if (a.hostname && a.hostname !== location.hostname) { a.target = '_blank'; a.rel = 'noreferrer'; }
});

/* Hero: a small ensemble Kalman filter, animated.
   Amber dots = ensemble members drifting under model noise.
   Every few seconds a white observation arrives and the ensemble
   is pulled toward it (analysis step, blue trail). */
(function () {
  const c = document.getElementById('da'); if (!c) return;
  const x = c.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W, H, dpr;
  function size() { dpr = Math.min(devicePixelRatio || 1, 2); W = c.clientWidth; H = c.clientHeight; c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0); }
  size(); addEventListener('resize', size);
  const N = 140, members = [];
  const truth = t => ({ x: W * 0.64 + Math.cos(t * 0.35) * W * 0.14 + Math.sin(t * 0.9) * W * 0.03, y: H * 0.5 + Math.sin(t * 0.5) * H * 0.22 });
  for (let i = 0; i < N; i++) members.push({ x: 0, y: 0, vx: 0, vy: 0, s: 0.6 + Math.random() * 1.2 });
  let t = 0, last = performance.now(), obsTimer = 0, obs = null, trail = [];
  const p0 = truth(0); members.forEach(m => { m.x = p0.x + (Math.random() - .5) * 260; m.y = p0.y + (Math.random() - .5) * 260; });
  function step(dt) {
    t += dt; const tr = truth(t); obsTimer += dt;
    if (obsTimer > 3.2) { obsTimer = 0; obs = { x: tr.x + (Math.random() - .5) * 40, y: tr.y + (Math.random() - .5) * 40, a: 1 }; }
    let mx = 0, my = 0; for (const m of members) { mx += m.x; my += m.y; } mx /= N; my /= N;
    for (const m of members) {
      m.vx += ((tr.x - m.x) * 0.22 + (Math.random() - .5) * 420) * dt;
      m.vy += ((tr.y - m.y) * 0.22 + (Math.random() - .5) * 420) * dt;
      if (obs && obs.a > 0.35) { m.vx += (obs.x - m.x) * 2.2 * dt * obs.a; m.vy += (obs.y - m.y) * 2.2 * dt * obs.a; }
      m.vx *= 0.94; m.vy *= 0.94; m.x += m.vx * dt; m.y += m.vy * dt;
    }
    if (obs) { obs.a -= dt * 0.45; if (obs.a <= 0) obs = null; }
    trail.push({ x: mx, y: my }); if (trail.length > 160) trail.shift();
  }
  function draw() {
    x.clearRect(0, 0, W, H);
    x.strokeStyle = 'rgba(255,255,255,.045)'; x.lineWidth = 1;
    for (let gx = 0; gx < W; gx += 48) { x.beginPath(); x.moveTo(gx, 0); x.lineTo(gx, H); x.stroke(); }
    for (let gy = 0; gy < H; gy += 48) { x.beginPath(); x.moveTo(0, gy); x.lineTo(W, gy); x.stroke(); }
    if (trail.length > 2) { x.beginPath(); x.moveTo(trail[0].x, trail[0].y); for (const p of trail) x.lineTo(p.x, p.y); x.strokeStyle = 'rgba(75,162,222,.75)'; x.lineWidth = 2; x.lineJoin = 'round'; x.stroke(); }
    for (const m of members) { x.beginPath(); x.arc(m.x, m.y, m.s, 0, 7); x.fillStyle = 'rgba(240,169,43,.85)'; x.fill(); }
    if (obs) { x.beginPath(); x.arc(obs.x, obs.y, 6 + 18 * (1 - obs.a), 0, 7); x.strokeStyle = `rgba(255,255,255,${obs.a * .7})`; x.lineWidth = 1.5; x.stroke(); x.beginPath(); x.arc(obs.x, obs.y, 3.5, 0, 7); x.fillStyle = `rgba(255,255,255,${Math.min(1, obs.a + .3)})`; x.fill(); }
  }
  function loop(now) { const dt = Math.min(.05, (now - last) / 1000); last = now; step(dt); draw(); requestAnimationFrame(loop); }
  if (reduce) { for (let i = 0; i < 400; i++) step(1 / 60); draw(); } else requestAnimationFrame(loop);
})();

/* Publications filters */
(function () {
  const kind = document.getElementById('kind'), year = document.getElementById('year'), q = document.getElementById('q');
  if (!kind) return;
  let k = 'all', y = 'all';
  function press(g, attr, val) { g.querySelectorAll('.chip').forEach(b => b.setAttribute('aria-pressed', b.dataset[attr] === val)); }
  kind.addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; k = b.dataset.k; press(kind, 'k', k); apply(); });
  year.addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; y = b.dataset.y; press(year, 'y', y); apply(); });
  q.addEventListener('input', apply);
  function apply() {
    const s = q.value.trim().toLowerCase(); let any = false;
    document.querySelectorAll('.yeargroup').forEach(sec => {
      let n = 0; sec.querySelectorAll('.pub').forEach(p => {
        const ok = (k === 'all' || p.dataset.k === k) && (y === 'all' || sec.dataset.y === y) && (!s || p.textContent.toLowerCase().includes(s));
        p.classList.toggle('hidden', !ok); if (ok) n++;
      });
      sec.classList.toggle('hidden', n === 0); sec.querySelector('small').textContent = n + (n === 1 ? ' paper' : ' papers'); any = any || n > 0;
    });
    document.getElementById('empty').classList.toggle('show', !any);
  }
})();

/* Lightbox for gallery figures: click to enlarge, arrows or keys to move */
(function () {
  const figs = [...document.querySelectorAll('.strip figure, .feat figure')];
  if (!figs.length) return;
  const info = f => { const img = f.querySelector('img'); const src = f.querySelector('source'); return { src: (src && src.srcset) || img.currentSrc || img.src, alt: img.alt, cap: (f.querySelector('figcaption') || {}).textContent || '' }; };
  let items = [];
  const box = document.createElement('div'); box.className = 'lightbox'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
  box.innerHTML = '<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-next" aria-label="Next">›</button><div class="lb-count"></div>';
  document.body.appendChild(box);
  const img = box.querySelector('img'), cap = box.querySelector('figcaption'), count = box.querySelector('.lb-count');
  let i = 0, open = false;
  function show(n) { i = (n + items.length) % items.length; img.src = items[i].src; img.alt = items[i].alt; cap.textContent = items[i].cap; count.textContent = (i + 1) + ' / ' + items.length; }
  function openAt(n) { const f = figs[n]; const group = f.closest('.strip') ? [...f.closest('.strip').querySelectorAll('figure')] : [f]; items = group.map(info); n = group.indexOf(f); show(n); box.classList.add('on'); document.body.style.overflow = 'hidden'; open = true; box.querySelector('.lb-close').focus(); }
  function close() { box.classList.remove('on'); document.body.style.overflow = ''; open = false; }
  figs.forEach((f, n) => { f.style.cursor = 'zoom-in'; f.tabIndex = 0; f.addEventListener('click', () => openAt(n)); f.addEventListener('keydown', e => { if (e.key === 'Enter') openAt(n); }); });
  box.querySelector('.lb-close').addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', () => show(i - 1));
  box.querySelector('.lb-next').addEventListener('click', () => show(i + 1));
  box.addEventListener('click', e => { if (e.target === box) close(); });
  document.addEventListener('keydown', e => { if (!open) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(i + 1); if (e.key === 'ArrowLeft') show(i - 1); });
  let x0 = null; box.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1)); x0 = null; });
})();

/* Carousel arrows */
document.querySelectorAll('.carousel').forEach(c => {
  const s = c.querySelector('.strip');
  c.querySelector('.prev').addEventListener('click', () => s.scrollBy({ left: -s.clientWidth * 0.8, behavior: 'smooth' }));
  c.querySelector('.next').addEventListener('click', () => s.scrollBy({ left: s.clientWidth * 0.8, behavior: 'smooth' }));
});
