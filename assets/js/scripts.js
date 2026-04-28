const SUPPORTED_LANGUAGES = ["en", "pt"];
const DEFAULT_LANGUAGE = "en";
const LANGUAGE_STORAGE_KEY = "infoweb-language";

const getNestedValue = (source, path) =>
  path.split(".").reduce((value, key) => (value ? value[key] : undefined), source);

const formatPaybackMoney = (value) => {
  const locale = document.documentElement.lang === "pt" ? "pt-PT" : "en-IE";
  const amount = Number(value);
  const fractional = Math.abs(amount - Math.round(amount)) > 1e-6;
  const minimumFractionDigits = Math.abs(amount) < 1 || fractional ? 2 : 0;

  return new Intl.NumberFormat(locale, {
    currency: "EUR",
    maximumFractionDigits: 2,
    minimumFractionDigits,
    style: "currency",
  }).format(amount);
};

const formatNumber = (value) =>
  new Intl.NumberFormat(document.documentElement.lang === "pt" ? "pt-PT" : "en-IE", {
    maximumFractionDigits: 0,
  }).format(value);

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
  updatePaybackSimulator();
};

const formatCadence = (clientsNeeded, language) => {
  if (clientsNeeded <= 1) {
    const daysBetween = Math.round(30 / Math.max(clientsNeeded, 0.001));
    return language === "pt"
      ? `1 cliente a cada ${daysBetween} dias`
      : `1 client every ${daysBetween} days`;
  }

  const daysBetween = Math.max(1, Math.round(30 / clientsNeeded));
  return language === "pt"
    ? `1 cliente a cada ${daysBetween} dias`
    : `1 client every ${daysBetween} days`;
};

const updatePaybackSimulator = () => {
  const simulator = document.querySelector("[data-payback-simulator]");

  if (!simulator) {
    return;
  }

  const planInput = simulator.querySelector('input[name="payback-plan"]:checked');
  const clientValueInput = simulator.querySelector("[data-payback-client-value-input]");
  const clientValueOutput = simulator.querySelector("[data-payback-client-value]");
  const clientsNeededOutput = simulator.querySelector("[data-payback-clients-needed]");
  const cadenceOutput = simulator.querySelector("[data-payback-cadence]");

  if (!planInput || !clientValueInput) {
    return;
  }

  const language = document.documentElement.lang === "pt" ? "pt" : "en";
  const monthlyPlanCost = Number(planInput.value);
  const clientValue = Math.max(0.5, Number(clientValueInput.value));
  const exactClientsNeeded = monthlyPlanCost / clientValue;
  const clientsNeeded = Math.max(1, Math.ceil(exactClientsNeeded));

  clientValueOutput.textContent = formatPaybackMoney(clientValue);
  clientsNeededOutput.textContent = formatNumber(clientsNeeded);
  cadenceOutput.textContent = formatCadence(clientsNeeded, language);
};

const setupPaybackSimulator = () => {
  const simulator = document.querySelector("[data-payback-simulator]");

  if (!simulator) {
    return;
  }

  simulator.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", updatePaybackSimulator);
    input.addEventListener("change", updatePaybackSimulator);
  });

  updatePaybackSimulator();
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => {
      applyLanguage(button.dataset.lang).catch(() => applyLanguage(DEFAULT_LANGUAGE));
    });
  });

  setupPaybackSimulator();
  applyLanguage(getPreferredLanguage()).catch(() => applyLanguage(DEFAULT_LANGUAGE));
});
