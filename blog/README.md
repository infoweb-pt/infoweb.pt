# InfoWeb Blog System

Static blog system for InfoWeb.pt — SEO-optimized, searchable, sortable blog posts with markdown content.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Directory Structure](#2-directory-structure)
3. [Creating a New Blog Post](#3-creating-a-new-blog-post)
4. [Metadata Specifications](#4-metadata-specifications)
5. [Content Guidelines](#5-content-guidelines)
6. [SEO Requirements](#6-seo-requirements)
7. [CTA Integration](#7-cta-integration)
8. [Updating the Index](#8-updating-the-index)
9. [Technical Requirements](#9-technical-requirements)
10. [Launch Checklist](#10-launch-checklist)

---

## 1. Overview

The InfoWeb blog is a static, file-based blog system that:
- Stores posts as markdown files with JSON metadata
- Automatically indexes all posts from the filesystem
- Provides search and sort functionality
- Optimizes for SEO with proper meta tags and structured data
- Includes CTAs to drive conversions

**Live URL:** `https://infoweb.sousadev.com/blog/`

---

## 2. Directory Structure

```
blog/
├── index.html              ← Main blog listing page
├── README.md               ← This file
├── style.css               ← Blog-specific styles
├── script.js               ← Blog functionality (search, sort, load posts)
└── posts/
    ├── metadata.json       ← Index of all blog posts (MUST UPDATE)
    └── [slug]/             ← Individual post folder (kebab-case)
        ├── content.md      ← Markdown content
        ├── metadata.json   ← Post metadata
        └── assets/         ← Images and media for this post
            └── *.{jpg,png,webp,gif}
```

### Key Rules

1. **One folder per post** under `posts/[slug]/`
2. **Slug naming:** lowercase, kebab-case, SEO-friendly (e.g., `como-escolher-dominio-para-negocio`)
3. **All posts MUST be listed** in `posts/metadata.json` to appear on the index
4. **Asset paths** in markdown must be relative: `./assets/image.jpg`
5. **No server-side code** — everything runs in the browser

---

## 3. Creating a New Blog Post

### Step-by-Step

1. **Create post folder:**
   ```bash
   mkdir -p blog/posts/your-post-slug/assets
   ```

2. **Write content:**
   Create `blog/posts/your-post-slug/content.md`:
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

3. **Create post metadata:**
   Create `blog/posts/your-post-slug/metadata.json`:
   ```json
   {
     "slug": "your-post-slug",
     "title": "Your Post Title",
     "description": "Brief description (150-160 characters for SEO)",
     "author": "InfoWeb",
     "dateCreated": "2026-05-20",
     "dateUpdated": "2026-05-20",
     "category": "Web Design",
     "tags": ["websites", "small business", "SEO"],
     "image": "./assets/featured.jpg",
     "imageAlt": "Descriptive alt text for accessibility",
     "readTime": 5,
     "featured": false,
     "published": true
   }
   ```

4. **Add images:**
   Place all images in `blog/posts/your-post-slug/assets/`

5. **Update posts index:**
   Add entry to `blog/posts/metadata.json`:
   ```json
   {
     "posts": [
       {
         "slug": "your-post-slug",
         "dateCreated": "2026-05-20",
         "dateUpdated": "2026-05-20"
       }
     ]
   }
   ```

6. **Test locally:**
   Open `blog/index.html` in browser and verify post appears

7. **Commit and push:**
   ```bash
   git add blog/posts/your-post-slug/
   git add blog/posts/metadata.json
   git commit -m "Add blog post: Your Post Title"
   git push
   ```

---

## 4. Metadata Specifications

### Post Metadata (`posts/[slug]/metadata.json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slug` | string | ✅ | URL-safe identifier (kebab-case) |
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

### Categories

Standard categories (keep consistent):
- `Web Design`
- `SEO`
- `Digital Marketing`
- `Small Business`
- `Tutorials`
- `Case Studies`
- `Company News`

### Index Metadata (`posts/metadata.json`)

```json
{
  "posts": [
    {
      "slug": "post-slug",
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

**⚠️ IMPORTANT:** Update this file every time you add/edit/delete a post!

---

## 5. Content Guidelines

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

- **Format:** WebP preferred (or JPG/PNG)
- **Size:** Max 1200px wide, optimize for web (<200KB)
- **Featured image:** 1200x630px for social sharing
- **Alt text:** Descriptive and accessible
- **Naming:** `kebab-case-descriptive.webp`

---

## 6. SEO Requirements

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
<meta property="og:image" content="https://infoweb.sousadev.com/blog/posts/slug/assets/featured.jpg" />
<meta property="og:url" content="https://infoweb.sousadev.com/blog/posts/slug/" />
<meta property="article:published_time" content="2026-05-20T00:00:00Z" />
<meta property="article:modified_time" content="2026-05-20T00:00:00Z" />
<meta property="article:author" content="InfoWeb" />
<meta property="article:section" content="Web Design" />
<meta property="article:tag" content="websites" />
```

### Structured Data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Post Title",
  "description": "Post description",
  "image": "https://infoweb.sousadev.com/blog/posts/slug/assets/featured.jpg",
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

## 7. CTA Integration

### CTA Placeholder

Use `{{CTA}}` in markdown. The blog script will replace it with:

```html
<div class="cta-block">
  <div class="cta-content">
    <h3>Precisa de um website profissional?</h3>
    <p>InfoWeb cria e gere o seu site. Domínio, hosting, manutenção incluídos.</p>
    <a href="/#pricing" class="cta-button" data-track="cta_click" data-track-location="blog_post" data-track-target="/#pricing">
      Ver Planos →
    </a>
  </div>
</div>
```

### CTA Variants

You can customize CTAs by using:
- `{{CTA:default}}` — Standard CTA (default)
- `{{CTA:tools}}` — Link to free tools
- `{{CTA:contact}}` — Contact form CTA

---

## 8. Updating the Index

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

## 9. Technical Requirements

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

## 10. Launch Checklist

Before publishing a new post:

- [ ] Slug is unique and SEO-friendly
- [ ] `content.md` has proper markdown formatting
- [ ] `metadata.json` has all required fields
- [ ] Featured image exists and is optimized
- [ ] All images have alt text
- [ ] CTAs are placed strategically
- [ ] `posts/metadata.json` is updated
- [ ] Meta tags are complete
- [ ] Structured data is valid (test with [schema.org validator](https://validator.schema.org/))
- [ ] Post appears on `blog/index.html`
- [ ] Search functionality finds the post
- [ ] Mobile rendering looks good
- [ ] All links work (internal and external)
- [ ] Analytics tracking works
- [ ] Sitemap is updated (if using `sitemap.xml`)

---

## Additional Resources

- [InfoWeb Main Site](https://infoweb.sousadev.com/)
- [Free Tools Hub](https://infoweb.sousadev.com/free-tools/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Schema.org BlogPosting](https://schema.org/BlogPosting)
- [Google Search Central](https://developers.google.com/search)

---

**Questions?** Contact the InfoWeb team at `info@sousadev.com`
