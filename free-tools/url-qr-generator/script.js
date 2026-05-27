'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

let qrCustomizer = null;
let uploadedLogo = null;
let smartQRData = null;
let toolRunStartedAt = 0;

const API_BASE = 'https://infoweb.api.sousadev.com';
const SMARTQR_API = `${API_BASE}/smartqr/codes/`;
const QR_PREVIEW_LIVE_SELECTOR = '#qr-preview-live';
const QR_PREVIEW_RESULT_ID = 'qr-preview-result';
const PREVIEW_URL = 'https://infoweb.sousadev.com/';

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}
function hideSpinner() {
  const el = document.getElementById('spinner');
  el.classList.add('hidden');
  el.classList.remove('show-flex');
}

function toAbsoluteUrl(url) {
  if (!url) return url;
  try {
    return new URL(url, `${API_BASE}/`).toString();
  } catch {
    return url;
  }
}

function normalizeUrl(raw) {
  const trimmed = (raw || '').trim();
  if (!trimmed) return null;
  const withProtocol = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
  try {
    const parsed = new URL(withProtocol);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') return null;
    return parsed.toString();
  } catch {
    return null;
  }
}

function syncResultPreview() {
  const resultContainer = document.getElementById(QR_PREVIEW_RESULT_ID);
  if (!resultContainer) return;
  resultContainer.innerHTML = '';
  if (!qrCustomizer || !qrCustomizer.canvas) return;

  const canvas = document.createElement('canvas');
  canvas.width = qrCustomizer.canvas.width;
  canvas.height = qrCustomizer.canvas.height;
  canvas.style.maxWidth = '100%';
  canvas.style.height = 'auto';
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  ctx.drawImage(qrCustomizer.canvas, 0, 0);
  resultContainer.appendChild(canvas);
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
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      uploadedLogo = img;
      document.getElementById('logo-label').textContent = file.name;
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

function validateLive() {
  const raw = document.getElementById('target-url').value;
  const urlError = document.getElementById('url-error');
  const normalized = normalizeUrl(raw);

  if (!raw.trim()) {
    urlError.classList.add('hidden');
    if (qrCustomizer) qrCustomizer.setText(PREVIEW_URL);
    updateQRStyle();
    return;
  }

  if (!normalized) {
    urlError.classList.remove('hidden');
    return;
  }

  urlError.classList.add('hidden');
  if (qrCustomizer) {
    qrCustomizer.setText(normalized);
    updateQRStyle();
  }
}

async function runTool() {
  const rawUrl = document.getElementById('target-url').value.trim();
  const label = document.getElementById('qr-label').value.trim();
  const targetUrl = normalizeUrl(rawUrl);

  if (!targetUrl) {
    document.getElementById('url-error').classList.remove('hidden');
    document.getElementById('target-url').focus();
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    if (!qrCustomizer) {
      qrCustomizer = new QRCustomizer({
        container: QR_PREVIEW_LIVE_SELECTOR,
        defaultText: targetUrl,
        onChange: () => syncResultPreview()
      });
    }

    qrCustomizer.setText(targetUrl);
    updateQRStyle();

    const response = await fetch(SMARTQR_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_url: targetUrl,
        label: label || targetUrl,
        tool_source: 'generic'
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[SmartQR API error]', errorData);
      throw new Error('SmartQR API: ' + (errorData.detail || response.status));
    }

    smartQRData = await response.json();

    const scanUrl = smartQRData.short_url ? toAbsoluteUrl(smartQRData.short_url) : '';
    if (scanUrl) {
      smartQRData.short_url = scanUrl;
      qrCustomizer.setText(scanUrl);
      updateQRStyle();
      await qrCustomizer.waitForRender();
    }

    renderResult(smartQRData);
  } catch (err) {
    console.error('[runTool]', err);
    hide('result-box');
    show('error-box');
  } finally {
    hideSpinner();
  }
}

function renderResult(smartQR) {
  const smartqrInfo = document.getElementById('smartqr-info');
  smartqrInfo.classList.remove('hidden');

  const shortUrlEl = document.getElementById('smartqr-short-url');
  const shortUrl = smartQR.short_url ? toAbsoluteUrl(smartQR.short_url) : '';
  smartQR.short_url = shortUrl;
  shortUrlEl.textContent = shortUrl;
  shortUrlEl.href = shortUrl;

  document.getElementById('smartqr-manage-url').href = smartQR.manage_url;

  show('result-box');
  syncResultPreview();
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_result_shown', {
      duration_ms: Math.round(performance.now() - toolRunStartedAt),
      has_smartqr: !!smartQR
    });
  }
}

function copyShortUrl() {
  if (!smartQRData || !smartQRData.short_url) return;

  const doFeedback = () => {
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('result_copied', { type: 'short_url' });
    }
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(smartQRData.short_url).then(doFeedback);
  }
}

function downloadQR() {
  if (!qrCustomizer) return;

  qrCustomizer.download('url-qr-code.png');

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded', { source: 'url_qr' });
  }
}

function resetTool() {
  hide('result-box');
  hide('error-box');
  hide('smartqr-info');

  document.getElementById('target-url').value = '';
  document.getElementById('qr-label').value = '';
  document.getElementById('url-error').classList.add('hidden');
  document.getElementById('logo-file').value = '';
  document.getElementById('logo-label').textContent = L(
    'Upload logo (PNG with transparency)',
    'Carregar logótipo (PNG com transparência)'
  );
  document.getElementById('frame-text').value = '';
  document.getElementById('qr-color').value = '#020617';
  document.getElementById('qr-bg').value = '#ffffff';

  uploadedLogo = null;
  smartQRData = null;

  if (qrCustomizer) {
    qrCustomizer.setText(PREVIEW_URL);
    qrCustomizer.removeLogo();
    qrCustomizer.removeFrame();
    qrCustomizer.update({
      colorDark: '#020617',
      colorLight: '#ffffff',
      dotStyle: 'square'
    });
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', function() {
  qrCustomizer = new QRCustomizer({
    container: QR_PREVIEW_LIVE_SELECTOR,
    defaultText: PREVIEW_URL,
    onChange: () => syncResultPreview()
  });
});
