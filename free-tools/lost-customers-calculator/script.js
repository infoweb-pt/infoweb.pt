'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

// ─── API endpoint ─────────────────────────────────────────────────────────────
// Production: deployed InfoWeb API (HTTPS + full URL — required for GitHub Pages fetch).
// Local dev: http://localhost:8001/leads/lost-customers/ (run `python manage.py runserver 8001` in api/).
// Expected POST body: { email, weekly_loss, monthly_loss }
const API_ENDPOINT = 'https://infoweb.api.sousadev.com/leads/lost-customers/';

// ─── State ────────────────────────────────────────────────────────────────────
let currentStep  = 1;
let weeklyLoss   = 0;
let monthlyLoss  = 0;
let toolRunStartedAt = 0;

function markToolSessionStart() {
  if (toolRunStartedAt === 0) toolRunStartedAt = performance.now();
}

function emitValidationError(field, reason) {
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_validation_error', { field, reason });
  }
}

// ─── UI helpers ───────────────────────────────────────────────────────────────
function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}

function clearStepError(errorId) {
  document.getElementById(errorId).classList.add('hidden');
}
function clearEmailError() {
  hide('gate-email-error');
  hide('email-api-error');
}

// ─── Progress bar ─────────────────────────────────────────────────────────────
function updateProgress(step) {
  const pct   = Math.round((step / 3) * 100);
  const fill  = document.getElementById('progress-fill');
  const label = document.getElementById('step-label');
  const pctEl = document.getElementById('step-pct');

  fill.style.width  = pct + '%';
  label.textContent = L(`Step ${step} of 3`, `Passo ${step} de 3`);
  pctEl.textContent = pct + '%';

  document.getElementById('progress-bar-container')
    .setAttribute('aria-valuenow', step);
}

// ─── Step navigation ──────────────────────────────────────────────────────────
function goToStep(targetStep) {
  const direction = targetStep > currentStep ? 'forward' : 'back';

  if (targetStep !== currentStep) markToolSessionStart();

  // Validate before advancing
  if (direction === 'forward') {
    if (!validateStep(currentStep)) return;
  }

  const currentEl = document.getElementById(`step-${currentStep}`);
  const targetEl  = document.getElementById(`step-${targetStep}`);

  // Animate out
  currentEl.classList.add(direction === 'forward' ? 'slide-out-left' : 'slide-out-right');

  setTimeout(() => {
    currentEl.classList.add('hidden');
    currentEl.classList.remove('slide-out-left', 'slide-out-right');
    targetEl.classList.remove('hidden');
    targetEl.classList.add(direction === 'forward' ? 'slide-in-right' : 'slide-in-left');

    // Focus first input in new step
    const firstInput = targetEl.querySelector('input');
    if (firstInput) firstInput.focus();

    setTimeout(() => {
      targetEl.classList.remove('slide-in-right', 'slide-in-left');
    }, 260);

    currentStep = targetStep;
    updateProgress(currentStep);
  }, 200);
}

// ─── Per-step validation ──────────────────────────────────────────────────────
function validateStep(step) {
  if (step === 1) {
    const val = parseFloat(document.getElementById('avg-spend').value);
    if (!val || val <= 0) {
      emitValidationError('avg_spend', 'invalid_or_empty');
      show('avg-spend-error');
      document.getElementById('avg-spend').focus();
      return false;
    }
  }
  if (step === 2) {
    const val = parseFloat(document.getElementById('contacts-missed').value);
    if (val === '' || isNaN(val) || val < 0) {
      emitValidationError('contacts_missed', 'invalid');
      show('contacts-missed-error');
      document.getElementById('contacts-missed').focus();
      return false;
    }
  }
  if (step === 3) {
    const missed = parseFloat(document.getElementById('contacts-missed').value) || 0;
    const lost   = parseFloat(document.getElementById('customers-lost').value);
    const errEl  = document.getElementById('customers-lost-error');
    if (isNaN(lost) || lost < 0) {
      emitValidationError('customers_lost', 'not_a_number');
      errEl.textContent = L('Please enter a number (0 or more).', 'Introduza um número (0 ou superior).');
      show('customers-lost-error');
      document.getElementById('customers-lost').focus();
      return false;
    }
    if (lost > missed) {
      emitValidationError('customers_lost', 'exceeds_contacts_missed');
      errEl.textContent = L(
        `Cannot be more than your step 2 answer (${missed}).`,
        `Não pode ser superior à resposta do passo 2 (${missed}).`
      );
      show('customers-lost-error');
      document.getElementById('customers-lost').focus();
      return false;
    }
  }
  return true;
}

// ─── Calculation ──────────────────────────────────────────────────────────────
function calculate() {
  if (!validateStep(3)) return;

  markToolSessionStart();

  const avgSpend      = parseFloat(document.getElementById('avg-spend').value)     || 0;
  const customersLost = parseFloat(document.getElementById('customers-lost').value) || 0;

  weeklyLoss  = avgSpend * customersLost;
  monthlyLoss = weeklyLoss * 4;

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_used', { weekly_loss: weeklyLoss, monthly_loss: monthlyLoss });
  }

  // Hide the form, show result
  hide('calculator-section');
  renderResult();
}

function renderResult() {
  const loc = PT ? 'pt-PT' : 'en-IE';
  const fmt = (n) =>
    n.toLocaleString(loc, { style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0 });

  document.getElementById('result-weekly').textContent  = fmt(weeklyLoss);
  document.getElementById('result-monthly').textContent = fmt(monthlyLoss);

  const customersLost = parseFloat(document.getElementById('customers-lost').value) || 0;
  const custWord =
    customersLost !== 1
      ? L('potential customers', 'potenciais clientes')
      : L('potential customer', 'potencial cliente');
  document.getElementById('result-sentence').textContent = PT
    ? `Está a perder cerca de ${fmt(weeklyLoss)} por semana — cerca de ${fmt(monthlyLoss)} por mês — porque ${customersLost} ${custWord} desistem por semana quando não obtêm resposta imediata.`
    : `You are losing approximately ${fmt(weeklyLoss)} per week — that is ${fmt(monthlyLoss)} per month — because ${customersLost} ${custWord} give up each week when they get no immediate reply.`;

  // Animate figures in
  ['result-weekly', 'result-monthly'].forEach(id => {
    document.getElementById(id).classList.add('result-animate');
  });

  show('result-box');
  document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      weekly_loss: weeklyLoss,
      monthly_loss: monthlyLoss,
      duration_ms:
        toolRunStartedAt > 0 ? Math.round(performance.now() - toolRunStartedAt) : undefined,
    });
  }
}

// ─── Email lead capture ───────────────────────────────────────────────────────
async function submitEmail() {
  const emailInput = document.getElementById('gate-email');
  const email      = emailInput.value.trim();

  // Client-side email validation
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    show('gate-email-error');
    emailInput.focus();
    return;
  }

  // Show spinner, hide button and errors
  hide('email-submit-btn');
  hide('email-api-error');
  showFlex('email-spinner');

  try {
    const payload = { email, weekly_loss: weeklyLoss, monthly_loss: monthlyLoss };

    // POST lead to API.
    const response = await fetch(API_ENDPOINT, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    // Success
    hide('email-spinner');
    hide('email-gate');
    show('email-success');
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submitted', { weekly_loss: weeklyLoss, monthly_loss: monthlyLoss });
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

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetCalculator() {
  // Reset inputs
  ['avg-spend', 'contacts-missed', 'customers-lost'].forEach(id => {
    document.getElementById(id).value = '';
  });
  ['avg-spend-error', 'contacts-missed-error', 'customers-lost-error'].forEach(id => {
    hide(id);
  });

  // Reset email gate — restore all gate elements so leads can be re-submitted
  document.getElementById('gate-email').value = '';
  hide('gate-email-error');
  hide('email-api-error');
  hide('email-spinner');
  hide('email-success');
  show('email-gate');
  show('email-submit-btn');

  // Reset state
  weeklyLoss  = 0;
  monthlyLoss = 0;
  currentStep = 1;
  toolRunStartedAt = 0;

  // Show step 1, hide others and result
  ['step-2', 'step-3'].forEach(id => hide(id));
  show('step-1');
  hide('result-box');
  show('calculator-section');
  updateProgress(1);

  window.scrollTo({ top: 0, behavior: 'smooth' });
  document.getElementById('avg-spend').focus();
}

// ─── Keyboard: Enter advances step ───────────────────────────────────────────
document.addEventListener('keydown', function (e) {
  if (e.key !== 'Enter') return;
  const active = document.activeElement;
  if (!active) return;
  if (active.id === 'avg-spend')        goToStep(2);
  else if (active.id === 'contacts-missed') goToStep(3);
  else if (active.id === 'customers-lost')  calculate();
  else if (active.id === 'gate-email')      submitEmail();
});

(function bindLostCalcAnalytics() {
  const debounce = {};
  function schedule(fieldId) {
    clearTimeout(debounce[fieldId]);
    debounce[fieldId] = setTimeout(function () {
      if (typeof window.trackEvent === 'function') {
        window.trackEvent('tool_input_changed', { field: fieldId });
      }
    }, 600);
  }
  ['avg-spend', 'contacts-missed', 'customers-lost'].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', function () {
        markToolSessionStart();
        schedule(id);
      });
    }
  });
  const gate = document.getElementById('gate-email');
  if (gate) {
    gate.addEventListener(
      'focus',
      function () {
        if (typeof window.trackEvent === 'function') {
          window.trackEvent('lead_form_opened', { form: 'lost_customers_report' });
        }
      },
      { once: true }
    );
  }
})();
