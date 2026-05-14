'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

const API_BASE = 'https://infoweb.api.sousadev.com';
const CONTACT_API_ENDPOINT = `${API_BASE}/leads/tool-contact/`;
const CONTACT_SOURCE = 'wifi_qr_generator';

let qrCustomizer = null;
let uploadedLogo = null;
let toolRunStartedAt = 0;
let lastWifiPayload = '';

function show(id) {
  document.getElementById(id).classList.remove('hidden');
}
function hide(id) {
  document.getElementById(id).classList.add('hidden');
}
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

/** Escape SSID / password per Wi-Fi QR (ZXing-style): \\ ; , : " */
function escapeWifiValue(value) {
  return String(value)
    .replace(/\\/g, '\\\\')
    .replace(/;/g, '\\;')
    .replace(/,/g, '\\,')
    .replace(/:/g, '\\:')
    .replace(/"/g, '\\"');
}

function buildWifiPayload() {
  const ssid = document.getElementById('wifi-ssid').value.trim();
  const password = document.getElementById('wifi-password').value;
  const security = document.getElementById('wifi-security').value;
  const hidden = document.getElementById('wifi-hidden').checked;

  if (!ssid) {
    return { error: L('Please enter your Wi-Fi network name (SSID).', 'Introduza o nome da rede Wi‑Fi (SSID).') };
  }

  if (security !== 'nopass' && !password) {
    return {
      error: L(
        'Please enter the Wi-Fi password, or choose “Open network”.',
        'Introduza a palavra-passe Wi‑Fi ou escolha «Rede aberta».'
      )
    };
  }

  const encS = escapeWifiValue(ssid);
  const encP = escapeWifiValue(password);

  let typeToken = 'WPA';
  if (security === 'WEP') typeToken = 'WEP';
  if (security === 'nopass') typeToken = 'nopass';

  let payload = 'WIFI:T:' + typeToken + ';S:' + encS + ';';
  if (security !== 'nopass') {
    payload += 'P:' + encP + ';';
  } else {
    payload += 'P:;';
  }
  if (hidden) {
    payload += 'H:true;';
  }
  payload += ';';
  return { payload: payload };
}

function updateQRStyle() {
  if (!qrCustomizer) return;
  const color = document.getElementById('qr-color').value;
  const bg = document.getElementById('qr-bg').value;
  const frameTextEl = document.getElementById('frame-text');
  const frameText = frameTextEl ? frameTextEl.value.trim() : '';

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
  document.querySelectorAll('.dot-style-btn').forEach(function (btn) {
    btn.classList.remove('active', 'border-green-500', 'text-green-400');
    btn.classList.add('border-slate-600', 'text-slate-300');
  });
  const activeBtn = document.querySelector('.dot-style-btn[data-style="' + style + '"]');
  if (activeBtn) {
    activeBtn.classList.add('active', 'border-green-500', 'text-green-400');
    activeBtn.classList.remove('border-slate-600', 'text-slate-300');
  }
  if (qrCustomizer) {
    qrCustomizer.setDotStyle(style);
  }
}

function handleLogoUpload(input) {
  const file = input.files[0];
  if (!file) return;
  if (file.size > 2 * 1024 * 1024) {
    alert(L('Logo too large. Max 2MB.', 'Logótipo demasiado grande. Máx. 2MB.'));
    input.value = '';
    return;
  }
  const reader = new FileReader();
  reader.onload = function (e) {
    const img = new Image();
    img.onload = function () {
      uploadedLogo = img;
      const label = document.getElementById('logo-label');
      if (label) label.textContent = file.name;
      if (qrCustomizer) {
        qrCustomizer.setLogo(img, 0.16);
      }
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_input_changed', { field: 'logo_file' });
  }
}

function validateSecurityPasswordUI() {
  const sec = document.getElementById('wifi-security').value;
  const passWrap = document.getElementById('password-wrap');
  const passInput = document.getElementById('wifi-password');
  if (sec === 'nopass') {
    passWrap.classList.add('opacity-50', 'pointer-events-none');
    passInput.disabled = true;
    passInput.value = '';
  } else {
    passWrap.classList.remove('opacity-50', 'pointer-events-none');
    passInput.disabled = false;
  }
}

async function runTool() {
  hide('form-error');
  const built = buildWifiPayload();
  if (built.error) {
    show('form-error');
    document.getElementById('form-error').textContent = built.error;
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_validation_error', { field: 'wifi_form', reason: 'validation' });
    }
    return;
  }

  if (!qrCustomizer) {
    show('error-box');
    return;
  }

  toolRunStartedAt = performance.now();
  lastWifiPayload = built.payload;
  hide('form-error');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    qrCustomizer.setText(built.payload);
    updateQRStyle();
    if (uploadedLogo) {
      qrCustomizer.setLogo(uploadedLogo, 0.16);
    }
    await qrCustomizer.waitForRender();

    document.getElementById('payload-display').textContent = built.payload;
    const ssid = document.getElementById('wifi-ssid').value.trim();
    document.getElementById('print-ssid').textContent = ssid;
    const showPass = document.getElementById('show-password-on-print').checked;
    const sec = document.getElementById('wifi-security').value;
    const passEl = document.getElementById('print-password-row');
    if (showPass && sec !== 'nopass') {
      passEl.classList.remove('hidden');
      document.getElementById('print-password').textContent = document.getElementById('wifi-password').value;
    } else {
      passEl.classList.add('hidden');
    }

    const printCanvas = document.getElementById('print-qr-canvas');
    if (printCanvas && qrCustomizer.canvas) {
      const ctx = printCanvas.getContext('2d');
      printCanvas.width = 400;
      printCanvas.height = 400;
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, 400, 400);
      ctx.drawImage(qrCustomizer.canvas, 0, 0, 400, 400);
    }

    show('result-box');
    document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_used', {
        security: document.getElementById('wifi-security').value,
        hidden: document.getElementById('wifi-hidden').checked
      });
      window.trackEvent('tool_result_shown', {
        duration_ms: Math.round(performance.now() - toolRunStartedAt)
      });
    }
  } catch (err) {
    console.error('[runTool]', err);
    show('error-box');
  } finally {
    hideFlex('spinner');
  }
}

function copyPayload() {
  if (!lastWifiPayload) return;
  navigator.clipboard.writeText(lastWifiPayload).then(
    function () {
      if (typeof window.trackEvent === 'function') {
        window.trackEvent('result_copied', { field: 'wifi_payload' });
      }
    },
    function () {}
  );
}

function downloadQR() {
  if (!qrCustomizer) return;
  qrCustomizer.download('wifi-qr.png');
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded');
  }
}

function printPoster() {
  window.print();
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('poster_printed');
  }
}

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

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('wifi-security').addEventListener('change', validateSecurityPasswordUI);
  validateSecurityPasswordUI();

  if (typeof window.QRCustomizer === 'undefined') {
    console.error('QRCustomizer not loaded');
    return;
  }
  qrCustomizer = new window.QRCustomizer({
    container: '#qr-preview',
    defaultText: 'WIFI:T:nopass;S:ExampleGuest;P:;;',
    onChange: function () {}
  });
  setDotStyle('square');
});
