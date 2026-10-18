# syria.fun — Public API integration (AR / EN)

A dependency-free, optional weather and air-quality widget for the **existing local static syria.fun site**. This repository currently does not contain the original 136-file website, so these files are **additive integration assets**, not a claim that the website was updated or deployed.

## العربية — طريقة الدمج

الخدمات المستخدمة: **Open-Meteo Weather API** و**Open-Meteo Air Quality API**. لا تحتاجان إلى API Key في حالة الاستخدام غير التجاري وفق شروط المزود. الخدمة المجانية محدودة ويجب ذكر مصدر البيانات وترخيص CC BY 4.0.

1. انسخ الملفين `src/api-widgets.js` و`src/api-widgets.css` إلى المسار نفسه داخل مشروع موقعك.
2. أضف إلى `<head>`:
   ```html
   <link rel="stylesheet" href="/integrations/syria-fun-api/src/api-widgets.css">
   <script type="module" src="/integrations/syria-fun-api/src/api-widgets.js"></script>
   ```
   (عدّل المسار إذا اخترت مكاناً مختلفاً للملفات).
3. أضف هذا العنصر داخل صفحة الوجهة، مثلاً دمشق:
   ```html
   <section data-sf-weather data-city-ar="دمشق" data-city-en="Damascus"
     data-latitude="33.5138" data-longitude="36.2765"></section>
   ```
   استخدم إحداثيات الوجهات من بيانات الموقع المحلية، وليس إحداثيات الزائر. لا تُضاف الواجهة تلقائياً إلى كل صفحة إلا إذا وضعت هذا العنصر.
4. افتح `examples/weather-air.html` باستخدام خادم HTTP محلي، مثل `python -m http.server 8000`، ثم جرّب النموذج.
5. بعد دمج الملفات مع الموقع الأصلي اختبر عرض العربية والإنجليزية، RTL/LTR، الوضع الداكن، انقطاع الاتصال، وLighthouse وAxe، قبل النشر.

### الأمان والأداء والخصوصية

- **ممنوع** إدخال API Keys أو كلمات مرور في كود المتصفح.
- لا يبدأ أي اتصال بـOpen-Meteo إلا بعد ضغط الزائر على الزر؛ عند الطلب يستقبل المزود عنوان IP الخاص بالزائر. أضف وصف ذلك إلى سياسة الخصوصية إن كانت مطلوبة لموقعك.
- تستخدم الطلبات HTTPS وعنوانين ثابتين فقط، `credentials: omit` و`referrerPolicy: no-referrer` ومهلة 8 ثوانٍ.
- النتائج تُخزَّن محلياً في متصفح الزائر لـ30 دقيقة، مع بديل مخزَّن بحد أقصى 24 ساعة موسوم بوضوح بأنه قديم.
- كل المحتوى القادم من الخدمة يظهر عبر `textContent` وليس `innerHTML`، لمنع إدخال HTML غير موثوق.
- البيانات الخاصة بجودة الهواء **تقديرات من نموذج CAMS عالمي بدقة تقريبية 45 كم** وليست قياسات محطة محلية؛ لا تستخدمها لاتخاذ قرارات طبية.
- لا تضع الواجهة في الصفحة الرئيسية فوق المحتوى الأساسي؛ حمّلها فقط داخل صفحات الوجهات.
- يمكن تضييق Content Security Policy إلى:
  ```text
  connect-src 'self' https://api.open-meteo.com https://air-quality-api.open-meteo.com;
  ```
  **أضف** هذين المصدرين إلى سياسة موقعك الحالية بدلاً من استبدال سياسة `connect-src` بالكامل.

## English — integration

Copy `src/api-widgets.js` and `src/api-widgets.css` into your original static website and reference them using `<script type="module">` and a stylesheet link. Put a `data-sf-weather` element with predefined destination coordinates into each desired destination page. Check `examples/weather-air.html` for a complete example.

There are **no automatic API calls**. Only explicit clicks trigger requests, with a 30-minute local cache, 8-second timeout, fixed HTTPS endpoints, safe text rendering, bilingual AR/EN strings and RTL/LTR. Air quality comes from a regional **forecast model**, not a local pollution sensor. Follow Open-Meteo's free non-commercial terms and CC BY 4.0 attribution.

## API documentation

- Weather: https://open-meteo.com/en/docs
- Air quality: https://open-meteo.com/en/docs/air-quality-api
- Terms: https://open-meteo.com/en/terms

## Tests

From the repository root on Node.js 20+:
```bash
node --test integrations/syria-fun-api/tests/api-widgets.test.mjs
```

No npm install is required. Browser, live API, accessibility, Lighthouse and full website integration checks are still required once the original website is available.
