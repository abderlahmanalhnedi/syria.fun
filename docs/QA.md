# Verification report

Executed locally on 2026-10-11 with Python 3.11, Playwright 1.63.0, installed Google Chrome 155 in headless mode, axe-core 4.14.0, and Lighthouse 13.5.0. The origin was `http://127.0.0.1:8000/`; these are local results, not a live-domain audit.

## Results

| Check | Result |
| --- | --- |
| Static HTML5 parsing | All 39 documents parsed in strict html5lib mode |
| Structure and navigation | Single H1, unique IDs, required metadata, real local targets, image dimensions/alt, and sitemap XML passed |
| Bilingual data | 29 records, centralized UI translations, and 4 × 5 quiz questions validated |
| JavaScript syntax | All runtime files passed Node syntax checks; every module also loaded in Chrome |
| Browser acceptance | All 18 acceptance groups passed |
| Accessibility automation | 101 page/state combinations, zero axe rule violations |
| Secret pattern check | Common GitHub token, private-key, AWS-key, and API-key patterns absent from project source |
| Safe DOM review | No dynamic `innerHTML` assignment, `eval`, or `new Function` in runtime source |

Browser coverage includes Arabic default and English switching; document language/direction and metadata; reload/navigation persistence; light/dark preference; Arabic normalized and English search; category filters, reset, and no-results; landmarks/food/culture global search; favorites, count, empty state, and stored data; dialog focus trapping, Escape and restoration; all four quizzes with perfect and zero scores, answer locking, feedback, progress, replay, and retained best scores; language changes during a quiz; reduced motion; missing-photo fallback; blocked/corrupt storage; failed JSON loading and retry; and static content without JavaScript.

The suite checked primary pages and representative detail pages at **320, 375, 390, 768, 1024, 1440, and 1920px** in both languages, without horizontal document overflow. Mobile navigation was opened, dismissed with Escape, and used to navigate. All 38 normal pages were crawled for working local navigation; the intended custom-domain 404 page was validated statically, rather than treated as a local routing test.

The axe matrix covers 12 representative pages × 2 widths × 2 languages × 2 themes, plus 5 interactive states: an open dialog, an active question, answer feedback, quiz results, and populated favorites. Audits use a separate context with CSP bypass solely to inject the development-only axe script. Normal-use tests retain the production CSP and reported no JavaScript/console errors. Automated rule coverage is not a WCAG certification; axe also lists items requiring human review.

## Lighthouse

| Homepage run | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Arabic, simulated mobile | 91 | 100 | 100 | 100 |
| Arabic, desktop preset | 99 | 100 | 100 | 100 |
| English, simulated mobile | 93 | 100 | 100 | 100 |

The Arabic mobile run measured FCP 1.9s, LCP 3.2s, TBT 0ms, and CLS 0.002. The English mobile run measured LCP 2.9s and CLS 0.09. The original Arabic mobile run was 79; responsive image sizing, a portrait hero derivative, fewer blocking style requests, local font subsets, early navigation layout, and avoiding an unnecessary Arabic text repaint improved the measured result. English also selects its layout direction and font preference before the bilingual text is loaded. Scores can vary with browser, machine, network, and hosting. The stated targets were reached for the measured homepage runs; no site-wide score guarantee is made.

Local detailed reports, browser snapshots, and audit JSON are in the ignored `.qa/` directory. The reusable verification scripts are committed under `tools/`. The GitHub workflow checks regeneration, structure, and browser behavior; its remote execution status is separate from local checks.

## Not executed / limits

- Publication, production DNS, live HTTPS, custom-domain redirects, and actual GitHub Pages 404 delivery have not been tested because deployment awaits owner confirmation.
- No manual screen-reader review, real iOS/Android device session, Firefox/Safari run, or comprehensive assisted-technology audit was executed.
- The HTML check is strict HTML5 parsing and explicit structure checks, not a claim that the Nu/W3C validator was run.
- The source pattern check is not an exhaustive credential detection or penetration test.
- External source/license pages were researched during content preparation; internal-link crawling does not certify future availability of those external pages.
- Photographs are archival, with source/license/capture provenance where available. Missing capture dates are stated rather than inferred from upload dates. Illustrations are identified as interpretive artwork.
- Preferences are per browser/origin. Storage may be cleared or blocked, and there is no account or cross-device synchronization.
