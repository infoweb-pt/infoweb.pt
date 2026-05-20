'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) { return PT ? pt : en; }

let toolRunStartedAt = 0;

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('flex');
}
function hideFlex(id) {
  const el = document.getElementById(id);
  el.classList.add('hidden');
  el.classList.remove('flex');
}

function normalizeUrl(raw) {
  const s = String(raw).trim();
  if (!s) return '';
  if (/^https?:\/\//i.test(s)) return s;
  return 'https://' + s.replace(/^\/+/, '');
}

function buildUtmUrl(base, source, medium, campaign, term, content) {
  const u = new URL(base);
  if (source) u.searchParams.set('utm_source', source);
  if (medium) u.searchParams.set('utm_medium', medium);
  if (campaign) u.searchParams.set('utm_campaign', campaign);
  if (term) u.searchParams.set('utm_term', term);
  if (content) u.searchParams.set('utm_content', content);
  return u.toString();
}

async function copyText(text, btnId) {
  try {
    await navigator.clipboard.writeText(text);
    const btn = document.getElementById(btnId);
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = L('Copied!', 'Copiado!');
      setTimeout(() => { btn.textContent = orig; }, 2000);
    }
    if (typeof window.trackEvent === 'function') window.trackEvent('tool_copy', { field: btnId });
  } catch (e) {
    alert(L('Copy failed — select the text manually.', 'Falha ao copiar — selecione o texto manualmente.'));
  }
}

async function runTool() {
  const base = normalizeUrl(document.getElementById('base-url').value);
  const source = document.getElementById('utm-source').value.trim();
  const medium = document.getElementById('utm-medium').value.trim();
  const campaign = document.getElementById('utm-campaign').value.trim();
  const term = document.getElementById('utm-term').value.trim();
  const content = document.getElementById('utm-content').value.trim();

  if (!base || !source || !medium || !campaign) {
    alert(L('Enter a valid URL plus utm_source, utm_medium, and utm_campaign.', 'Introduza um URL válido e utm_source, utm_medium e utm_campaign.'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const full = buildUtmUrl(base, source, medium, campaign, term, content);
    const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
    document.getElementById('result-box').innerHTML = `
      <div class="bg-slate-900 border border-sky-500/30 rounded-2xl p-5">
        <p class="text-xs font-bold uppercase tracking-widest text-sky-400 mb-3">${L('Your tagged URL', 'O seu URL com UTM')}</p>
        <div class="copy-row">
          <input type="text" id="out-full" readonly value="${esc(full)}" />
          <button type="button" id="btn-copy-full" onclick="copyText(document.getElementById('out-full').value,'btn-copy-full')"
            class="shrink-0 bg-sky-600 hover:bg-sky-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy', 'Copiar')}</button>
        </div>
      </div>
      <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center">
        <h3 class="text-xl font-bold text-white mb-3">${L('Landing pages that convert', 'Páginas que convertem')}</h3>
        <p class="text-slate-400 mb-4 text-sm">${L('Pair UTMs with fast pages that capture leads.', 'Combine UTMs com páginas rápidas que captam leads.')}</p>
        <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=utm_link_builder&utm_campaign=result_cta#pricing" target="_blank" rel="noopener"
           class="inline-flex bg-sky-600 hover:bg-sky-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans', 'Ver planos de website')}</a>
      </div>
      <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 hover:text-slate-300 underline">${L('Build another', 'Criar outro')}</button></p>`;
    show('result-box');
    document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_result_shown', { duration_ms: Math.round(performance.now() - toolRunStartedAt) });
    }
  } catch (err) {
    console.error(err);
    show('error-box');
  } finally {
    hideFlex('spinner');
  }
}

function resetTool() {
  hide('result-box');
  hide('error-box');
  document.getElementById('base-url').value = '';
  document.getElementById('utm-campaign').value = '';
  document.getElementById('utm-term').value = '';
  document.getElementById('utm-content').value = '';
  document.getElementById('utm-source').value = 'freetool';
  document.getElementById('utm-medium').value = 'utm_link_builder';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
  if (!document.getElementById('utm-source').value) document.getElementById('utm-source').value = 'freetool';
  if (!document.getElementById('utm-medium').value) document.getElementById('utm-medium').value = 'utm_link_builder';
});
