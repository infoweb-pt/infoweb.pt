'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let lastWaLink = '';
let qrInstance  = null;

// ─── Analytics helper ─────────────────────────────────────────────────────────
function trackEvent(eventName, params) {
  params = Object.assign({ tool_name: 'whatsapp_qr_generator' }, params || {});
  if (typeof gtag !== 'undefined') {
    gtag('event', eventName, params);
  }
  console.debug('[trackEvent]', eventName, params);
}

// ─── UI helpers ───────────────────────────────────────────────────────────────
function show(id)   { const el = document.getElementById(id); el.classList.remove('hidden'); }
function hide(id)   { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('show-flex');
}

function showSpinner()  { showFlex('spinner'); }
function hideSpinner()  { hide('spinner'); document.getElementById('spinner').classList.remove('show-flex'); }

function clearErrors() {
  hide('phone-error');
  const phoneInput = document.getElementById('phone-number');
  phoneInput.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
}

function updateCharCount() {
  const msg = document.getElementById('wa-message').value;
  document.getElementById('char-count').textContent = msg.length;
}

// ─── Validation ───────────────────────────────────────────────────────────────
function validateInputs() {
  const phone = document.getElementById('phone-number').value.trim();
  const digitsOnly = phone.replace(/\D/g, '');

  if (!digitsOnly || digitsOnly.length < 6) {
    show('phone-error');
    const phoneInput = document.getElementById('phone-number');
    phoneInput.classList.add('ring-2', 'ring-red-500', 'border-red-500');
    phoneInput.focus();
    return false;
  }
  return true;
}

// ─── Main tool logic ──────────────────────────────────────────────────────────
function runTool() {
  clearErrors();

  if (!validateInputs()) return;

  trackEvent('tool_used');

  showSpinner();
  hide('result-box');
  hide('error-box');

  // Simulate brief async for UX (QR generation is sync but feels instant otherwise)
  setTimeout(() => {
    try {
      const countryCode = document.getElementById('country-code').value;
      const phone       = document.getElementById('phone-number').value.trim().replace(/\D/g, '');
      const message     = document.getElementById('wa-message').value.trim();

      const fullNumber = countryCode + phone;
      const encoded    = message ? encodeURIComponent(message) : '';
      lastWaLink       = encoded
        ? `https://wa.me/${fullNumber}?text=${encoded}`
        : `https://wa.me/${fullNumber}`;

      renderResult(lastWaLink);
    } catch (err) {
      console.error('[runTool]', err);
      showFriendlyError();
    } finally {
      hideSpinner();
    }
  }, 400);
}

function renderResult(waLink) {
  // Update link display
  document.getElementById('wa-link-display').textContent = waLink;
  document.getElementById('wa-link-open').href = waLink;

  // Generate QR Code
  const canvas = document.getElementById('qr-canvas');

  // Clear previous QR if any
  if (qrInstance) {
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  }

  // QRCode.js renders into a div, so we use a temp container then copy to canvas
  const tempDiv = document.createElement('div');
  tempDiv.style.display = 'none';
  document.body.appendChild(tempDiv);

  qrInstance = new QRCode(tempDiv, {
    text: waLink,
    width: 220,
    height: 220,
    colorDark: '#020617',
    colorLight: '#ffffff',
    correctLevel: QRCode.CorrectLevel.H
  });

  // QRCode.js creates an <img> element asynchronously
  setTimeout(() => {
    const qrImg = tempDiv.querySelector('img');
    if (qrImg) {
      const img = new Image();
      img.onload = () => {
        canvas.width  = 220;
        canvas.height = 220;
        canvas.getContext('2d').drawImage(img, 0, 0, 220, 220);
      };
      img.src = qrImg.src;
    }
    document.body.removeChild(tempDiv);
  }, 100);

  // Show result
  show('result-box');

  // Scroll to result
  document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

  trackEvent('tool_result_shown');
}

function showFriendlyError() {
  hide('result-box');
  show('error-box');
}

// ─── Copy link ────────────────────────────────────────────────────────────────
function copyLink() {
  if (!lastWaLink) return;

  navigator.clipboard.writeText(lastWaLink).then(() => {
    const btn  = document.getElementById('copy-btn-text');
    btn.textContent = 'Copied!';
    const linkDisplay = document.getElementById('wa-link-display');
    linkDisplay.classList.add('copy-flash');
    setTimeout(() => {
      btn.textContent = 'Copy link';
      linkDisplay.classList.remove('copy-flash');
    }, 2000);
    trackEvent('result_copied');
  }).catch(() => {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = lastWaLink;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    document.getElementById('copy-btn-text').textContent = 'Copied!';
    setTimeout(() => { document.getElementById('copy-btn-text').textContent = 'Copy link'; }, 2000);
    trackEvent('result_copied');
  });
}

// ─── Download QR Code ─────────────────────────────────────────────────────────
function downloadQR() {
  const canvas = document.getElementById('qr-canvas');
  if (!canvas || canvas.width === 0) return;

  // Create a higher-res version for printing quality
  const printCanvas  = document.createElement('canvas');
  const scale        = 4; // 4× for print quality
  printCanvas.width  = 220 * scale;
  printCanvas.height = 220 * scale;
  const ctx          = printCanvas.getContext('2d');

  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, printCanvas.width, printCanvas.height);
  ctx.drawImage(canvas, 0, 0, printCanvas.width, printCanvas.height);

  const link    = document.createElement('a');
  link.download = 'whatsapp-qr-infoweb.png';
  link.href     = printCanvas.toDataURL('image/png');
  link.click();

  trackEvent('qr_downloaded');
}

// ─── Reset ────────────────────────────────────────────────────────────────────
function resetTool() {
  hide('result-box');
  hide('error-box');
  clearErrors();
  document.getElementById('phone-number').value = '';
  document.getElementById('wa-message').value   = '';
  document.getElementById('char-count').textContent = '0';
  lastWaLink  = '';
  qrInstance  = null;
  document.getElementById('phone-number').focus();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Allow Enter key on phone field ──────────────────────────────────────────
document.getElementById('phone-number').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') runTool();
});
