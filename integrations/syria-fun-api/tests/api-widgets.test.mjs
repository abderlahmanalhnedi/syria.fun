import test from "node:test";
import assert from "node:assert/strict";
import {
  validateCoordinates, buildApiUrl, normalizeWeather, normalizeAir,
  aqiCategory, weatherCategory
} from "../src/api-widgets.js";

test("Coordinates must be valid", () => {
  assert.deepEqual(validateCoordinates(33.5138, 36.2765), { lat: 33.5138, lon: 36.2765 });
  assert.throws(() => validateCoordinates("", "25"));
  assert.throws(() => validateCoordinates(100, 25));
  assert.throws(() => validateCoordinates("abc", 25));
});
test("API URL only permits fixed providers with one-day range", () => {
  const a = new URL(buildApiUrl("weather", 33.5, 36.2));
  const b = new URL(buildApiUrl("air", 33.5, 36.2));
  assert.equal(a.hostname, "api.open-meteo.com");
  assert.equal(b.hostname, "air-quality-api.open-meteo.com");
  assert.equal(a.searchParams.get("forecast_days"), "1");
  assert.equal(b.searchParams.get("domains"), "cams_global");
  assert.throws(() => buildApiUrl("https://evil.example", 33, 36));
});
test("Partial weather readings are tolerated", () => {
  assert.deepEqual(normalizeWeather({ current: { temperature_2m: 28 } }).humidity, null);
  assert.throws(() => normalizeWeather({ current: { temperature_2m: null } }));
});
test("Air quality data requires at least one numeric reading", () => {
  assert.equal(normalizeAir({ current: { european_aqi: 38, pm2_5: null } }).aqi, 38);
  assert.throws(() => normalizeAir({ current: { european_aqi: null, pm2_5: null } }));
});
test("European AQI bands", () => {
  assert.equal(aqiCategory(20), "good");
  assert.equal(aqiCategory(40), "fair");
  assert.equal(aqiCategory(100), "veryPoor");
  assert.equal(aqiCategory(130), "extremelyPoor");
  assert.equal(aqiCategory(null), "unknown");
});
test("WMO weather codes", () => {
  assert.equal(weatherCategory(0), "clear");
  assert.equal(weatherCategory(3), "overcast");
  assert.equal(weatherCategory(95), "thunder");
  assert.equal(weatherCategory(999), "unknown");
});
