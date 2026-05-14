/**
 * Digital Business Card QR Generator
 */

'use strict';

const SAMPLE_VCARD =
  'BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Your Name\r\nN:Your Name;;;;\r\nEND:VCARD';

// ─── State ────────────────────────────────────────────────────────────────────
let vCardData = null;
let toolRunStartedAt = 0;
let qrCustomizer = null;
let uploadedLogo = null;

// ─── UI Helpers ───────────────────────────────────────────────────────────────
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

// ─── QR style (shared with menu-qr pattern) ───────────────────────────────────
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
    alert('Logo too large. Max 2MB.');
    input.value = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    const img = new Image();
    img.onload = function () {
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

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  const name = document.getElementById('card-name').value.trim();
  const title = document.getElementById('card-title').value.trim();
  const company = document.getElementById('card-company').value.trim();
  const phone = document.getElementById('card-phone').value.trim();
  const email = document.getElementById('card-email').value.trim();
  const website = document.getElementById('card-website').value.trim();

  if (!name) {
    alert('Please enter your name.');
    document.getElementById('card-name').focus();
    return;
  }

  if (!qrCustomizer) {
    alert('QR preview is not ready. Please refresh the page.');
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    vCardData = generateVCard({ name, title, company, phone, email, website });

    try {
      qrCustomizer.setText(vCardData);
      updateQRStyle();
    } catch (e) {
      console.error('QR customizer failed:', e);
      showFriendlyError();
      return;
    }

    renderResult({ name, title, company, phone, email, website });
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

/** RFC 2426 / vCard 3.0 value escaping */
function escapeVCardValue(value) {
  return String(value)
    .replace(/\r/g, '')
    .replace(/\\/g, '\\\\')
    .replace(/\n/g, '\\n')
    .replace(/;/g, '\\;')
    .replace(/,/g, '\\,');
}

function generateVCard(data) {
  const e = escapeVCardValue;
  const nl = '\r\n';
  let vCard = 'BEGIN:VCARD' + nl;
  vCard += 'VERSION:3.0' + nl;
  vCard += 'FN:' + e(data.name) + nl;
  vCard += 'N:' + e(data.name) + ';;;;' + nl;

  if (data.title) {
    vCard += 'TITLE:' + e(data.title) + nl;
  }
  if (data.company) {
    vCard += 'ORG:' + e(data.company) + nl;
  }
  if (data.phone) {
    vCard += 'TEL:' + e(data.phone) + nl;
  }
  if (data.email) {
    vCard += 'EMAIL:' + e(data.email) + nl;
  }
  if (data.website) {
    vCard += 'URL:' + e(data.website) + nl;
  }

  vCard += 'END:VCARD';
  return vCard;
}

function renderResult(data) {
  document.getElementById('preview-name').textContent = data.name;
  document.getElementById('preview-title').textContent = data.title || '';
  document.getElementById('preview-company').textContent = data.company || '';
  document.getElementById('preview-phone').textContent = data.phone ? `📞 ${data.phone}` : '';
  document.getElementById('preview-email').textContent = data.email ? `✉️ ${data.email}` : '';
  document.getElementById('preview-website').textContent = data.website ? `🌐 ${data.website}` : '';

  show('result-box');
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt)
    });
  }
}

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

// ─── Download QR ──────────────────────────────────────────────────────────────
function downloadQR() {
  if (!qrCustomizer) return;
  qrCustomizer.download('business-card-qr.png');

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded');
  }
}

// ─── Download vCard ───────────────────────────────────────────────────────────
function downloadVCard() {
  if (!vCardData) return;

  const blob = new Blob([vCardData], { type: 'text/vcard;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'contact.vcf';
  link.click();
  URL.revokeObjectURL(url);

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('vcard_downloaded');
  }
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');

  document.getElementById('card-name').value = '';
  document.getElementById('card-title').value = '';
  document.getElementById('card-company').value = '';
  document.getElementById('card-phone').value = '';
  document.getElementById('card-email').value = '';
  document.getElementById('card-website').value = '';

  const logoInput = document.getElementById('logo-file');
  if (logoInput) logoInput.value = '';
  const logoLabel = document.getElementById('logo-label');
  if (logoLabel) logoLabel.textContent = 'Upload logo (PNG with transparency)';

  const frameEl = document.getElementById('frame-text');
  if (frameEl) frameEl.value = '';

  const qc = document.getElementById('qr-color');
  const qb = document.getElementById('qr-bg');
  if (qc) qc.value = '#020617';
  if (qb) qb.value = '#ffffff';

  uploadedLogo = null;
  vCardData = null;

  if (qrCustomizer) {
    qrCustomizer.removeLogo();
    qrCustomizer.removeFrame();
    qrCustomizer.update({
      colorDark: '#020617',
      colorLight: '#ffffff',
      dotStyle: 'square'
    });
    qrCustomizer.setText(SAMPLE_VCARD);
    setDotStyle('square');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  if (typeof window.QRCustomizer === 'undefined') {
    console.error('QRCustomizer not loaded');
    return;
  }
  qrCustomizer = new window.QRCustomizer({
    container: '#qr-preview',
    defaultText: SAMPLE_VCARD,
    onChange: function () {}
  });
  setDotStyle('square');
});
