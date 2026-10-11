# Architecture

The deployed artifact is plain HTML, CSS, native JavaScript modules, local media, and JSON. Every main section and all 29 editorial records have an actual static HTML URL. Content is present in Arabic before JavaScript runs, including navigation, descriptions, highlights, facts, and source links. There is no router, rewrite requirement, API, database, tracking script, or site-side authentication.

`tools/build_pages.py` is an optional standard-library editorial generator. It centralizes header, footer, cards, page templates, SEO, and sitemap, avoiding independently maintained copies. Generated pages are committed; GitHub Pages serves them directly without a build step. JSON is the content source of truth. Regenerate after changing content or templates.

`assets/data/translations.json` contains UI text; three content files contain bilingual records; `quizzes.json` contains questions, options, answers, explanations, and sources. `media.json` records exact source, creator, license, archival date, and local sizes. Photos are served locally. SVG illustrations are interpretive. Fonts use `font-display: swap` and local WOFF2 subsets.

Runtime modules:

| Module | Responsibility |
| --- | --- |
| `boot.js` | Guarded, early theme, preferred text direction and font selection before CSS paint |
| `main.js` | Load local data, start interactions, preserve static content on loading failure |
| `i18n.js` | Translation hooks, language preference, document direction, titles and share metadata |
| `theme.js` | Theme switching and accessible action label |
| `storage.js` | Guarded JSON storage with in-page memory fallback |
| `search.js` | Arabic normalization, bilingual matching, category filtering, and empty states |
| `favorites.js` | Validate saved IDs, update buttons/count, collection and cross-tab synchronization |
| `quiz.js` | Deterministic question state, answer locking, scoring, replay and best scores |
| `modal.js` | Native dialog, keyboard boundary handling, Escape, and focus restoration |
| `cards.js`, `dom.js` | Safe DOM construction and local image fallback |

Search covers both languages regardless of the selected display language. Multiple normalized words must all match the record. Catalog pages filter by editorial category; global search filters by content kind. All IDs and routes originate in maintained content, rather than user input. Dynamic content uses `textContent`, attribute setters, and element construction. There is no dynamic HTML injection.

LocalStorage uses namespaced keys: `syria.language`, `syria.theme`, `syria.favorites`, and `syria.score.<quiz-id>`. Values are JSON. Browser storage may be blocked or cleared; interaction remains functional on the current page, with a visible persistence notice. Favorites synchronize with storage changes from other tabs.

The language switch updates static hooks and dynamic views, preserves active quiz state, and updates `lang`, `dir`, title, description, Open Graph, and Twitter metadata. Arabic is the canonical static edition. `?lang=en` is a client-side display preference, not a separately indexed English edition. No misleading `hreflang` alternate is advertised. Search, favorites, and 404 pages are `noindex`. SEO discovery depends on actual crawl/hosting conditions, not a promised ranking.

The optional page generator combines font definitions and base → components → responsive CSS into a committed `site.css` file, reducing blocking requests while retaining modular source files. Layouts use logical properties and ordinary flow, so RTL/LTR mirror cleanly. Motion is limited to short transitions and an initial hero entry; reduced-motion preferences disable them. Native dialog semantics provide background inertness; explicit Tab boundaries keep focus within content and restore the opener on close.

The meta CSP restricts scripts, styles, fonts, JSON, and images to this origin; objects and inline executable scripts are disabled. JSON-LD is inert structured data. GitHub Pages does not offer custom HTTP response headers through repository files. For header-based policies, use a hosting provider or proxy with that capability; do not claim that a `_headers` file configures GitHub Pages. Production must use HTTPS. No credentials belong in static files.

Limitations: preferences are per browser/origin; there is no synchronization between devices. Interactive features need JavaScript. Content and photos are cultural introductions, not live travel/access information. No claim of complete WCAG certification is made; see QA evidence and outstanding manual checks.
