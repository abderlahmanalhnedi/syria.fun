/*
 * Syria.fun public API widgets
 * No dependencies, API keys, cookies, third-party scripts, or automatic requests.
 * Data requests start only after a visitor clicks "Load".
 */
const ENDPOINTS = Object.freeze({
  weather: "https://api.open-meteo.com/v1/forecast",
  air: "https://air-quality-api.open-meteo.com/v1/air-quality"
});
const CACHE_DURATION = 30 * 60 * 1000;
const MAX_STALE_AGE = 24 * 60 * 60 * 1000;
const I18N = {
  ar: {
    title: "الطقس وجودة الهواء", intro: "اطّلع على بيانات المنطقة عند الطلب.",
    load: "عرض البيانات", retry: "تحديث البيانات", loading: "جارٍ جلب البيانات…",
    weather: "حالة الطقس", air: "جودة الهواء", temperature: "درجة الحرارة",
    humidity: "الرطوبة", wind: "سرعة الرياح", aqi: "مؤشر جودة الهواء الأوروبي",
    particles: "جسيمات PM2.5", updated: "وقت البيانات المحلي", estimated: "بيانات جودة الهواء تقديرية من نماذج إقليمية؛ ليست قياساً مباشراً داخل المدينة.",
    privacy: "عند الضغط، يتصل متصفحك بخدمة Open-Meteo ويرسل عنوان IP الخاص بك إليها.",
    unavailable: "البيانات غير متاحة حالياً.", failed: "تعذر تحميل البيانات. حاول لاحقاً.",
    cached: "نسخة مخزنة مؤقتاً", stale: "نسخة قديمة من الذاكرة (ليست بيانات آنية)",
    live: "بيانات من الخدمة", good: "جيدة", fair: "مقبولة", moderate: "متوسطة",
    poor: "سيئة", veryPoor: "سيئة جداً", extremelyPoor: "سيئة للغاية",
    clear: "سماء صافية", cloudy: "غائم جزئياً", overcast: "غائم",
    fog: "ضباب", rain: "مطر", snow: "ثلج", thunder: "عواصف رعدية",
    unknown: "غير محدد", source: "المصدر: Open-Meteo · CC BY 4.0"
  },
  en: {
    title: "Weather & air quality", intro: "Load local estimates only when you choose.",
    load: "Load information", retry: "Refresh information", loading: "Loading…",
    weather: "Weather", air: "Air quality", temperature: "Temperature",
    humidity: "Humidity", wind: "Wind speed", aqi: "European air quality index",
    particles: "PM2.5", updated: "Local data time", estimated: "Air-quality information is a regional model estimate, not an on-site measurement.",
    privacy: "When you click, your browser contacts Open-Meteo and sends your IP address to that service.",
    unavailable: "Information is currently unavailable.", failed: "Unable to load. Please try again later.",
    cached: "Cached result", stale: "Outdated cached result (not current)",
    live: "Provider data", good: "Good", fair: "Fair", moderate: "Moderate",
    poor: "Poor", veryPoor: "Very poor", extremelyPoor: "Extremely poor",
    clear: "Clear sky", cloudy: "Partly cloudy", overcast: "Overcast",
    fog: "Fog", rain: "Rain", snow: "Snow", thunder: "Thunderstorms",
    unknown: "Unknown", source: "Source: Open-Meteo · CC BY 4.0"
  }
};

export function validateCoordinates(latitude, longitude) {
  if (latitude === "" || longitude === "" || latitude == null || longitude == null) {
    throw new TypeError("Missing latitude or longitude");
  }
  const lat = Number(latitude);
  const lon = Number(longitude);
  if (!Number.isFinite(lat) || !Number.isFinite(lon) ||
      lat < -90 || lat > 90 || lon < -180 || lon > 180) {
    throw new RangeError("Invalid coordinates");
  }
  return { lat, lon };
}

export function buildApiUrl(kind, latitude, longitude) {
  const { lat, lon } = validateCoordinates(latitude, longitude);
  if (!Object.prototype.hasOwnProperty.call(ENDPOINTS, kind)) {
    throw new RangeError("Unknown API type");
  }
  const url = new URL(ENDPOINTS[kind]);
  url.searchParams.set("latitude", String(lat));
  url.searchParams.set("longitude", String(lon));
  url.searchParams.set("timezone", "Asia/Damascus");
  if (kind === "weather") {
    url.searchParams.set("current", "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m");
    url.searchParams.set("forecast_days", "1");
  } else {
    url.searchParams.set("current", "european_aqi,pm2_5");
    url.searchParams.set("domains", "cams_global");
    url.searchParams.set("forecast_days", "1");
  }
  return url.href;
}

function finiteOrNull(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

export function normalizeWeather(payload) {
  const values = payload && payload.current;
  if (!values || finiteOrNull(values.temperature_2m) === null) {
    throw new Error("Missing weather readings");
  }
  return {
    temperature: values.temperature_2m,
    humidity: finiteOrNull(values.relative_humidity_2m),
    wind: finiteOrNull(values.wind_speed_10m),
    code: finiteOrNull(values.weather_code),
    time: typeof values.time === "string" ? values.time : ""
  };
}

export function normalizeAir(payload) {
  const values = payload && payload.current;
  if (!values) throw new Error("Missing air readings");
  const aqi = finiteOrNull(values.european_aqi);
  const pm25 = finiteOrNull(values.pm2_5);
  if (aqi === null && pm25 === null) throw new Error("Air readings unavailable");
  return { aqi, pm25, time: typeof values.time === "string" ? values.time : "" };
}

export function aqiCategory(aqi) {
  if (typeof aqi !== "number" || !Number.isFinite(aqi) || aqi < 0) return "unknown";
  if (aqi <= 20) return "good";
  if (aqi <= 40) return "fair";
  if (aqi <= 60) return "moderate";
  if (aqi <= 80) return "poor";
  if (aqi <= 100) return "veryPoor";
  return "extremelyPoor";
}

export function weatherCategory(code) {
  if (code === 0) return "clear";
  if ([1, 2].includes(code)) return "cloudy";
  if (code === 3) return "overcast";
  if ([45, 48].includes(code)) return "fog";
  if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return "rain";
  if ([71, 73, 75, 77, 85, 86].includes(code)) return "snow";
  if ([95, 96, 99].includes(code)) return "thunder";
  return "unknown";
}

function readCache(key) {
  try {
    const result = JSON.parse(localStorage.getItem(key));
    if (!result || typeof result.savedAt !== "number" ||
        !result.data || Date.now() - result.savedAt < 0 ||
        Date.now() - result.savedAt > MAX_STALE_AGE) return null;
    return result;
  } catch {
    return null;
  }
}
function saveCache(key, data) {
  try { localStorage.setItem(key, JSON.stringify({ data, savedAt: Date.now() })); }
  catch { /* Storage is optional: private mode remains functional. */ }
}
async function fetchJson(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(url, {
      method: "GET", signal: controller.signal, mode: "cors",
      credentials: "omit", referrerPolicy: "no-referrer",
      cache: "no-store", headers: { Accept: "application/json" }
    });
    if (!response.ok) throw new Error("Open-Meteo error: " + response.status);
    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}
async function loadApi(kind, lat, lon) {
  const key = "syria.fun:api:v1:" + kind + ":" + lat + ":" + lon;
  const cached = readCache(key);
  if (cached && Date.now() - cached.savedAt < CACHE_DURATION) {
    return { data: cached.data, source: "cached" };
  }
  try {
    const payload = await fetchJson(buildApiUrl(kind, lat, lon));
    const data = kind === "weather" ? normalizeWeather(payload) : normalizeAir(payload);
    saveCache(key, data);
    return { data, source: "live" };
  } catch (error) {
    if (cached) return { data: cached.data, source: "stale" };
    throw error;
  }
}
function element(tag, className, textValue) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (textValue !== undefined) el.textContent = String(textValue);
  return el;
}
function metric(parent, label, value) {
  const row = element("div", "sf-api-metric");
  row.append(element("dt", "", label), element("dd", "", value));
  parent.append(row);
}
function format(value, lang, unit) {
  if (value === null) return "—";
  return new Intl.NumberFormat(lang === "ar" ? "ar" : "en", {
    maximumFractionDigits: 1
  }).format(value) + (unit || "");
}
function currentLanguage(node) {
  const langNode = node.closest("[lang]");
  const lang = (langNode ? langNode.lang : document.documentElement.lang).toLowerCase();
  return lang.startsWith("ar") ? "ar" : "en";
}
function createResultBlock(title, dataResult, kind, locale, lang) {
  const section = element("section", "sf-api-result");
  section.append(element("h4", "", title));
  if (!dataResult) {
    section.append(element("p", "sf-api-note", locale.unavailable));
    return section;
  }
  const { data, source } = dataResult;
  const list = element("dl", "sf-api-metrics");
  if (kind === "weather") {
    metric(list, locale.temperature, format(data.temperature, lang, " °C"));
    metric(list, locale.humidity, format(data.humidity, lang, " %"));
    metric(list, locale.wind, format(data.wind, lang, " km/h"));
    metric(list, locale.title, locale[weatherCategory(data.code)]);
  } else {
    metric(list, locale.aqi, data.aqi === null ? "—" :
      format(data.aqi, lang) + " · " + locale[aqiCategory(data.aqi)]);
    metric(list, locale.particles, format(data.pm25, lang, " µg/m³"));
  }
  section.append(list);
  if (data.time) section.append(element("p", "sf-api-note", locale.updated + ": " + data.time.replace("T", " ")));
  section.append(element("p", "sf-api-note", locale[source]));
  if (kind === "air") section.append(element("p", "sf-api-note", locale.estimated));
  return section;
}

export function mountSyriaApiWidget(root) {
  if (!root || root.dataset.sfApiMounted === "yes") return null;
  const { lat, lon } = validateCoordinates(root.dataset.latitude, root.dataset.longitude);
  root.dataset.sfApiMounted = "yes";
  const title = element("h3", "sf-api-title");
  const intro = element("p", "sf-api-intro");
  const privacy = element("p", "sf-api-note");
  const button = element("button", "sf-api-button");
  button.type = "button";
  const status = element("p", "sf-api-status");
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  const output = element("div", "sf-api-output");
  const source = element("a", "sf-api-credit");
  source.href = "https://open-meteo.com/";
  source.target = "_blank";
  source.rel = "noopener noreferrer";
  root.classList.add("sf-api-widget");
  root.replaceChildren(title, intro, privacy, button, status, output, source);
  let weather = null, air = null, pending = false, loaded = false, failed = false;
  function render() {
    const lang = currentLanguage(root);
    const t = I18N[lang];
    root.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    const city = root.dataset[lang === "ar" ? "cityAr" : "cityEn"] || "";
    title.textContent = t.title + (city ? " — " + city : "");
    intro.textContent = t.intro;
    privacy.textContent = t.privacy;
    button.textContent = loaded ? t.retry : t.load;
    button.disabled = pending;
    status.textContent = pending ? t.loading : failed ? t.failed : "";
    source.textContent = t.source;
    output.replaceChildren();
    if (loaded) {
      output.append(createResultBlock(t.weather, weather, "weather", t, lang));
      output.append(createResultBlock(t.air, air, "air", t, lang));
    }
  }
  button.addEventListener("click", async () => {
    if (pending) return;
    pending = true; failed = false; render();
    try {
      const [w, a] = await Promise.allSettled([
        loadApi("weather", lat, lon), loadApi("air", lat, lon)
      ]);
      weather = w.status === "fulfilled" ? w.value : null;
      air = a.status === "fulfilled" ? a.value : null;
      loaded = Boolean(weather || air);
      failed = !loaded;
    } catch {
      failed = true;
    } finally {
      pending = false; render();
    }
  });
  const observer = new MutationObserver(() => render());
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  if (root.closest("[lang]") && root.closest("[lang]") !== document.documentElement) {
    observer.observe(root.closest("[lang]"), { attributes: true, attributeFilter: ["lang"] });
  }
  render();
  return { refreshLanguage: render, destroy() { observer.disconnect(); delete root.dataset.sfApiMounted; } };
}

export function initializeSyriaApiWidgets() {
  return Array.from(document.querySelectorAll("[data-sf-weather]")).map(node => {
    try { return mountSyriaApiWidget(node); }
    catch (error) {
      // Do not leak coordinates or private data in logs.
      const status = element("p", "sf-api-status", "Weather widget unavailable.");
      node.replaceChildren(status);
      return null;
    }
  }).filter(Boolean);
}
if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeSyriaApiWidgets, { once: true });
  } else {
    initializeSyriaApiWidgets();
  }
}
