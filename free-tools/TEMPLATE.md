# Free Tool Marketing — Standard Requirements & Template

> **How to use this file:** Copy this document every time you start a new free tool. Fill in the placeholders (marked with `[BRACKETS]`), follow every checklist item, and delete this intro block before publishing.

---

## Table of Contents

1. [Concept Brief](#1-concept-brief)
2. [Folder & File Structure](#2-folder--file-structure)
3. [SEO & Meta Tags Template](#3-seo--meta-tags-template)
4. [Technical Requirements](#4-technical-requirements)
5. [UI / UX Page Structure](#5-ui--ux-page-structure)
6. [HTML Page Skeleton](#6-html-page-skeleton)
7. [Marketing Funnel & Conversion](#7-marketing-funnel--conversion)
8. [Analytics & Tracking](#8-analytics--tracking)
9. [Launch QA Checklist](#9-launch-qa-checklist)

---

## 1. Concept Brief

Fill this section before writing a single line of code.

| Field | Value |
|---|---|
| **Tool name** | `[e.g. WhatsApp Link Generator]` |
| **URL slug** | `[e.g. whatsapp-link-generator]` |
| **Full URL** | `https://[YOUR-GITHUB-USERNAME].github.io/[REPO]/[slug]/` |
| **Target persona** | `[e.g. Restaurant owners, local clinics, freelancers]` |
| **Primary keyword** | `[e.g. "free whatsapp link generator"]` |
| **Secondary keywords** | `[e.g. "whatsapp click to chat link", "create whatsapp link free"]` |
| **Search intent** | `[ ] Informational  [ ] Navigational  [x] Transactional / Tool` |
| **Value delivered** | `[One sentence — what problem does it solve instantly?]` |
| **Gating strategy** | `[ ] Open Access (CTA after result)  [ ] Lead Capture (email for full report)` |
| **UTM medium** | `[e.g. whatsapp_link_generator]` |
| **Estimated build time** | `[e.g. 3 hours]` |

---

## 2. Folder & File Structure

Every tool lives in its **own subfolder** under the `free-tools/` directory so it is accessible at `/<repo>/free-tools/[slug]/`.

```
free-tools/
└── [slug]/                   ← one folder per tool
    ├── index.html            ← the tool page (required)
    ├── style.css             ← tool-specific styles (optional)
    ├── script.js             ← tool logic (optional, can be inline)
    └── og-image.png          ← 1200×630 px Open Graph image (required)
```

**Rules:**
- The `index.html` must be self-contained or reference only relative paths and CDN links.
- No server-side code. Everything runs in the browser.
- The `og-image.png` must clearly show the tool name and brand for WhatsApp / social previews.
- Do **not** commit API keys. All sensitive calls go through the Django API hosted at **`https://infoweb.api.sousadev.com`**.

---

## 3. SEO & Meta Tags Template

Copy this `<head>` block into every tool's `index.html`. Replace every `[PLACEHOLDER]`.

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- ═══════════════════════════════════════════
       PRIMARY SEO
  ═══════════════════════════════════════════ -->
  <title>[Primary Keyword] — Free Tool by InfoWeb</title>
  <!-- Keep title under 60 characters. Lead with the keyword. -->

  <meta name="description"
    content="[150–160 char description. State the benefit + action. E.g.: Generate a free WhatsApp click-to-chat link in seconds. No sign-up needed. Perfect for restaurants, clinics and freelancers.]" />

  <meta name="keywords"
    content="[primary keyword], [secondary keyword 1], [secondary keyword 2], [brand name], free tool" />
  <!-- Keywords still help Bing/Yahoo; do not skip. -->

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="author" content="InfoWeb by Sousa Dev" />
  <link rel="canonical" href="https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/" />

  <!-- ═══════════════════════════════════════════
       OPEN GRAPH (Facebook, WhatsApp, LinkedIn)
  ═══════════════════════════════════════════ -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="InfoWeb" />
  <meta property="og:url" content="https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/" />
  <meta property="og:title" content="[Tool Name] — Free Tool by InfoWeb" />
  <meta property="og:description"
    content="[Same as meta description, or a slightly punchier version. Max 200 chars.]" />
  <meta property="og:image" content="https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="en_GB" />

  <!-- ═══════════════════════════════════════════
       TWITTER / X CARD
  ═══════════════════════════════════════════ -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="[Tool Name] — Free Tool by InfoWeb" />
  <meta name="twitter:description" content="[Same as OG description.]" />
  <meta name="twitter:image" content="https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/og-image.png" />

  <!-- ═══════════════════════════════════════════
       STRUCTURED DATA — WebApplication (JSON-LD)
  ═══════════════════════════════════════════ -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "[Tool Name]",
    "url": "https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/",
    "description": "[Same as meta description.]",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Any",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "EUR"
    },
    "author": {
      "@type": "Organization",
      "name": "InfoWeb",
      "url": "https://infoweb.sousadev.com"
    }
  }
  </script>

  <!-- ═══════════════════════════════════════════
       FAVICON
  ═══════════════════════════════════════════ -->
  <link rel="icon" type="image/png" href="https://[GITHUB-USER].github.io/[REPO]/favicon_io/favicon-32x32.png" />
  <link rel="apple-touch-icon" href="https://[GITHUB-USER].github.io/[REPO]/favicon_io/apple-touch-icon.png" />

  <!-- ═══════════════════════════════════════════
       PERFORMANCE HINTS
  ═══════════════════════════════════════════ -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <!-- Add preconnect for any CDN you depend on (Tailwind, etc.) -->

  <!-- Styles -->
  <link rel="stylesheet" href="style.css" />
</head>
```

---

## 4. Technical Requirements

### 4.1 Environment Constraints (GitHub Pages)

| Rule | Detail |
|---|---|
| **Static only** | Pure HTML + CSS + JS. No PHP, no Node, no server rendering. |
| **Client-side first** | All calculations, validations and data transformations happen in the browser. Only reach the Django API when strictly necessary (external data, AI, DB reads). |
| **No exposed keys** | Sensitive API keys (OpenAI, DB credentials, etc.) live exclusively in the API backend (`api/`). Never in source files on GitHub Pages. |
| **CORS** | The Django API (`https://infoweb.api.sousadev.com`) must allow browser `fetch()` from your GitHub Pages origin `https://[GITHUB-USER].github.io`. In production set `CORS_ALLOWED_ORIGINS` on the API; avoid `CORS_ALLOW_ALL_ORIGINS` except local dev. |
| **Paths** | Use **relative** paths for local assets. Use absolute URLs for GitHub-hosted static pages + the Django API (see §4.1b). CDN libraries stay as absolute URLs. |

### 4.1b Django API URL (lead capture)

- **Production base:** `https://infoweb.api.sousadev.com`
- **Path pattern:** `https://infoweb.api.sousadev.com/leads/[endpoint]/` — there is **no** `/api` prefix before `leads/`.
- In each tool's `script.js`, set `API_ENDPOINT` to the **full HTTPS URL above** when shipping to GitHub Pages (browser `fetch` is cross-origin; relative URLs like `/api/...` hit the Pages host, not Django).
- **Local:** `http://localhost:8001/leads/[endpoint]/` with `python manage.py runserver 8001` from `api/`.

### 4.2 Loading States (Mandatory)

Any action that triggers an async call **must** show a loading indicator before the result appears.

```html
<!-- Spinner example -->
<div id="spinner" class="hidden" aria-live="polite" aria-label="Loading...">
  <svg class="animate-spin h-6 w-6 text-blue-600" ...></svg>
  <span>Generating your result…</span>
</div>
```

```js
// Pattern to follow for every async call
async function runTool() {
  showSpinner();
  try {
    const result = await fetchFromApi(payload);
    renderResult(result);
    trackEvent('tool_used');
  } catch (err) {
    showFriendlyError();   // Never expose raw error messages to users
  } finally {
    hideSpinner();
  }
}
```

### 4.3 Error Handling Rules

- **Never** show raw `console.error` or HTTP status codes to the user.
- Always display a friendly message: *"Something went wrong. Please try again in a moment."*
- Log the error to the console for debugging only.
- Provide a visible **"Try again"** button that re-runs the last action.

---

## 5. UI / UX Page Structure

Every tool page follows this exact vertical layout, top to bottom:

```
┌─────────────────────────────────────────┐
│  HEADER (minimal)                       │
│  Logo  |  "See Website Plans" button    │
├─────────────────────────────────────────┤
│  HERO SECTION                           │
│  H1: Benefit-focused headline           │
│  Subtitle: Short explanation            │
├─────────────────────────────────────────┤
│  TOOL AREA — INPUT                      │
│  Short form / inputs                    │
│  Real-time validation                   │
│  Primary CTA button: "Generate / Run"   │
├─────────────────────────────────────────┤
│  TOOL AREA — OUTPUT (visually distinct) │
│  Result box with contrasting background │
│  Copy / Download / Share button         │
│  [Loading spinner replaces this area    │
│   while result is being generated]      │
├─────────────────────────────────────────┤
│  CONVERSION CTA                         │
│  Bridge sentence + big CTA button       │
│  pointing to InfoWeb plans (UTM link)   │
├─────────────────────────────────────────┤
│  SOCIAL PROOF (micro)                   │
│  "Built by InfoWeb · X local businesses │
│   already growing online."              │
├─────────────────────────────────────────┤
│  FAQ (SEO — at least 4 questions)       │
│  Accordion or simple Q&A                │
│  Targets long-tail keywords             │
├─────────────────────────────────────────┤
│  FOOTER (minimal)                       │
│  © InfoWeb · Privacy · Back to tools   │
└─────────────────────────────────────────┘
```

### Design Tokens (keep consistent across all tools)

| Token | Value |
|---|---|
| Primary colour | Match InfoWeb brand (`#020617` dark / accent from main site) |
| Font | Same as main site (Instrument Sans or fallback system-ui) |
| Border radius | `0.75rem` (cards), `0.5rem` (inputs) |
| Max content width | `640px` centred (single-column, mobile-first) |
| Output box background | Light neutral or subtle brand tint — visually different from page bg |

---

## 6. HTML Page Skeleton

Copy this skeleton into `free-tools/[slug]/index.html` and build from here.

```html
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <!-- ▶ Paste the full <head> from Section 3 here ◀ -->
</head>
<body class="bg-slate-950 text-white font-sans antialiased">

  <!-- ══════════ HEADER ══════════ -->
  <header class="sticky top-0 z-50 bg-slate-950/80 backdrop-blur border-b border-slate-800">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=[SLUG]_header"
         target="_blank" rel="noopener" aria-label="InfoWeb homepage">
        <img src="[PATH_TO_LOGO]" alt="InfoWeb" class="h-8 w-auto" />
      </a>
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=[SLUG]_header_btn#pricing"
         target="_blank" rel="noopener"
         class="text-sm font-medium border border-slate-600 rounded-full px-4 py-1.5 hover:border-white transition"
         onclick="trackEvent('header_cta_click')">
        See Website Plans
      </a>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 py-12">

    <!-- ══════════ HERO ══════════ -->
    <section class="text-center mb-10">
      <h1 class="text-3xl md:text-4xl font-bold leading-tight mb-3">
        [Benefit-focused headline — e.g. "Generate Your WhatsApp Link in 5 Seconds"]
      </h1>
      <p class="text-slate-400 text-lg">
        [Short subtitle — max 20 words. What does it do and who is it for?]
      </p>
    </section>

    <!-- ══════════ TOOL: INPUT ══════════ -->
    <section aria-labelledby="tool-input-heading" class="mb-6">
      <h2 id="tool-input-heading" class="sr-only">Tool Input</h2>
      <div class="bg-slate-900 rounded-xl p-6 space-y-4">

        <!-- Add your form fields here -->
        <div>
          <label for="field1" class="block text-sm font-medium text-slate-300 mb-1">
            [Label]
          </label>
          <input
            id="field1" type="text"
            placeholder="[Helpful placeholder]"
            class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white
                   placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-describedby="field1-hint" />
          <p id="field1-hint" class="text-xs text-slate-500 mt-1">[Optional inline hint]</p>
          <p id="field1-error" class="text-xs text-red-400 mt-1 hidden" role="alert">
            [Validation error message]
          </p>
        </div>

        <button id="btn-generate" type="button"
          onclick="runTool()"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg
                 px-6 py-3 transition focus:outline-none focus:ring-2 focus:ring-blue-400">
          [Generate / Calculate / Run] — It's Free
        </button>

      </div>
    </section>

    <!-- ══════════ TOOL: OUTPUT ══════════ -->
    <section aria-labelledby="tool-output-heading" class="mb-10" id="output-section">
      <h2 id="tool-output-heading" class="sr-only">Your Result</h2>

      <!-- Loading spinner (hidden by default) -->
      <div id="spinner" class="hidden flex-col items-center justify-center py-10 text-slate-400" aria-live="polite">
        <svg class="animate-spin h-8 w-8 mb-3 text-blue-500" xmlns="http://www.w3.org/2000/svg"
             fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        <span>Generating your result…</span>
      </div>

      <!-- Error state (hidden by default) -->
      <div id="error-box" class="hidden bg-red-900/30 border border-red-700 rounded-xl p-5 text-center" role="alert">
        <p class="text-red-300 mb-3">Something went wrong. Please try again in a moment.</p>
        <button onclick="runTool()"
          class="text-sm underline text-red-400 hover:text-red-200">Try again</button>
      </div>

      <!-- Result box (hidden until result is ready) -->
      <div id="result-box" class="hidden bg-slate-800 border border-slate-700 rounded-xl p-6">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-3">Your Result</p>

        <!-- Render dynamic content here -->
        <div id="result-content" class="text-lg font-mono break-all text-white mb-4"></div>

        <button onclick="copyResult()"
          class="flex items-center gap-2 text-sm border border-slate-600 rounded-lg px-4 py-2
                 hover:border-white transition text-slate-300 hover:text-white">
          <svg class="h-4 w-4" ...></svg> Copy to clipboard
        </button>
      </div>
    </section>

    <!-- ══════════ CONVERSION CTA ══════════ -->
    <section aria-label="Call to action" class="mb-12 text-center bg-slate-900 rounded-2xl p-8">
      <p class="text-slate-400 mb-2 text-sm uppercase tracking-widest">Liked how easy that was?</p>
      <h2 class="text-2xl font-bold mb-3">
        Your business website can work just as smoothly.
      </h2>
      <p class="text-slate-400 mb-6">
        InfoWeb builds, hosts and maintains your site for a flat monthly rate.
        No agencies, no tech headaches.
      </p>
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=[SLUG]_cta#pricing"
         target="_blank" rel="noopener"
         class="inline-block bg-white text-slate-950 font-bold rounded-full px-8 py-3
                hover:bg-slate-200 transition text-base"
         onclick="trackEvent('cta_click')">
        See Website Plans →
      </a>
    </section>

    <!-- ══════════ FAQ (SEO) ══════════ -->
    <section aria-labelledby="faq-heading" class="mb-12">
      <h2 id="faq-heading" class="text-2xl font-bold mb-6">Frequently Asked Questions</h2>

      <!-- Repeat this block for each Q&A. Minimum 4 questions. -->
      <details class="border border-slate-800 rounded-xl mb-3 group">
        <summary class="px-5 py-4 cursor-pointer font-medium list-none flex justify-between items-center">
          [Question targeting a long-tail keyword]
          <span class="ml-4 text-slate-500 group-open:rotate-180 transition-transform">▾</span>
        </summary>
        <p class="px-5 pb-4 text-slate-400 leading-relaxed">
          [Answer — 2–4 sentences. Natural language. Include keywords naturally.]
        </p>
      </details>

      <!-- FAQ Schema — add one entry per question -->
      <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "[Question text exactly as shown in the accordion]",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "[Answer text.]"
            }
          }
        ]
      }
      </script>
    </section>

    <!-- ══════════ MICRO SOCIAL PROOF ══════════ -->
    <section class="text-center text-slate-500 text-sm mb-8">
      <p>
        Built by <a href="https://infoweb.sousadev.com" target="_blank" rel="noopener"
          class="underline hover:text-white">InfoWeb</a> ·
        Helping local businesses grow online since 2024.
      </p>
    </section>

  </main>

  <!-- ══════════ FOOTER ══════════ -->
  <footer class="border-t border-slate-800 py-6">
    <div class="max-w-2xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center
                gap-3 text-xs text-slate-600">
      <span>© <span id="year"></span> InfoWeb by Sousa Dev</span>
      <nav class="flex gap-4">
        <a href="https://infoweb.sousadev.com" target="_blank" rel="noopener"
           class="hover:text-white transition">Main site</a>
        <a href="../" class="hover:text-white transition">All free tools</a>
      </nav>
    </div>
  </footer>

  <!-- ══════════ SCRIPTS ══════════ -->
  <script src="script.js" defer></script>
  <script>
    // Auto-update copyright year
    document.getElementById('year').textContent = new Date().getFullYear();
  </script>

</body>
</html>
```

---

## 7. Marketing Funnel & Conversion

### 7.1 The 80% Free Value Rule

Deliver **at least 80% of the promised value with zero friction** (no sign-up, no email, no paywall).  
Trust is built before you ask for anything. The remaining 20% (e.g. PDF export, advanced options, email report) can be gated.

### 7.2 Gating Options

| Option | When to use | Implementation |
|---|---|---|
| **A — Open Access** | Most tools (lower friction, higher volume) | Show CTA immediately below result |
| **B — Lead Capture** | High-value reports / analysis tools | Show partial result → ask email → send full breakdown via Django API |

#### Option B — Email gate pattern

```html
<!-- Show this INSTEAD of the full result-box when using lead capture -->
<div id="gate-box" class="hidden bg-slate-800 rounded-xl p-6 text-center">
  <p class="font-semibold mb-1">Your report is ready!</p>
  <p class="text-slate-400 text-sm mb-4">
    Enter your email and we'll send you the full breakdown instantly.
  </p>
  <input id="gate-email" type="email" placeholder="your@email.com"
    class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2.5 mb-3 text-white" />
  <button onclick="submitEmail()" class="w-full bg-blue-600 hover:bg-blue-500 ...">
    Send me the report
  </button>
</div>
```

### 7.3 CTA Formula

Place the CTA section **immediately after** the output area, always visible after a result is generated.

> **Template:**  
> *"Liked how easy that was? Your business website can work just as smoothly."*  
> **→ [See Website Plans]** `(opens in new tab, with UTM params)`

### 7.4 UTM Link Formula

All links from a free tool to the main InfoWeb site **must** include UTM parameters:

```
https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=[SLUG]&utm_campaign=[SECTION]#pricing
```

| Parameter | Value |
|---|---|
| `utm_source` | Always `freetool` |
| `utm_medium` | Tool slug (e.g. `whatsapp_generator`) |
| `utm_campaign` | Section (e.g. `header_btn`, `cta`, `footer`) |

---

## 8. Analytics & Tracking

### 8.1 Events to fire (Google Analytics 4)

Add `gtag.js` to the `<head>` and fire these events at the appropriate moments:

```js
// Fires when user clicks the main action button
function trackEvent(eventName, params = {}) {
  if (typeof gtag !== 'undefined') {
    gtag('event', eventName, {
      tool_name: '[SLUG]',  // e.g. 'whatsapp_generator'
      ...params
    });
  }
}
```

| Moment | Event name | When to call |
|---|---|---|
| User clicks Generate / Calculate | `tool_used` | Inside `runTool()` before the API call |
| Result is shown successfully | `tool_result_shown` | Inside `renderResult()` |
| User clicks the CTA button | `cta_click` | `onclick` on the CTA anchor |
| User copies the result | `result_copied` | Inside `copyResult()` |
| User submits email (Option B) | `lead_submitted` | Inside `submitEmail()` after success |

### 8.2 Google Analytics Setup

Paste this block in `index.html` `<head>` (before `</head>`). Use measurement ID **`G-XXQSMBERJM`** — do not swap for a placeholder.

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XXQSMBERJM');
</script>
```

Before publishing, run **`bash scripts/check-html-ga.sh`** from the repo root so no tool ships without GA.

---

## 9. Launch QA Checklist

Complete **every item** before pushing to GitHub Pages.

### SEO & Meta
- [ ] `<title>` is under 60 characters and starts with the primary keyword
- [ ] `<meta name="description">` is 150–160 characters with a clear benefit
- [ ] Canonical URL is correct and matches the final published URL
- [ ] Open Graph tags are filled in (title, description, image URL)
- [ ] `og:image` is a 1200×630 px PNG/JPG saved as `og-image.png` in the tool folder
- [ ] `WebApplication` JSON-LD schema is present and valid (test at [schema.org/validator](https://validator.schema.org))
- [ ] FAQ JSON-LD schema is present with at least 4 questions
- [ ] Favicon links point to the correct shared favicon path

### Functionality
- [ ] Tool produces the correct output for valid input
- [ ] Real-time validation shows errors **before** the user clicks Generate
- [ ] Loading spinner appears for **every** async operation
- [ ] Friendly error message appears when the API fails (no raw errors shown)
- [ ] "Try again" button successfully re-runs the tool
- [ ] Copy-to-clipboard works on mobile browsers (test on iOS Safari)
- [ ] All links open in a new tab (`target="_blank" rel="noopener"`)

### Conversion
- [ ] CTA button uses the correct UTM parameters
- [ ] CTA button opens InfoWeb pricing page in a new tab
- [ ] Lead-capture email field validates format before submitting (Option B tools only)
- [ ] `trackEvent('tool_used')` fires on Generate click
- [ ] `trackEvent('cta_click')` fires on CTA click

### Analytics
- [ ] Google tag (gtag.js) is in `<head>` with measurement ID **`G-XXQSMBERJM`** (loader URL and `gtag('config', …)` must match)
- [ ] `bash scripts/check-html-ga.sh` passes from repo root (covers this tool and the rest of the site)

### Design & Accessibility
- [ ] Page is fully responsive — tested at 375px, 768px and 1280px widths
- [ ] Colour contrast ratio is ≥ 4.5:1 for all body text (use [Contrast Checker](https://webaim.org/resources/contrastchecker/))
- [ ] All images have descriptive `alt` attributes
- [ ] All form inputs have associated `<label>` elements or `aria-label`
- [ ] Error messages use `role="alert"` so screen readers announce them
- [ ] Page can be navigated fully with keyboard (Tab, Enter, Space)

### Performance
- [ ] Lighthouse Performance score ≥ 90 on mobile (test in Chrome DevTools)
- [ ] No render-blocking scripts (use `defer` or `async` on all `<script>` tags)
- [ ] Images are compressed (use WebP where possible)
- [ ] No sensitive API keys visible in page source or JS files

### Final
- [ ] Tool URL works when accessed directly: `https://[GITHUB-USER].github.io/[REPO]/free-tools/[slug]/`
- [ ] Shared via WhatsApp — preview shows the correct OG image, title and description
- [ ] Added a link to the new tool in the main `free-tools/` index page (or InfoWeb nav)
- [ ] Announced via InfoWeb social channels / newsletter

---

*Template version 1.0 — InfoWeb by Sousa Dev*
