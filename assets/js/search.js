import { t, number, translationsFor } from './i18n.js';
import { createCard } from './cards.js';
import { updateFavorites } from './favorites.js';
import { imageFallbacks } from './dom.js';
export function normalize(text) {
  return String(text).normalize('NFKD').toLocaleLowerCase().replace(/[\u064B-\u065F\u0670\u0640\u0300-\u036f]/g, '').replace(/[أإآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/\s+/g, ' ').trim();
}
function searchable(item) {
  return normalize([item.id, ...Object.values(item.name), ...Object.values(item.subtitle), ...Object.values(item.description), ...Object.values(item.body), ...Object.values(item.highlights).flat(), item.category, ...translationsFor(item.category)].join(' '));
}
export function initializeSearch(items, media) {
  const input = document.querySelector('#catalog-search');
  if (!input) return;
  const page = document.body.dataset.page;
  const global = page === 'search';
  const kind = { explore: 'destinations', food: 'foods', culture: 'cultures' }[page];
  const pool = global ? items : items.filter(item => item.kind === kind);
  const grid = document.querySelector('#catalog-grid');
  const chips = [...document.querySelectorAll('[data-filter]')];
  let selected = 'all';
  const params = new URLSearchParams(location.search);
  input.value = params.get('q') || '';
  const initial = params.get('category');
  if (chips.some(chip => chip.dataset.filter === initial)) selected = initial;
  function render() {
    const words = normalize(input.value).split(' ').filter(Boolean);
    const found = pool.filter(item => (selected === 'all' || (global ? item.kind : item.category) === selected) && words.every(word => searchable(item).includes(word)));
    grid.replaceChildren(...found.map(item => createCard(item, media)));
    document.querySelector('#no-results').hidden = found.length > 0;
    document.querySelector('#result-count').textContent = `${number(found.length)} ${t('results')}`;
    chips.forEach(chip => chip.setAttribute('aria-pressed', String(chip.dataset.filter === selected)));
    updateFavorites();
    imageFallbacks(grid);
  }
  input.addEventListener('input', render);
  chips.forEach(chip => chip.addEventListener('click', () => { selected = chip.dataset.filter; render(); }));
  document.querySelector('#clear-search').addEventListener('click', () => {
    input.value = '';
    selected = 'all';
    const locationURL = new URL(location.href);
    locationURL.searchParams.delete('q');
    locationURL.searchParams.delete('category');
    history.replaceState(null, '', locationURL);
    render();
    input.focus();
  });
  document.addEventListener('language-change', render);
  render();
}
