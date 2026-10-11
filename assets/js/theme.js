import { write } from './storage.js';
import { t } from './i18n.js';
export function updateThemeLabel() {
  const dark = document.documentElement.dataset.theme === 'dark';
  const button = document.querySelector('#theme-toggle');
  button.setAttribute('aria-label', t(dark ? 'light' : 'dark'));
  button.setAttribute('aria-pressed', String(dark));
}
export function initializeTheme() {
  const toggle = document.querySelector('#theme-toggle');
  toggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    write('theme', next);
    updateThemeLabel();
  });
  document.addEventListener('language-change', updateThemeLabel);
  updateThemeLabel();
}
