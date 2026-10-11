import { t } from './i18n.js';
export const rootURL = new URL('../../', import.meta.url);
export const url = path => new URL(path, rootURL).href;
export function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
export function icon(name) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'icon');
  svg.setAttribute('aria-hidden', 'true');
  const use = document.createElementNS(svg.namespaceURI, 'use');
  use.setAttribute('href', `#icon-${name}`);
  svg.append(use);
  return svg;
}
export function imageFallbacks(root = document) {
  root.querySelectorAll('img').forEach(img => {
    const fallback = () => {
      if (img.dataset.failed) return;
      img.dataset.failed = 'true';
      const label = t('imageUnavailable') === 'imageUnavailable' ? (img.dataset.fallbackAlt || '') : t('imageUnavailable');
      img.removeAttribute('data-alt-content');
      img.dataset.i18nAlt = 'imageUnavailable';
      img.alt = label;
      const caption = img.closest('figure')?.querySelector('figcaption') || img.closest('.hero')?.querySelector('.hero-caption');
      if (caption) {
        const notice = element('span', '', label);
        notice.dataset.i18n = 'imageUnavailable';
        caption.replaceChildren(notice);
      }
      img.closest('picture')?.querySelectorAll('source').forEach(source => source.remove());
      img.removeAttribute('srcset');
      img.src = url('assets/images/fallback.svg');
    };
    img.addEventListener('error', fallback, { once: true });
    if (img.complete && img.naturalWidth === 0) fallback();
  });
}
