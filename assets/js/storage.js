const memory = new Map();
let failed = false;
export function read(key, fallback) {
  try {
    const value = localStorage.getItem(`syria.${key}`);
    return value === null ? fallback : JSON.parse(value);
  } catch { return memory.get(key) ?? fallback; }
}
export function write(key, value) {
  memory.set(key, value);
  try { localStorage.setItem(`syria.${key}`, JSON.stringify(value)); }
  catch {
    if (!failed) { failed = true; document.dispatchEvent(new CustomEvent('storage-unavailable')); }
  }
}
