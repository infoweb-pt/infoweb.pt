/**
 * Cost Per Lead Calculator
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
  const campaignCost = parseFloat(document.getElementById('campaign-cost').value);
  const leadsGenerated = parseFloat(document.getElementById('leads-generated').value);
  const conversionRate = parseFloat(document.getElementById('conversion-rate').value);
  const customerValue = parseFloat(document.getElementById('customer-value').value);

  if (!Number.isFinite(campaignCost) || campaignCost <= 0 ||
      !Number.isFinite(leadsGenerated) || leadsGenerated <= 0 ||
      !Number.isFinite(conversionRate) || conversionRate <= 0 ||
      !Number.isFinite(customerValue) || customerValue <= 0) {
    alert(L('Please fill in all fields with valid numbers (greater than 0).', 'Preencha todos os campos com números válidos (superiores a 0).'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const costPerLead = campaignCost / leadsGenerated;
    const customersAcquired = Math.round(leadsGenerated * (conversionRate / 100));
    const costPerCustomer = customersAcquired > 0 ? campaignCost / customersAcquired : 0;
    const revenueGenerated = customersAcquired * customerValue;
    const roi = revenueGenerated > 0 ? ((revenueGenerated - campaignCost) / campaignCost) * 100 : -100;

    renderResult({ costPerLead, costPerCustomer, customersAcquired, revenueGenerated, roi });
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

  document.getElementById('cost-per-lead').textContent = formatCurrency(data.costPerLead);
  document.getElementById('cost-per-customer').textContent = formatCurrency(data.costPerCustomer);
  document.getElementById('customers-acquired').textContent = formatNumber(data.customersAcquired);
  document.getElementById('revenue-generated').textContent = formatCurrency(data.revenueGenerated);

  let roiText;
  if (data.roi <= -100) {
    roiText = '-100%';
  } else {
    roiText = formatNumber(Math.round(data.roi)) + '%';
  }
  document.getElementById('roi').textContent = roiText;

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      cost_per_lead: data.costPerLead,
      roi: data.roi
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
  document.getElementById('campaign-cost').value = '';
  document.getElementById('leads-generated').value = '';
  document.getElementById('conversion-rate').value = '';
  document.getElementById('customer-value').value = '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
