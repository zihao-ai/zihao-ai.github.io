const year = document.querySelector("[data-year]");
const toggle = document.querySelector("[data-theme-toggle]");
const root = document.documentElement;
const publications = window.SITE_PUBLICATIONS || [];
const news = window.SITE_NEWS || [];

const linkIcons = {
  paper: "file-text",
  code: "github",
  project: "globe",
  dataset: "database",
  slides: "presentation",
};

const linkLabels = {
  paper: "Paper",
  code: "Code",
  project: "Project",
  dataset: "Dataset",
  slides: "Slides",
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${value}T00:00:00Z`));
}

function newsText(item) {
  const links = item.links?.length
    ? ` ${item.links
        .map((link) => `<a href="${escapeHtml(link.href)}">${escapeHtml(link.label)}</a>`)
        .join(" ")}`
    : "";

  return `${escapeHtml(item.text)}${links}`;
}

function highlightAuthor(name) {
  return name === "Zihao Zhu" ? `<strong>${escapeHtml(name)}</strong>` : escapeHtml(name);
}

function publicationLinks(links = {}) {
  return Object.entries(links)
    .filter(([, href]) => Boolean(href))
    .map(([kind, href]) => {
      const icon = linkIcons[kind] || "external-link";
      const label = linkLabels[kind] || kind;
      if (icon === "github") {
        return `<a href="${escapeHtml(href)}"><iconify-icon icon="simple-icons:github" aria-hidden="true"></iconify-icon>${escapeHtml(label)}</a>`;
      }
      return `<a href="${escapeHtml(href)}"><i class="icon" data-lucide="${icon}" aria-hidden="true"></i>${escapeHtml(label)}</a>`;
    })
    .join("");
}

function topicTags(paper, activeTopic = "") {
  if (!paper.topics?.length) return "";

  return `
    <div class="paper-topics" aria-label="Topics">
      ${paper.topics
        .map(
          (topic) =>
            `<button type="button" class="${activeTopic === topic ? "is-active" : ""}" data-topic-filter="${escapeHtml(topic)}">${escapeHtml(topic)}</button>`,
        )
        .join("")}
    </div>
  `;
}

function publicationItem(paper, options = {}) {
  const showTopics = Boolean(options.showTopics);
  const activeTopic = options.activeTopic || "";
  return `
    <article class="publication" data-year="${paper.year}" data-type="${escapeHtml(paper.type)}">
      <div class="venue-badge">
        <strong>${escapeHtml(paper.venue)}</strong>
        <span>${paper.year}</span>
      </div>
      <div class="paper-body">
        <h3>${escapeHtml(paper.title)}</h3>
        <p class="authors">${paper.authors.map(highlightAuthor).join(", ")}</p>
        <p class="paper-meta">${publicationLinks(paper.links)}</p>
        ${showTopics ? topicTags(paper, activeTopic) : ""}
      </div>
    </article>
  `;
}

function renderIcons() {
  window.lucide?.createIcons();
}

function sortPublications(items) {
  return [...items].sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
}

function renderHome() {
  const preview = document.querySelector("[data-publications-preview]");
  if (preview) {
    preview.innerHTML = sortPublications(publications)
      .filter((paper) => paper.selected)
      .map(publicationItem)
      .join("");
  }

  const newsPreview = document.querySelector("[data-news-preview]");
  if (newsPreview) {
    newsPreview.innerHTML = [...news]
      .sort((a, b) => new Date(`${b.date}T00:00:00Z`) - new Date(`${a.date}T00:00:00Z`))
      .slice(0, 10)
      .map(
        (item) => `
          <li>
            <time datetime="${escapeHtml(item.date)}">${formatDate(item.date)}</time>
            <p>${newsText(item)}</p>
          </li>
        `,
      )
      .join("");
  }
}

function renderPublicationYears(items, options = {}) {
  const years = [...new Set(items.map((paper) => paper.year))].sort((a, b) => b - a);
  return years
    .map((pubYear) => {
      const yearItems = items.filter((paper) => paper.year === pubYear);
      const rows = yearItems.map((paper) => publicationItem(paper, { showTopics: true, activeTopic: options.activeTopic })).join("");
      return `
        <section class="year-group" data-year-group="${pubYear}">
          <div class="year-heading">
            <h2>${pubYear}</h2>
            <span>${yearItems.length} ${yearItems.length === 1 ? "paper" : "papers"}</span>
          </div>
          <div class="publication-list">${rows}</div>
        </section>
      `;
    })
    .join("");
}

function renderPublicationYearTabs(activeYear = "all") {
  const yearTabs = document.querySelector("[data-year-tabs]");
  if (!yearTabs) return;

  const years = [...new Set(publications.map((paper) => paper.year))].sort((a, b) => b - a);
  const buttons = [
    `<button type="button" class="${activeYear === "all" ? "is-active" : ""}" data-year-tab="all">All</button>`,
    ...years.map(
      (pubYear) =>
        `<button type="button" class="${String(activeYear) === String(pubYear) ? "is-active" : ""}" data-year-tab="${pubYear}">${pubYear}</button>`,
    ),
  ];

  yearTabs.innerHTML = buttons.join("");
}

function bindPublicationYearTabs(onChange) {
  const yearTabs = document.querySelector("[data-year-tabs]");
  if (!yearTabs) return;

  yearTabs.addEventListener("click", (event) => {
    const button = event.target.closest("[data-year-tab]");
    if (!button) return;
    onChange(button.dataset.yearTab || "all");
  });
}

function getTopicCounts() {
  const counts = new Map();
  publications.forEach((paper) => {
    paper.topics.forEach((topic) => {
      counts.set(topic, (counts.get(topic) || 0) + 1);
    });
  });

  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

function renderPublicationTopicTabs(activeTopic = "") {
  const topicTabs = document.querySelector("[data-topic-tabs]");
  if (!topicTabs) return;

  topicTabs.innerHTML = getTopicCounts()
    .map(
      ([topic]) =>
        `<button type="button" class="${activeTopic === topic ? "is-active" : ""}" data-topic-filter="${escapeHtml(topic)}">${escapeHtml(topic)}</button>`,
    )
    .join("");
}

function bindPublicationTopicFilters(onChange) {
  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-topic-filter]");
    if (!button) return;
    onChange(button.dataset.topicFilter || "");
  });
}

function activeYearLabel(activeYear) {
  return activeYear === "all" ? "All years" : String(activeYear);
}

function renderFilteredYearHeading(items, activeYear, activeTopic = "") {
  if (activeYear === "all") return renderPublicationYears(items, { activeTopic });

  return `
    <section class="year-group" data-year-group="${activeYear}">
      <div class="year-heading">
        <h2>${activeYearLabel(activeYear)}</h2>
        <span>${items.length} ${items.length === 1 ? "paper" : "papers"}</span>
      </div>
      <div class="publication-list">${items.map((paper) => publicationItem(paper, { showTopics: true, activeTopic })).join("")}</div>
    </section>
  `;
}

function renderPublicationsPage() {
  const list = document.querySelector("[data-publications-list]");
  const count = document.querySelector("[data-publication-count]");
  if (!list) return;

  const search = document.querySelector("[data-publication-search]");
  let activeYear = "all";
  let activeTopic = "";

  const applyFilters = () => {
    const query = (search?.value || "").trim().toLowerCase();
    const filtered = sortPublications(publications).filter((paper) => {
      const haystack = [
        paper.title,
        paper.authors.join(" "),
        paper.venue,
        paper.venueFull,
        paper.topics.join(" "),
      ]
        .join(" ")
        .toLowerCase();
      return (
        (!query || haystack.includes(query)) &&
        (activeYear === "all" || String(paper.year) === activeYear) &&
        (!activeTopic || paper.topics.includes(activeTopic))
      );
    });

    list.innerHTML = filtered.length ? renderFilteredYearHeading(filtered, activeYear, activeTopic) : `<p class="empty-state">No papers match the current filters.</p>`;
    if (count) count.textContent = `${filtered.length} ${filtered.length === 1 ? "paper" : "papers"}`;
    renderPublicationTopicTabs(activeTopic);
    renderIcons();
  };

  renderPublicationYearTabs(activeYear);
  renderPublicationTopicTabs(activeTopic);
  bindPublicationYearTabs((nextYear) => {
    activeYear = nextYear;
    renderPublicationYearTabs(activeYear);
    applyFilters();
  });
  bindPublicationTopicFilters((nextTopic) => {
    activeTopic = activeTopic === nextTopic ? "" : nextTopic;
    applyFilters();
  });
  search?.addEventListener("input", applyFilters);
  applyFilters();
}

function renderNewsPage() {
  const list = document.querySelector("[data-news-list]");
  if (!list) return;

  list.innerHTML = news
    .map(
      (item) => `
        <li>
          <time datetime="${escapeHtml(item.date)}">${formatDate(item.date)}</time>
          <p>${newsText(item)}</p>
          <div class="news-tags">${(item.tags || []).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
        </li>
      `,
    )
    .join("");
}

renderHome();
renderPublicationsPage();
renderNewsPage();
renderIcons();

if (year) {
  year.textContent = new Date().getFullYear();
}

const storedTheme = window.localStorage.getItem("theme");
if (storedTheme === "dark") {
  root.dataset.theme = "dark";
}

toggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = nextTheme === "dark" ? "dark" : "";
  window.localStorage.setItem("theme", nextTheme);
});
