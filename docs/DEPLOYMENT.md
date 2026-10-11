# GitHub Pages deployment / النشر على GitHub Pages

Prepared domain: **syria.fun**. Repository: **abderlahmanalhnedi/syria.fun**. No website has been published by this implementation, and no DNS or Pages settings have been changed. Publication requires explicit owner confirmation. CI only verifies source; it never deploys.

النطاق المقصود `syria.fun` والمستودع `abderlahmanalhnedi/syria.fun`. لم تُغيَّر إعدادات النشر أو DNS أثناء التنفيذ. يلزم تأكيد صريح قبل النشر. سير عمل GitHub يفحص المشروع فقط.

## After approval

1. Review and merge the website PR into `main`. Do not force-push. If only local code exists, push the branch and review it before merging.
2. In repository **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, **main**, **/(root)**, then Save. There is no application build command.
3. Under **Custom domain**, set **syria.fun**. The root `CNAME` file already contains exactly that hostname; `.nojekyll` prevents Jekyll processing.
4. Verify ownership in your account's Pages settings using the specific TXT record GitHub supplies. Do not invent the verification value. Follow [GitHub domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).
5. At your DNS provider, configure the records below. Preserve unrelated mail or service records. Do not create wildcard records.
6. Wait for GitHub's DNS check and TLS certificate provisioning. Once available, enable **Enforce HTTPS**. Test both `https://syria.fun/` and `https://www.syria.fun/`, direct detail-page URLs, assets, and the 404 response.
7. Run the browser/Lighthouse checks against the deployed HTTPS origin. Local results do not measure DNS, CDN behavior, certificate provisioning, or live social previews.

بعد الموافقة: راجع الفرع وادمجه في `main`، وفعّل Pages من جذر الفرع، واضبط النطاق، ثم تحقّق من ملكيته وأضف سجلات DNS التالية. انتظر التحقق وإصدار الشهادة، ثم فعّل HTTPS وافحص الموقع المنشور.

## DNS records

Verified against [GitHub's official custom-domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) during implementation. Recheck that page before applying changes if doing so later.

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | abderlahmanalhnedi.github.io |

Optional IPv6: add all four `AAAA` records for `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`. An apex `ALIAS`/`ANAME` to `abderlahmanalhnedi.github.io` is an alternative supported by some providers. Do not include `/syria.fun` in the DNS target. Avoid conflicting apex records. Configure `www` if you want GitHub's apex/subdomain redirect behavior.

## Static compatibility

Assets and navigation use relative paths, including `../` from detail pages, so normal content works at a project subpath before the custom domain is active. Canonicals and share assets intentionally use the final domain. `404.html` uses a custom-domain base so its assets work when served at an arbitrary missing path; it is intended for the final domain. Search/favorites are marked `noindex`. No rewrite rules or SPA fallbacks are needed.

## HTTPS and security

Use [GitHub's HTTPS guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https). Never add secrets to repository files or client JSON. GitHub Pages does not support repository-defined custom HTTP headers; the app includes a restrictive meta CSP, safe DOM rendering, and local assets. Do not claim that `_headers` or `.htaccess` files configure this host. Browser preferences contain no account or personal information. GitHub hosting itself is subject to GitHub's privacy policy.

## Troubleshooting

- Missing CSS/modules: verify case-sensitive filenames, branch/root selection, and actual asset URLs.
- Custom domain check fails: check all relevant DNS records, ownership TXT verification, conflicting entries, and propagation; use provider tools or `nslookup syria.fun` / `nslookup www.syria.fun`.
- HTTPS unavailable: wait for successful domain validation and certificate provisioning, then follow GitHub's official troubleshooting guidance.
- A fresh site still shows old content: check the Pages deployment status and clear cache after confirming the correct commit.
- Reverting: revert the reviewed commit through Git and let Pages deploy it; preserve domain verification. Never force-push as a rollback.
