const SUPPORTED_LANGUAGES = ["en", "pt"];
const DEFAULT_LANGUAGE = "en";
const LANGUAGE_STORAGE_KEY = "infoweb-language";

const getNestedValue = (source, path) =>
  path.split(".").reduce((value, key) => (value ? value[key] : undefined), source);

const getPreferredLanguage = () => {
  const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY);
  if (SUPPORTED_LANGUAGES.includes(stored)) return stored;
  const browser = navigator.language?.slice(0, 2).toLowerCase();
  return SUPPORTED_LANGUAGES.includes(browser) ? browser : DEFAULT_LANGUAGE;
};

const fetchTranslations = async (language) => {
  const response = await fetch(`../locales/${language}.json`);
  if (!response.ok) throw new Error(`Missing translation file for "${language}"`);
  return response.json();
};

const translateTextNodes = (translations) => {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const value = getNestedValue(translations, el.dataset.i18n);
    if (typeof value === "string") el.textContent = value;
  });
};

const translateAttributes = (translations) => {
  document.querySelectorAll("[data-i18n-attr]").forEach((el) => {
    el.dataset.i18nAttr.split(";").forEach((entry) => {
      const [attr, path] = entry.split(":");
      const value = getNestedValue(translations, path);
      if (attr && typeof value === "string") el.setAttribute(attr, value);
    });
  });
};

const updateLanguageControls = (language) => {
  document.documentElement.lang = language;
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    const active = btn.dataset.lang === language;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-pressed", String(active));
  });
};

const applyLanguage = async (language) => {
  const safe = SUPPORTED_LANGUAGES.includes(language) ? language : DEFAULT_LANGUAGE;
  const translations = await fetchTranslations(safe);
  translateTextNodes(translations);
  translateAttributes(translations);
  updateLanguageControls(safe);
  localStorage.setItem(LANGUAGE_STORAGE_KEY, safe);
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    btn.addEventListener("click", () => {
      applyLanguage(btn.dataset.lang).catch(() => applyLanguage(DEFAULT_LANGUAGE).catch(() => {}));
    });
  });

  applyLanguage(getPreferredLanguage()).catch(() => applyLanguage(DEFAULT_LANGUAGE).catch(() => {}));

  document.getElementById("year").textContent = new Date().getFullYear();
});
