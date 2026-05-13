/**
 * Free Tools Shared Library
 * Common utilities for all InfoWeb free tools
 */

// ─── API Configuration ────────────────────────────────────────────────────────
const API_BASE = 'https://infoweb.api.sousadev.com';
const CONTACT_API_ENDPOINT = `${API_BASE}/leads/tool-contact/`;

// ─── UI Helpers ───────────────────────────────────────────────────────────────
function show(id)   { 
  const el = document.getElementById(id);
  if (el) el.classList.remove('hidden'); 
}

function hide(id)   { 
  const el = document.getElementById(id);
  if (el) el.classList.add('hidden'); 
}

function showFlex(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.remove('hidden');
    el.classList.add('show-flex');
  }
}

function hideFlex(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('hidden');
    el.classList.remove('show-flex');
  }
}

function toggle(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('hidden');
}

// ─── Form Validation ──────────────────────────────────────────────────────────
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhone(phone, minLength = 6) {
  const digits = phone.replace(/\D/g, '');
  return digits.length >= minLength;
}

function validateRequired(value) {
  return value && value.trim().length > 0;
}

// ─── Lead Capture ─────────────────────────────────────────────────────────────
async function submitContactLead(email, source, options = {}) {
  const {
    onSuccess = () => {},
    onError = () => {},
    onValidationError = () => {}
  } = options;

  if (!validateEmail(email)) {
    onValidationError('Invalid email');
    return false;
  }

  try {
    const response = await fetch(CONTACT_API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, source })
    });

    if (!response.ok) throw new Error('HTTP ' + response.status);

    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submitted', { form: 'tool_contact', source });
    }
    
    onSuccess();
    return true;
  } catch (err) {
    console.error('[submitContactLead]', err);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('lead_submit_failed', { error_type: 'api_error', form: 'tool_contact' });
    }
    onError(err);
    return false;
  }
}

// ─── Copy to Clipboard ────────────────────────────────────────────────────────
async function copyToClipboard(text, feedbackEl = null) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      fallbackCopy(text);
    }
    
    if (feedbackEl) {
      const originalText = feedbackEl.textContent;
      feedbackEl.textContent = 'Copied!';
      setTimeout(() => {
        feedbackEl.textContent = originalText;
      }, 2000);
    }
    
    return true;
  } catch (err) {
    console.error('Copy failed:', err);
    return false;
  }
}

function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
}

// ─── File Upload ──────────────────────────────────────────────────────────────
async function uploadFile(file, options = {}) {
  const {
    maxSize = 10 * 1024 * 1024,
    allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    onProgress = () => {}
  } = options;

  if (file.size > maxSize) {
    throw new Error(`File too large. Max size: ${maxSize / (1024 * 1024)}MB`);
  }

  if (!allowedTypes.includes(file.type)) {
    throw new Error('File type not allowed');
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload/`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Upload failed');
  }

  return await response.json();
}

// ─── SmartQR Integration ──────────────────────────────────────────────────────
async function createSmartQR(targetUrl, label, toolSource, options = {}) {
  const response = await fetch(`${API_BASE}/smartqr/codes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      target_url: targetUrl,
      label: label,
      tool_source: toolSource,
      ...options
    })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'SmartQR creation failed');
  }

  return await response.json();
}

// ─── Debounce Utility ─────────────────────────────────────────────────────────
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ─── Number Formatting ────────────────────────────────────────────────────────
function formatCurrency(value, currency = 'EUR', locale = 'pt-PT') {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency
  }).format(value);
}

function formatNumber(value, locale = 'pt-PT') {
  return new Intl.NumberFormat(locale).format(value);
}

// ─── Scroll to Element ────────────────────────────────────────────────────────
function scrollToElement(selector, offset = 0) {
  const element = document.querySelector(selector);
  if (element) {
    const top = element.getBoundingClientRect().top + window.pageYOffset + offset;
    window.scrollTo({ top, behavior: 'smooth' });
  }
}

// ─── Export for module systems ────────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    API_BASE,
    CONTACT_API_ENDPOINT,
    show,
    hide,
    showFlex,
    hideFlex,
    toggle,
    validateEmail,
    validatePhone,
    validateRequired,
    submitContactLead,
    copyToClipboard,
    uploadFile,
    createSmartQR,
    debounce,
    formatCurrency,
    formatNumber,
    scrollToElement
  };
}
