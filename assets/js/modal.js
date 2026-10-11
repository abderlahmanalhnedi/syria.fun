import { localized, t } from './i18n.js';
import { url, element, imageFallbacks } from './dom.js';
import { updateFavorites } from './favorites.js';
export function initializeModal(items, media) {
  const dialog = document.querySelector('#detail-dialog');
  let current = null;
  let opener = null;
  function render() {
    const item = current;
    const container = dialog.querySelector('#dialog-content');
    const title = element('h2', 'dialog-title', localized(item.name));
    title.id = 'dialog-title';
    const image = element('img', 'dialog-image');
    const asset = media[item.photo || item.id];
    image.src = url(asset?.large || `assets/images/${item.id}.svg`);
    image.alt = localized(item.name);
    image.width = 640;
    image.height = 440;
    const summary = element('p', 'lead', localized(item.description));
    const story = element('p', '', localized(item.body));
    const heading = element('h3', '', t(item.kind === 'foods' ? 'ingredients' : 'highlights'));
    const list = element('ul', 'highlights');
    localized(item.highlights).forEach(text => list.append(element('li', '', text)));
    const read = element('a', 'button primary', t('read'));
    read.href = url(item.href);
    const save = element('button', 'button secondary', t('save'));
    save.type = 'button';
    save.dataset.favorite = item.id;
    const actions = element('div', 'button-row');
    actions.append(read, save);
    container.replaceChildren(image, title, summary, story, heading, list, actions);
    updateFavorites();
    imageFallbacks(container);
  }
  document.addEventListener('click', event => {
    const trigger = event.target.closest('[data-preview]');
    if (!trigger) return;
    current = items.find(item => item.id === trigger.dataset.preview);
    if (!current) return;
    opener = trigger;
    render();
    dialog.showModal();
  });
  dialog.querySelector('[data-close-dialog]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const focusable = [...dialog.querySelectorAll('button:not(:disabled), a[href], [tabindex="0"]')].filter(node => node.getClientRects().length);
    const first = focusable[0];
    const last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { current = null; if (opener?.isConnected) opener.focus(); });
  document.addEventListener('language-change', () => { if (current) render(); });
}
