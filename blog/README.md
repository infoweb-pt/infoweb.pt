# InfoWeb Blog System

Static blog system for InfoWeb.pt — SEO-optimized, searchable, sortable blog posts with markdown content.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Bilingual Blog Posts](#2-bilingual-blog-posts)
3. [Directory Structure](#3-directory-structure)
4. [Creating a New Blog Post](#4-creating-a-new-blog-post)
5. [Metadata Specifications](#5-metadata-specifications)
6. [Content Guidelines](#6-content-guidelines)
7. [SEO Requirements](#7-seo-requirements)
8. [CTA Integration](#8-cta-integration)
9. [Updating the Index](#9-updating-the-index)
10. [Technical Requirements](#10-technical-requirements)
11. [Launch Checklist](#11-launch-checklist)

---

## 1. Overview

The InfoWeb blog is a static, file-based blog system that:
- Stores posts as markdown files with JSON metadata
- Automatically indexes all posts from the filesystem
- Provides search and sort functionality
- Optimizes for SEO with proper meta tags and structured data
- Includes CTAs to drive conversions
- **Supports bilingual content (English and Portuguese)**

**Live URL:** `https://infoweb.sousadev.com/blog/`

---

## 2. Bilingual Blog Posts

**⚠️ IMPORTANT: Every blog post MUST have both English and Portuguese versions.**

### Language Strategy

- **Two separate post folders** — one for each language with localized slugs
- **Cross-referenced metadata** — each post links to its translation
- **Localized content** — adapt examples, references, and focus for each market
- **Independent SEO** — each version optimized for its target language and keywords

### Naming Convention

```
English version (default):
blog/posts/choosing-perfect-domain/

Portuguese version:
blog/posts/como-escolher-dominio-perfeito/
```

### Content Adaptation Guidelines

**Don't just translate — adapt:**

1. **English posts should focus on:**
   - International markets (.com, .net, .org domains)
   - Global best practices
   - English-language examples and case studies
   - International tools and services

2. **Portuguese posts should focus on:**
   - Portuguese market (.pt domains)
   - Local regulations and practices (Portugal-specific)
   - Portuguese examples and case studies
   - Local services (DNS.PT, etc.)

### Example Adaptations

**Domain post:**
- EN: Focus on .com domains, international registrars (GoDaddy, Namecheap)
- PT: Focus on .pt domains, DNS.PT, Portuguese registrars

**SEO post:**
- EN: Google.com optimization, international keywords
- PT: Google.pt optimization, Portuguese keywords, local search

**Marketing post:**
- EN: International platforms, global strategies
- PT: Portuguese market specifics, local platforms

### Linking Between Languages

Each post must reference its translation in metadata:

```json
{
  "slug": "choosing-perfect-domain",
  "language": "en",
  "alternateLanguage": {
    "pt": "como-escolher-dominio-perfeito"
  }
}
```

This enables:
- Language switcher on post pages
- Proper hreflang tags for SEO
- Better user experience for bilingual visitors

**Live URL:** `https://infoweb.sousadev.com/blog/`

---

## 3. Directory Structure

```
blog/
├── index.html              ← Main blog listing page
├── README.md               ← This file
├── blog-i18n.js            ← Shared EN/PT strings, categories, CTAs (required)
├── post.css                ← Shared post + CTA styles (link from each post)
├── post-loader.js          ← Loads markdown, injects CTAs, renders post
├── script.js               ← Blog index (search, sort, language filter)
└── posts/
    ├── metadata.json       ← Index of all blog posts (MUST UPDATE)
    ├── choosing-perfect-domain/        ← English post
    │   ├── content.md
    │   ├── metadata.json
    │   ├── image-prompt.md   ← Required prompt for featured image generation
    │   ├── index.html
    │   └── assets/
    └── como-escolher-dominio-perfeito/ ← Portuguese post (translation)
        ├── content.md
        ├── metadata.json
        ├── image-prompt.md   ← Required prompt for featured image generation
        ├── index.html
        └── assets/
```

### Key Rules

1. **Two folders per topic** — one for EN, one for PT under `posts/[slug]/`
2. **Slug naming:** lowercase, kebab-case, SEO-friendly, language-appropriate
   - EN: `choosing-perfect-domain`
   - PT: `como-escolher-dominio-perfeito`
3. **All posts MUST be listed** in `posts/metadata.json` to appear on the index
4. **Asset paths** in markdown must be relative: `./assets/image.jpg`
5. **Cross-reference translations** in metadata using `alternateLanguage` field
6. **No server-side code** — everything runs in the browser

---

## 4. Creating a New Blog Post

### Step-by-Step (Bilingual)

**⚠️ IMPORTANT: You MUST create BOTH English and Portuguese versions.**

#### Step 1: Create English Version

1. **Create post folder:**
   ```bash
   mkdir -p blog/posts/your-post-slug-en/assets
   ```

2. **Write English content:**
   Create `blog/posts/your-post-slug-en/content.md`:
   ```markdown
   # Your Post Title
   
   Introduction paragraph...
   
   ## Section 1
   
   Content here...
   
   ![Alt text](./assets/image.jpg)
   
   {{CTA}}
   
   ## Section 2
   
   More content...
   
   {{CTA}}
   ```

3. **Create English metadata:**
   Create `blog/posts/your-post-slug-en/metadata.json`:
   ```json
   {
     "slug": "your-post-slug-en",
     "language": "en",
     "title": "Your Post Title",
     "description": "Brief description (150-160 characters for SEO)",
     "author": "InfoWeb",
     "dateCreated": "2026-05-20",
     "dateUpdated": "2026-05-20",
     "category": "web-design",
     "tags": ["websites", "small business", "SEO"],
     "image": "./assets/featured.png",
     "imageAlt": "Descriptive alt text for accessibility",
     "readTime": 5,
     "featured": false,
     "published": true,
     "alternateLanguage": {
       "pt": "your-post-slug-pt"
     }
   }
   ```

4. **Create English image prompt:**
   Create `blog/posts/your-post-slug-en/image-prompt.md` with the exact prompt an image-generation agent should use for the featured image. Include:
   - target size: `1200x630`
   - output filename: `featured.png` (canonical — must match `index.html` OG/Twitter/JSON-LD URLs)
   - style direction matching InfoWeb (dark navy, gold accent, premium small-business SaaS feel)
   - market-specific visual cues for EN content
   - things to avoid (logos, watermarks, unreadable text, real brand screenshots)

5. **Add English images:**
   Place generated images in `blog/posts/your-post-slug-en/assets/`

   **Required:** generate `featured.png` automatically (do not skip or hand-wave with placeholders):

   ```bash
   python3 scripts/blog_featured_image.py blog/posts/your-post-slug-en/
   # or regenerate all missing:
   python3 scripts/sync-blog-posts.py
   ```

   The generator writes a 1200×630 navy/gold OG card with the post title. Run this for **every** new post before commit.

#### Step 2: Create Portuguese Version

6. **Create Portuguese folder:**
   ```bash
   mkdir -p blog/posts/your-post-slug-pt/assets
   ```

7. **Write Portuguese content:**
   Create `blog/posts/your-post-slug-pt/content.md`:
   - Translate content to Portuguese
   - Adapt examples for Portuguese market (.pt domains, local services)
   - Localize references and case studies

8. **Create Portuguese metadata:**
   Create `blog/posts/your-post-slug-pt/metadata.json`:
   ```json
   {
     "slug": "your-post-slug-pt",
     "language": "pt",
     "title": "Seu Título em Português",
     "description": "Descrição breve (150-160 caracteres para SEO)",
     "author": "InfoWeb",
     "dateCreated": "2026-05-20",
     "dateUpdated": "2026-05-20",
     "category": "web-design",
     "tags": ["websites", "pequenos negócios", "SEO"],
     "image": "./assets/featured.png",
     "imageAlt": "Texto alt descritivo para acessibilidade",
     "readTime": 5,
     "featured": false,
     "published": true,
     "alternateLanguage": {
       "en": "your-post-slug-en"
     }
   }
   ```

9. **Create Portuguese image prompt:**
   Create `blog/posts/your-post-slug-pt/image-prompt.md`. Do not blindly translate the EN prompt; adapt visual cues to the Portuguese market when relevant (`.pt`, Portuguese local business context, PT examples).

10. **Add Portuguese images:**
   Place images in `blog/posts/your-post-slug-pt/assets/`

   Generate the PT featured image the same way (each language version has its own `assets/featured.png`):

   ```bash
   python3 scripts/blog_featured_image.py blog/posts/your-post-slug-pt/
   ```

#### Step 3: Update Index and Deploy

11. **Update posts index:**
   Add BOTH entries to `blog/posts/metadata.json`:
   ```json
   {
     "posts": [
       {
         "slug": "your-post-slug-en",
         "language": "en",
         "dateCreated": "2026-05-20",
         "dateUpdated": "2026-05-20"
       },
       {
         "slug": "your-post-slug-pt",
         "language": "pt",
         "dateCreated": "2026-05-20",
         "dateUpdated": "2026-05-20"
       }
     ]
   }
   ```

12. **Test locally:**
    - Open `blog/index.html` and verify both posts appear
    - Test language switcher works on post pages

13. **Commit and push:**
    ```bash
    git add blog/posts/your-post-slug-en/
    git add blog/posts/your-post-slug-pt/
    git add blog/posts/metadata.json
    git commit -m "Add bilingual blog post: Your Post Title (EN/PT)"
    git push
    ```

---

## 5. Metadata Specifications

### Post Metadata (`posts/[slug]/metadata.json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slug` | string | ✅ | URL-safe identifier (kebab-case) |
| `language` | string | ✅ | Language code: "en" or "pt" |
| `title` | string | ✅ | Post title (max 60 chars for SEO) |
| `description` | string | ✅ | Meta description (150-160 chars) |
| `author` | string | ✅ | Author name (default: "InfoWeb") |
| `dateCreated` | string | ✅ | ISO date format (YYYY-MM-DD) |
| `dateUpdated` | string | ✅ | ISO date format (YYYY-MM-DD) |
| `category` | string | ✅ | Main category |
| `tags` | array | ✅ | Array of tag strings |
| `image` | string | ✅ | Path to featured image (relative) |
| `imageAlt` | string | ✅ | Alt text for featured image |
| `readTime` | number | ✅ | Estimated read time in minutes |
| `featured` | boolean | ✅ | Show in featured section |
| `published` | boolean | ✅ | Publish status |
| `alternateLanguage` | object | ✅ | Cross-reference to translation (e.g., `{"pt": "slug-pt"}` or `{"en": "slug-en"}`) |

### Categories

**⚠️ IMPORTANT:** Categories use **keys** (not display names) and are automatically translated.

Use these category keys in your `metadata.json`:

| Category Key | English Display | Portuguese Display |
|--------------|-----------------|-------------------|
| `domains-hosting` | Domains & Hosting | Domínios & Hosting |
| `web-design` | Web Design | Web Design |
| `seo` | SEO | SEO |
| `digital-marketing` | Digital Marketing | Marketing Digital |
| `small-business` | Small Business | Pequenos Negócios |
| `tutorials` | Tutorials | Tutoriais |
| `case-studies` | Case Studies | Casos de Estudo |
| `company-news` | Company News | Notícias |

**Example in metadata.json:**
```json
{
  "category": "domains-hosting",
  ...
}
```

**Important:** 
- Always use the **key** (lowercase with hyphens), not the display name
- The blog system automatically shows the correct translation based on language
- Choose categories that accurately describe the post topic
- Don't default to one category for everything — use the most specific and relevant one

### Index Metadata (`posts/metadata.json`)

```json
{
  "posts": [
    {
      "slug": "post-slug-en",
      "language": "en",
      "dateCreated": "2026-05-20",
      "dateUpdated": "2026-05-20"
    },
    {
      "slug": "post-slug-pt",
      "language": "pt",
      "dateCreated": "2026-05-20",
      "dateUpdated": "2026-05-20"
    }
  ],
  "lastUpdated": "2026-05-20T10:00:00Z"
}
```

This file is used for:
- Quick indexing without reading every post
- Sorting by date
- Detecting new posts
- Language filtering

**⚠️ IMPORTANT:** Update this file every time you add/edit/delete a post! Include both EN and PT versions.

---

## 6. Content Guidelines

### Markdown Formatting

- Use `#` for main title (H1) — only one per post
- Use `##` for sections (H2)
- Use `###` for subsections (H3)
- Use `**bold**` for emphasis
- Use `*italic*` for secondary emphasis
- Use `` `code` `` for inline code
- Use triple backticks for code blocks
- Use `![Alt](./assets/image.jpg)` for images

### CTA Placement

Use the `{{CTA}}` placeholder in markdown:

```markdown
## Section content here...

{{CTA}}

## More content...
```

CTAs will be automatically replaced with a conversion component. Place them:
- After the introduction (1st occurrence)
- In the middle of the post (2nd occurrence)
- At the end of the post (3rd occurrence)

### Writing Guidelines

1. **Title:** Clear, benefit-driven, includes target keyword
2. **Introduction:** Hook + promise + what reader will learn
3. **Body:** Short paragraphs (2-4 sentences), use subheadings
4. **Conclusion:** Summarize + next steps + CTA
5. **Tone:** Professional but approachable, direct, avoid fluff
6. **Length:** Aim for 800-1500 words for SEO
7. **Keywords:** Use naturally, avoid keyword stuffing

### Image Guidelines

- **Featured image (social card):** Must be `assets/featured.png` at exactly **1200×630px**, optimized for web (<250KB). This filename is a contract — used by `metadata.json`, `index.html` OG tags, Twitter Card, and JSON-LD. If you change the filename or format, update all four places.
- **Always generate featured images:** After creating `metadata.json`, run `python3 scripts/blog_featured_image.py blog/posts/[slug]/` (or `python3 scripts/sync-blog-posts.py` to fill all missing). Do not commit a post without `assets/featured.png`.
- **Generator script:** `scripts/blog_featured_image.py` renders the standard InfoWeb navy/gold OG card with the post title. `image-prompt.md` remains useful for future AI art swaps but is not a substitute for committing `featured.png`.
- **In-body images:** WebP preferred (or JPG/PNG)
- **Size:** Max 1200px wide, optimize for web (<200KB)
- **Alt text:** Descriptive and accessible (must match `imageAlt` in metadata and `og:image:alt` / `twitter:image:alt` in `index.html`)
- **Naming:** `kebab-case-descriptive.webp` for in-body images; featured is always `featured.png`

---

## 7. SEO Requirements

Every blog post page must include:

### Meta Tags

```html
<title>Post Title — InfoWeb Blog</title>
<meta name="description" content="Post description 150-160 chars" />
<meta name="keywords" content="keyword1, keyword2, keyword3" />
<meta name="author" content="InfoWeb" />
<link rel="canonical" href="https://infoweb.sousadev.com/blog/posts/slug/" />
```

### Open Graph

```html
<meta property="og:type" content="article" />
<meta property="og:title" content="Post Title" />
<meta property="og:description" content="Post description" />
<meta property="og:image" content="https://infoweb.sousadev.com/blog/posts/slug/assets/featured.png" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Descriptive alt text from metadata imageAlt" />
<meta property="og:url" content="https://infoweb.sousadev.com/blog/posts/slug/" />
<meta property="article:published_time" content="2026-05-20T00:00:00Z" />
<meta property="article:modified_time" content="2026-05-20T00:00:00Z" />
<meta property="article:author" content="InfoWeb" />
<meta property="article:section" content="Web Design" />
<meta property="article:tag" content="websites" />
```

### Twitter Card

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Post Title" />
<meta name="twitter:description" content="Post description" />
<meta name="twitter:image" content="https://infoweb.sousadev.com/blog/posts/slug/assets/featured.png" />
<meta name="twitter:image:alt" content="Descriptive alt text from metadata imageAlt" />
```

### Structured Data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Post Title",
  "description": "Post description",
  "image": "https://infoweb.sousadev.com/blog/posts/slug/assets/featured.png",
  "author": {
    "@type": "Organization",
    "name": "InfoWeb"
  },
  "publisher": {
    "@type": "Organization",
    "name": "InfoWeb",
    "logo": {
      "@type": "ImageObject",
      "url": "https://infoweb.sousadev.com/assets/images/infoweb-logo.png"
    }
  },
  "datePublished": "2026-05-20",
  "dateModified": "2026-05-20",
  "mainEntityOfPage": "https://infoweb.sousadev.com/blog/posts/slug/"
}
</script>
```

---

## 8. CTA Integration

### CTA Placeholder

Use `{{CTA}}` on its own line in `content.md` (not inside a paragraph). **`post-loader.js` replaces placeholders in the raw markdown before `marked.parse()`**, so CTAs are not wrapped in invalid `<p><div>…</div></p>` markup.

Copy is chosen from [`blog/blog-i18n.js`](blog-i18n.js) using the post’s `metadata.language` field (`en` or `pt`).

| Placeholder | EN (example) | PT (example) |
|-------------|--------------|--------------|
| `{{CTA}}` / `{{CTA:default}}` | “Need a professional website?” → See plans | “Precisa de um website profissional?” → Ver planos |
| `{{CTA:tools}}` | Free tools CTA | Ferramentas grátis CTA |
| `{{CTA:contact}}` | Get in touch | Entrar em contacto |

Links use **relative paths** (`../../../#pricing`, `../../../free-tools/`) so they work on subdirectory deploys.

### CTA Variants

- `{{CTA}}` or `{{CTA:default}}` — Plans / pricing
- `{{CTA:tools}}` — Free tools hub
- `{{CTA:contact}}` — Email contact

To change CTA copy for all posts, edit `ctaTemplates` in `blog-i18n.js` only (do not hardcode HTML in markdown).

### Post page scripts (required order)

```html
<link rel="stylesheet" href="../../post.css" />
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="../../blog-i18n.js"></script>
<script src="../../post-loader.js"></script>
```

### Language persistence (blog index)

The blog index uses the same `localStorage` key as the main site: **`infoweb-language`** (default `en`). Switching language on the homepage carries over to `/blog/`.

---

## 9. Updating the Index

### Manual Update (Required)

Every time you add/edit/delete a post, update `posts/metadata.json`:

```json
{
  "posts": [
    {
      "slug": "new-post-slug",
      "dateCreated": "2026-05-20",
      "dateUpdated": "2026-05-20"
    }
  ],
  "lastUpdated": "2026-05-20T10:30:00Z"
}
```

### Automatic Indexing

The `blog/script.js` will:
1. Fetch `posts/metadata.json`
2. For each post, fetch `posts/[slug]/metadata.json`
3. Render post cards on `index.html`
4. Enable search and sort functionality

---

## 10. Technical Requirements

### Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile-responsive (Tailwind CSS)
- Progressive enhancement (works without JS for crawlers)

### Performance

- Lazy load images
- Minify assets for production
- Use CDN for external libraries
- Optimize images (WebP, compression)

### Accessibility

- Semantic HTML
- Alt text on all images
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance (WCAG AA)

### Analytics

All blog pages include Google Analytics:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "G-XXQSMBERJM");
</script>
<script src="../assets/js/analytics.js" defer></script>
```

Track events:
- `blog_post_view` — Post page view
- `blog_post_click` — Post card click from index
- `cta_click` — CTA button click
- `search_query` — Search term used

---

## 11. Launch Checklist

Before publishing a new post:

**English Version:**
- [ ] Slug is unique and SEO-friendly
- [ ] `content.md` has proper markdown formatting
- [ ] `metadata.json` has all required fields including `language: "en"` and `alternateLanguage`
- [ ] `image-prompt.md` exists and includes size, style, output filename, and avoid-list
- [ ] Featured image exists at `assets/featured.png`, 1200×630, and OG/Twitter/JSON-LD URLs match exactly
- [ ] Featured image was generated via `python3 scripts/blog_featured_image.py` (not missing, not a broken export)
- [ ] `og:image:width`, `og:image:height`, `og:image:alt`, and `twitter:image:alt` are set in `index.html`
- [ ] All images have alt text
- [ ] CTAs are placed strategically
- [ ] Content focuses on international market (.com domains, global examples)

**Portuguese Version:**
- [ ] Slug is unique and SEO-friendly (Portuguese naming)
- [ ] `content.md` is adapted (not just translated) for Portuguese market
- [ ] `metadata.json` has all required fields including `language: "pt"` and `alternateLanguage`
- [ ] `image-prompt.md` exists and includes size, style, output filename, and avoid-list
- [ ] Featured image exists at `assets/featured.png`, 1200×630, and OG/Twitter/JSON-LD URLs match exactly
- [ ] Featured image was generated via `python3 scripts/blog_featured_image.py` (not missing, not a broken export)
- [ ] `og:image:width`, `og:image:height`, `og:image:alt`, and `twitter:image:alt` are set in `index.html`
- [ ] All images have alt text
- [ ] CTAs are placed strategically
- [ ] Content focuses on Portuguese market (.pt domains, local examples)

**Both Versions:**
- [ ] `posts/metadata.json` is updated with BOTH posts
- [ ] Meta tags are complete
- [ ] Structured data is valid (test with [schema.org validator](https://validator.schema.org/))
- [ ] Both posts appear on `blog/index.html`
- [ ] Search functionality finds both posts
- [ ] Mobile rendering looks good
- [ ] All links work (internal and external)
- [ ] Analytics tracking works
- [ ] Sitemap is updated with both URLs
- [ ] Language switcher links between EN/PT versions
- [ ] CTA blocks show correct language; **button label is readable** (dark text on gold button)
- [ ] Post `index.html` links `../../post.css` and loads `blog-i18n.js` before `post-loader.js`

---

## Additional Resources

- [InfoWeb Main Site](https://infoweb.sousadev.com/)
- [Free Tools Hub](https://infoweb.sousadev.com/free-tools/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Schema.org BlogPosting](https://schema.org/BlogPosting)
- [Google Search Central](https://developers.google.com/search)

---

**Questions?** Contact the InfoWeb team at `info@sousadev.com`
