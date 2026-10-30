# AGENTS.md

Instructions for Codex when working with code in this repository.

## Overview

Personal portfolio site for Pavel Iskrinsky (frontend developer), hosted on GitHub Pages at https://paveliskrinsky.github.io. All site content is in Russian.

There is no build step, package manager, or test suite. The main page is a single `index.html` containing the HTML, an inline `<style>` block, and an inline `<script>` block with vanilla JS. `privacy.html` (privacy policy, linked from the form's consent checkbox and the footer) and `404.html` share `page.css`; `404.html` uses root-absolute paths because GitHub Pages serves it at any URL. `robots.txt` and `sitemap.xml` (update `lastmod` when content changes) sit at the root. Pushing to `main` deploys via GitHub Pages.

The only linter is html-validate, configured in `.htmlvalidate.json` (recommended rules, self-closing void elements):

```bash
npx html-validate index.html privacy.html 404.html
```

## Local preview

```bash
python -m http.server 8000
```

This is also configured as the `site` entry in `.claude/launch.json` for the preview tools.

## Architecture of `index.html`

The file is about 3,000 lines: the head scripts come first, then the `<style>` block (about 2,000 lines), the markup, and the main `<script>` at the end. Find the part you need with grep (by section id or class) instead of reading the whole file.

- **Head:** meta and SEO tags (Open Graph tags pointing to `img/og.jpg`; a schema.org `Person` JSON-LD block, so update it when the name, role or contacts change; a `FAQPage` JSON-LD block that must mirror the `#faq` questions and answers), favicons and the web manifest, a preload of the hero avatar for ≥641px only, and the Yandex.Metrika counter (id `113365152`; its `<noscript>` pixel sits at the start of `<body>`). Yandex Webmaster ownership is verified by the `<meta name="yandex-verification">` tag, not by an HTML file at the root, so keep the tag.
- **Fonts:** self-hosted in `fonts/` (Manrope for body text, Unbounded for headings via `--font-head`; variable woff2, cyrillic and latin subsets, `unbounded-cyrillic` preloaded for the h1). The `@font-face` rules open the `<style>` block, followed by `Manrope Fallback` and `Unbounded Fallback` faces on local Arial with metric overrides that keep the layout from shifting when the fonts swap in. `python tools/fonts.py` downloads the files from Google Fonts and prints all these rules. `page.css` and `_src/og.html` use the same files.
- **Theming:** CSS custom properties on `:root`. Every color token is written as `light-dark(<light>, <dark>)`, so add new colors as tokens there rather than hard-coding them. The tokens meet WCAG AA in both themes (axe reports 0 violations): body-size text uses `--text` or `--muted`, never the decorative accents; `--accent2-text` is the readable variant of `--accent2`; `.btn-primary` uses the `--btn-from`/`--btn-to` gradient, which keeps white text at 4.5:1 or higher. `:root` has `color-scheme: dark` by default; `@media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) }` and `:root[data-theme="light"]` switch it to `light`. The `#theme-toggle` button in the nav sets `data-theme` on `<html>` and saves it to `localStorage` (`theme`); an inline script in the head applies it before paint. Without a saved choice the OS theme is used. The dark `--bg` value (`#0f1117`) is also used in `<meta name="theme-color">` (JS swaps it to `#f6f6f9` in light mode) and in `site.webmanifest`, so keep them in sync.
- **Audience:** the site is aimed at clients ordering websites, not employers (reworked 2026-10-27). Copy talks about client benefits, the user works as самозанятый (договор и чек) and replies within a day. Prices, payment terms and warranty are deliberately not stated. Every claim and review must be real: reviews are quoted from freelance.ru, where the author name comes before each review.
- **Sections:** `#hero` (ends with the static `.clients` list «Работал с»), `#projects`, `#skills` («Чем могу помочь», «Услуги» in the nav), `#reviews`, `#process`, `#about` (includes a short `.career` list instead of a full experience section), `#faq` (`details.faq-item`), `#contact`, in that order on purpose (work first, then services). The nav links to every section except the hero. It switches to the burger at ≤1100px because seven links barely fit the 1060px nav. On ≤640px the hero photo becomes a 64px round avatar next to the badge (the `.hero-text` wrapper is `display: contents` there), own-project cards turn into rows with a small thumbnail, and only three reviews show until «Показать ещё» (`.review--extra`). Own projects and «Опыт» are `h3.section-tag` subheadings, and their cards use `h4`.
- **JS behaviors:**
  - the inline head script adds the `js` class to `<html>`. Styles that hide content until JS runs (`.reveal`, the collapsed reviews) are scoped to `.js`, so the page stays complete without JS and in print. `@media print` hides the nav, form and decor and prints link URLs, and a `beforeprint` handler opens every `details`.
  - the theme toggle, which also follows OS theme changes (`matchMedia` listener) when no `data-theme` is set
  - the mobile burger menu (`#burger` / `#nav-links`, with `aria-expanded`)
  - an `IntersectionObserver` that adds `.visible` to `.reveal` elements, so new content that should animate in needs the `reveal` class
  - the `.scrolled` class on `#nav` and `<body>` after 60px of scroll. The body class shows `.sticky-cta`, the fixed Telegram button on ≤860px, which sits inside `<main>` so that it is inside a landmark.
  - the cursor spotlight on `.card.spot` elements, through the `--mx` and `--my` custom properties, with the card's rect cached per hover and updates batched in `requestAnimationFrame`
  - the custom select (`.select[data-select]`): a styled listbox built over a native `<select>` that stays in the form and is kept in sync, including on form reset
  - the reviews «Показать ещё» button
  - Metrika goals through `goal()`: `lead` after a successful form submit, `form_error` on a failed one, `form_start` on the first input in the form, `telegram`, `email` and `freelance` on clicks of `t.me`, `mailto:` and freelance.ru links, `project` on clicks of external links in `#projects`, `faq` when a FAQ item opens, `reviews_more` on «Показать ещё». The goals must also exist in the Metrika UI as «Целевое событие» goals with the same identifiers.
  - the AJAX submit and status message for the contact form
- **Projects:** client work is a large `<article class="project">` with a browser-frame screenshot and a `dl.case` (Задача / Что сделал / Результат). `project--flip` alternates the side the image sits on, and the inline `--p-glow` sets the glow color. The user's own projects go below in the `.mini-projects` grid of `article.mini-project` cards.
- **Contact form:** posts to Formspree (`https://formspree.io/f/mqparwza`) with `fetch` and shows a Russian status message in `#form-status`, which stays in the DOM and only changes its text so screen readers announce it. Without JS it falls back to a plain POST. It has a hidden `_gotcha` honeypot and a required consent checkbox for personal data. It has no backend in this repo.

## Files that must stay at the repo root

- The icons (`favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`) and `site.webmanifest` are referenced by relative paths from the root. They are generated from `_src/logo.jpg` by `python tools/icons.py`: the photo in a circle with a gradient ring for `favicon.svg` (photo embedded as base64), `favicon.ico` and `icon-192/512`, and the plain square photo for `apple-touch-icon.png` and `icon-maskable-512.png`. Never edit them by hand.

## Images

Source images live in `_src/`, which GitHub Pages' Jekyll build does not publish. Optimized copies go to `img/`, and only `img/` is referenced from the page. Never edit the files in `img/` by hand.

- `_src/avatar.jpg` produces `img/avatar-{160,480,560,800}`, cropped to 3:4, with AVIF quality 45 because of the grainy background.
- `_src/logo.jpg` produces `img/logo-96` for the nav logo.
- `_src/projects/<name>.png` produces `img/projects/<name>-{520,640,1200}`.

Every size is written in `.avif`, `.webp` and `.jpg`. The page serves them through `<picture>` with an AVIF source, a WebP source and a JPG fallback, each with a `srcset`. Keep the `sizes` attributes in line with the real card widths when the layout changes.

```bash
python tools/images.py [avatar|logo|projects/<name> ...]
python tools/previews.py [--changed] [name ...]
```

`tools/images.py` rebuilds the optimized copies from `_src/` (requires Pillow with AVIF support). `tools/previews.py` takes new screenshots with local headless Edge (hard-coded path in `BROWSER`, 1440×2000 viewport cropped to 1800px height so the sites' cookie banners stay out of frame; the 4:5 ratio must stay taller than the card frame, which `object-fit: cover` fills from the top, otherwise the sides get cropped) into `_src/projects/` and then rebuilds them. To add a site, add it to `SITES` in that script. With no arguments, these scripts process everything. `--changed` reshoots every site first and rebuilds only those whose pixels differ from the saved screenshot (the comparison is exact, so sites with animations or rotating content always count as changed).

`python tools/og.py` renders `_src/og.html` (1200×630, uses `img/avatar-800.jpg` and the fonts in `fonts/`) with the same Edge into `_src/og.png` and `img/og.jpg`, the Open Graph image.

`python tools/pagespeed.py [name|url ...]` runs local Lighthouse (via `npx lighthouse@12` with the same Edge) on the `SITES` (imported together with `BROWSER` from `tools/previews.py`, and it needs Node.js) or on any URL such as `http://localhost:8000/`, and prints mobile/desktop scores. Locally the Metrika script dominates TBT, so for numbers comparable to the audit run `npx lighthouse@12` directly with `--blocked-url-patterns=*mc.yandex.ru*`. The PageSpeed Insights API is not used because it returns 429 without a key. Project cards show no scores or report links; they were removed at the owner's request.

## Conventions

- Decorative icons are hidden from screen readers with `aria-hidden="true"`. Keep doing this.
- Wrap every content `<img>` in `<picture>`. The one exception is the Yandex.Metrika tracking pixel inside `<noscript>` at the start of `<body>`. Leave it as a bare `<img>` exactly as Yandex provides it (an html-validate comment above it allows its inline style).
- `AGENTS.md` and `.claude/` are listed in `.gitignore`, so they are local only.
- `_PLAN.md` (in Russian) is the improvement plan from the 2026-10-29 page audit, with finished items checked off. The leading underscore keeps it out of the Jekyll build.
- `README.md` (in Russian) summarizes the site's sections. Update it when you add or remove sections or projects.
