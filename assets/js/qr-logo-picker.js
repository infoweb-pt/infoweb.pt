/**
 * Curated centre-icon picker + custom logo upload for QR generator tools.
 */
(function () {
  'use strict';

  const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
  function L(en, pt) {
    return PT ? pt : en;
  }

  const INK = '#020617';

  function iconSvg(body) {
    return (
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="' +
      INK +
      '" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">' +
      body +
      '</svg>'
    );
  }

  const CURATED_ICONS = [
    { id: 'globe', label: L('Website', 'Website'), svg: iconSvg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 010 18M12 3a15 15 0 000 18"/>') },
    { id: 'link', label: L('Link', 'Link'), svg: iconSvg('<path d="M10 13a5 5 0 007.07 0l1.41-1.41a5 5 0 00-7.07-7.07L10 5"/><path d="M14 11a5 5 0 00-7.07 0L5.52 12.4a5 5 0 007.07 7.07L14 19"/>') },
    { id: 'whatsapp', label: 'WhatsApp', svg: iconSvg('<path d="M7 18l-1 3 3-1 9-9a4 4 0 10-5.66-5.66L7 18z"/><path d="M15.5 8.5a3 3 0 010 4"/>') },
    { id: 'wifi', label: 'Wi‑Fi', svg: iconSvg('<path d="M5 9a11 11 0 0114 0"/><path d="M8.5 12.5a7 7 0 017 0"/><path d="M12 20h.01"/><path d="M11 16a3 3 0 014 0"/>') },
    { id: 'menu', label: L('Menu', 'Ementa'), svg: iconSvg('<path d="M4 7h16M4 12h16M4 17h10"/>') },
    { id: 'contact', label: L('Contact', 'Contacto'), svg: iconSvg('<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h8M8 14h5"/>') },
    { id: 'star', label: L('Review', 'Avaliação'), svg: iconSvg('<path d="M12 3l2.4 4.86 5.36.78-3.88 3.78.92 5.34L12 15.9l-4.8 2.52.92-5.34L4.24 8.64l5.36-.78L12 3z"/>') },
    { id: 'shop', label: L('Shop', 'Loja'), svg: iconSvg('<path d="M4 9h16l-1 11H5L4 9z"/><path d="M8 9V6a4 4 0 018 0v3"/>') },
    { id: 'location', label: L('Location', 'Local'), svg: iconSvg('<path d="M12 21s7-4.5 7-10a7 7 0 10-14 0c0 5.5 7 10 7 10z"/><circle cx="12" cy="11" r="2.5"/>') },
    { id: 'phone', label: L('Phone', 'Telefone'), svg: iconSvg('<path d="M8 3h8l1 4-3 2a11 11 0 003 3l2-3 4 1v8a2 2 0 01-2 2C9.8 20 4 14.2 4 6a2 2 0 012-2z"/>') },
    { id: 'email', label: L('Email', 'Email'), svg: iconSvg('<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 8l9 6 9-6"/>') },
    { id: 'instagram', label: 'Instagram', svg: iconSvg('<rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="12" cy="12" r="3.5"/><path d="M16.5 7.5h.01"/>') },
    { id: 'facebook', label: 'Facebook', svg: iconSvg('<path d="M14 8h2V5h-2a3 3 0 00-3 3v2H9v3h2v7h3v-7h2.5L17 10h-3V8.5A.5.5 0 0114.5 8H14z"/>') },
    { id: 'youtube', label: 'YouTube', svg: iconSvg('<rect x="3" y="7" width="18" height="10" rx="3"/><path d="M11 10l5 3-5 3v-6z"/>') },
    { id: 'calendar', label: L('Booking', 'Reserva'), svg: iconSvg('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>') },
    { id: 'download', label: L('Download', 'Download'), svg: iconSvg('<path d="M12 4v10"/><path d="M8 10l4 4 4-4"/><path d="M5 20h14"/>') }
  ];

  const state = {
    logoImage: null,
    selectedIconId: null,
    customFileName: '',
    getCustomizer: function () {
      return null;
    },
    logoSize: 0.16
  };

  function svgToDataUrl(svg) {
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }

  function loadImageFromSrc(src) {
    return new Promise(function (resolve, reject) {
      const img = new Image();
      img.onload = function () {
        resolve(img);
      };
      img.onerror = reject;
      img.src = src;
    });
  }

  function setStatus(text) {
    const el = document.getElementById('qr-logo-picker-status');
    if (el) el.textContent = text || '';
  }

  function updateActiveButtons() {
    document.querySelectorAll('.qr-logo-picker-icon').forEach(function (btn) {
      const isNone = btn.dataset.iconId === 'none';
      const isActive = isNone ? !state.selectedIconId && !state.logoImage : btn.dataset.iconId === state.selectedIconId;
      btn.classList.toggle('is-active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  function applyLogo(img, meta) {
    state.logoImage = img;
    const customizer = state.getCustomizer();
    if (customizer) {
      customizer.setLogo(img, state.logoSize);
    }
    if (meta && meta.iconId) {
      state.selectedIconId = meta.iconId;
      state.customFileName = '';
    } else if (meta && meta.fileName) {
      state.selectedIconId = null;
      state.customFileName = meta.fileName;
    }
    updateActiveButtons();
    if (meta && meta.status) setStatus(meta.status);
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_input_changed', {
        field: meta && meta.iconId ? 'logo_icon' : 'logo_file',
        icon_id: meta && meta.iconId ? meta.iconId : undefined
      });
    }
  }

  async function selectIcon(iconId) {
    if (iconId === 'none') {
      clearSelection();
      return;
    }
    const icon = CURATED_ICONS.find(function (item) {
      return item.id === iconId;
    });
    if (!icon) return;

    const fileInput = document.getElementById('logo-file');
    if (fileInput) fileInput.value = '';

    try {
      const img = await loadImageFromSrc(svgToDataUrl(icon.svg));
      applyLogo(img, {
        iconId: icon.id,
        status: L('Icon: ', 'Ícone: ') + icon.label
      });
    } catch (err) {
      console.error('[QRLogoPicker] icon load failed', err);
    }
  }

  function clearSelection() {
    state.logoImage = null;
    state.selectedIconId = null;
    state.customFileName = '';
    const fileInput = document.getElementById('logo-file');
    if (fileInput) fileInput.value = '';
    const customizer = state.getCustomizer();
    if (customizer) customizer.removeLogo();
    updateActiveButtons();
    setStatus('');
  }

  function handleLogoUpload(input) {
    const file = input.files && input.files[0];
    if (!file) return;

    if (file.size > 2 * 1024 * 1024) {
      alert(L('Logo too large. Max 2MB.', 'Logótipo demasiado grande. Máx. 2MB.'));
      input.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      loadImageFromSrc(e.target.result)
        .then(function (img) {
          applyLogo(img, {
            fileName: file.name,
            status: L('Custom logo: ', 'Logótipo: ') + file.name
          });
        })
        .catch(function (err) {
          console.error('[QRLogoPicker] custom logo load failed', err);
        });
    };
    reader.readAsDataURL(file);
  }

  function buildPicker(mount) {
    const label = document.createElement('span');
    label.className = 'qr-logo-picker-label';
    label.textContent = L('Centre icon (optional)', 'Ícone central (opcional)');

    const grid = document.createElement('div');
    grid.className = 'qr-logo-picker-grid';
    grid.setAttribute('role', 'group');
    grid.setAttribute('aria-label', L('Curated centre icons', 'Ícones centrais'));

    const noneBtn = document.createElement('button');
    noneBtn.type = 'button';
    noneBtn.className = 'qr-logo-picker-icon is-active';
    noneBtn.dataset.iconId = 'none';
    noneBtn.title = L('No icon', 'Sem ícone');
    noneBtn.setAttribute('aria-label', L('No icon', 'Sem ícone'));
    noneBtn.setAttribute('aria-pressed', 'true');
    noneBtn.innerHTML = '<span class="qr-logo-picker-none">' + L('None', 'Nenhum') + '</span>';
    noneBtn.addEventListener('click', function () {
      clearSelection();
    });
    grid.appendChild(noneBtn);

    CURATED_ICONS.forEach(function (icon) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'qr-logo-picker-icon';
      btn.dataset.iconId = icon.id;
      btn.title = icon.label;
      btn.setAttribute('aria-label', icon.label);
      btn.setAttribute('aria-pressed', 'false');

      const img = document.createElement('img');
      img.src = svgToDataUrl(icon.svg);
      img.alt = '';
      btn.appendChild(img);

      btn.addEventListener('click', function () {
        selectIcon(icon.id);
      });
      grid.appendChild(btn);
    });

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.id = 'logo-file';
    fileInput.accept = '.png,.jpg,.jpeg,.webp,.svg';
    fileInput.className = 'hidden';
    fileInput.addEventListener('change', function () {
      handleLogoUpload(fileInput);
    });

    const uploadLabel = document.createElement('label');
    uploadLabel.className = 'qr-logo-picker-upload';
    uploadLabel.setAttribute('for', 'logo-file');
    uploadLabel.innerHTML =
      '<svg class="h-5 w-5 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">' +
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>' +
      '</svg>' +
      '<span id="logo-label" class="qr-logo-picker-upload-text">' +
      L('Upload your own logo', 'Carregar logótipo personalizado') +
      '</span>';

    const status = document.createElement('p');
    status.id = 'qr-logo-picker-status';
    status.className = 'qr-logo-picker-status';
    status.setAttribute('aria-live', 'polite');

    mount.innerHTML = '';
    mount.appendChild(label);
    mount.appendChild(grid);
    mount.appendChild(fileInput);
    mount.appendChild(uploadLabel);
    mount.appendChild(status);
  }

  window.QRLogoPicker = {
    init: function (options) {
      options = options || {};
      if (typeof options.getCustomizer === 'function') {
        state.getCustomizer = options.getCustomizer;
      }
      if (options.logoSize) {
        state.logoSize = options.logoSize;
      }
      const mount = document.getElementById('qr-logo-picker');
      if (mount && !mount.dataset.built) {
        buildPicker(mount);
        mount.dataset.built = 'true';
      }
    },
    reset: function () {
      clearSelection();
    },
    getLogo: function () {
      return state.logoImage;
    },
    applyTo: function (customizer) {
      if (customizer && state.logoImage) {
        customizer.setLogo(state.logoImage, state.logoSize);
      }
    },
    icons: CURATED_ICONS
  };

  window.handleLogoUpload = handleLogoUpload;
  window.selectQRLogoIcon = selectIcon;
  window.clearQRLogoSelection = clearSelection;
})();
