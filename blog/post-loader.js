// InfoWeb Blog - Post Content Loader

// Get the current post slug from the URL
function getPostSlug() {
  const pathParts = window.location.pathname.split('/').filter(p => p);
  const postsIndex = pathParts.indexOf('posts');
  if (postsIndex >= 0 && pathParts[postsIndex + 1]) {
    return pathParts[postsIndex + 1];
  }
  return null;
}

// CTA templates
const CTA_TEMPLATES = {
  default: `
    <div class="cta-block">
      <div class="cta-content">
        <h3>Precisa de um website profissional?</h3>
        <p>InfoWeb cria e gere o seu site. Domínio, hosting, manutenção incluídos.</p>
        <a href="/#pricing" class="cta-button" data-track="cta_click" data-track-location="blog_post_content" data-track-target="/#pricing">
          Ver Planos →
        </a>
      </div>
    </div>
  `,
  tools: `
    <div class="cta-block">
      <div class="cta-content">
        <h3>Ferramentas grátis para o seu negócio</h3>
        <p>Calculadoras, geradores de QR, e mais. Sem registo, use já.</p>
        <a href="/free-tools/" class="cta-button" data-track="cta_click" data-track-location="blog_post_content" data-track-target="/free-tools/">
          Ver Ferramentas →
        </a>
      </div>
    </div>
  `,
  contact: `
    <div class="cta-block">
      <div class="cta-content">
        <h3>Vamos conversar sobre o seu projeto?</h3>
        <p>Agende uma chamada gratuita para discutir as suas necessidades.</p>
        <a href="mailto:info@sousadev.com" class="cta-button" data-track="cta_click" data-track-location="blog_post_content" data-track-target="mailto">
          Entrar em Contacto →
        </a>
      </div>
    </div>
  `
};

// Replace CTA placeholders with actual CTAs
function replaceCTAPlaceholders(content) {
  // Replace {{CTA}} or {{CTA:default}}
  content = content.replace(/\{\{CTA(:default)?\}\}/g, CTA_TEMPLATES.default);
  
  // Replace {{CTA:tools}}
  content = content.replace(/\{\{CTA:tools\}\}/g, CTA_TEMPLATES.tools);
  
  // Replace {{CTA:contact}}
  content = content.replace(/\{\{CTA:contact\}\}/g, CTA_TEMPLATES.contact);
  
  return content;
}

// Format date to Portuguese format
function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('pt-PT', options);
}

// Load and render the blog post
async function loadPost() {
  const slug = getPostSlug();
  
  if (!slug) {
    showError('Post não encontrado');
    return;
  }
  
  try {
    // Load metadata
    const metadataResponse = await fetch(`./metadata.json`);
    if (!metadataResponse.ok) {
      throw new Error('Failed to load metadata');
    }
    const metadata = await metadataResponse.json();
    
    // Load content
    const contentResponse = await fetch(`./content.md`);
    if (!contentResponse.ok) {
      throw new Error('Failed to load content');
    }
    const markdownContent = await contentResponse.text();
    
    // Parse markdown to HTML
    let htmlContent = marked.parse(markdownContent);
    
    // Replace CTA placeholders
    htmlContent = replaceCTAPlaceholders(htmlContent);
    
    // Update page title and meta
    document.title = `${metadata.title} — Blog InfoWeb`;
    
    // Update meta tags
    updateMetaTags(metadata);
    
    // Render content
    document.getElementById('postContent').innerHTML = htmlContent;
    
    // Update post meta info
    document.getElementById('postCategory').textContent = metadata.category;
    document.getElementById('postDate').textContent = formatDate(metadata.dateCreated);
    document.getElementById('postReadTime').textContent = `${metadata.readTime} min leitura`;
    
    // Render tags
    renderTags(metadata.tags);
    
    // Setup share buttons
    setupShareButtons(metadata);
    
    // Track page view
    if (typeof gtag === 'function') {
      gtag('event', 'blog_post_view', {
        post_slug: slug,
        post_title: metadata.title,
        post_category: metadata.category
      });
    }
    
  } catch (error) {
    console.error('Error loading post:', error);
    showError('Erro ao carregar o artigo. Por favor, tente novamente mais tarde.');
  }
}

// Update meta tags dynamically
function updateMetaTags(metadata) {
  // Description
  const descMeta = document.querySelector('meta[name="description"]');
  if (descMeta) descMeta.setAttribute('content', metadata.description);
  
  // Keywords
  const keywordsMeta = document.querySelector('meta[name="keywords"]');
  if (keywordsMeta) keywordsMeta.setAttribute('content', metadata.tags.join(', '));
  
  // OG tags
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) ogTitle.setAttribute('content', metadata.title);
  
  const ogDesc = document.querySelector('meta[property="og:description"]');
  if (ogDesc) ogDesc.setAttribute('content', metadata.description);
  
  // Twitter tags
  const twitterTitle = document.querySelector('meta[name="twitter:title"]');
  if (twitterTitle) twitterTitle.setAttribute('content', metadata.title);
  
  const twitterDesc = document.querySelector('meta[name="twitter:description"]');
  if (twitterDesc) twitterDesc.setAttribute('content', metadata.description);
}

// Render tags
function renderTags(tags) {
  const tagsContainer = document.getElementById('postTags');
  if (!tagsContainer) return;
  
  tagsContainer.innerHTML = tags.map(tag => 
    `<span class="px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-slate-300 text-sm">
      #${tag}
    </span>`
  ).join('');
}

// Setup share buttons
function setupShareButtons(metadata) {
  const postUrl = encodeURIComponent(window.location.href);
  const postTitle = encodeURIComponent(metadata.title);
  
  // Twitter
  const twitterBtn = document.getElementById('shareTwitter');
  if (twitterBtn) {
    twitterBtn.href = `https://twitter.com/intent/tweet?url=${postUrl}&text=${postTitle}`;
  }
  
  // Facebook
  const facebookBtn = document.getElementById('shareFacebook');
  if (facebookBtn) {
    facebookBtn.href = `https://www.facebook.com/sharer/sharer.php?u=${postUrl}`;
  }
  
  // LinkedIn
  const linkedinBtn = document.getElementById('shareLinkedIn');
  if (linkedinBtn) {
    linkedinBtn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${postUrl}`;
  }
  
  // Copy link
  const copyBtn = document.getElementById('copyLink');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        copyBtn.textContent = '✓ Copiado!';
        setTimeout(() => {
          copyBtn.textContent = 'Copiar link';
        }, 2000);
      } catch (error) {
        console.error('Failed to copy:', error);
      }
    });
  }
}

// Show error message
function showError(message) {
  const contentDiv = document.getElementById('postContent');
  if (contentDiv) {
    contentDiv.innerHTML = `
      <div class="text-center py-20">
        <p class="text-red-400 text-lg">${message}</p>
        <a href="../../" class="mt-4 inline-block text-signal hover:opacity-80 transition">
          ← Voltar ao blog
        </a>
      </div>
    `;
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadPost);
} else {
  loadPost();
}
