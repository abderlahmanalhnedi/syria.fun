import { read, write } from './storage.js';
let dictionary = {};
let records = new Map();
let quizzes = new Map();
let language = 'ar';
export const lang = () => language;
export const t = key => dictionary[key]?.[language] ?? key;
export const translationsFor = key => Object.values(dictionary[key] ?? {});
export const localized = value => value?.[language] ?? '';
export const number = value => new Intl.NumberFormat(language).format(value);
export function initializeI18n(strings, content, quizData) {
  dictionary = strings;
  records = new Map(content.map(item => [item.id, item]));
  quizzes = new Map(quizData.map(item => [item.id, item]));
  const query = new URLSearchParams(location.search).get('lang');
  const preference = query || read('language', 'ar');
  language = preference === 'en' ? 'en' : 'ar';
  if (language !== document.documentElement.lang) translate();
}
export function translate(root = document) {
  root.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = t(node.dataset.i18n); });
  ['placeholder', 'aria-label', 'title', 'alt'].forEach(attribute => {
    root.querySelectorAll(`[data-i18n-${attribute}]`).forEach(node => node.setAttribute(attribute, t(node.getAttribute(`data-i18n-${attribute}`))));
  });
  root.querySelectorAll('[data-content]').forEach(node => {
    const [id, field, index] = node.dataset.content.split('.');
    const value = localized(records.get(id)?.[field]);
    node.textContent = index === undefined ? value : value?.[Number(index)] ?? '';
  });
  root.querySelectorAll('[data-quiz-text]').forEach(node => {
    const [id, field] = node.dataset.quizText.split('.');
    node.textContent = localized(quizzes.get(id)?.[field]);
  });
  root.querySelectorAll('[data-alt-content]').forEach(node => {
    const item = records.get(node.dataset.altContent);
    node.alt = localized(item?.name);
  });
  if (root !== document) return;
  document.documentElement.lang = language;
  document.documentElement.dataset.pendingLanguage = language;
  document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
  const button = document.querySelector('#language-toggle');
  button.textContent = language === 'ar' ? 'EN' : 'عربي';
  button.lang = language === 'ar' ? 'en' : 'ar';
  button.setAttribute('aria-label', t('language'));
  const detail = records.get(document.body.dataset.item);
  const title = detail ? localized(detail.name) : t(document.body.dataset.title);
  const description = detail ? localized(detail.description) : t(document.body.dataset.description);
  document.title = `${title} | Syria.fun`;
  document.querySelector('meta[name="description"]').content = description;
  document.querySelector('meta[property="og:title"]').content = document.title;
  document.querySelector('meta[property="og:description"]').content = description;
  document.querySelector('meta[property="og:locale"]').content = language === 'ar' ? 'ar_SY' : 'en_US';
  document.querySelector('meta[name="twitter:title"]').content = document.title;
  document.querySelector('meta[name="twitter:description"]').content = description;
  const structured = document.querySelector('script[type="application/ld+json"]');
  if (structured) {
    const value = JSON.parse(structured.textContent);
    value.name = document.body.dataset.page === 'home' ? 'Syria.fun' : document.title;
    value.description = description;
    if (value['@type'] === 'WebPage') value.inLanguage = language;
    structured.textContent = JSON.stringify(value);
  }
}
export function switchLanguage() {
  language = language === 'ar' ? 'en' : 'ar';
  write('language', language);
  const url = new URL(location.href);
  url.searchParams.set('lang', language);
  history.replaceState(null, '', url);
  translate();
  document.dispatchEvent(new CustomEvent('language-change'));
}
