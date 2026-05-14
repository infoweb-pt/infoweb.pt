/**
 * Google Review Link Generator
 */

'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let reviewLink = '';
let suggestedReviewText = '';
let toolRunStartedAt = 0;

// ─── UI Helpers ───────────────────────────────────────────────────────────────
function show(id)   { document.getElementById(id).classList.remove('hidden'); }
function hide(id)   { document.getElementById(id).classList.add('hidden'); }
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

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  const businessName = document.getElementById('business-name').value.trim();
  const placeId = document.getElementById('place-id').value.trim();
  const reviewMessage = document.getElementById('review-message').value.trim();

  if (!businessName) {
    alert('Please enter your business name.');
    document.getElementById('business-name').focus();
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

    renderResult();
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

function renderResult() {
  // Update link display
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

  // Generate QR Code
  const qrContainer = document.getElementById('qr-container');
  qrContainer.innerHTML = '';

  if (typeof qrcode === 'undefined') {
    console.error('QR library not loaded');
    showFriendlyError();
    return;
  }

  try {
    const qr = qrcode(0, 'H');
    qr.addData(reviewLink);
    qr.make();

    const canvas = document.createElement('canvas');
    const size = 220;
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    const moduleCount = qr.getModuleCount();
    const moduleSize = size / moduleCount;

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, size, size);

    for (let row = 0; row < moduleCount; row++) {
      for (let col = 0; col < moduleCount; col++) {
        if (qr.isDark(row, col)) {
          ctx.fillStyle = '#020617';
          ctx.fillRect(col * moduleSize, row * moduleSize, moduleSize, moduleSize);
        }
      }
    }

    qrContainer.appendChild(canvas);
  } catch (e) {
    console.error('QR generation failed:', e);
    showFriendlyError();
    return;
  }

  // Show result
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

  const doFeedback = () => {
    const el = document.getElementById('copy-suggested-btn-text');
    if (!el) return;
    el.textContent = 'Copied!';
    setTimeout(() => {
      el.textContent = 'Copy suggested text';
    }, 2000);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('suggested_review_copied');
    }
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(suggestedReviewText).then(doFeedback).catch(() => fallbackCopySuggested(doFeedback));
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

  const doFeedback = () => {
    const btn = document.getElementById('copy-btn-text');
    btn.textContent = 'Copied!';
    setTimeout(() => {
      btn.textContent = 'Copy link';
    }, 2000);
    if (typeof window.trackEvent === 'function') window.trackEvent('result_copied');
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(reviewLink).then(doFeedback).catch(() => fallbackCopy(doFeedback));
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
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
  if (callback) callback();
}

// ─── Download QR ──────────────────────────────────────────────────────────────
function downloadQR() {
  const canvas = document.querySelector('#qr-container canvas');
  if (!canvas) return;

  const link = document.createElement('a');
  link.download = 'google-review-qr.png';
  link.href = canvas.toDataURL('image/png');
  link.click();

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
  document.getElementById('qr-container').innerHTML = '';

  reviewLink = '';
  suggestedReviewText = '';

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Char Counter ─────────────────────────────────────────────────────────────
document.getElementById('review-message').addEventListener('input', function() {
  document.getElementById('char-count').textContent = this.value.length;
});

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  // Initialize
});
