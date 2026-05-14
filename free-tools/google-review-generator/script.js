/**
 * Google Review Link Generator
 */

'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) {
  return PT ? pt : en;
}

const DEFAULT_QR_TEXT =
  'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('My Business');

// ─── State ────────────────────────────────────────────────────────────────────
let reviewLink = '';
let suggestedReviewText = '';
let toolRunStartedAt = 0;
let qrCustomizer = null;

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

// ─── QR style ─────────────────────────────────────────────────────────────────
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

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  const businessName = document.getElementById('business-name').value.trim();
  const placeId = document.getElementById('place-id').value.trim();
  const reviewMessage = document.getElementById('review-message').value.trim();

  if (!businessName) {
    alert(L('Please enter your business name.', 'Introduza o nome do negócio.'));
    document.getElementById('business-name').focus();
    return;
  }

  if (!qrCustomizer) {
    alert(
      L(
        'QR preview is not ready. Please refresh the page.',
        'A pré-visualização do QR não está pronta. Atualize a página.'
      )
    );
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    suggestedReviewText = reviewMessage;

    if (placeId) {
      reviewLink =
        'https://search.google.com/local/writereview?placeid=' +
        encodeURIComponent(placeId);
    } else {
      reviewLink =
        'https://www.google.com/maps/search/?api=1&query=' +
        encodeURIComponent(businessName);
    }

    try {
      qrCustomizer.setText(reviewLink);
      updateQRStyle();
    } catch (e) {
      console.error('QR customizer failed:', e);
      showFriendlyError();
      return;
    }

    renderResult();
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

function renderResult() {
  const linkEl = document.getElementById('review-link');
  linkEl.textContent = reviewLink;
  linkEl.href = reviewLink;

  const testLink = document.getElementById('test-link');
  testLink.href = reviewLink;

  const wrap = document.getElementById('suggested-copy-wrap');
  const preview = document.getElementById('suggested-preview-text');
  if (suggestedReviewText) {
    wrap.classList.remove('hidden');
    preview.textContent = suggestedReviewText;
  } else {
    wrap.classList.add('hidden');
    preview.textContent = '';
  }

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

function copySuggestedText() {
  if (!suggestedReviewText) return;

  const doFeedback = function () {
    const el = document.getElementById('copy-suggested-btn-text');
    if (!el) return;
    el.textContent = L('Copied!', 'Copiado!');
    setTimeout(function () {
      el.textContent = L('Copy suggested text', 'Copiar texto sugerido');
    }, 2000);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('suggested_review_copied');
    }
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(suggestedReviewText).then(doFeedback).catch(function () {
      fallbackCopySuggested(doFeedback);
    });
  } else {
    fallbackCopySuggested(doFeedback);
  }
}

function fallbackCopySuggested(callback) {
  const ta = document.createElement('textarea');
  ta.value = suggestedReviewText;
  ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
  } catch (_) {}
  document.body.removeChild(ta);
  if (callback) callback();
}

// ─── Copy Link ────────────────────────────────────────────────────────────────
function copyLink() {
  if (!reviewLink) return;

  const doFeedback = function () {
    const btn = document.getElementById('copy-btn-text');
    btn.textContent = L('Copied!', 'Copiado!');
    setTimeout(function () {
      btn.textContent = L('Copy link', 'Copiar link');
    }, 2000);
    if (typeof window.trackEvent === 'function') window.trackEvent('result_copied');
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(reviewLink).then(doFeedback).catch(function () {
      fallbackCopy(doFeedback);
    });
  } else {
    fallbackCopy(doFeedback);
  }
}

function fallbackCopy(callback) {
  const ta = document.createElement('textarea');
  ta.value = reviewLink;
  ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
  } catch (_) {}
  document.body.removeChild(ta);
  if (callback) callback();
}

// ─── Download QR ──────────────────────────────────────────────────────────────
function downloadQR() {
  if (!qrCustomizer) return;
  qrCustomizer.download('google-review-qr.png');

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded');
  }
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');

  document.getElementById('business-name').value = '';
  document.getElementById('place-id').value = '';
  document.getElementById('review-message').value = '';
  document.getElementById('char-count').textContent = '0';

  const logoInput = document.getElementById('logo-file');
  if (logoInput) logoInput.value = '';
  const logoLabel = document.getElementById('logo-label');
  if (logoLabel) logoLabel.textContent = L('Upload logo (PNG with transparency)', 'Carregar logótipo (PNG com transparência)');

  const frameEl = document.getElementById('frame-text');
  if (frameEl) frameEl.value = '';

  const qc = document.getElementById('qr-color');
  const qb = document.getElementById('qr-bg');
  if (qc) qc.value = '#020617';
  if (qb) qb.value = '#ffffff';

  reviewLink = '';
  suggestedReviewText = '';

  if (qrCustomizer) {
    qrCustomizer.removeLogo();
    qrCustomizer.removeFrame();
    qrCustomizer.update({
      colorDark: '#020617',
      colorLight: '#ffffff',
      dotStyle: 'square'
    });
    qrCustomizer.setText(DEFAULT_QR_TEXT);
    setDotStyle('square');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('review-message').addEventListener('input', function () {
    document.getElementById('char-count').textContent = String(this.value.length);
  });

  if (typeof window.QRCustomizer === 'undefined') {
    console.error('QRCustomizer not loaded');
    return;
  }
  qrCustomizer = new window.QRCustomizer({
    container: '#qr-preview',
    defaultText: DEFAULT_QR_TEXT,
    onChange: function () {}
  });
  setDotStyle('square');
});
