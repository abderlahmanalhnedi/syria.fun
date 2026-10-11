import { initializeI18n, switchLanguage, t } from './i18n.js';
import { initializeTheme } from './theme.js';
import { initializeFavorites } from './favorites.js';
import { initializeSearch } from './search.js';
import { initializeModal } from './modal.js';
import { initializeQuizzes } from './quiz.js';
import { imageFallbacks } from './dom.js';

const dataURL = new URL('../data/', import.meta.url);
const files = ['translations', 'destinations', 'foods', 'culture', 'quizzes', 'media'];
let announcementTimer;
function announce(message) {
  const status = document.querySelector('#live-status');
  status.textContent = message;
  status.classList.add('visible');
  clearTimeout(announcementTimer);
  announcementTimer = setTimeout(() => status.classList.remove('visible'), 4000);
}
function initializeNavigation() {
  const button = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#main-navigation');
  function close(returnFocus = false) {
    button.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
    button.setAttribute('aria-label', t('menu'));
    if (returnFocus) button.focus();
  }
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', t(open ? 'closeMenu' : 'menu'));
    nav.classList.toggle('open', open);
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) close(true); });
  document.addEventListener('click', event => { if (!nav.contains(event.target) && !button.contains(event.target)) close(); });
  nav.addEventListener('focusout', event => { if (!nav.contains(event.relatedTarget) && event.relatedTarget !== button) close(); });
  matchMedia('(min-width: 1000px)').addEventListener('change', () => close());
  document.addEventListener('language-change', () => close());
}
async function initialize() {
  const values = await Promise.all(files.map(async name => {
    const response = await fetch(new URL(`${name}.json`, dataURL));
    if (!response.ok) throw new Error(`Content unavailable: ${name}`);
    return response.json();
  }));
  const [strings, destinations, foods, culture, quizzes, media] = values;
  const items = [
    ...destinations.map(item => ({ ...item, kind: 'destinations', href: `places/${item.id}.html` })),
    ...foods.map(item => ({ ...item, kind: 'foods', href: `dishes/${item.id}.html` })),
    ...culture.map(item => ({ ...item, kind: 'cultures', href: `stories/${item.id}.html` }))
  ];
  initializeI18n(strings, items, quizzes);
  document.body.classList.add('ready');
  document.querySelector('#app-error').hidden = true;
  initializeNavigation();
  initializeTheme();
  document.querySelector('#language-toggle').addEventListener('click', switchLanguage);
  initializeFavorites(items, media, announce);
  initializeSearch(items, media);
  initializeModal(items, media);
  initializeQuizzes(quizzes);
  document.addEventListener('storage-unavailable', () => announce(t('storageError')));
}
imageFallbacks();
initialize().catch(error => {
  console.error(error);
  document.documentElement.classList.remove('js');
  document.documentElement.lang = 'ar';
  document.documentElement.dir = 'rtl';
  document.documentElement.dataset.pendingLanguage = 'ar';
  const banner = document.querySelector('#app-error');
  banner.hidden = false;
  document.querySelector('#retry-load').addEventListener('click', () => location.reload());
});
