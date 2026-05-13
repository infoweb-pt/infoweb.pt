/**
 * Website ROI Calculator
 */

'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let toolRunStartedAt = 0;

// ─── UI Helpers ───────────────────────────────────────────────────────────────
function show(id)   { document.getElementById(id).classList.remove('hidden'); }
function hide(id)   { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}
function hideFlex(id) {
  const el = document.getElementById(id);
  el.classList.add('hidden');
  el.classList.remove('show-flex');
}

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  const customerValue = parseFloat(document.getElementById('customer-value').value);
  const monthlyVisitors = parseFloat(document.getElementById('monthly-visitors').value);
  const conversionRate = parseFloat(document.getElementById('conversion-rate').value);
  const websiteCost = parseFloat(document.getElementById('website-cost').value);

  if (!customerValue || !monthlyVisitors || !conversionRate || !websiteCost) {
    alert('Please fill in all fields.');
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    // Calculate ROI
    const monthlyCustomers = Math.round(monthlyVisitors * (conversionRate / 100));
    const monthlyRevenue = monthlyCustomers * customerValue;
    const annualRevenue = monthlyRevenue * 12;
    const roi = ((annualRevenue - websiteCost) / websiteCost) * 100;
    const breakEven = websiteCost / monthlyRevenue;

    renderResult({
      monthlyRevenue,
      annualRevenue,
      roi,
      breakEven,
      monthlyCustomers
    });
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

function renderResult(data) {
  // Format numbers
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-PT', {
      style: 'currency',
      currency: 'EUR'
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('pt-PT').format(value);
  };

  // Update display
  document.getElementById('monthly-revenue').textContent = formatCurrency(data.monthlyRevenue);
  document.getElementById('annual-revenue').textContent = formatCurrency(data.annualRevenue);
  document.getElementById('roi-percentage').textContent = formatNumber(Math.round(data.roi)) + '%';
  document.getElementById('break-even').textContent = data.breakEven <= 1 
    ? '< 1 month' 
    : Math.ceil(data.breakEven) + ' months';
  document.getElementById('new-customers').textContent = formatNumber(data.monthlyCustomers);

  // Show result
  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      monthly_revenue: data.monthlyRevenue,
      roi: data.roi
    });
  }
}

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');

  document.getElementById('customer-value').value = '';
  document.getElementById('monthly-visitors').value = '';
  document.getElementById('conversion-rate').value = '';
  document.getElementById('website-cost').value = '';

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  // Initialize
});
