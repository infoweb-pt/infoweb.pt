/**
 * Free tools hub — category filters + search (EN / PT index pages).
 */
(function () {
  const grid = document.getElementById("tools-grid");
  if (!grid) return;

  const items = Array.from(grid.querySelectorAll("[data-tool-item]"));
  const searchInput = document.getElementById("tools-search");
  const filterButtons = Array.from(document.querySelectorAll("[data-tool-filter]"));
  const visibleCountEl = document.getElementById("tools-visible-count");
  const totalCountEl = document.getElementById("tools-total-count");
  const emptyEl = document.getElementById("tools-empty");

  let activeCategory = "all";
  let searchQuery = "";

  if (totalCountEl) totalCountEl.textContent = String(items.length);

  function normalize(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function setFilterActive(btn) {
    const on = btn.dataset.toolFilter === activeCategory;
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.classList.toggle("border-signal/70", on);
    btn.classList.toggle("bg-slate-800", on);
    btn.classList.toggle("text-white", on);
    btn.classList.toggle("border-slate-700", !on);
    btn.classList.toggle("bg-slate-900/50", !on);
    btn.classList.toggle("text-slate-400", !on);
  }

  function applyFilters() {
    const q = normalize(searchQuery.trim());
    let visible = 0;

    items.forEach((li) => {
      const categories = (li.dataset.toolCategories || "").split(/\s+/).filter(Boolean);
      const matchCategory = activeCategory === "all" || categories.includes(activeCategory);
      const haystack = normalize(li.dataset.toolSearch || "");
      const matchSearch = !q || haystack.includes(q);
      const show = matchCategory && matchSearch;

      li.classList.toggle("hidden", !show);
      if (show) visible += 1;
    });

    if (visibleCountEl) visibleCountEl.textContent = String(visible);
    if (emptyEl) emptyEl.classList.toggle("hidden", visible > 0);
  }

  searchInput?.addEventListener("input", (event) => {
    searchQuery = event.target.value;
    applyFilters();
  });

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      activeCategory = btn.dataset.toolFilter || "all";
      filterButtons.forEach(setFilterActive);
      applyFilters();
    });
  });

  filterButtons.forEach(setFilterActive);
  applyFilters();
})();
