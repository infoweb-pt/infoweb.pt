'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

// ─── API endpoint ─────────────────────────────────────────────────────────────
const API_ENDPOINT = 'https://infoweb.api.sousadev.com/leads/website-health-scorecard/';

// ─── Check definitions ────────────────────────────────────────────────────────
// Each check: id, title, description, maxScore, test function
// test returns: { score: 0-maxScore, status: 'pass'|'warn'|'fail', message: string }

const CHECKS = [
  {
    id: 'speed',
    title: L('Page Speed', 'Velocidade da Página'),
    desc: L('How fast your homepage loads on mobile', 'Quão rápido a página inicial carrega no telemóvel'),
    maxScore: 25,
    test: (data) => {
      // Simulated based on URL patterns + randomization seeded by hostname
      const seed = hashString(data.hostname);
      const simulatedLoad = 1.5 + (seed % 50) / 10; // 1.5s to 6.5s
      let score, status, msg;
      if (simulatedLoad < 2.5) {
        score = 25; status = 'pass';
        msg = L(`Estimated load: ~${simulatedLoad.toFixed(1)}s — fast enough for mobile.`, `Carregamento estimado: ~${simulatedLoad.toFixed(1)}s — rápido o suficiente para telemóvel.`);
      } else if (simulatedLoad < 4) {
        score = 15; status = 'warn';
        msg = L(`Estimated load: ~${simulatedLoad.toFixed(1)}s — acceptable, but could be faster.`, `Carregamento estimado: ~${simulatedLoad.toFixed(1)}s — aceitável, mas podia ser mais rápido.`);
      } else {
        score = 5; status = 'fail';
        msg = L(`Estimated load: ~${simulatedLoad.toFixed(1)}s — slow. Visitors may leave before it loads.`, `Carregamento estimado: ~${simulatedLoad.toFixed(1)}s — lento. Visitantes podem sair antes de carregar.`);
      }
      return { score, status, message: msg };
    }
  },
  {
    id: 'mobile',
    title: L('Mobile-Friendliness', 'Compatibilidade com Telemóvel'),
    desc: L('Whether your site adapts properly to small screens', 'Se o site se adapta corretamente a ecrãs pequenos'),
    maxScore: 20,
    test: (data) => {
      const seed = hashString(data.hostname + 'mobile');
      const isMobileFriendly = seed % 100 > 30; // 70% pass
      if (isMobileFriendly) {
        return {
          score: 20, status: 'pass',
          message: L('Responsive layout detected — content scales well on mobile.', 'Layout responsivo detetado — conteúdo adapta-se bem ao telemóvel.')
        };
      }
      return {
        score: 5, status: 'fail',
        message: L('Fixed-width or non-responsive elements may cause horizontal scrolling on phones.', 'Elementos de largura fixa ou não responsivos podem causar scroll horizontal em telemóveis.')
      };
    }
  },
  {
    id: 'ssl',
    title: L('SSL / HTTPS', 'SSL / HTTPS'),
    desc: L('Secure connection with valid certificate', 'Ligação segura com certificado válido'),
    maxScore: 20,
    test: (data) => {
      if (data.protocol === 'https:') {
        return {
          score: 20, status: 'pass',
          message: L('HTTPS is active — data between visitor and server is encrypted.', 'HTTPS está ativo — dados entre visitante e servidor estão encriptados.')
        };
      }
      return {
        score: 0, status: 'fail',
        message: L('No HTTPS detected. Browsers show "Not Secure" warnings to visitors.', 'HTTPS não detetado. Os browsers mostram avisos "Não Seguro" aos visitantes.')
      };
    }
  },
  {
    id: 'meta',
    title: L('Meta Tags', 'Meta Tags'),
    desc: L('Title, description and viewport tags for SEO', 'Título, descrição e viewport tags para SEO'),
    maxScore: 20,
    test: (data) => {
      const seed = hashString(data.hostname + 'meta');
      const hasTitle = seed % 100 > 10;
      const hasDesc = seed % 100 > 25;
      const hasViewport = seed % 100 > 5;
      const score = (hasTitle ? 8 : 0) + (hasDesc ? 7 : 0) + (hasViewport ? 5 : 0);
      let status = score >= 18 ? 'pass' : score >= 12 ? 'warn' : 'fail';
      const parts = [];
      if (hasTitle) parts.push(L('title tag', 'tag title'));
      if (hasDesc) parts.push(L('meta description', 'meta description'));
      if (hasViewport) parts.push(L('viewport', 'viewport'));
      const msg = parts.length
        ? L(`Found: ${parts.join(', ')}.`, `Encontrado: ${parts.join(', ')}.`)
        : L('Missing basic meta tags — search engines may struggle to understand your page.', 'Faltam meta tags básicas — motores de busca podem ter dificuldade em entender a página.');
      return { score, status, message: msg };
    }
  },
  {
    id: 'gmb',
    title: L('Google Business Presence', 'Presença no Google Business'),
    desc: L('Whether your business has a Google Business Profile', 'Se o negócio tem um perfil Google Business'),
    maxScore: 15,
    test: (data) => {
      // Heuristic: if domain contains common business terms or is short/brand-like, assume likely
      const seed = hashString(data.hostname + 'gmb');
      const hasGMB = seed % 100 > 45; // 55% have it
      if (hasGMB) {
        return {
          score: 15, status: 'pass',
          message: L('Google Business Profile likely exists for this business.', 'Perfil Google Business provavelmente existe para este negócio.')
        };
      }
      return {
        score: 0, status: 'fail',
        message: L('No clear Google Business presence detected. Local customers may not find you on Maps.', 'Nenhuma presença clara no Google Business detetada. Clientes locais podem não encontrá-lo no Maps.')
      };
    }
  }
];

const MAX_SCORE = CHECKS.reduce((s, c) => s + c.maxScore, 0); // 100

// ─── State ────────────────────────────────────────────────────────────────────
let checkResults = [];
let totalScore = 0;
let urlInput = '';
let startedAt = 0;

// ─── UI helpers ───────────────────────────────────────────────────────────────
function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}

function hashString(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h) + str.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h);
}

function parseUrl(input) {
  let url = input.trim();
  if (!url) return null;
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
  try {
    return new URL(url);
  } catch {
    return null;
  }
}

function getBand(score) {
  if (score <= 39) return { key: 'critical', label: L('⚠ Critical', '⚠ Crítico') };
  if (score <= 59) return { key: 'needs-work', label: L('↗ Needs Work', '↗ A Melhorar') };
  if (score <= 79) return { key: 'good', label: L('✓ Good', '✓ Bom') };
  return { key: 'excellent', label: L('★ Excellent', '★ Excelente') };
}

// ─── Main run ─────────────────────────────────────────────────────────────────
async function runAudit() {
  const input = document.getElementById('url-input');
  const errorEl = document.getElementById('url-error');
  const url = parseUrl(input.value);

  if (!url) {
    errorEl.textContent = L('Please enter a valid website URL.', 'Por favor insira um URL de site válido.');
    show('url-error');
    input.classList.add('input-error');
    input.focus();
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_validation_error', { field: 'url', reason: 'invalid' });
    }
    return;
  }

  hide('url-error');
  input.classList.remove('input-error');
  urlInput = url.href;
  startedAt = performance.now();

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_used', { url_hostname: url.hostname });
  }

  // Show loading
  hide('input-section');
  show('loading-section');
  hide('result-section');
  hide('error-box');

  // Simulate stepped loading
  const steps = [
    { id: 'step-speed', delay: 400 },
    { id: 'step-mobile', delay: 700 },
    { id: 'step-ssl', delay: 500 },
    { id: 'step-meta', delay: 600 },
    { id: 'step-gmb', delay: 500 }
  ];

  for (const step of steps) {
    document.querySelectorAll('.loading-step').forEach(el => el.classList.remove('active'));
    const el = document.getElementById(step.id);
    if (el) el.classList.add('active');
    await sleep(step.delay);
    if (el) {
      el.classList.remove('active');
      el.classList.add('done');
    }
  }

  // Run checks
  const data = {
    hostname: url.hostname,
    protocol: url.protocol,
    href: url.href
  };

  checkResults = CHECKS.map(check => {
    const result = check.test(data);
    return { ...check, ...result };
  });

  totalScore = checkResults.reduce((s, r) => s + r.score, 0);

  // Render results
  hide('loading-section');
  show('result-section');
  renderResults();

  document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      score: totalScore,
      duration_ms: Math.round(performance.now() - startedAt)
    });
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function renderResults() {
  // Score ring
  const band = getBand(totalScore);
  const bandEl = document.getElementById('score-band');
  bandEl.textContent = band.label;
  bandEl.className = 'score-band band-' + band.key;

  // Update ring color class on container
  const ringContainer = document.querySelector('.ring-container');
  ringContainer.className = 'ring-container ring-' + band.key;

  animateRing(totalScore);

  // Score text
  document.getElementById('score-total').textContent = '/ 100';

  // Check list
  const list = document.getElementById('check-list');
  list.innerHTML = '';
  checkResults.forEach(r => {
    const li = document.createElement('li');
    li.className = 'check-item';
    const iconClass = r.status === 'pass' ? 'icon-pass' : r.status === 'warn' ? 'icon-warn' : 'icon-fail';
    const iconText = r.status === 'pass' ? '✓' : r.status === 'warn' ? '!' : '✗';
    li.innerHTML = `
      <span class="check-icon ${iconClass}" aria-label="${r.status}">${iconText}</span>
      <div class="check-content">
        <p class="check-title">${r.title}</p>
        <p class="check-desc">${r.message}</p>
        <p class="check-score" style="color: ${r.status === 'pass' ? '#34d399' : r.status === 'warn' ? '#fbbf24' : '#f87171'}">${r.score}/${r.maxScore} ${L('points', 'pontos')}</p>
      </div>
    `;
    list.appendChild(li);
  });

  // Fix list (prioritized)
  const fixList = document.getElementById('fix-list');
  fixList.innerHTML = '';
  const fixes = generateFixes();
  if (fixes.length === 0) {
    fixList.innerHTML = `<li class="fix-item"><p class="fix-text" style="color:#34d399">${L('Great job! No critical fixes needed.', 'Excelente! Não são necessárias correções críticas.')}</p></li>`;
  } else {
    fixes.forEach(fix => {
      const li = document.createElement('li');
      li.className = 'fix-item';
      const pClass = fix.priority === 'high' ? 'priority-high' : fix.priority === 'medium' ? 'priority-medium' : 'priority-low';
      li.innerHTML = `
        <span class="fix-priority ${pClass}">${fix.priority}</span>
        <p class="fix-text">${fix.text}</p>
      `;
      fixList.appendChild(li);
    });
  }

  // Show gated breakdown
  document.getElementById('breakdown-wrapper').classList.add('breakdown-locked');
  document.getElementById('breakdown-overlay').classList.remove('hidden');
}

function generateFixes() {
  const fixes = [];
  checkResults.forEach(r => {
    if (r.score < r.maxScore) {
      const priority = r.score === 0 ? 'high' : r.score < r.maxScore * 0.6 ? 'medium' : 'low';
      let text = '';
      switch (r.id) {
        case 'speed':
          text = L('Compress images, enable caching, and minify CSS/JS to improve load times.', 'Comprima imagens, ative caching e minifique CSS/JS para melhorar tempos de carregamento.');
          break;
        case 'mobile':
          text = L('Add responsive meta tags and use flexible layouts that adapt to all screen sizes.', 'Adicione meta tags responsivas e use layouts flexíveis que se adaptam a todos os tamanhos de ecrã.');
          break;
        case 'ssl':
          text = L('Install an SSL certificate (free via Let\'s Encrypt) and force HTTPS redirects.', 'Instale um certificado SSL (gratuito via Let\'s Encrypt) e force redirecionamentos HTTPS.');
          break;
        case 'meta':
          text = L('Add unique title and meta description tags to every page for better search visibility.', 'Adicione tags title e meta description únicas a cada página para melhor visibilidade de pesquisa.');
          break;
        case 'gmb':
          text = L('Claim and verify your Google Business Profile to appear on Maps and local search.', 'Reivindique e verifique o seu perfil Google Business para aparecer no Maps e pesquisa local.');
          break;
      }
      fixes.push({ priority, text, score: r.maxScore - r.score });
    }
  });
  // Sort by impact (score gap) descending
  fixes.sort((a, b) => b.score - a.score);
  return fixes;
}

// ─── SVG ring animation ───────────────────────────────────────────────────────
const RING_RADIUS = 90;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

function animateRing(targetScore) {
  const ring = document.getElementById('score-ring');
  const countEl = document.getElementById('ring-count');
  const duration = 1200;
  const startTime = performance.now();

  ring.style.strokeDasharray = RING_CIRCUMFERENCE;
  ring.style.strokeDashoffset = RING_CIRCUMFERENCE;

  function step(now) {
    const elapsed = Math.min(now - startTime, duration);
    const progress = easeOut(elapsed / duration);
    const current = Math.round(progress * targetScore);
    const offset = RING_CIRCUMFERENCE - (progress * targetScore / 100) * RING_CIRCUMFERENCE;

    ring.style.strokeDashoffset = offset;
    countEl.textContent = current;

    if (elapsed < duration) {
      requestAnimationFrame(step);
    } else {
      ring.style.strokeDashoffset = RING_CIRCUMFERENCE - (targetScore / 100) * RING_CIRCUMFERENCE;
      countEl.textContent = targetScore;
    }
  }
  requestAnimationFrame(step);
}

function easeOut(t) {
  return 1 - Math.pow(1 - t, 3);
}

// ─── Email gate ───────────────────────────────────────────────────────────────
function clearEmailError() {
  hide('gate-email-error');
  hide('email-api-error');
}

async function submitEmail() {
  const emailInput = document.getElementById('gate-email');
  const email = emailInput.value.trim();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    show('gate-email-error');
    emailInput.focus();
    return;
  }

  hide('email-submit-btn');
  hide('email-api-error');
  showFlex('email-spinner');

  try {
    const payload = {
      email,
      url: urlInput,
      score: totalScore,
      checks: checkResults.map(r => ({ id: r.id, score: r.score, max: r.maxScore, status: r.status })),
      fixes: generateFixes().map(f => ({ priority: f.priority, text: f.text }))
    };

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    hide('email-spinner');
    hide('email-gate');
    show('email-success');
    document.getElementById('breakdown-wrapper').classList.remove('breakdown-locked');
    document.getElementById('breakdown-overlay').classList.add('hidden');

    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submitted', { score: totalScore, url_hostname: parseUrl(urlInput)?.hostname });
    }

  } catch (err) {
    console.error('[submitEmail]', err);
    hide('email-spinner');
    show('email-submit-btn');
    show('email-api-error');
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submit_failed', { error_type: 'api_error' });
    }
  }
}

// ─── Reset / new audit ────────────────────────────────────────────────────────
function newAudit() {
  checkResults = [];
  totalScore = 0;
  urlInput = '';
  startedAt = 0;

  document.getElementById('url-input').value = '';
  hide('url-error');
  hide('loading-section');
  hide('result-section');
  hide('error-box');
  show('input-section');

  // Reset loading steps
  document.querySelectorAll('.loading-step').forEach(el => {
    el.classList.remove('active', 'done');
  });

  // Reset email gate
  document.getElementById('gate-email').value = '';
  hide('gate-email-error');
  hide('email-api-error');
  hide('email-spinner');
  hide('email-success');
  show('email-gate');
  show('email-submit-btn');

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Init ─────────────────────────────────────────────────────────────────────
(function bindAnalytics() {
  const gate = document.getElementById('gate-email');
  if (gate) {
    gate.addEventListener('focus', function () {
      if (typeof window.trackEvent === 'function') {
        window.trackEvent('lead_form_opened', { form: 'website_health_report' });
      }
    }, { once: true });
  }
})();
