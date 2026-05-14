'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let qrCustomizer = null;
let uploadedFile = null;
let uploadedLogo = null;
let smartQRData = null;
let toolRunStartedAt = 0;

// ─── API Configuration ────────────────────────────────────────────────────────
const API_BASE = 'https://infoweb.api.sousadev.com';
const SMARTQR_API = `${API_BASE}/smartqr/codes/`;
const QR_PREVIEW_LIVE_SELECTOR = '#qr-preview-live';
const QR_PREVIEW_RESULT_ID = 'qr-preview-result';

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

function toAbsoluteUrl(url) {
  if (!url) return url;
  try {
    return new URL(url, `${API_BASE}/`).toString();
  } catch {
    return url;
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

// ─── File Upload Handling ─────────────────────────────────────────────────────
function handleFileUpload(input) {
  const file = input.files[0];
  if (!file) return;
  
  if (file.size > 10 * 1024 * 1024) {
    alert('File too large. Max 10MB.');
    input.value = '';
    return;
  }
  
  uploadedFile = file;
  document.getElementById('file-label').textContent = file.name;
  
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('tool_input_changed', { field: 'menu_file', file_type: file.type });
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

// ─── Main Tool Logic ──────────────────────────────────────────────────────────
async function runTool() {
  const restaurantName = document.getElementById('restaurant-name').value.trim();
  
  if (!uploadedFile) {
    alert('Please upload your menu file first.');
    return;
  }
  
  if (!restaurantName) {
    alert('Please enter your restaurant name.');
    document.getElementById('restaurant-name').focus();
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showSpinner();
  hide('result-box');
  hide('error-box');

  try {
    // Upload file to API
    let menuUrl = null;
    if (uploadedFile) {
      showSpinner();
      const formData = new FormData();
      formData.append('file', uploadedFile);
      
      const uploadResponse = await fetch(`${API_BASE}/upload/`, {
        method: 'POST',
        body: formData
      });
      
      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json().catch(() => ({}));
        throw new Error('Upload failed: ' + (errorData.detail || uploadResponse.status));
      }
      
      const uploadResult = await uploadResponse.json();
      menuUrl = toAbsoluteUrl(uploadResult.url);
    } else {
      menuUrl = `https://infoweb.api.sousadev.com/menu/${encodeURIComponent(restaurantName.toLowerCase().replace(/\s+/g, '-'))}`;
    }
    
    // Generate QR with customizer
    if (!qrCustomizer) {
      qrCustomizer = new QRCustomizer({
        container: QR_PREVIEW_LIVE_SELECTOR,
        defaultText: menuUrl,
        onChange: () => syncResultPreview()
      });
    }
    
    qrCustomizer.setText(menuUrl);
    
    // Apply current settings
    updateQRStyle();
    
    // Create SmartQR via API
    const response = await fetch(SMARTQR_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_url: menuUrl,
        label: `${restaurantName} Menu`,
        tool_source: 'menu_qr'
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
    showFriendlyError();
  } finally {
    hideSpinner();
  }
}

function renderResult(smartQR) {
  // Show SmartQR info
  const smartqrInfo = document.getElementById('smartqr-info');
  smartqrInfo.classList.remove('hidden');
  
  const shortUrlEl = document.getElementById('smartqr-short-url');
  const shortUrl = smartQR.short_url ? toAbsoluteUrl(smartQR.short_url) : '';
  smartQR.short_url = shortUrl;
  shortUrlEl.textContent = shortUrl;
  shortUrlEl.href = shortUrl;
  
  const manageEl = document.getElementById('smartqr-manage-url');
  manageEl.href = smartQR.manage_url;

  // Show result
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

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

// ─── Copy Short URL ───────────────────────────────────────────────────────────
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

// ─── Download QR ──────────────────────────────────────────────────────────────
function downloadQR() {
  if (!qrCustomizer) return;
  
  qrCustomizer.download('menu-qr-code.png');
  
  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded', { source: 'menu_qr' });
  }
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');
  hide('smartqr-info');
  
  document.getElementById('restaurant-name').value = '';
  document.getElementById('menu-file').value = '';
  document.getElementById('file-label').textContent = 'Click to upload PDF or image';
  document.getElementById('logo-file').value = '';
  document.getElementById('logo-label').textContent = 'Upload logo (PNG with transparency)';
  document.getElementById('frame-text').value = '';
  document.getElementById('qr-color').value = '#020617';
  document.getElementById('qr-bg').value = '#ffffff';
  
  uploadedFile = null;
  uploadedLogo = null;
  smartQRData = null;
  
  if (qrCustomizer) {
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

// ─── Initialize QR Customizer on load ─────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  qrCustomizer = new QRCustomizer({
    container: QR_PREVIEW_LIVE_SELECTOR,
    defaultText: 'https://infoweb.api.sousadev.com/free-tools/qr-example/',
    onChange: () => syncResultPreview()
  });
});
