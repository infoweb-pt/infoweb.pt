/**
 * [TOOL_NAME] - Tool Logic
 * 
 * Uses shared utilities from ../../assets/js/free-tools-shared.js
 */

'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let toolRunStartedAt = 0;

// ─── UI Helpers (from shared) ─────────────────────────────────────────────────
// show, hide, showFlex, hideFlex, toggle, validateEmail, validatePhone, 
// validateRequired, submitContactLead, copyToClipboard, uploadFile, 
// createSmartQR, debounce, formatCurrency, formatNumber, scrollToElement

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  toolRunStartedAt = performance.now();
  
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_used');
  }

  showSpinner();
  hide('result-box');
  hide('error-box');

  try {
    // [TOOL_LOGIC]
    
    renderResult();
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideSpinner();
  }
}

function renderResult() {
  show('result-box');
  scrollToElement('#output-section');

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

function showSpinner() { showFlex('spinner'); }
function hideSpinner() { hideFlex('spinner'); }

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');
  
  // [RESET_LOGIC]
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  // [INIT_LOGIC]
});
