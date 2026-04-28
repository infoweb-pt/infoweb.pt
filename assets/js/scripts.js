const SUPPORTED_LANGUAGES = ["en", "pt"];
const DEFAULT_LANGUAGE = "en";
const LANGUAGE_STORAGE_KEY = "infoweb-language";

const getNestedValue = (source, path) =>
  path.split(".").reduce((value, key) => (value ? value[key] : undefined), source);

const getPreferredLanguage = () => {
  const storedLanguage = localStorage.getItem(LANGUAGE_STORAGE_KEY);

  if (SUPPORTED_LANGUAGES.includes(storedLanguage)) {
    return storedLanguage;
  }

  const browserLanguage = navigator.language?.slice(0, 2).toLowerCase();
  return SUPPORTED_LANGUAGES.includes(browserLanguage) ? browserLanguage : DEFAULT_LANGUAGE;
};

const fetchTranslations = async (language) => {
  const response = await fetch(`locales/${language}.json`);

  if (!response.ok) {
    throw new Error(`Missing translation file for "${language}"`);
  }

  return response.json();
};

const translateTextNodes = (translations) => {
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const translation = getNestedValue(translations, element.dataset.i18n);

    if (typeof translation === "string") {
      element.textContent = translation;
    }
  });
};

const translateHtmlNodes = (translations) => {
  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    const translation = getNestedValue(translations, element.dataset.i18nHtml);

    if (typeof translation === "string") {
      element.innerHTML = translation;
    }
  });
};

const translateAttributes = (translations) => {
  document.querySelectorAll("[data-i18n-attr]").forEach((element) => {
    const attributes = element.dataset.i18nAttr.split(";");

    attributes.forEach((entry) => {
      const [attribute, path] = entry.split(":");
      const translation = getNestedValue(translations, path);

      if (attribute && typeof translation === "string") {
        element.setAttribute(attribute, translation);
      }
    });
  });
};

const updateLanguageControls = (language) => {
  document.documentElement.lang = language;

  document.querySelectorAll("[data-lang]").forEach((button) => {
    const isActive = button.dataset.lang === language;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
};

const applyLanguage = async (language) => {
  const safeLanguage = SUPPORTED_LANGUAGES.includes(language) ? language : DEFAULT_LANGUAGE;
  const translations = await fetchTranslations(safeLanguage);

  translateTextNodes(translations);
  translateHtmlNodes(translations);
  translateAttributes(translations);
  updateLanguageControls(safeLanguage);
  localStorage.setItem(LANGUAGE_STORAGE_KEY, safeLanguage);
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => {
      applyLanguage(button.dataset.lang).catch(() => applyLanguage(DEFAULT_LANGUAGE));
    });
  });

  applyLanguage(getPreferredLanguage()).catch(() => applyLanguage(DEFAULT_LANGUAGE));
});
