'use strict';

// ─── API endpoint ─────────────────────────────────────────────────────────────
// Production: deployed InfoWeb API (HTTPS + full URL — required for GitHub Pages fetch).
// Local dev: http://localhost:8001/leads/presence-score/ (run `python manage.py runserver 8001` in api/).
// Expected POST body: { email, score, answers }
const API_ENDPOINT = 'https://infoweb.sousadev.com/leads/presence-score/';

// ─── Quiz data ────────────────────────────────────────────────────────────────
// points: weighted values — Q1, Q5, Q7 = 16; rest = 12; max raw = 96
const QUESTIONS = [
  {
    id: 1,
    points: 16,
    text: 'Does your business appear on the first page of Google when someone searches your service?',
    weakness: 'Your biggest gap: your business can\'t be found on Google — you are invisible to potential customers searching for your service right now.'
  },
  {
    id: 2,
    points: 12,
    text: 'Do you have your own domain (.com, .pt or similar)?',
    weakness: 'Your biggest gap: you don\'t have your own domain, which makes your business look unestablished and is hard to find or remember online.'
  },
  {
    id: 3,
    points: 12,
    text: 'Is your Google Business Profile complete and up to date?',
    weakness: 'Your biggest gap: your Google Business Profile is incomplete — local customers searching nearby may choose a competitor with a complete listing instead.'
  },
  {
    id: 4,
    points: 12,
    text: 'Do you have a page where customers can see your menu, services, or portfolio?',
    weakness: 'Your biggest gap: you have nowhere to showcase what you offer — customers can\'t see your menu, services, or prices without calling you first.'
  },
  {
    id: 5,
    points: 16,
    text: 'Can customers book, enquire, or order online without calling you?',
    weakness: 'Your biggest gap: customers cannot book or enquire online — you are losing sales to every competitor who offers 24/7 self-service booking.'
  },
  {
    id: 6,
    points: 12,
    text: 'Does your website load in under 3 seconds on mobile?',
    weakness: 'Your biggest gap: your website is slow on mobile — most users leave within 3 seconds, and Google penalises slow sites in search rankings.'
  },
  {
    id: 7,
    points: 16,
    text: 'Is your business listed correctly on Google Maps?',
    weakness: 'Your biggest gap: your business is not correctly listed on Google Maps — local customers physically nearby simply cannot find you.'
  }
];

const MAX_RAW_SCORE = QUESTIONS.reduce((sum, q) => sum + q.points, 0); // 96

// ─── State ────────────────────────────────────────────────────────────────────
let currentQuestion = 0;   // 0-indexed
let answers         = [];  // 'yes' | 'no' for each question
let finalScore      = 0;
let weaknessMsg     = '';
let firstStarted    = false;
let quizStartedAt = 0;

// ─── UI helpers ───────────────────────────────────────────────────────────────
function show(id)  { document.getElementById(id).classList.remove('hidden'); }
function hide(id)  { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}

// ─── Quiz render ──────────────────────────────────────────────────────────────
function renderQuestion(idx) {
  const q = QUESTIONS[idx];
  const total = QUESTIONS.length;

  document.getElementById('q-text').textContent   = q.text;
  document.getElementById('q-counter').textContent = `Question ${idx + 1} of ${total}`;

  const pct = Math.round(((idx + 1) / total) * 100);
  document.getElementById('quiz-progress-fill').style.width = pct + '%';
  document.getElementById('quiz-pct').textContent = pct + '%';
  document.getElementById('quiz-progress-bar')
    .setAttribute('aria-valuenow', idx + 1);
}

function answerQuestion(answer) {
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('quiz_question_answered', { step: currentQuestion + 1, answer });
  }

  // Fire tool_used on first answer
  if (!firstStarted) {
    firstStarted = true;
    quizStartedAt = performance.now();
    if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');
  }

  answers[currentQuestion] = answer;

  // Animate card out
  const card = document.getElementById('question-card');
  card.classList.add('card-exit');

  setTimeout(() => {
    card.classList.remove('card-exit');

    if (currentQuestion < QUESTIONS.length - 1) {
      currentQuestion++;
      renderQuestion(currentQuestion);
      card.classList.add('card-enter');
      setTimeout(() => card.classList.remove('card-enter'), 300);
    } else {
      // All questions answered — compute score and show result
      computeScore();
      hide('quiz-section');
      show('result-section');
      document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
      animateRing(finalScore);
      if (typeof window.trackEvent === 'function') {
        window.trackEvent('tool_result_shown', {
          score: finalScore,
          duration_ms: Math.round(performance.now() - quizStartedAt),
        });
      }
    }
  }, 220);
}

// ─── Scoring ──────────────────────────────────────────────────────────────────
function computeScore() {
  let raw = 0;
  weaknessMsg = '';

  answers.forEach((ans, i) => {
    if (ans === 'yes') {
      raw += QUESTIONS[i].points;
    } else if (!weaknessMsg) {
      weaknessMsg = QUESTIONS[i].weakness;
    }
  });

  // Normalize to 0–100
  finalScore = Math.round((raw / MAX_RAW_SCORE) * 100);

  // Populate result elements
  document.getElementById('score-total').textContent    = '/ 100';

  const band = getBand(finalScore);
  const bandEl = document.getElementById('score-band');
  bandEl.textContent  = band.label;
  bandEl.className    = 'score-band band-' + band.key;

  document.getElementById('weakness-msg').textContent =
    weaknessMsg || 'Excellent work — your online presence is strong across all areas!';

  // Build per-question breakdown
  buildBreakdown();
}

function getBand(score) {
  if (score <= 39) return { key: 'critical',    label: '⚠ Critical'    };
  if (score <= 69) return { key: 'needs-work',  label: '↗ Needs Work'  };
  if (score <= 89) return { key: 'good',        label: '✓ Good'        };
  return               { key: 'excellent',    label: '★ Excellent'   };
}

function buildBreakdown() {
  const list = document.getElementById('breakdown-list');
  list.innerHTML = '';
  QUESTIONS.forEach((q, i) => {
    const ans = answers[i];
    const li = document.createElement('li');
    li.className = 'breakdown-item';
    li.innerHTML = `
      <span class="breakdown-icon ${ans === 'yes' ? 'icon-yes' : 'icon-no'}"
            aria-label="${ans === 'yes' ? 'Yes' : 'No'}">
        ${ans === 'yes' ? '✓' : '✗'}
      </span>
      <span class="breakdown-text">${q.text}</span>
    `;
    list.appendChild(li);
  });
}

// ─── SVG ring animation ───────────────────────────────────────────────────────
const RING_RADIUS      = 90;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS; // ~565.5

function animateRing(targetScore) {
  const ring       = document.getElementById('score-ring');
  const countEl    = document.getElementById('ring-count');
  const duration   = 1200; // ms
  const startTime  = performance.now();

  // Set full stroke-dasharray; start fully offset (empty)
  ring.style.strokeDasharray  = RING_CIRCUMFERENCE;
  ring.style.strokeDashoffset = RING_CIRCUMFERENCE;

  function step(now) {
    const elapsed  = Math.min(now - startTime, duration);
    const progress = easeOut(elapsed / duration);
    const current  = Math.round(progress * targetScore);
    const offset   = RING_CIRCUMFERENCE - (progress * targetScore / 100) * RING_CIRCUMFERENCE;

    ring.style.strokeDashoffset = offset;
    countEl.textContent         = current;

    if (elapsed < duration) {
      requestAnimationFrame(step);
    } else {
      ring.style.strokeDashoffset = RING_CIRCUMFERENCE - (targetScore / 100) * RING_CIRCUMFERENCE;
      countEl.textContent         = targetScore;
    }
  }

  requestAnimationFrame(step);
}

function easeOut(t) {
  return 1 - Math.pow(1 - t, 3);
}

// ─── Email gate ───────────────────────────────────────────────────────────────
function clearEmailError() {
  hide('gate-email-error');
  hide('email-api-error');
}

async function submitEmail() {
  const emailInput = document.getElementById('gate-email');
  const email      = emailInput.value.trim();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    show('gate-email-error');
    emailInput.focus();
    return;
  }

  hide('email-submit-btn');
  hide('email-api-error');
  showFlex('email-spinner');

  try {
    const payload = { email, score: finalScore, answers };

    // POST lead to InfoWeb API.
    const response = await fetch(API_ENDPOINT, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    // Success — unlock breakdown and show confirmation
    hide('email-spinner');
    hide('email-gate');
    show('email-success');
    document.getElementById('breakdown-wrapper').classList.remove('breakdown-locked');
    document.getElementById('breakdown-overlay').classList.add('hidden');

    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submitted', { score: finalScore });
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

// ─── Retake ───────────────────────────────────────────────────────────────────
function retakeQuiz() {
  // Reset state
  currentQuestion = 0;
  answers         = [];
  finalScore      = 0;
  weaknessMsg     = '';
  firstStarted    = false;
  quizStartedAt   = 0;

  // Reset email gate
  document.getElementById('gate-email').value = '';
  hide('gate-email-error');
  hide('email-api-error');
  hide('email-spinner');
  hide('email-success');
  show('email-gate');
  show('email-submit-btn');

  // Reset ring
  const ring  = document.getElementById('score-ring');
  const count = document.getElementById('ring-count');
  ring.style.strokeDashoffset = RING_CIRCUMFERENCE;
  count.textContent = '0';

  // Reset breakdown lock
  document.getElementById('breakdown-wrapper').classList.add('breakdown-locked');
  document.getElementById('breakdown-overlay').classList.remove('hidden');

  // Re-render first question
  renderQuestion(0);
  hide('result-section');
  show('quiz-section');

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Init ─────────────────────────────────────────────────────────────────────
renderQuestion(0);

(function bindPresenceLeadAnalytics() {
  const gate = document.getElementById('gate-email');
  if (gate) {
    gate.addEventListener(
      'focus',
      function () {
        if (typeof window.trackEvent === 'function') {
          window.trackEvent('lead_form_opened', { form: 'presence_score_report' });
        }
      },
      { once: true }
    );
  }
})();
