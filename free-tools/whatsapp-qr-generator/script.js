'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let lastWaLink = '';
let smartQRData = null;
let qrReady = false;
let toolRunStartedAt = 0;
let qrCustomizer = null;
let uploadedLogo = null;

// ─── API Configuration ────────────────────────────────────────────────────────
const API_BASE = 'https://infoweb.api.sousadev.com';
const SMARTQR_API = `${API_BASE}/smartqr/codes/`;

// ─── Contact lead API ─────────────────────────────────────────────────────────
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

// ─── Logo Upload ──────────────────────────────────────────────────────────────
function handleLogoUpload(input) {
  const file = input.files[0];
  if (!file) return;
  
  if (file.size > 2 * 1024 * 1024) {
    alert('Logo too large. Max 2MB.');
    input.value = '';
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      uploadedLogo = img;
      document.getElementById('logo-label').textContent = file.name;
      if (qrCustomizer) {
        qrCustomizer.setLogo(img, 0.2);
      }
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
  
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_input_changed', { field: 'logo_file' });
  }
}

// ─── QR Style Updates ─────────────────────────────────────────────────────────
function updateQRStyle() {
  if (!qrCustomizer) return;
  
  const color = document.getElementById('qr-color').value;
  const bg = document.getElementById('qr-bg').value;
  const frameText = document.getElementById('frame-text').value;
  
  qrCustomizer.update({
    colorDark: color,
    colorLight: bg
  });
  
  if (frameText) {
    qrCustomizer.setFrame(frameText, color, bg);
  } else {
    qrCustomizer.removeFrame();
  }
}

function setDotStyle(style) {
  document.querySelectorAll('.dot-style-btn').forEach(btn => {
    btn.classList.remove('active', 'border-green-500', 'text-green-400');
    btn.classList.add('border-slate-600', 'text-slate-300');
  });
  
  const activeBtn = document.querySelector(`[data-style="${style}"]`);
  if (activeBtn) {
    activeBtn.classList.add('active', 'border-green-500', 'text-green-400');
    activeBtn.classList.remove('border-slate-600', 'text-slate-300');
  }
  
  if (qrCustomizer) {
    qrCustomizer.setDotStyle(style);
  }
}

// ─── Live phone validation ────────────────────────────────────────────────────
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
  
  // Update preview if valid
  if (digits.length >= 6) {
    updatePreview();
  }
}

// ─── Update preview with current inputs ───────────────────────────────────────
function updatePreview() {
  if (!qrCustomizer) return;
  
  // Preview always shows example page, not actual WhatsApp link
  // This avoids requiring input and shows a working demo
  qrCustomizer.setText('https://infoweb.api.sousadev.com/free-tools/qr-example/');
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
  updatePreview();
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

    // Update customizer with final link
    qrCustomizer.setText(lastWaLink);

    // Create SmartQR via API
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

  // Move QR from preview to result
  const qrPreview = document.getElementById('qr-preview');
  const qrContainer = document.getElementById('qr-container');
  qrContainer.innerHTML = '';
  if (qrPreview && qrPreview.firstChild) {
    qrContainer.appendChild(qrPreview.firstChild);
  }

  qrReady = true;
  setDownloadEnabled(true);

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

// ─── Download QR Code ─────────────────────────────────────────────────────────
function downloadQR() {
  if (!qrCustomizer) return;
  
  qrCustomizer.download('whatsapp-qr-infoweb.png');
  
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded', { source: 'whatsapp_qr' });
  }
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
  document.getElementById('frame-text').value = '';
  document.getElementById('qr-color').value = '#020617';
  document.getElementById('qr-bg').value = '#ffffff';
  document.getElementById('logo-file').value = '';
  document.getElementById('logo-label').textContent = 'Upload logo (PNG with transparency)';

  lastWaLink = '';
  smartQRData = null;
  qrReady = false;
  uploadedLogo = null;
  setDownloadEnabled(false);

  // Reset customizer
  if (qrCustomizer) {
    qrCustomizer.removeLogo();
    qrCustomizer.removeFrame();
    qrCustomizer.update({
      colorDark: '#020617',
      colorLight: '#ffffff',
      dotStyle: 'square'
    });
    qrCustomizer.setText('https://infoweb.api.sousadev.com/free-tools/qr-example/');
  }

  // Reset dot style buttons
  setDotStyle('square');

  // Hide manage link
  const manageEl = document.getElementById('smartqr-manage-url');
  if (manageEl) manageEl.classList.add('hidden');

  inputEl.focus();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Keyboard shortcut ────────────────────────────────────────────────────────
document.getElementById('phone-number').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') runTool();
});

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  qrCustomizer = new QRCustomizer({
    container: '#qr-preview',
    defaultText: 'https://infoweb.api.sousadev.com/free-tools/qr-example/',
    onChange: (config) => console.log('QR config:', config)
  });
  
  // Bind analytics
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
      updatePreview();
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
});
