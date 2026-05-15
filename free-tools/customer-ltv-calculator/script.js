/**
 * Customer LTV Calculator
 */

'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

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

async function runTool() {
  const avgOrderValue = parseFloat(document.getElementById('avg-order-value').value);
  const purchaseFrequency = parseFloat(document.getElementById('purchase-frequency').value);
  const customerLifespan = parseFloat(document.getElementById('customer-lifespan').value);
  const profitMargin = parseFloat(document.getElementById('profit-margin').value);

  if (!Number.isFinite(avgOrderValue) || avgOrderValue <= 0 ||
      !Number.isFinite(purchaseFrequency) || purchaseFrequency <= 0 ||
      !Number.isFinite(customerLifespan) || customerLifespan <= 0 ||
      !Number.isFinite(profitMargin) || profitMargin <= 0 || profitMargin > 100) {
    alert(L('Please fill in all fields with valid numbers.', 'Preencha todos os campos com números válidos.'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const annualValue = avgOrderValue * purchaseFrequency;
    const ltv = annualValue * customerLifespan;
    const totalOrders = Math.round(purchaseFrequency * customerLifespan);
    const grossProfit = ltv * (profitMargin / 100);
    const monthlyValue = annualValue / 12;

    renderResult({ ltv, annualValue, totalOrders, grossProfit, monthlyValue });
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

function renderResult(data) {
  const loc = PT ? 'pt-PT' : 'en-GB';
  const formatCurrency = (value) => new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR' }).format(value);
  const formatNumber = (value) => new Intl.NumberFormat(loc).format(value);

  document.getElementById('ltv').textContent = formatCurrency(data.ltv);
  document.getElementById('annual-value').textContent = formatCurrency(data.annualValue);
  document.getElementById('total-orders').textContent = formatNumber(data.totalOrders);
  document.getElementById('gross-profit').textContent = formatCurrency(data.grossProfit);
  document.getElementById('monthly-value').textContent = formatCurrency(data.monthlyValue);

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      ltv: data.ltv,
      annual_value: data.annualValue
    });
  }
}

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

function resetTool() {
  hide('result-box');
  hide('error-box');
  document.getElementById('avg-order-value').value = '';
  document.getElementById('purchase-frequency').value = '';
  document.getElementById('customer-lifespan').value = '';
  document.getElementById('profit-margin').value = '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
