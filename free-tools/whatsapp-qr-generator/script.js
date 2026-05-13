'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let lastWaLink = '';
let smartQRData = null;  // { slug, short_url, manage_url, manage_token, qr_png_url }
let qrReady    = false;
let toolRunStartedAt = 0;

// ─── API Configuration ────────────────────────────────────────────────────────
const API_BASE = 'https://infoweb.api.sousadev.com';
const SMARTQR_API = `${API_BASE}/smartqr/codes/`;

// ─── Contact lead API (optional — presence / InfoWeb follow-up) ────────────────
const CONTACT_API_ENDPOINT = `${API_BASE}/leads/tool-contact/`;
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
async function runTool() {
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

  try {
    const countryCode = document.getElementById('country-code').value;
    const phone       = document.getElementById('phone-number').value.trim().replace(/\D/g, '');
    const message     = document.getElementById('wa-message').value.trim();
    const fullNumber  = countryCode + phone;
    const encoded     = message ? encodeURIComponent(message) : '';

    lastWaLink = encoded
      ? `https://wa.me/${fullNumber}?text=${encoded}`
      : `https://wa.me/${fullNumber}`;

    // Create SmartQR code via API
    const response = await fetch(SMARTQR_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_url: lastWaLink,
        label: `WhatsApp: +${fullNumber}`,
        tool_source: 'whatsapp_qr_generator'
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[SmartQR API error]', errorData);
      throw new Error('SmartQR API: ' + (errorData.detail || response.status));
    }

    smartQRData = await response.json();
    renderResult(lastWaLink, smartQRData);
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideSpinner();
  }
}

function renderResult(waLink, smartQR) {
  // Update direct link display
  document.getElementById('wa-link-display').textContent = waLink;
  document.getElementById('wa-link-open').href = waLink;

  // Update SmartQR short URL
  const shortUrlEl = document.getElementById('smartqr-short-url');
  if (shortUrlEl && smartQR) {
    shortUrlEl.textContent = smartQR.short_url;
    shortUrlEl.href = smartQR.short_url;
  }

  // Update manage link
  const manageEl = document.getElementById('smartqr-manage-url');
  if (manageEl && smartQR) {
    manageEl.href = smartQR.manage_url;
    manageEl.classList.remove('hidden');
  }

  // Render QR Code using server-generated PNG
  const qrContainer = document.getElementById('qr-container');
  qrContainer.innerHTML = '';

  if (smartQR && smartQR.qr_png_url) {
    const img = document.createElement('img');
    img.src = smartQR.qr_png_url;
    img.alt = 'WhatsApp QR Code';
    img.className = 'w-full h-full';
    img.onload = function() {
      qrReady = true;
      setDownloadEnabled(true);
    };
    img.onerror = function() {
      // Fallback to local QR generation if server PNG fails
      renderLocalQR(waLink);
    };
    qrContainer.appendChild(img);
  } else {
    renderLocalQR(waLink);
  }

  // Show result section and scroll to it
  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      has_smartqr: !!smartQR
    });
  }
}

function renderLocalQR(waLink) {
  const container = document.getElementById('qr-container');
  container.innerHTML = '';

  new QRCode(container, {
    text: waLink,
    width: 220,
    height: 220,
    colorDark:  '#020617',
    colorLight: '#ffffff',
    correctLevel: QRCode.CorrectLevel.H
  });

  qrReady = true;
  setDownloadEnabled(true);
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

function copyShortUrl() {
  if (!smartQRData || !smartQRData.short_url) return;

  const doFeedback = () => {
    const btn = document.getElementById('copy-short-btn-text');
    btn.textContent = 'Copied!';
    setTimeout(() => {
      btn.textContent = 'Copy short link';
    }, 2000);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('result_copied', { type: 'short_url' });
    }
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(smartQRData.short_url).then(doFeedback).catch(() => fallbackCopy(doFeedback, smartQRData.short_url));
  } else {
    fallbackCopy(doFeedback, smartQRData.short_url);
  }
}

function fallbackCopy(callback, text) {
  const ta = document.createElement('textarea');
  ta.value = text || lastWaLink;
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

  // If we have a server-generated QR, download that
  if (smartQRData && smartQRData.qr_png_url) {
    const link = document.createElement('a');
    link.href = smartQRData.qr_png_url + '?size=1024&logo=1';
    link.download = 'whatsapp-qr-infoweb.png';
    link.target = '_blank';
    link.click();
    if (typeof window.trackEvent === 'function') window.trackEvent('qr_downloaded', { source: 'smartqr' });
    return;
  }

  // Fallback: download locally-generated QR
  const srcCanvas = document.querySelector('#qr-container canvas');
  if (!srcCanvas) return;

  const scale       = 4;
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

  if (typeof window.trackEvent === 'function') window.trackEvent('qr_downloaded', { source: 'local' });
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
  smartQRData = null;
  qrReady    = false;
  setDownloadEnabled(false);

  // Hide SmartQR elements
  const manageEl = document.getElementById('smartqr-manage-url');
  if (manageEl) manageEl.classList.add('hidden');

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
