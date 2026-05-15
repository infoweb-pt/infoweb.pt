/**
 * Freelancer Hourly Rate Calculator
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
  const monthlyExpenses = parseFloat(document.getElementById('monthly-expenses').value);
  const billableHours = parseFloat(document.getElementById('billable-hours').value);
  const taxRate = parseFloat(document.getElementById('tax-rate').value);
  const profitMargin = parseFloat(document.getElementById('profit-margin').value);

  if (!Number.isFinite(monthlyExpenses) || monthlyExpenses < 0 ||
      !Number.isFinite(billableHours) || billableHours <= 0 ||
      !Number.isFinite(taxRate) || taxRate < 0 || taxRate > 100 ||
      !Number.isFinite(profitMargin) || profitMargin < 0 || profitMargin > 100) {
    alert(L('Please fill in all fields with valid numbers.', 'Preencha todos os campos com números válidos.'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const baseRate = monthlyExpenses / billableHours;
    const rateWithTax = baseRate / (1 - (taxRate / 100));
    const hourlyRate = rateWithTax / (1 - (profitMargin / 100));
    const dailyRate = hourlyRate * 8;
    const monthlyIncome = hourlyRate * billableHours;
    const afterTax = monthlyIncome * (1 - (taxRate / 100));
    const afterExpenses = afterTax - monthlyExpenses;

    renderResult({ hourlyRate, dailyRate, monthlyIncome, afterTax, afterExpenses });
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

  document.getElementById('hourly-rate').textContent = formatCurrency(data.hourlyRate);
  document.getElementById('daily-rate').textContent = formatCurrency(data.dailyRate);
  document.getElementById('monthly-income').textContent = formatCurrency(data.monthlyIncome);
  document.getElementById('after-tax').textContent = formatCurrency(data.afterTax);
  document.getElementById('after-expenses').textContent = formatCurrency(data.afterExpenses);

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      hourly_rate: data.hourlyRate,
      monthly_income: data.monthlyIncome
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
  document.getElementById('monthly-expenses').value = '';
  document.getElementById('billable-hours').value = '';
  document.getElementById('tax-rate').value = '';
  document.getElementById('profit-margin').value = '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
