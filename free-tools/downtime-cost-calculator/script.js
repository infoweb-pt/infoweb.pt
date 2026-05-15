/**
 * Downtime Cost Calculator
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
  const monthlyRevenue = parseFloat(document.getElementById('monthly-revenue').value);
  const downtimeHours = parseFloat(document.getElementById('downtime-hours').value);
  const conversionRate = parseFloat(document.getElementById('conversion-rate').value);

  if (!Number.isFinite(monthlyRevenue) || monthlyRevenue <= 0 ||
      !Number.isFinite(downtimeHours) || downtimeHours <= 0 ||
      !Number.isFinite(conversionRate) || conversionRate <= 0) {
    alert(L('Please fill in all fields with valid numbers (greater than 0).', 'Preencha todos os campos com números válidos (superiores a 0).'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const hourlyRevenue = monthlyRevenue / (30 * 24);
    const costPerHour = hourlyRevenue;
    const totalLoss = costPerHour * downtimeHours;
    const lossPerMinute = costPerHour / 60;
    const annualLoss = totalLoss * 12;
    const lostCustomers = Math.round((monthlyRevenue / 30 / 24) * downtimeHours * (conversionRate / 100));

    renderResult({ costPerHour, totalLoss, lossPerMinute, annualLoss, lostCustomers });
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

  document.getElementById('cost-per-hour').textContent = formatCurrency(data.costPerHour);
  document.getElementById('total-loss').textContent = formatCurrency(data.totalLoss);
  document.getElementById('loss-per-minute').textContent = formatCurrency(data.lossPerMinute);
  document.getElementById('annual-loss').textContent = formatCurrency(data.annualLoss);
  document.getElementById('lost-customers').textContent = formatNumber(data.lostCustomers);

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      total_loss: data.totalLoss,
      lost_customers: data.lostCustomers
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
  document.getElementById('monthly-revenue').value = '';
  document.getElementById('downtime-hours').value = '';
  document.getElementById('conversion-rate').value = '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
