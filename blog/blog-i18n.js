/**
 * Shared i18n for InfoWeb blog (index + post pages).
 * Exposed on window.BlogI18n for classic script tags.
 */
(function (global) {
  const SUPPORTED_LANGUAGES = ['en', 'pt'];
  const DEFAULT_LANGUAGE = 'en';
  const LANGUAGE_STORAGE_KEY = 'infoweb-language';

  const categoryTranslations = {
    'domains-hosting': {
      en: 'Domains & Hosting',
      pt: 'Domínios & Hosting'
    },
    'web-design': {
      en: 'Web Design',
      pt: 'Web Design'
    },
    seo: {
      en: 'SEO',
      pt: 'SEO'
    },
    'digital-marketing': {
      en: 'Digital Marketing',
      pt: 'Marketing Digital'
    },
    'small-business': {
      en: 'Small Business',
      pt: 'Pequenos Negócios'
    },
    tutorials: {
      en: 'Tutorials',
      pt: 'Tutoriais'
    },
    'case-studies': {
      en: 'Case Studies',
      pt: 'Casos de Estudo'
    },
    'company-news': {
      en: 'Company News',
      pt: 'Notícias'
    }
  };

  const ctaTemplates = {
    default: {
      en: {
        title: 'Need a professional website?',
        body: 'InfoWeb builds and manages your site. Domain, hosting, and maintenance included.',
        label: 'See plans →',
        href: '../../../#pricing',
        trackTarget: '/#pricing'
      },
      pt: {
        title: 'Precisa de um website profissional?',
        body: 'InfoWeb cria e gere o seu site. Domínio, hosting, manutenção incluídos.',
        label: 'Ver planos →',
        href: '../../../#pricing',
        trackTarget: '/#pricing'
      }
    },
    tools: {
      en: {
        title: 'Free tools for your business',
        body: 'Calculators, QR generators, and more. No sign-up required.',
        label: 'Browse free tools →',
        href: '../../../free-tools/',
        trackTarget: '/free-tools/'
      },
      pt: {
        title: 'Ferramentas grátis para o seu negócio',
        body: 'Calculadoras, geradores de QR, e mais. Sem registo, use já.',
        label: 'Ver ferramentas →',
        href: '../../../free-tools/',
        trackTarget: '/free-tools/'
      }
    },
    contact: {
      en: {
        title: "Let's talk about your project",
        body: 'Book a free call to discuss what your business needs online.',
        label: 'Get in touch →',
        href: 'mailto:info@sousadev.com',
        trackTarget: 'mailto'
      },
      pt: {
        title: 'Vamos conversar sobre o seu projeto?',
        body: 'Agende uma chamada gratuita para discutir as suas necessidades.',
        label: 'Entrar em contacto →',
        href: 'mailto:info@sousadev.com',
        trackTarget: 'mailto'
      }
    }
  };

  const indexTranslations = {
    en: {
      heroTitle: 'Tips to grow your business online',
      heroSubtitle:
        'Practical articles about web design, SEO, digital marketing, and proven strategies for small businesses.',
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
      heroSubtitle:
        'Artigos práticos sobre web design, SEO, marketing digital e estratégias comprovadas para pequenos negócios em Portugal.',
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

  const postUiStrings = {
    en: {
      postNotFound: 'Post not found',
      loadError: 'Error loading article. Please try again later.',
      backToBlog: '← Back to blog',
      loading: 'Loading article...',
      minRead: 'min read',
      copyLink: 'Copy link',
      copied: 'Copied!',
      copyLinkDefault: 'Copy link'
    },
    pt: {
      postNotFound: 'Post não encontrado',
      loadError: 'Erro ao carregar o artigo. Por favor, tente novamente mais tarde.',
      backToBlog: '← Voltar ao blog',
      loading: 'A carregar artigo...',
      minRead: 'min leitura',
      copyLink: 'Copiar link',
      copied: 'Copiado!',
      copyLinkDefault: 'Copiar link'
    }
  };

  function normalizeLanguage(lang) {
    return SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  }

  function getPreferredLanguage() {
    const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY);
    if (SUPPORTED_LANGUAGES.includes(stored)) {
      return stored;
    }
    const legacyBlog = localStorage.getItem('blogLanguage');
    if (SUPPORTED_LANGUAGES.includes(legacyBlog)) {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, legacyBlog);
      return legacyBlog;
    }
    const browser = navigator.language?.slice(0, 2).toLowerCase();
    return SUPPORTED_LANGUAGES.includes(browser) ? browser : DEFAULT_LANGUAGE;
  }

  function setPreferredLanguage(lang) {
    const safe = normalizeLanguage(lang);
    localStorage.setItem(LANGUAGE_STORAGE_KEY, safe);
    return safe;
  }

  function getCategoryName(categoryKey, lang) {
    const safeLang = normalizeLanguage(lang);
    if (categoryTranslations[categoryKey]) {
      return categoryTranslations[categoryKey][safeLang] || categoryKey;
    }
    return categoryKey;
  }

  function getCtaHtml(variant, lang) {
    const safeLang = normalizeLanguage(lang);
    const key = variant === 'default' || !variant ? 'default' : variant;
    const template = ctaTemplates[key]?.[safeLang] || ctaTemplates.default[safeLang];

    return `
<div class="cta-block">
  <div class="cta-content">
    <h3>${template.title}</h3>
    <p>${template.body}</p>
    <a href="${template.href}" class="cta-button" data-track="cta_click" data-track-location="blog_post_content" data-track-target="${template.trackTarget}">
      ${template.label}
    </a>
  </div>
</div>`;
  }

  function replaceCtaPlaceholdersInMarkdown(markdown, lang) {
    let content = markdown;
    const safeLang = normalizeLanguage(lang);

    content = content.replace(/\{\{CTA(:default)?\}\}/g, () => getCtaHtml('default', safeLang));
    content = content.replace(/\{\{CTA:tools\}\}/g, () => getCtaHtml('tools', safeLang));
    content = content.replace(/\{\{CTA:contact\}\}/g, () => getCtaHtml('contact', safeLang));

    return content;
  }

  function formatPostDate(dateString, lang) {
    const date = new Date(dateString);
    const locale = normalizeLanguage(lang) === 'pt' ? 'pt-PT' : 'en-GB';
    return date.toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  function getPostUi(lang) {
    return postUiStrings[normalizeLanguage(lang)];
  }

  function getIndexTranslations(lang) {
    return indexTranslations[normalizeLanguage(lang)];
  }

  global.BlogI18n = {
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    LANGUAGE_STORAGE_KEY,
    categoryTranslations,
    ctaTemplates,
    indexTranslations,
    postUiStrings,
    normalizeLanguage,
    getPreferredLanguage,
    setPreferredLanguage,
    getCategoryName,
    getCtaHtml,
    replaceCtaPlaceholdersInMarkdown,
    formatPostDate,
    getPostUi,
    getIndexTranslations
  };
})(typeof window !== 'undefined' ? window : globalThis);
