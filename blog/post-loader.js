// InfoWeb Blog - Post Content Loader

const {
  getCategoryName,
  replaceCtaPlaceholdersInMarkdown,
  formatPostDate,
  getPostUi,
  normalizeLanguage,
  replaceDynamicTokens
} = window.BlogI18n;

if (typeof marked !== 'undefined' && typeof marked.use === 'function') {
  marked.use({
    gfm: true,
    breaks: false
  });
}

function enhanceMarkdownHtml(html) {
  return html
    .replace(/<table>/g, '<div class="table-wrapper"><table>')
    .replace(/<\/table>/g, '</table></div>');
}

// Get the current post slug from the URL
function getPostSlug() {
  const pathParts = window.location.pathname.split('/').filter((p) => p);
  const postsIndex = pathParts.indexOf('posts');
  if (postsIndex >= 0 && pathParts[postsIndex + 1]) {
    return pathParts[postsIndex + 1];
  }
  return null;
}

// Load and render the blog post
async function loadPost() {
  const slug = getPostSlug();
  const lang = document.documentElement.lang?.slice(0, 2) || 'en';
  const ui = getPostUi(lang);

  if (!slug) {
    const pageLang = normalizeLanguage(document.documentElement.lang?.slice(0, 2));
    showError(getPostUi(pageLang).postNotFound, pageLang);
    return;
  }

  try {
    const metadataResponse = await fetch('./metadata.json');
    if (!metadataResponse.ok) {
      throw new Error('Failed to load metadata');
    }
    const metadata = await metadataResponse.json();
    const postLang = normalizeLanguage(metadata.language);
    const postUi = getPostUi(postLang);

    document.documentElement.lang = postLang;

    const contentResponse = await fetch('./content.md');
    if (!contentResponse.ok) {
      throw new Error('Failed to load content');
    }
    let markdownContent = await contentResponse.text();

    markdownContent = replaceDynamicTokens(markdownContent);
    markdownContent = replaceCtaPlaceholdersInMarkdown(markdownContent, postLang);
    let htmlContent = marked.parse(markdownContent);
    htmlContent = enhanceMarkdownHtml(htmlContent);

    // Avoid duplicate H1: static H1 exists in HTML for crawlers; strip first heading from markdown body
    htmlContent = htmlContent.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>\s*/i, '');

    const title = replaceDynamicTokens(metadata.title);
    const description = replaceDynamicTokens(metadata.description);

    document.title = `${title} — Blog InfoWeb`;

    updateMetaTags({ ...metadata, title, description }, postLang);

    document.getElementById('postContent').innerHTML = htmlContent;

    const postTitleEl = document.getElementById('postTitle');
    if (postTitleEl) {
      postTitleEl.textContent = title;
    }

    const categoryName = getCategoryName(metadata.category, postLang);
    document.getElementById('postCategory').textContent = categoryName;
    document.getElementById('postDate').textContent = formatPostDate(metadata.dateCreated, postLang);
    document.getElementById('postReadTime').textContent = `${metadata.readTime} ${postUi.minRead}`;

    renderTags(metadata.tags);
    setupShareButtons(metadata, postLang);

    if (typeof gtag === 'function') {
      gtag('event', 'blog_post_view', {
        post_slug: slug,
        post_title: title,
        post_category: metadata.category,
        language: postLang
      });
    }
  } catch (error) {
    console.error('Error loading post:', error);
    showError(ui.loadError, lang);
  }
}

function updateMetaTags(metadata, lang) {
  const categoryName = getCategoryName(metadata.category, lang);

  const descMeta = document.querySelector('meta[name="description"]');
  if (descMeta) descMeta.setAttribute('content', metadata.description);

  const keywordsMeta = document.querySelector('meta[name="keywords"]');
  if (keywordsMeta) keywordsMeta.setAttribute('content', metadata.tags.join(', '));

  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) ogTitle.setAttribute('content', metadata.title);

  const ogDesc = document.querySelector('meta[property="og:description"]');
  if (ogDesc) ogDesc.setAttribute('content', metadata.description);

  const articleSection = document.querySelector('meta[property="article:section"]');
  if (articleSection) articleSection.setAttribute('content', categoryName);

  const twitterTitle = document.querySelector('meta[name="twitter:title"]');
  if (twitterTitle) twitterTitle.setAttribute('content', metadata.title);

  const twitterDesc = document.querySelector('meta[name="twitter:description"]');
  if (twitterDesc) twitterDesc.setAttribute('content', metadata.description);
}

function renderTags(tags) {
  const tagsContainer = document.getElementById('postTags');
  if (!tagsContainer) return;

  tagsContainer.innerHTML = tags
    .map(
      (tag) =>
        `<span class="px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-slate-300 text-sm">#${tag}</span>`
    )
    .join('');
}

function setupShareButtons(metadata, lang) {
  const ui = getPostUi(lang);
  const postUrl = encodeURIComponent(window.location.href);
  const postTitle = encodeURIComponent(replaceDynamicTokens(metadata.title));

  const twitterBtn = document.getElementById('shareTwitter');
  if (twitterBtn) {
    twitterBtn.href = `https://twitter.com/intent/tweet?url=${postUrl}&text=${postTitle}`;
  }

  const facebookBtn = document.getElementById('shareFacebook');
  if (facebookBtn) {
    facebookBtn.href = `https://www.facebook.com/sharer/sharer.php?u=${postUrl}`;
  }

  const linkedinBtn = document.getElementById('shareLinkedIn');
  if (linkedinBtn) {
    linkedinBtn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${postUrl}`;
  }

  const copyBtn = document.getElementById('copyLink');
  if (copyBtn) {
    copyBtn.textContent = ui.copyLinkDefault;
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        copyBtn.textContent = ui.copied;
        setTimeout(() => {
          copyBtn.textContent = ui.copyLinkDefault;
        }, 2000);
      } catch (error) {
        console.error('Failed to copy:', error);
      }
    });
  }
}

function showError(message, lang) {
  const ui = getPostUi(lang);
  const contentDiv = document.getElementById('postContent');
  if (contentDiv) {
    contentDiv.innerHTML = `
      <div class="text-center py-20">
        <p class="text-red-400 text-lg">${message}</p>
        <a href="../../" class="mt-4 inline-block text-signal hover:opacity-80 transition">
          ${ui.backToBlog}
        </a>
      </div>
    `;
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadPost);
} else {
  loadPost();
}
