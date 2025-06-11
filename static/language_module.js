// language_module.js

const supportedLanguages = {
  en: "English",
  es: "Español",
  fr: "Français",
  de: "Deutsch",
  it: "Italiano",
  pt: "Português",
  hi: "हिन्दी",
  zh: "中文",
  ja: "日本語",
  ru: "Русский",
  sv: "Svenska",
  ar: "العربية",
  ko: "한국어"
};

// Called on load to populate dropdown
function populateLanguageSelector(selectId = "language") {
  const select = document.getElementById(selectId);
  for (const [code, name] of Object.entries(supportedLanguages)) {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = name;
    select.appendChild(option);
  }
}

// Gets selected language value
function getSelectedLanguage(selectId = "language") {
  const select = document.getElementById(selectId);
  return select ? select.value : "en";
}
