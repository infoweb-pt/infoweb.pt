/**
 * Digital Business Card QR Generator
 */

'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let vCardData = null;
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

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    // Generate vCard data
    vCardData = generateVCard({ name, title, company, phone, email, website });

    // Generate QR Code
    const qrContainer = document.getElementById('qr-container');
    qrContainer.innerHTML = '';

    try {
      if (typeof qrcode !== 'undefined') {
        const qr = qrcode(0, 'H');
        qr.addData(vCardData);
        qr.make();

        // Create canvas
        const canvas = document.createElement('canvas');
        const size = 220;
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        // Draw QR
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
      }
    } catch (e) {
      console.error('QR generation failed:', e);
    }

    renderResult({ name, title, company, phone, email, website });
  } catch (err) {
    console.error('[runTool]', err);
    showFriendlyError();
  } finally {
    hideFlex('spinner');
  }
}

function generateVCard(data) {
  let vCard = 'BEGIN:VCARD\n';
  vCard += 'VERSION:3.0\n';
  vCard += `FN:${data.name}\n`;
  vCard += `N:${data.name};;;\n`;
  
  if (data.title) {
    vCard += `TITLE:${data.title}\n`;
  }
  if (data.company) {
    vCard += `ORG:${data.company}\n`;
  }
  if (data.phone) {
    vCard += `TEL:${data.phone}\n`;
  }
  if (data.email) {
    vCard += `EMAIL:${data.email}\n`;
  }
  if (data.website) {
    vCard += `URL:${data.website}\n`;
  }
  
  vCard += 'END:VCARD';
  return vCard;
}

function renderResult(data) {
  // Update preview
  document.getElementById('preview-name').textContent = data.name;
  document.getElementById('preview-title').textContent = data.title || '';
  document.getElementById('preview-company').textContent = data.company || '';
  document.getElementById('preview-phone').textContent = data.phone ? `📞 ${data.phone}` : '';
  document.getElementById('preview-email').textContent = data.email ? `✉️ ${data.email}` : '';
  document.getElementById('preview-website').textContent = data.website ? `🌐 ${data.website}` : '';

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

// ─── Download QR ──────────────────────────────────────────────────────────────
function downloadQR() {
  const canvas = document.querySelector('#qr-container canvas');
  if (!canvas) return;

  const link = document.createElement('a');
  link.download = 'business-card-qr.png';
  link.href = canvas.toDataURL('image/png');
  link.click();

  if (typeof window.trackEvent === 'function') {
    window.trackEvent('qr_downloaded');
  }
}

// ─── Download vCard ───────────────────────────────────────────────────────────
function downloadVCard() {
  if (!vCardData) return;

  const blob = new Blob([vCardData], { type: 'text/vcard' });
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
  document.getElementById('qr-container').innerHTML = '';

  vCardData = null;

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  // Initialize
});
