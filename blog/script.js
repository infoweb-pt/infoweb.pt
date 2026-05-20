// InfoWeb Blog - Dynamic Post Loading and Filtering

let allPosts = [];
let filteredPosts = [];
let categories = new Set();
let currentLanguage = 'pt'; // default

// UI translations
const translations = {
  en: {
    heroTitle: 'Tips to grow your business online',
    heroSubtitle: 'Practical articles about web design, SEO, digital marketing, and proven strategies for small businesses.',
    searchPlaceholder: 'Search articles...',
    allCategories: 'All categories',
    sortNewest: 'Newest first',
    sortOldest: 'Oldest first',
    sortTitleAsc: 'Title (A-Z)',
    sortTitleDesc: 'Title (Z-A)',
    loading: 'Loading articles...',
    noResults: 'No articles found.',
    clearFilters: 'Clear filters',
    featured: 'Featured',
    allPosts: 'All articles',
    minRead: 'min read',
    readMore: 'Read more',
    freeTools: 'Free Tools',
    plans: 'Plans',
    contact: 'Contact',
    copyright: '© 2026 InfoWeb by Sousa Dev. All rights reserved.'
  },
  pt: {
    heroTitle: 'Dicas para o seu negócio crescer online',
    heroSubtitle: 'Artigos práticos sobre web design, SEO, marketing digital e estratégias comprovadas para pequenos negócios em Portugal.',
    searchPlaceholder: 'Pesquisar artigos...',
    allCategories: 'Todas as categorias',
    sortNewest: 'Mais recentes',
    sortOldest: 'Mais antigos',
    sortTitleAsc: 'Título (A-Z)',
    sortTitleDesc: 'Título (Z-A)',
    loading: 'A carregar artigos...',
    noResults: 'Nenhum artigo encontrado.',
    clearFilters: 'Limpar filtros',
    featured: 'Em destaque',
    allPosts: 'Todos os artigos',
    minRead: 'min leitura',
    readMore: 'Ler mais',
    freeTools: 'Ferramentas Grátis',
    plans: 'Planos',
    contact: 'Contacto',
    copyright: '© 2026 InfoWeb by Sousa Dev. Todos os direitos reservados.'
  }
};

// Get current language from localStorage or default to PT
function getCurrentLanguage() {
  return localStorage.getItem('blogLanguage') || 'pt';
}

// Set and persist language
function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('blogLanguage', lang);
  updateUILanguage();
  filterByLanguage();
}

// Update all UI text based on current language
function updateUILanguage() {
  const t = translations[currentLanguage];
  
  // Update language buttons
  document.getElementById('langEN').classList.toggle('bg-slate-800', currentLanguage === 'en');
  document.getElementById('langEN').classList.toggle('border-slate-500', currentLanguage === 'en');
  document.getElementById('langEN').classList.toggle('text-white', currentLanguage === 'en');
  
  document.getElementById('langPT').classList.toggle('bg-slate-800', currentLanguage === 'pt');
  document.getElementById('langPT').classList.toggle('border-slate-500', currentLanguage === 'pt');
  document.getElementById('langPT').classList.toggle('text-white', currentLanguage === 'pt');
  
  // Update hero text
  document.getElementById('heroTitle').textContent = t.heroTitle;
  document.getElementById('heroSubtitle').textContent = t.heroSubtitle;
  
  // Update search placeholder
  document.getElementById('searchInput').placeholder = t.searchPlaceholder;
  
  // Update filter options
  document.getElementById('allCategoriesOption').textContent = t.allCategories;
  document.getElementById('sortNewestOption').textContent = t.sortNewest;
  document.getElementById('sortOldestOption').textContent = t.sortOldest;
  document.getElementById('sortTitleAscOption').textContent = t.sortTitleAsc;
  document.getElementById('sortTitleDescOption').textContent = t.sortTitleDesc;
  
  // Update status messages
  document.getElementById('loadingText').textContent = t.loading;
  document.getElementById('noResultsText').textContent = t.noResults;
  document.getElementById('clearFiltersBtn').textContent = t.clearFilters;
  
  // Update section titles
  document.getElementById('featuredTitle').textContent = t.featured;
  document.getElementById('allPostsTitle').textContent = t.allPosts;
  
  // Update header/footer
  document.getElementById('headerToolsText').textContent = t.freeTools;
  document.getElementById('headerPlansText').textContent = t.plans;
  document.getElementById('footerToolsLink').textContent = t.freeTools;
  document.getElementById('footerPlansLink').textContent = t.plans;
  document.getElementById('footerContactLink').textContent = t.contact;
  document.getElementById('footerCopyright').textContent = t.copyright;
}

// Initialize the blog
async function initBlog() {
  currentLanguage = getCurrentLanguage();
  updateUILanguage();
  
  try {
    await loadPosts();
    filterByLanguage();
    setupEventListeners();
  } catch (error) {
    console.error('Error initializing blog:', error);
    const t = translations[currentLanguage];
    document.getElementById('loadingState').innerHTML = 
      `<p class="text-red-400">${currentLanguage === 'en' ? 'Error loading articles. Please try again later.' : 'Erro ao carregar artigos. Por favor, tente novamente mais tarde.'}</p>`;
  }
}

// Load posts from metadata files
async function loadPosts() {
  try {
    // Load the posts index
    const indexResponse = await fetch('./posts/metadata.json');
    if (!indexResponse.ok) throw new Error('Failed to load posts index');
    
    const indexData = await indexResponse.json();
    
    // Load metadata for each post
    const postPromises = indexData.posts.map(async (postRef) => {
      try {
        const metadataResponse = await fetch(`./posts/${postRef.slug}/metadata.json`);
        if (!metadataResponse.ok) throw new Error(`Failed to load metadata for ${postRef.slug}`);
        
        const metadata = await metadataResponse.json();
        
        // Only include published posts
        if (metadata.published) {
          return metadata;
        }
        return null;
      } catch (error) {
        console.error(`Error loading post ${postRef.slug}:`, error);
        return null;
      }
    });
    
    allPosts = (await Promise.all(postPromises)).filter(post => post !== null);
    
  } catch (error) {
    console.error('Error loading posts:', error);
    throw error;
  }
}

// Filter posts by current language
function filterByLanguage() {
  // Filter posts by language
  filteredPosts = allPosts.filter(post => post.language === currentLanguage);
  
  // Rebuild categories from filtered posts
  categories = new Set();
  filteredPosts.forEach(post => {
    categories.add(post.category);
  });
  
  populateCategoryFilter();
  applyCategoryFilter();
}

// Populate category filter dropdown
function populateCategoryFilter() {
  const categoryFilter = document.getElementById('categoryFilter');
  const t = translations[currentLanguage];
  
  // Clear existing options except the first one
  while (categoryFilter.options.length > 1) {
    categoryFilter.remove(1);
  }
  
  // Update first option text
  categoryFilter.options[0].textContent = t.allCategories;
  
  const sortedCategories = Array.from(categories).sort();
  
  sortedCategories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categoryFilter.appendChild(option);
  });
}

// Render posts to the DOM
function renderPosts() {
  const loadingState = document.getElementById('loadingState');
  const noResults = document.getElementById('noResults');
  const featuredSection = document.getElementById('featuredPosts');
  const allPostsSection = document.getElementById('allPostsSection');
  const featuredGrid = document.getElementById('featuredPostsGrid');
  const allPostsGrid = document.getElementById('allPostsGrid');
  
  // Hide loading
  loadingState.classList.add('hidden');
  
  // Check if we have posts
  if (filteredPosts.length === 0) {
    noResults.classList.remove('hidden');
    featuredSection.classList.add('hidden');
    allPostsSection.classList.add('hidden');
    return;
  }
  
  noResults.classList.add('hidden');
  
  // Separate featured and regular posts
  const featured = filteredPosts.filter(post => post.featured);
  const regular = filteredPosts.filter(post => !post.featured);
  
  // Render featured posts
  if (featured.length > 0) {
    featuredSection.classList.remove('hidden');
    featuredGrid.innerHTML = featured.map(post => createPostCard(post, true)).join('');
  } else {
    featuredSection.classList.add('hidden');
  }
  
  // Render all posts
  if (regular.length > 0) {
    allPostsSection.classList.remove('hidden');
    allPostsGrid.innerHTML = regular.map(post => createPostCard(post, false)).join('');
  } else if (featured.length === 0) {
    allPostsSection.classList.add('hidden');
  }
  
  // Track analytics
  if (typeof gtag === 'function') {
    gtag('event', 'blog_index_view', {
      posts_count: filteredPosts.length,
      language: currentLanguage
    });
  }
}

// Create a post card HTML
function createPostCard(post, isFeatured = false) {
  const t = translations[currentLanguage];
  const imageUrl = `./posts/${post.slug}/${post.image}`;
  const postUrl = `./posts/${post.slug}/`;
  const formattedDate = formatDate(post.dateCreated);
  const tagsHtml = post.tags.slice(0, 3).map(tag => 
    `<span class="text-xs text-slate-400">#${tag}</span>`
  ).join(' ');
  
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
              ${post.category}
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
            ${post.title}
          </h3>
          <p class="text-sm text-slate-400 mb-4 line-clamp-2">
            ${post.description}
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

// Format date to appropriate locale
function formatDate(dateString) {
  const date = new Date(dateString);
  const locale = currentLanguage === 'en' ? 'en-GB' : 'pt-PT';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString(locale, options);
}

// Search posts
function searchPosts(query) {
  const searchTerm = query.toLowerCase().trim();
  
  // Start with language-filtered posts
  const languagePosts = allPosts.filter(post => post.language === currentLanguage);
  
  if (!searchTerm) {
    filteredPosts = languagePosts;
  } else {
    filteredPosts = languagePosts.filter(post => {
      return (
        post.title.toLowerCase().includes(searchTerm) ||
        post.description.toLowerCase().includes(searchTerm) ||
        post.category.toLowerCase().includes(searchTerm) ||
        post.tags.some(tag => tag.toLowerCase().includes(searchTerm))
      );
    });
    
    // Track search analytics
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

// Apply category filter
function applyCategoryFilter() {
  const categoryFilter = document.getElementById('categoryFilter');
  const selectedCategory = categoryFilter.value;
  
  if (selectedCategory) {
    filteredPosts = filteredPosts.filter(post => post.category === selectedCategory);
  }
  
  applySorting();
}

// Apply sorting
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

// Reset all filters
function resetFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('categoryFilter').value = '';
  document.getElementById('sortBy').value = 'dateDesc';
  
  filterByLanguage();
}

// Setup event listeners
function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortBy = document.getElementById('sortBy');
  const langEN = document.getElementById('langEN');
  const langPT = document.getElementById('langPT');
  
  // Language switchers
  langEN.addEventListener('click', () => {
    if (currentLanguage !== 'en') {
      setLanguage('en');
      
      // Track analytics
      if (typeof gtag === 'function') {
        gtag('event', 'language_switch', {
          from: 'pt',
          to: 'en',
          location: 'blog_index'
        });
      }
    }
  });
  
  langPT.addEventListener('click', () => {
    if (currentLanguage !== 'pt') {
      setLanguage('pt');
      
      // Track analytics
      if (typeof gtag === 'function') {
        gtag('event', 'language_switch', {
          from: 'en',
          to: 'pt',
          location: 'blog_index'
        });
      }
    }
  });
  
  // Debounce search input
  let searchTimeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      searchPosts(e.target.value);
    }, 300);
  });
  
  categoryFilter.addEventListener('change', () => {
    // Start fresh from language-filtered posts
    filteredPosts = allPosts.filter(post => post.language === currentLanguage);
    searchPosts(searchInput.value);
  });
  
  sortBy.addEventListener('change', () => {
    applySorting();
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initBlog);
} else {
  initBlog();
}

// Export for use in HTML
window.resetFilters = resetFilters;
