// InfoWeb Blog - Dynamic Post Loading and Filtering

const {
  getPreferredLanguage,
  setPreferredLanguage,
  getCategoryName,
  formatPostDate,
  getIndexTranslations,
  replaceDynamicTokens
} = window.BlogI18n;

let allPosts = [];
let filteredPosts = [];
let categories = new Set();
let currentLanguage = 'en';

function getCurrentLanguage() {
  return getPreferredLanguage();
}

function setLanguage(lang) {
  currentLanguage = setPreferredLanguage(lang);
  document.documentElement.lang = currentLanguage;
  updateUILanguage();
  filterByLanguage();
}

function updateUILanguage() {
  const t = getIndexTranslations(currentLanguage);

  document.getElementById('langEN').classList.toggle('bg-slate-800', currentLanguage === 'en');
  document.getElementById('langEN').classList.toggle('border-slate-500', currentLanguage === 'en');
  document.getElementById('langEN').classList.toggle('text-white', currentLanguage === 'en');

  document.getElementById('langPT').classList.toggle('bg-slate-800', currentLanguage === 'pt');
  document.getElementById('langPT').classList.toggle('border-slate-500', currentLanguage === 'pt');
  document.getElementById('langPT').classList.toggle('text-white', currentLanguage === 'pt');

  document.getElementById('heroTitle').textContent = t.heroTitle;
  document.getElementById('heroSubtitle').textContent = t.heroSubtitle;
  document.getElementById('searchInput').placeholder = t.searchPlaceholder;
  document.getElementById('allCategoriesOption').textContent = t.allCategories;
  document.getElementById('sortNewestOption').textContent = t.sortNewest;
  document.getElementById('sortOldestOption').textContent = t.sortOldest;
  document.getElementById('sortTitleAscOption').textContent = t.sortTitleAsc;
  document.getElementById('sortTitleDescOption').textContent = t.sortTitleDesc;
  document.getElementById('loadingText').textContent = t.loading;
  document.getElementById('noResultsText').textContent = t.noResults;
  document.getElementById('clearFiltersBtn').textContent = t.clearFilters;
  document.getElementById('featuredTitle').textContent = t.featured;
  document.getElementById('allPostsTitle').textContent = t.allPosts;
  document.getElementById('headerToolsText').textContent = t.freeTools;
  document.getElementById('headerPlansText').textContent = t.plans;
  document.getElementById('footerToolsLink').textContent = t.freeTools;
  document.getElementById('footerPlansLink').textContent = t.plans;
  document.getElementById('footerContactLink').textContent = t.contact;
  document.getElementById('footerCopyright').textContent = t.copyright;
}

async function initBlog() {
  currentLanguage = getCurrentLanguage();
  document.documentElement.lang = currentLanguage;
  updateUILanguage();

  try {
    await loadPosts();
    filterByLanguage();
    setupEventListeners();
  } catch (error) {
    console.error('Error initializing blog:', error);
    const t = getIndexTranslations(currentLanguage);
    document.getElementById('loadingState').innerHTML = `<p class="text-red-400">${
      currentLanguage === 'en'
        ? 'Error loading articles. Please try again later.'
        : 'Erro ao carregar artigos. Por favor, tente novamente mais tarde.'
    }</p>`;
  }
}

async function loadPosts() {
  const indexResponse = await fetch('./posts/metadata.json');
  if (!indexResponse.ok) throw new Error('Failed to load posts index');

  const indexData = await indexResponse.json();

  const postPromises = indexData.posts.map(async (postRef) => {
    try {
      const metadataResponse = await fetch(`./posts/${postRef.slug}/metadata.json`);
      if (!metadataResponse.ok) throw new Error(`Failed to load metadata for ${postRef.slug}`);

      const metadata = await metadataResponse.json();
      if (metadata.published) {
        return metadata;
      }
      return null;
    } catch (error) {
      console.error(`Error loading post ${postRef.slug}:`, error);
      return null;
    }
  });

  allPosts = (await Promise.all(postPromises)).filter((post) => post !== null);
}

function filterByLanguage() {
  filteredPosts = allPosts.filter((post) => post.language === currentLanguage);

  categories = new Set();
  filteredPosts.forEach((post) => {
    categories.add(post.category);
  });

  populateCategoryFilter();
  applyCategoryFilter();
}

function populateCategoryFilter() {
  const categoryFilter = document.getElementById('categoryFilter');
  const t = getIndexTranslations(currentLanguage);

  while (categoryFilter.options.length > 1) {
    categoryFilter.remove(1);
  }

  categoryFilter.options[0].textContent = t.allCategories;

  Array.from(categories)
    .sort()
    .forEach((categoryKey) => {
      const option = document.createElement('option');
      option.value = categoryKey;
      option.textContent = getCategoryName(categoryKey, currentLanguage);
      categoryFilter.appendChild(option);
    });
}

function renderPosts() {
  const loadingState = document.getElementById('loadingState');
  const noResults = document.getElementById('noResults');
  const featuredSection = document.getElementById('featuredPosts');
  const allPostsSection = document.getElementById('allPostsSection');
  const featuredGrid = document.getElementById('featuredPostsGrid');
  const allPostsGrid = document.getElementById('allPostsGrid');

  loadingState.classList.add('hidden');

  if (filteredPosts.length === 0) {
    noResults.classList.remove('hidden');
    featuredSection.classList.add('hidden');
    allPostsSection.classList.add('hidden');
    return;
  }

  noResults.classList.add('hidden');

  const featured = filteredPosts.filter((post) => post.featured);
  const regular = filteredPosts.filter((post) => !post.featured);

  if (featured.length > 0) {
    featuredSection.classList.remove('hidden');
    featuredGrid.innerHTML = featured.map((post) => createPostCard(post)).join('');
  } else {
    featuredSection.classList.add('hidden');
  }

  if (regular.length > 0) {
    allPostsSection.classList.remove('hidden');
    allPostsGrid.innerHTML = regular.map((post) => createPostCard(post)).join('');
  } else if (featured.length === 0) {
    allPostsSection.classList.add('hidden');
  }

  if (typeof gtag === 'function') {
    gtag('event', 'blog_index_view', {
      posts_count: filteredPosts.length,
      language: currentLanguage
    });
  }
}

function createPostCard(post) {
  const t = getIndexTranslations(currentLanguage);
  const imageUrl = `./posts/${post.slug}/${post.image}`;
  const postUrl = `./posts/${post.slug}/`;
  const formattedDate = formatPostDate(post.dateCreated, currentLanguage);
  const categoryName = getCategoryName(post.category, currentLanguage);
  const title = replaceDynamicTokens(post.title);
  const description = replaceDynamicTokens(post.description);
  const tagsHtml = post.tags
    .slice(0, 3)
    .map((tag) => `<span class="text-xs text-slate-400">#${tag}</span>`)
    .join(' ');

  return `
    <article class="group block h-full rounded-2xl border border-slate-800/90 bg-slate-900/55 overflow-hidden hover:border-signal/60 hover:bg-slate-900/90 hover:-translate-y-0.5 transition duration-200 shadow-[0_10px_35px_rgba(2,6,23,0.35)]">
      <a href="${postUrl}" class="block" data-track="blog_post_click" data-track-post_slug="${post.slug}">
        <div class="relative overflow-hidden">
          <img 
            src="${imageUrl}" 
            alt="${post.imageAlt}" 
            class="blog-card-image w-full"
            loading="lazy"
            onerror="this.src='../assets/images/og-image.png'"
          />
          <div class="absolute top-3 left-3">
            <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-slate-950/80 text-signal border border-signal/30">
              ${categoryName}
            </span>
          </div>
        </div>
        <div class="p-5">
          <div class="flex items-center gap-3 text-xs text-slate-500 mb-3">
            <span>${formattedDate}</span>
            <span>•</span>
            <span>${post.readTime} ${t.minRead}</span>
          </div>
          <h3 class="text-white text-lg font-bold mb-2 group-hover:text-signal transition">
            ${title}
          </h3>
          <p class="text-sm text-slate-400 mb-4 line-clamp-2">
            ${description}
          </p>
          <div class="flex items-center justify-between">
            <div class="flex gap-2 flex-wrap">
              ${tagsHtml}
            </div>
            <span class="text-xs font-semibold text-signal/90">${t.readMore} →</span>
          </div>
        </div>
      </a>
    </article>
  `;
}

function searchPosts(query) {
  const searchTerm = query.toLowerCase().trim();
  const languagePosts = allPosts.filter((post) => post.language === currentLanguage);

  if (!searchTerm) {
    filteredPosts = languagePosts;
  } else {
    filteredPosts = languagePosts.filter((post) => {
      const categoryLabel = getCategoryName(post.category, currentLanguage).toLowerCase();
      return (
        replaceDynamicTokens(post.title).toLowerCase().includes(searchTerm) ||
        replaceDynamicTokens(post.description).toLowerCase().includes(searchTerm) ||
        categoryLabel.includes(searchTerm) ||
        post.tags.some((tag) => tag.toLowerCase().includes(searchTerm))
      );
    });

    if (typeof gtag === 'function') {
      gtag('event', 'search_query', {
        search_term: searchTerm,
        results_count: filteredPosts.length,
        language: currentLanguage
      });
    }
  }

  applyCategoryFilter();
}

function applyCategoryFilter() {
  const categoryFilter = document.getElementById('categoryFilter');
  const selectedCategory = categoryFilter.value;

  if (selectedCategory) {
    filteredPosts = filteredPosts.filter((post) => post.category === selectedCategory);
  }

  applySorting();
}

function applySorting() {
  const sortBy = document.getElementById('sortBy').value;
  const locale = currentLanguage === 'en' ? 'en-GB' : 'pt-PT';

  switch (sortBy) {
    case 'dateDesc':
      filteredPosts.sort((a, b) => new Date(b.dateCreated) - new Date(a.dateCreated));
      break;
    case 'dateAsc':
      filteredPosts.sort((a, b) => new Date(a.dateCreated) - new Date(b.dateCreated));
      break;
    case 'titleAsc':
      filteredPosts.sort((a, b) => a.title.localeCompare(b.title, locale));
      break;
    case 'titleDesc':
      filteredPosts.sort((a, b) => b.title.localeCompare(a.title, locale));
      break;
  }

  renderPosts();
}

function resetFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('categoryFilter').value = '';
  document.getElementById('sortBy').value = 'dateDesc';
  filterByLanguage();
}

function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortBy = document.getElementById('sortBy');
  const langEN = document.getElementById('langEN');
  const langPT = document.getElementById('langPT');

  langEN.addEventListener('click', () => {
    if (currentLanguage !== 'en') {
      const from = currentLanguage;
      setLanguage('en');
      if (typeof gtag === 'function') {
        gtag('event', 'language_switch', { from, to: 'en', location: 'blog_index' });
      }
    }
  });

  langPT.addEventListener('click', () => {
    if (currentLanguage !== 'pt') {
      const from = currentLanguage;
      setLanguage('pt');
      if (typeof gtag === 'function') {
        gtag('event', 'language_switch', { from, to: 'pt', location: 'blog_index' });
      }
    }
  });

  let searchTimeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      searchPosts(e.target.value);
    }, 300);
  });

  categoryFilter.addEventListener('change', () => {
    filteredPosts = allPosts.filter((post) => post.language === currentLanguage);
    searchPosts(searchInput.value);
  });

  sortBy.addEventListener('change', () => {
    applySorting();
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initBlog);
} else {
  initBlog();
}

window.resetFilters = resetFilters;
