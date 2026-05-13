/**
 * QR Code Customizer - Reusable Component
 * Works with qrcode-generator library (qrcode-generator.com)
 */

class QRCustomizer {
  constructor(options = {}) {
    this.container = document.querySelector(options.container || '#qr-preview');
    this.onChange = options.onChange || (() => {});
    this.defaultText = options.defaultText || 'https://infoweb.sousadev.com';
    
    this.config = {
      text: this.defaultText,
      size: 512,
      margin: 2,
      colorDark: '#020617',
      colorLight: '#ffffff',
      errorCorrectionLevel: 'H',
      logo: null,
      dotStyle: 'square',
      cornerStyle: 'square',
      frame: null,
    };
    
    this.canvas = null;
    this.ctx = null;
    
    this.init();
  }
  
  init() {
    if (!this.container) {
      console.error('QRCustomizer: Container not found');
      return;
    }
    
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.config.size;
    this.canvas.height = this.config.size;
    this.canvas.style.maxWidth = '100%';
    this.canvas.style.height = 'auto';
    this.container.innerHTML = '';
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    
    this.render();
  }
  
  update(updates) {
    Object.assign(this.config, updates);
    this.render();
    this.onChange(this.getConfig());
  }
  
  getConfig() {
    return { ...this.config };
  }
  
  setText(text) {
    this.config.text = text;
    this.render();
    this.onChange(this.getConfig());
  }
  
  setColors(colorDark, colorLight) {
    this.config.colorDark = colorDark;
    this.config.colorLight = colorLight;
    this.render();
    this.onChange(this.getConfig());
  }
  
  setLogo(image, size = 0.25) {
    this.config.logo = { image, size };
    this.render();
    this.onChange(this.getConfig());
  }
  
  removeLogo() {
    this.config.logo = null;
    this.render();
    this.onChange(this.getConfig());
  }
  
  setDotStyle(style) {
    this.config.dotStyle = style;
    this.render();
    this.onChange(this.getConfig());
  }
  
  setCornerStyle(style) {
    this.config.cornerStyle = style;
    this.render();
    this.onChange(this.getConfig());
  }
  
  setFrame(text, color, bgColor) {
    this.config.frame = { text, color, bgColor };
    this.render();
    this.onChange(this.getConfig());
  }
  
  removeFrame() {
    this.config.frame = null;
    this.render();
    this.onChange(this.getConfig());
  }
  
  async render() {
    if (!this.ctx) return;
    
    const { size, colorLight, frame } = this.config;
    const frameHeight = frame ? 80 : 0;
    const totalHeight = size + frameHeight;
    
    this.canvas.width = size;
    this.canvas.height = totalHeight;
    
    // Clear
    this.ctx.fillStyle = colorLight;
    this.ctx.fillRect(0, 0, size, totalHeight);
    
    // Generate QR matrix
    const matrix = this.generateQRMatrix();
    if (!matrix) {
      // Draw error message
      this.ctx.fillStyle = '#ef4444';
      this.ctx.font = 'bold 16px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('QR Error', size/2, size/2);
      return;
    }
    
    // Draw QR code
    await this.drawQR(matrix);
    
    // Draw frame if present
    if (frame) {
      this.drawFrame(size, frameHeight);
    }
  }
  
  generateQRMatrix() {
    try {
      // Check for qrcode-generator library
      if (typeof qrcode === 'undefined') {
        console.error('QRCustomizer: qrcode library not loaded');
        return null;
      }
      
      // qrcode-generator API: qrcode(typeNumber, errorCorrectionLevel)
      const typeNumber = 0; // Auto-detect
      const errorCorrectionLevel = this.config.errorCorrectionLevel;
      
      const qr = qrcode(typeNumber, errorCorrectionLevel);
      qr.addData(this.config.text);
      qr.make();
      
      // Return the module count and accessor function
      return {
        getModuleCount: () => qr.getModuleCount(),
        isDark: (row, col) => qr.isDark(row, col)
      };
    } catch (e) {
      console.error('QRCustomizer: QR generation failed', e);
      return null;
    }
  }
  
  async drawQR(qrData) {
    const { size, margin, colorDark, colorLight, dotStyle, cornerStyle, logo } = this.config;
    const moduleCount = qrData.getModuleCount();
    const moduleSize = (size - (margin * 2)) / moduleCount;
    const offset = margin;
    
    // Draw modules
    for (let row = 0; row < moduleCount; row++) {
      for (let col = 0; col < moduleCount; col++) {
        if (qrData.isDark(row, col)) {
          const x = offset + col * moduleSize;
          const y = offset + row * moduleSize;
          
          // Check if this is a corner finder pattern
          const isCorner = this.isCornerFinder(moduleCount, row, col);
          
          this.ctx.fillStyle = colorDark;
          
          if (isCorner) {
            this.drawCornerModule(x, y, moduleSize, cornerStyle);
          } else {
            this.drawDotModule(x, y, moduleSize, dotStyle);
          }
        }
      }
    }
    
    // Draw logo if present
    if (logo && logo.image) {
      await this.drawLogo(size, logo);
    }
  }
  
  isCornerFinder(moduleCount, row, col) {
    const size = 7; // Finder pattern size
    // Top-left
    if (row < size && col < size) return true;
    // Top-right
    if (row < size && col >= moduleCount - size) return true;
    // Bottom-left
    if (row >= moduleCount - size && col < size) return true;
    return false;
  }
  
  drawCornerModule(x, y, size, style) {
    this.ctx.beginPath();
    
    switch (style) {
      case 'rounded':
        this.roundRect(x, y, size, size, size * 0.2);
        break;
      default: // square
        this.ctx.rect(x, y, size, size);
    }
    
    this.ctx.fill();
  }
  
  drawDotModule(x, y, size, style) {
    this.ctx.beginPath();
    
    switch (style) {
      case 'rounded':
        this.roundRect(x, y, size, size, size * 0.3);
        break;
      case 'dots':
        this.ctx.arc(x + size/2, y + size/2, size * 0.4, 0, Math.PI * 2);
        break;
      default: // square
        this.ctx.rect(x, y, size, size);
    }
    
    this.ctx.fill();
  }
  
  async drawLogo(canvasSize, logo) {
    return new Promise((resolve) => {
      const logoSize = canvasSize * logo.size;
      const x = (canvasSize - logoSize) / 2;
      const y = (canvasSize - logoSize) / 2;
      
      // White background for logo
      this.ctx.fillStyle = this.config.colorLight;
      this.ctx.beginPath();
      this.roundRect(x - 4, y - 4, logoSize + 8, logoSize + 8, 8);
      this.ctx.fill();
      
      // Draw logo image
      if (logo.image.complete) {
        this.ctx.drawImage(logo.image, x, y, logoSize, logoSize);
        resolve();
      } else {
        logo.image.onload = () => {
          this.ctx.drawImage(logo.image, x, y, logoSize, logoSize);
          resolve();
        };
        logo.image.onerror = resolve;
      }
    });
  }
  
  drawFrame(qrSize, frameHeight) {
    const { frame } = this.config;
    
    // Frame background
    this.ctx.fillStyle = frame.bgColor;
    this.ctx.fillRect(0, qrSize, qrSize, frameHeight);
    
    // Frame text
    this.ctx.fillStyle = frame.color;
    this.ctx.font = `bold ${frameHeight * 0.35}px "Instrument Sans", sans-serif`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(frame.text, qrSize / 2, qrSize + frameHeight / 2);
  }
  
  roundRect(x, y, width, height, radius) {
    this.ctx.moveTo(x + radius, y);
    this.ctx.lineTo(x + width - radius, y);
    this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    this.ctx.lineTo(x + width, y + height - radius);
    this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    this.ctx.lineTo(x + radius, y + height);
    this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    this.ctx.lineTo(x, y + radius);
    this.ctx.quadraticCurveTo(x, y, x + radius, y);
    this.ctx.closePath();
  }
  
  async generate(text) {
    if (text) this.config.text = text;
    await this.render();
    return this.canvas.toDataURL('image/png');
  }
  
  download(filename = 'qr-code.png') {
    const link = document.createElement('a');
    link.download = filename;
    link.href = this.canvas.toDataURL('image/png');
    link.click();
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = QRCustomizer;
}
