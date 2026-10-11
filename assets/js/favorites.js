import { read, write } from './storage.js';
import { t, localized, number } from './i18n.js';
import { createCard } from './cards.js';
import { imageFallbacks } from './dom.js';
let items = [];
let assets = {};
let favorites = new Set();
function restore() {
  const stored = read('favorites', []);
  const valid = new Set(items.map(item => item.id));
  favorites = new Set(Array.isArray(stored) ? stored.filter(id => typeof id === 'string' && valid.has(id)) : []);
}
export function updateFavorites() {
  document.querySelectorAll('[data-favorite]').forEach(button => {
    const saved = favorites.has(button.dataset.favorite);
    const item = items.find(item => item.id === button.dataset.favorite);
    button.setAttribute('aria-pressed', String(saved));
    button.setAttribute('aria-label', `${t(saved ? 'remove' : 'save')}: ${localized(item?.name)}`);
    const label = button.querySelector('[data-i18n]');
    if (label) { label.dataset.i18n = saved ? 'remove' : 'save'; label.textContent = t(label.dataset.i18n); }
  });
  document.querySelectorAll('[data-favorites-count]').forEach(node => { node.textContent = number(favorites.size); });
  document.querySelectorAll('.favorite-link').forEach(node => { node.setAttribute('aria-label', `${t('favorites')}: ${number(favorites.size)}`); });
}
export function renderFavorites() {
  const grid = document.querySelector('#favorites-grid');
  if (!grid) return;
  const selected = items.filter(item => favorites.has(item.id));
  grid.replaceChildren(...selected.map(item => createCard(item, assets)));
  document.querySelector('#favorites-empty').hidden = selected.length > 0;
  imageFallbacks(grid);
  updateFavorites();
}
export function initializeFavorites(content, media, announce) {
  items = content;
  assets = media;
  restore();
  updateFavorites();
  renderFavorites();
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-favorite]');
    if (!button) return;
    const id = button.dataset.favorite;
    if (!items.some(item => item.id === id)) return;
    const saved = favorites.has(id);
    if (saved) favorites.delete(id); else favorites.add(id);
    write('favorites', [...favorites]);
    announce(t(saved ? 'removed' : 'saved'));
    if (document.querySelector('#favorites-grid')) {
      const cards = [...document.querySelectorAll('#favorites-grid [data-favorite]')];
      const index = cards.indexOf(button);
      renderFavorites();
      const remaining = [...document.querySelectorAll('#favorites-grid [data-favorite]')];
      (remaining[Math.min(index, remaining.length - 1)] || document.querySelector('#favorites-empty a')).focus();
    }
    updateFavorites();
  });
  document.addEventListener('language-change', () => { renderFavorites(); updateFavorites(); });
  window.addEventListener('storage', event => {
    if (event.key === 'syria.favorites' || event.key === null) { restore(); renderFavorites(); updateFavorites(); }
  });
}
