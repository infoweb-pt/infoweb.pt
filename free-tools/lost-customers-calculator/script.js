'use strict';

// ─── Intermediate API endpoint ────────────────────────────────────────────────
// Replace with your actual backend URL when wiring up.
// Expected POST body: { email, weekly_loss, monthly_loss }
const API_ENDPOINT = 'https://api.YOUR-BACKEND.com/leads/lost-customers';

// ─── State ────────────────────────────────────────────────────────────────────
let currentStep  = 1;
let weeklyLoss   = 0;
let monthlyLoss  = 0;

// ─── Analytics helper ─────────────────────────────────────────────────────────
function trackEvent(eventName, params) {
  params = Object.assign({ tool_name: 'lost_customers_calculator' }, params || {});
  if (typeof gtag !== 'undefined') gtag('event', eventName, params);
  console.debug('[trackEvent]', eventName, params);
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
  label.textContent = `Step ${step} of 3`;
  pctEl.textContent = pct + '%';

  document.getElementById('progress-bar-container')
    .setAttribute('aria-valuenow', step);
}

// ─── Step navigation ──────────────────────────────────────────────────────────
function goToStep(targetStep) {
  const direction = targetStep > currentStep ? 'forward' : 'back';

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
      show('avg-spend-error');
      document.getElementById('avg-spend').focus();
      return false;
    }
  }
  if (step === 2) {
    const val = parseFloat(document.getElementById('contacts-missed').value);
    if (val === '' || isNaN(val) || val < 0) {
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
      errEl.textContent = 'Please enter a number (0 or more).';
      show('customers-lost-error');
      document.getElementById('customers-lost').focus();
      return false;
    }
    if (lost > missed) {
      errEl.textContent = `Cannot be more than your step 2 answer (${missed}).`;
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

  const avgSpend      = parseFloat(document.getElementById('avg-spend').value)     || 0;
  const customersLost = parseFloat(document.getElementById('customers-lost').value) || 0;

  weeklyLoss  = avgSpend * customersLost;
  monthlyLoss = weeklyLoss * 4;

  trackEvent('tool_used', { weekly_loss: weeklyLoss, monthly_loss: monthlyLoss });

  // Hide the form, show result
  hide('calculator-section');
  renderResult();
}

function renderResult() {
  const fmt = (n) => '€' + n.toLocaleString('en-IE', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

  document.getElementById('result-weekly').textContent  = fmt(weeklyLoss);
  document.getElementById('result-monthly').textContent = fmt(monthlyLoss);

  const customersLost = parseFloat(document.getElementById('customers-lost').value) || 0;
  document.getElementById('result-sentence').textContent =
    `You are losing approximately ${fmt(weeklyLoss)} per week — that is ${fmt(monthlyLoss)} per month — because ${customersLost} potential customer${customersLost !== 1 ? 's' : ''} give up each week when they get no immediate reply.`;

  // Animate figures in
  ['result-weekly', 'result-monthly'].forEach(id => {
    document.getElementById(id).classList.add('result-animate');
  });

  show('result-box');
  document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  trackEvent('tool_result_shown', { weekly_loss: weeklyLoss, monthly_loss: monthlyLoss });
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
    // ── Simulated submission (backend not yet wired) ────────────────────────
    // When API_ENDPOINT is live, replace the block below with a real fetch().
    // The payload is logged here so it is visible in the browser console and
    // the lead data is ready to copy into any backend system.
    const payload = { email, weekly_loss: weeklyLoss, monthly_loss: monthlyLoss };
    console.log('[submitEmail] Lead payload (POST to', API_ENDPOINT, '):', payload);

    // Simulate async latency so the spinner and UX feel realistic
    await new Promise(resolve => setTimeout(resolve, 900));

    // Uncomment and replace the block above once the backend is ready:
    // const response = await fetch(API_ENDPOINT, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(payload)
    // });
    // if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // ── End of simulated block ─────────────────────────────────────────────

    // Success
    hide('email-spinner');
    hide('email-gate');
    show('email-success');
    trackEvent('lead_submitted', { weekly_loss: weeklyLoss, monthly_loss: monthlyLoss });

  } catch (err) {
    console.error('[submitEmail]', err);
    hide('email-spinner');
    show('email-submit-btn');
    show('email-api-error');
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
