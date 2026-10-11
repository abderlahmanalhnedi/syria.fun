# Syria.fun — سوريا.fun

An independent bilingual guide to Syrian places, food, and living culture. Arabic is the default; English, RTL/LTR, light/dark themes, search, favorites, and four short quizzes are implemented. A lightweight static website for [syria.fun](https://syria.fun), maintained in [GitHub](https://github.com/abderlahmanalhnedi/syria.fun).

مساحة مستقلة للتعرّف إلى مدن سوريا ومطبخها وثقافتها. العربية هي اللغة الافتراضية، مع الإنجليزية واتجاهي RTL/LTR والمظهرين الفاتح والداكن والبحث والمفضلة وأربع جولات أسئلة. لا حسابات، ولا خدمات خلفية، ولا تتبّع مضاف من المشروع.

## Local preview / المعاينة المحلية

From the repository directory, with Python 3 installed:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Open **http://127.0.0.1:8000/**. Stop with `Ctrl+C`. An editor's static HTTP server also works. Use HTTP rather than opening `index.html` as a `file://` URL: native modules and JSON loading require a web origin.

من مجلد المشروع، شغّل الأمر أعلاه وافتح الرابط المحلي. أوقف الخادم عبر `Ctrl+C`. فتح HTML مباشرةً من القرص لا يفعّل الوحدات والبيانات بصورة موثوقة.

## Implemented / الميزات المنفذة

- 39 static HTML pages: home, explore, food, culture, quiz, favorites, about, global search, image credits, 404, and 29 detail pages.
- 10 places, 10 dishes, and 9 cultural stories, with Arabic and English descriptions, highlights, facts, and source links.
- Search-as-you-type across names, landmarks, descriptions, and culture; Arabic diacritic and letter normalization; category filters and reset.
- 4 quizzes with 5 bilingual questions each, immediate explanations, correct scoring, progress, replay, and locally stored best scores.
- Favorites for all content, a dedicated collection, empty state, count, and persistence.
- Native accessible quick-view dialogs, keyboard controls, visible focus, skip link, reduced motion, and a mobile menu.
- Self-hosted Cairo/Inter fonts and 15 licensed photographs in responsive WebP sizes. Other illustrations are original SVG artwork, clearly identified as illustrations.
- Static Arabic content remains readable if JavaScript or JSON loading is unavailable. Interactive tools require JavaScript.
- Canonical and share metadata, valid structured data, sitemap, robots file, favicon, and custom-domain preparation.

٣٩ صفحة HTML ثابتة، و١٠ وجهات و١٠ أكلات و٩ حكايات ثقافية، و٢٠ سؤالاً موزعاً على أربع جولات. تشمل الميزات البحث والفلاتر والمفضلة وتبديل اللغة والمظهر، مع محتوى ثابت قابل للقراءة حتى عند تعذّر تحميل الأدوات التفاعلية.

## Technology and structure / التقنيات والبنية

Semantic HTML5, CSS Grid/Flexbox, native JavaScript modules, JSON, SVG, and LocalStorage. **No framework, backend, runtime dependency, or mandatory build system.** Python tools are optional editorial and QA utilities; committed HTML deploys directly.

```text
index.html, explore.html, food.html, culture.html, quiz.html
favorites.html, about.html, search.html, credits.html, 404.html
places/       10 destination pages
dishes/       10 food pages
stories/       9 culture pages
assets/css/   base, components, responsive rules, local fonts
assets/js/    shared modules and browser interactions
assets/data/  centralized bilingual content, UI strings, quizzes, media credits
assets/images/, assets/fonts/, assets/icons/
tools/        optional HTML generation and QA
docs/         architecture, content, deployment, verification
.github/workflows/  verification only; no automatic deployment
```

الموقع ثابت بالكامل. الأدوات في `tools/` اختيارية للتحرير والفحص، ولا تحتاج الاستضافة إلى Python أو Node أو عملية بناء.

## Editing content / تحرير المحتوى

Edit `assets/data/destinations.json`, `foods.json`, or `culture.json`. Every visible field has `ar` and `en` values. Keep stable, unique ASCII IDs; each record produces a direct detail page. Add UI labels to `translations.json`, questions to `quizzes.json`, and verified photo provenance to `media.json`.

After changing editorial data or shared page templates:

```powershell
python tools/build_pages.py
```

This refreshes static HTML, sitemap, illustrations, and `PHOTO_CREDITS.md`. It uses only Python's standard library. Commit both source data and regenerated HTML. Existing visitors do not run the generator. See [the content guide](docs/CONTENT_GUIDE.md) for destination/quiz schemas and image rules.

عدّل ملفات JSON المركزية، وأضف العربية والإنجليزية لكل حقل. ثم شغّل أداة توليد الصفحات أعلاه وأضف البيانات والصفحات الناتجة إلى Git. تفاصيل إضافة وجهة أو أسئلة جديدة في [دليل المحتوى](docs/CONTENT_GUIDE.md).

## Verification / الفحص

Dev-only packages:

```powershell
python -m pip install -r tools/requirements-qa.txt
python tools/validate.py
python tools/browser_tests.py --browser "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

Keep the preview server running for browser checks. On other systems, pass your Chromium executable or run `python -m playwright install chromium` and omit `--browser`. Optional accessibility audit: `python tools/accessibility_tests.py --browser "C:\Program Files\Google\Chrome\Application\chrome.exe" --axe .qa/axe.min.js`. Supply a local axe-core distribution; it is never served to visitors.

See [QA results](docs/QA.md) for executed checks and measured limits. Automated checks support accessibility review; they do not establish full WCAG conformance.

الحزم المذكورة للفحص فقط. نتائج الفحص المنفّذ وحدوده موثقة في [تقرير الجودة](docs/QA.md). الفحص الآلي لا يعادل مراجعة وصول كاملة باستخدام قارئ شاشة.

## Deployment / النشر

**Deployment and DNS changes require the owner's explicit confirmation.** This repository contains no deployment trigger. When approved, merge the reviewed website branch, choose `main / (root)` under Settings → Pages, configure `syria.fun`, verify domain ownership, update DNS, and enable HTTPS. [Exact instructions and official DNS references](docs/DEPLOYMENT.md).

**النشر وتعديل DNS يحتاجان إلى تأكيد صريح من صاحب المشروع.** لا يوجد نشر تلقائي. بعد الموافقة، ادمج الفرع المراجع، واختر `main / (root)` في إعدادات Pages، واضبط النطاق وتحقّق من ملكيته ثم فعّل HTTPS. [خطوات النشر](docs/DEPLOYMENT.md).

## Troubleshooting / حل المشكلات

- Interactive tools unavailable: use HTTP, check the network for missing `assets/data/*.json`, and use the visible retry button. Static content remains available.
- Language/theme/favorites reset: private browsing, blocked storage, different origins, or cleared browser data can prevent persistence. In-page interaction still works if storage is blocked.
- Image unavailable: the interface substitutes a local SVG. Check paths and media attribution before replacing an image.
- Content differs from HTML: regenerate with `python tools/build_pages.py` after data edits.
- GitHub Pages 404: verify the selected branch/root, case-sensitive paths, domain configuration, and the presence of `index.html` and `.nojekyll`.
- Photographs are archival. They do not confirm current access or condition. No live festival, restaurant, or travel schedule is provided.

إذا تعطّلت الأدوات التفاعلية، استخدم خادماً محلياً وتحقق من ملفات JSON. إذا لم تُحفظ التفضيلات، راجع إعدادات تخزين المتصفح. بعد تحرير المحتوى أعد توليد HTML. الصور أرشيفية ولا تثبت الحالة الحالية أو إمكانية الوصول.

## License / الترخيص

Code and original artwork: [MIT](LICENSE). Third-party photos retain the licenses recorded in [PHOTO_CREDITS.md](PHOTO_CREDITS.md); fonts retain their bundled SIL OFL licenses. [Architecture](docs/ARCHITECTURE.md) · [Content guide](docs/CONTENT_GUIDE.md) · [Deployment](docs/DEPLOYMENT.md).
