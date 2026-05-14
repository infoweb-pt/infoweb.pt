'use strict';

const fmt = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'EUR',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

function parseNum(raw) {
  const s = String(raw).replace(',', '.').trim();
  if (s === '') return NaN;
  return parseFloat(s);
}

function getMode() {
  return document.querySelector('input[name="mm-mode"]:checked').value;
}

function updateModeFields() {
  const mode = getMode();
  document.getElementById('label-second').textContent =
    mode === 'margin'
      ? 'Target margin (%)'
      : mode === 'markup'
        ? 'Markup on cost (%)'
        : 'Selling price (€)';
  document.getElementById('second-field-hint').textContent =
    mode === 'margin'
      ? 'Margin is profit as a % of selling price (e.g. 40 means you keep 40% of the price as gross profit).'
      : mode === 'markup'
        ? 'Markup is profit as a % of cost (e.g. 100 doubles your cost).'
        : 'Price you charge customers (must be greater than cost).';
}

function compute() {
  const cost = parseNum(document.getElementById('mm-cost').value);
  const second = parseNum(document.getElementById('mm-second').value);
  const mode = getMode();

  const errCost = document.getElementById('err-cost');
  const errSecond = document.getElementById('err-second');
  errCost.classList.add('hidden');
  errSecond.classList.add('hidden');

  let valid = true;
  if (Number.isNaN(cost) || cost <= 0) {
    errCost.classList.remove('hidden');
    valid = false;
  }

  let price;
  let marginPct;
  let markupPct;
  let profit;

  if (mode === 'margin') {
    if (Number.isNaN(second) || second <= 0 || second >= 100) {
      errSecond.textContent = 'Enter a margin between 0 and 100 (exclusive).';
      errSecond.classList.remove('hidden');
      valid = false;
    } else {
      marginPct = second;
      price = cost / (1 - marginPct / 100);
      profit = price - cost;
      markupPct = (profit / cost) * 100;
    }
  } else if (mode === 'markup') {
    if (Number.isNaN(second) || second <= -100) {
      errSecond.textContent = 'Enter a valid markup % (greater than −100).';
      errSecond.classList.remove('hidden');
      valid = false;
    } else {
      markupPct = second;
      price = cost * (1 + markupPct / 100);
      profit = price - cost;
      marginPct = (profit / price) * 100;
    }
  } else {
    if (Number.isNaN(second) || second <= cost) {
      errSecond.textContent = 'Selling price must be greater than cost.';
      errSecond.classList.remove('hidden');
      valid = false;
    } else {
      price = second;
      profit = price - cost;
      marginPct = (profit / price) * 100;
      markupPct = (profit / cost) * 100;
    }
  }

  if (!valid) {
    document.getElementById('result-panel').classList.add('hidden');
    return null;
  }

  document.getElementById('out-cost').textContent = fmt.format(cost);
  document.getElementById('out-price').textContent = fmt.format(price);
  document.getElementById('out-profit').textContent = fmt.format(profit);
  document.getElementById('out-margin').textContent =
    marginPct.toFixed(2).replace('.', ',') + '%';
  document.getElementById('out-markup').textContent =
    markupPct.toFixed(2).replace('.', ',') + '%';

  document.getElementById('result-panel').classList.remove('hidden');
  return { mode: mode, cost: cost, price: price };
}

function scheduleCompute() {
  compute();
}

function runCalculate() {
  const r = compute();
  if (!r) return;
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_used', { mode: r.mode });
    window.trackEvent('tool_result_shown', {});
  }
  document.getElementById('result-panel').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function copyText(id) {
  const el = document.getElementById(id);
  if (!el) return;
  try {
    await navigator.clipboard.writeText(el.textContent);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('result_copied', { field: id });
    }
  } catch (e) {
    console.error(e);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  updateModeFields();
  document.querySelectorAll('input[name="mm-mode"]').forEach(function (el) {
    el.addEventListener('change', function () {
      updateModeFields();
      scheduleCompute();
    });
  });
  document.getElementById('mm-cost').addEventListener('input', scheduleCompute);
  document.getElementById('mm-second').addEventListener('input', scheduleCompute);
});
