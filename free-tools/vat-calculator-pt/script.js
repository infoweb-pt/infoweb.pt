'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

const REGION_RATES = {
  continente: [
    { label: '6%', value: 0.06 },
    { label: '13%', value: 0.13 },
    { label: '23%', value: 0.23 }
  ],
  madeira: [
    { label: '5%', value: 0.05 },
    { label: '12%', value: 0.12 },
    { label: '22%', value: 0.22 }
  ],
  acores: [
    { label: '4%', value: 0.04 },
    { label: '9%', value: 0.09 },
    { label: '16%', value: 0.16 }
  ]
};

let debounceTimer = null;
const fmt = new Intl.NumberFormat(PT ? 'pt-PT' : 'en-GB', { style: 'currency', currency: 'EUR' });

function getRegion() {
  return document.querySelector('input[name="vat-region"]:checked').value;
}

function getRate() {
  return parseFloat(document.getElementById('vat-rate').value);
}

function getMode() {
  return document.querySelector('input[name="vat-mode"]:checked').value;
}

function parseAmount() {
  const raw = document.getElementById('vat-amount').value.replace(',', '.').trim();
  if (raw === '') return NaN;
  const n = parseFloat(raw);
  return n;
}

function regionSuffix(region) {
  const cap = region.charAt(0).toUpperCase() + region.slice(1);
  if (!PT) return ' (' + cap + ' VAT)';
  const map = { continente: 'Continente', madeira: 'Madeira', acores: 'Açores' };
  return ' (IVA ' + (map[region] || cap) + ')';
}

function renderRateOptions() {
  const region = getRegion();
  const sel = document.getElementById('vat-rate');
  const rates = REGION_RATES[region];
  sel.innerHTML = '';
  rates.forEach(function (r, i) {
    const opt = document.createElement('option');
    opt.value = String(r.value);
    opt.textContent = r.label + regionSuffix(region);
    sel.appendChild(opt);
    if (region === 'continente' && r.value === 0.23) opt.selected = true;
    if (region === 'madeira' && r.value === 0.22) opt.selected = true;
    if (region === 'acores' && r.value === 0.16) opt.selected = true;
  });
}

function compute() {
  const amount = parseAmount();
  const rate = getRate();
  const mode = getMode();

  const err = document.getElementById('amount-error');
  const out = document.getElementById('result-panel');

  if (Number.isNaN(amount) || amount < 0) {
    err.classList.remove('hidden');
    out.classList.add('hidden');
    return;
  }
  err.classList.add('hidden');

  let net;
  let gross;
  let vat;

  if (mode === 'add') {
    net = amount;
    gross = net * (1 + rate);
    vat = gross - net;
  } else {
    gross = amount;
    net = gross / (1 + rate);
    vat = gross - net;
  }

  document.getElementById('out-net').textContent = fmt.format(net);
  document.getElementById('out-vat').textContent = fmt.format(vat);
  document.getElementById('out-gross').textContent = fmt.format(gross);
  document.getElementById('out-rate-pct').textContent = (rate * 100).toFixed(0).replace('.', ',') + '%';
  out.classList.remove('hidden');

  return { net: net, vat: vat, gross: gross, rate: rate, mode: mode, region: getRegion() };
}

function scheduleCompute() {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(function () {
    const r = compute();
    if (r && typeof window.trackEvent === 'function') {
      window.trackEvent('tool_input_changed', {
        field: 'vat_amount',
        region: r.region,
        mode: r.mode
      });
    }
  }, 350);
}

function runCalculate() {
  const r = compute();
  if (!r) return;
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_used', {
      mode: r.mode,
      rate: r.rate,
      region: r.region
    });
    window.trackEvent('tool_result_shown', { region: r.region });
  }
  document.getElementById('result-panel').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function copyField(field) {
  const map = { net: 'out-net', vat: 'out-vat', gross: 'out-gross' };
  const text = document.getElementById(map[field]).textContent;
  try {
    await navigator.clipboard.writeText(text);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('result_copied', { field: field });
    }
  } catch (e) {
    console.error(e);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  renderRateOptions();
  document.querySelectorAll('input[name="vat-region"]').forEach(function (el) {
    el.addEventListener('change', function () {
      renderRateOptions();
      scheduleCompute();
    });
  });
  document.getElementById('vat-rate').addEventListener('change', scheduleCompute);
  document.querySelectorAll('input[name="vat-mode"]').forEach(function (el) {
    el.addEventListener('change', scheduleCompute);
  });
  document.getElementById('vat-amount').addEventListener('input', scheduleCompute);
});
