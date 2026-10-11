# Content and translations / دليل المحتوى والترجمة

Maintain original, respectful Arabic and English copy. Do not invent dates, rankings, statistics, origins, or access conditions. Cite the source supporting each fact. Shared traditions should not be claimed exclusively for one community. Regional examples are examples, rather than universal rules. Food ingredient lists are typical components, not recipes or allergen guarantees.

اكتب محتوى أصلياً بالعربية والإنجليزية، واحترم تنوع السكان والتقاليد. وثّق الحقائق، ولا تخترع أرقاماً أو تواريخ أو نسباً. قوائم المكونات أمثلة شائعة وليست وصفات موحدة أو ضماناً للحساسية الغذائية.

## Add a destination

Append a record to `assets/data/destinations.json`:

```json
{
  "id": "new-place",
  "category": "heritage",
  "name": {"ar": "اسم المكان", "en": "Place name"},
  "subtitle": {"ar": "عنوان فرعي", "en": "Subtitle"},
  "description": {"ar": "مقدمة قصيرة", "en": "Short introduction"},
  "body": {"ar": "نص موثق", "en": "Sourced original prose"},
  "highlights": {"ar": ["معلم موثق"], "en": ["Verified highlight"]},
  "fact": {"ar": "حقيقة موثقة", "en": "A sourced fact"},
  "source": "https://example.org/source"
}
```

Replace illustrative values with verified content. IDs must be unique lowercase ASCII slugs and remain stable for stored favorites and URLs. Existing place categories: `heritage`, `central`, `coast`, `river`, `mountain`. Adding a category also requires bilingual UI text and a catalog filter in the generator. Run `python tools/build_pages.py`; this creates `places/new-place.html`, updates catalogs/search and sitemap. If there is no verified photo, a clearly identified SVG illustration is generated.

Food follows the same schema in `foods.json` and generates `dishes/<id>.html`; its highlights are common ingredients. Categories: `mains`, `salads`, `street`, `sweets`. Culture uses `culture.json` and `stories/<id>.html`; categories: `everyday`, `craft`, `heritage`, `arts`. Culture can specify `"photo": "damascus"` to reuse an attributed, verified photo when the text actually discusses that place. Otherwise use an original illustration.

## Add questions

Questions live exclusively in `assets/data/quizzes.json`, outside runtime logic. Each quiz has an ID, bilingual name and description, icon, and at least five questions:

```json
{
  "prompt": {"ar": "سؤال", "en": "Question"},
  "options": {"ar": ["أ", "ب", "ج", "د"], "en": ["A", "B", "C", "D"]},
  "answer": 1,
  "explanation": {"ar": "شرح موثق", "en": "Sourced explanation"},
  "source": "https://example.org/source"
}
```

`answer` is a zero-based index; both option arrays must use the same order. Keep existing quiz IDs stable. The initial quiz score guard assumes five questions, so update that bound if changing round length. Regenerate pages when adding a quiz or changing the selection copy. Runtime questions are fetched from the JSON; no question text belongs in `quiz.js`.

## Images and fonts

Before using a photo, verify the depicted subject, the creator, exact license terms, and whether edits are permitted. Record source/author/license/date and local paths in `media.json`. Include the license URL, identify cropping/resizing, and keep share-alike derivatives under the same license. Never relabel an unrelated photo as a Syrian location. A dish photo outside Syria may illustrate a shared dish only if clearly contextualized; it must not be described as a Syrian venue.

`tools/fetch_assets.py` is optional and requires Pillow. It downloads only an explicit list of reviewed Commons filenames and optimizes 640/1600 WebP variants. Its font helper downloads Cairo/Inter WOFF2 subsets and license texts. Review new assets before changing its list; do not blindly accept search results from `research_assets.py`. Preserve archival dates and distinguish illustrations from documentary photography. Regeneration refreshes `PHOTO_CREDITS.md` and the public `credits.html` page.

## UI translations and publication checks

All UI strings live in `translations.json` as `key: {ar, en}`. Static templates use `data-i18n`, `data-content`, and `data-quiz-text` hooks. Attribute hooks cover accessible labels and placeholders. The generator reads Arabic; the shared runtime reads either language. Avoid independently editing generated translations in HTML.

After editing, regenerate, run static checks, preview both languages and themes, check mobile widths, verify correct quiz answers, and inspect all new source/license links. Run `python tools/validate.py` and the browser suite. Re-review content before publication; site text should reflect what is actually supported.
