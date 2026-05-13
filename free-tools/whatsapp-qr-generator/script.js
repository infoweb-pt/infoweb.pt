'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let lastWaLink = '';
let qrReady    = false;
let toolRunStartedAt = 0;

// ─── Contact lead API (optional — presence / InfoWeb follow-up) ────────────────
// Production: full HTTPS URL required for GitHub Pages fetch.
// Local dev: http://localhost:8001/leads/tool-contact/
const CONTACT_API_ENDPOINT = 'https://infoweb.api.sousadev.com/leads/tool-contact/';
const CONTACT_SOURCE = 'whatsapp_qr_generator';

function clearContactEmailError() {
  hide('contact-email-error');
  hide('contact-api-error');
}

async function submitContactLead() {
  const emailInput = document.getElementById('contact-email');
  const email = emailInput.value.trim();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    show('contact-email-error');
    emailInput.focus();
    return;
  }

  clearContactEmailError();
  hide('contact-submit-btn');
  showFlex('contact-spinner');

  try {
    const response = await fetch(CONTACT_API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, source: CONTACT_SOURCE })
    });

    if (!response.ok) throw new Error('HTTP ' + response.status);

    hide('contact-spinner');
    hide('contact-lead-form');
    show('contact-success');
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submitted', { form: 'tool_contact', source: CONTACT_SOURCE });
    }
  } catch (err) {
    console.error('[submitContactLead]', err);
    hide('contact-spinner');
    show('contact-submit-btn');
    show('contact-api-error');
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submit_failed', { error_type: 'api_error', form: 'tool_contact' });
    }
  }
}

// ─── UI helpers ───────────────────────────────────────────────────────────────
function show(id)   { document.getElementById(id).classList.remove('hidden'); }
function hide(id)   { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}
function showSpinner()  { showFlex('spinner'); }
function hideSpinner()  {
  const el = document.getElementById('spinner');
  el.classList.add('hidden');
  el.classList.remove('show-flex');
}

function setDownloadEnabled(enabled) {
  const btn = document.getElementById('btn-download');
  btn.disabled = !enabled;
}

// ─── Live phone validation (fires on every keystroke) ─────────────────────────
function validateLive() {
  const phone     = document.getElementById('phone-number').value.trim();
  const digits    = phone.replace(/\D/g, '');
  const errorEl   = document.getElementById('phone-error');
  const inputEl   = document.getElementById('phone-number');
  const hasValue  = phone.length > 0;
  const isInvalid = hasValue && (digits.length < 6 || digits !== phone.replace(/\s|-/g, ''));

  if (isInvalid) {
    errorEl.classList.remove('hidden');
    inputEl.classList.add('ring-2', 'ring-red-500', 'border-red-500');
    inputEl.classList.remove('focus:ring-green-500');
  } else {
    errorEl.classList.add('hidden');
    inputEl.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
    inputEl.classList.add('focus:ring-green-500');
  }
}

// ─── Submit-time validation ───────────────────────────────────────────────────
function validateInputs() {
  const phone  = document.getElementById('phone-number').value.trim();
  const digits = phone.replace(/\D/g, '');

  if (!digits || digits.length < 6) {
    const errorEl = document.getElementById('phone-error');
    const inputEl = document.getElementById('phone-number');
    errorEl.classList.remove('hidden');
    inputEl.classList.add('ring-2', 'ring-red-500', 'border-red-500');
    inputEl.focus();
    return false;
  }
  return true;
}

// ─── Char counter ─────────────────────────────────────────────────────────────
function updateCharCount() {
  document.getElementById('char-count').textContent =
    document.getElementById('wa-message').value.length;
}

// ─── Main tool logic ──────────────────────────────────────────────────────────
function runTool() {
  if (!validateInputs()) {
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_validation_error', { field: 'phone', reason: 'invalid_or_short' });
    }
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showSpinner();
  hide('result-box');
  hide('error-box');
  setDownloadEnabled(false);
  qrReady = false;

  // Brief delay so spinner is visible; QR gen itself is synchronous
  setTimeout(() => {
    try {
      const countryCode = document.getElementById('country-code').value;
      const phone       = document.getElementById('phone-number').value.trim().replace(/\D/g, '');
      const message     = document.getElementById('wa-message').value.trim();
      const fullNumber  = countryCode + phone;
      const encoded     = message ? encodeURIComponent(message) : '';

      lastWaLink = encoded
        ? `https://wa.me/${fullNumber}?text=${encoded}`
        : `https://wa.me/${fullNumber}`;

      renderResult(lastWaLink);
    } catch (err) {
      console.error('[runTool]', err);
      showFriendlyError();
    } finally {
      hideSpinner();
    }
  }, 350);
}

function renderResult(waLink) {
  // Update link display
  document.getElementById('wa-link-display').textContent = waLink;
  document.getElementById('wa-link-open').href = waLink;

  // Render QR Code directly into #qr-container
  // qrcode.js draws synchronously onto a <canvas> it creates inside the container
  const container = document.getElementById('qr-container');
  container.innerHTML = ''; // clear any previous QR

  new QRCode(container, {
    text: waLink,
    width: 220,
    height: 220,
    colorDark:  '#020617',
    colorLight: '#ffffff',
    correctLevel: QRCode.CorrectLevel.H
  });

  // qrcode.js draws the canvas synchronously; enable download immediately
  qrReady = true;
  setDownloadEnabled(true);

  // Show result section and scroll to it
  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
    });
  }
}

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

// ─── Copy link ────────────────────────────────────────────────────────────────
function copyLink() {
  if (!lastWaLink) return;

  const doFeedback = () => {
    const btn = document.getElementById('copy-btn-text');
    const box = document.getElementById('wa-link-display');
    btn.textContent = 'Copied!';
    box.classList.add('copy-flash');
    setTimeout(() => {
      btn.textContent = 'Copy link';
      box.classList.remove('copy-flash');
    }, 2000);
    if (typeof window.trackEvent === 'function') window.trackEvent('result_copied');
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(lastWaLink).then(doFeedback).catch(() => fallbackCopy(doFeedback));
  } else {
    fallbackCopy(doFeedback);
  }
}

function fallbackCopy(callback) {
  const ta = document.createElement('textarea');
  ta.value = lastWaLink;
  ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
  if (callback) callback();
}

// ─── Download QR Code (high-res, print-ready) ─────────────────────────────────
function downloadQR() {
  if (!qrReady) return;

  // qrcode.js creates a <canvas> directly inside #qr-container
  const srcCanvas = document.querySelector('#qr-container canvas');
  if (!srcCanvas) return;

  const scale       = 4; // 4× = 880×880 px — suitable for print
  const printCanvas = document.createElement('canvas');
  printCanvas.width  = srcCanvas.width  * scale;
  printCanvas.height = srcCanvas.height * scale;

  const ctx = printCanvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, printCanvas.width, printCanvas.height);
  ctx.drawImage(srcCanvas, 0, 0, printCanvas.width, printCanvas.height);

  const link    = document.createElement('a');
  link.download = 'whatsapp-qr-infoweb.png';
  link.href     = printCanvas.toDataURL('image/png');
  link.click();

  if (typeof window.trackEvent === 'function') window.trackEvent('qr_downloaded');
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');

  const inputEl = document.getElementById('phone-number');
  inputEl.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
  document.getElementById('phone-error').classList.add('hidden');
  inputEl.value = '';
  document.getElementById('wa-message').value = '';
  document.getElementById('char-count').textContent = '0';
  document.getElementById('qr-container').innerHTML = '';

  lastWaLink = '';
  qrReady    = false;
  setDownloadEnabled(false);

  inputEl.focus();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Keyboard shortcut: Enter on phone field triggers generate ────────────────
document.getElementById('phone-number').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') runTool();
});

(function bindToolAnalytics() {
  const debounce = {};
  function schedule(fieldId) {
    clearTimeout(debounce[fieldId]);
    debounce[fieldId] = setTimeout(function () {
      if (typeof window.trackEvent === 'function') window.trackEvent('tool_input_changed', { field: fieldId });
    }, 600);
  }
  ['phone-number', 'wa-message'].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', function () { schedule(id); });
  });
  const cc = document.getElementById('country-code');
  if (cc) {
    cc.addEventListener('change', function () {
      if (typeof window.trackEvent === 'function') {
        window.trackEvent('tool_input_changed', { field: 'country_code', value: cc.value });
      }
    });
  }
  const contactEmail = document.getElementById('contact-email');
  if (contactEmail) {
    contactEmail.addEventListener(
      'focus',
      function () {
        if (typeof window.trackEvent === 'function') {
          window.trackEvent('lead_form_opened', { form: 'tool_contact' });
        }
      },
      { once: true }
    );
  }
})();
