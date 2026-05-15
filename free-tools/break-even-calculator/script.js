/**
 * Break-Even Calculator
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
  const fixedCosts = parseFloat(document.getElementById('fixed-costs').value);
  const sellingPrice = parseFloat(document.getElementById('selling-price').value);
  const variableCost = parseFloat(document.getElementById('variable-cost').value);

  if (!Number.isFinite(fixedCosts) || fixedCosts <= 0 ||
      !Number.isFinite(sellingPrice) || sellingPrice <= 0 ||
      !Number.isFinite(variableCost) || variableCost < 0) {
    alert(L('Please fill in all fields with valid numbers.', 'Preencha todos os campos com números válidos.'));
    return;
  }

  if (variableCost >= sellingPrice) {
    alert(L('Variable cost must be less than selling price, or you lose money on every sale.', 'O custo variável deve ser inferior ao preço de venda, ou perde dinheiro em cada venda.'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const profitPerUnit = sellingPrice - variableCost;
    const breakEvenUnits = Math.ceil(fixedCosts / profitPerUnit);
    const breakEvenRevenue = breakEvenUnits * sellingPrice;
    const contributionMargin = (profitPerUnit / sellingPrice) * 100;
    const profit2x = profitPerUnit * (breakEvenUnits * 2) - fixedCosts;

    renderResult({ breakEvenUnits, breakEvenRevenue, profitPerUnit, contributionMargin, profit2x });
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

  document.getElementById('break-even-units').textContent = formatNumber(data.breakEvenUnits);
  document.getElementById('break-even-revenue').textContent = formatCurrency(data.breakEvenRevenue);
  document.getElementById('profit-per-unit').textContent = formatCurrency(data.profitPerUnit);
  document.getElementById('contribution-margin').textContent = formatNumber(Math.round(data.contributionMargin)) + '%';
  document.getElementById('profit-2x').textContent = formatCurrency(data.profit2x);

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      break_even_units: data.breakEvenUnits,
      contribution_margin: data.contributionMargin
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
  document.getElementById('fixed-costs').value = '';
  document.getElementById('selling-price').value = '';
  document.getElementById('variable-cost').value = '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
