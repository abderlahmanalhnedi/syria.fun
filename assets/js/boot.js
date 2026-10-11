// Run before styles paint. The full application uses the same guarded storage.
document.documentElement.classList.add('js');
try {
  const lang = new URLSearchParams(location.search).get('lang') || JSON.parse(localStorage.getItem('syria.language') || 'null');
  // Arabic HTML remains readable until the bilingual dictionaries are available.
  document.documentElement.dataset.pendingLanguage = lang === 'en' ? 'en' : 'ar';
  document.documentElement.dir = lang === 'en' ? 'ltr' : 'rtl';
  const theme = JSON.parse(localStorage.getItem('syria.theme') || 'null');
  document.documentElement.dataset.theme = ['light', 'dark'].includes(theme) ? theme : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
} catch {
  document.documentElement.dataset.theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}
