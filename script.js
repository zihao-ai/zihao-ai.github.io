const year = document.querySelector("[data-year]");
const toggle = document.querySelector("[data-theme-toggle]");
const root = document.documentElement;
const publications = window.SITE_PUBLICATIONS || [];
const news = window.SITE_NEWS || [];
const siteBlogPosts = window.SITE_BLOG_POSTS || [];
const talks = window.SITE_TALKS || [];

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
  video: "Video",
  report: "Report",
  event: "Event",
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

function sortBlogPosts(items) {
  return [...items].sort((a, b) => new Date(`${b.date}T00:00:00Z`) - new Date(`${a.date}T00:00:00Z`));
}

function blogPostUrl(post) {
  return `post.html?slug=${encodeURIComponent(post.slug)}`;
}

function sortTalks(items) {
  return [...items].sort((a, b) => new Date(`${b.date}T00:00:00Z`) - new Date(`${a.date}T00:00:00Z`));
}

function talkLinks(links = {}) {
  const icons = {
    video: "video",
    slides: "presentation",
    report: "newspaper",
    event: "calendar",
  };

  return Object.entries(links)
    .filter(([, href]) => Boolean(href))
    .map(([kind, href]) => {
      const icon = icons[kind] || "external-link";
      const label = linkLabels[kind] || kind;
      return `<a href="${escapeHtml(href)}"><i class="icon" data-lucide="${icon}" aria-hidden="true"></i>${escapeHtml(label)}</a>`;
    })
    .join("");
}

function talkItem(talk) {
  const tags = (talk.tags || []).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("");
  const links = talkLinks(talk.links);
  return `
    <article class="talk-card">
      <div class="talk-date">
        <time datetime="${escapeHtml(talk.date)}">${formatDate(talk.date)}</time>
        ${talk.type ? `<span>${escapeHtml(talk.type)}</span>` : ""}
      </div>
      <div class="talk-body">
        <h3>${escapeHtml(talk.title)}</h3>
        <p class="talk-event">${[talk.event, talk.location].filter(Boolean).map(escapeHtml).join(" · ")}</p>
        ${talk.description ? `<p class="talk-description">${escapeHtml(talk.description)}</p>` : ""}
        ${tags ? `<div class="talk-tags">${tags}</div>` : ""}
        ${links ? `<div class="talk-links">${links}</div>` : ""}
      </div>
    </article>
  `;
}

function renderTalkYears(items) {
  const years = [...new Set(items.map((talk) => new Date(`${talk.date}T00:00:00Z`).getUTCFullYear()))].sort((a, b) => b - a);
  return years
    .map((yearValue) => {
      const yearTalks = items.filter((talk) => new Date(`${talk.date}T00:00:00Z`).getUTCFullYear() === yearValue);
      return `
        <section class="talk-year-group">
          <div class="year-heading">
            <h2>${yearValue}</h2>
            <span>${yearTalks.length} ${yearTalks.length === 1 ? "talk" : "talks"}</span>
          </div>
          <div class="talk-list">${yearTalks.map(talkItem).join("")}</div>
        </section>
      `;
    })
    .join("");
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
      .slice(0, 5)
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

  const blogPreview = document.querySelector("[data-blog-preview]");
  if (blogPreview) {
    blogPreview.innerHTML = sortBlogPosts(siteBlogPosts)
      .slice(0, 5)
      .map(
        (post) => `
          <li>
            <time datetime="${escapeHtml(post.date)}">${formatDate(post.date)}</time>
            <h3><a href="${blogPostUrl(post)}">${escapeHtml(post.title)}</a></h3>
            <p>${escapeHtml(post.description || "")}</p>
          </li>
        `,
      )
      .join("");
  }

  const talkPreview = document.querySelector("[data-talk-preview]");
  if (talkPreview) {
    const recentTalks = sortTalks(talks).slice(0, 5);
    talkPreview.innerHTML = recentTalks.length
      ? recentTalks
          .map(
            (talk) => `
              <li>
                <time datetime="${escapeHtml(talk.date)}">${formatDate(talk.date)}</time>
                <h3>${escapeHtml(talk.title)}</h3>
                <p>${[talk.event, talk.location].filter(Boolean).map(escapeHtml).join(" · ")}</p>
              </li>
            `,
          )
          .join("")
      : `<li class="empty-inline">No talks listed yet.</li>`;
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

  list.innerHTML = [...news]
    .sort((a, b) => new Date(`${b.date}T00:00:00Z`) - new Date(`${a.date}T00:00:00Z`))
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

function renderTalkTypeFilters(activeType = "") {
  const target = document.querySelector("[data-talk-types]");
  if (!target) return;

  const types = [...new Set(talks.map((talk) => talk.type).filter(Boolean))].sort((a, b) => a.localeCompare(b));
  target.innerHTML = [
    `<button type="button" class="${activeType ? "" : "is-active"}" data-talk-type="">All</button>`,
    ...types.map(
      (type) =>
        `<button type="button" class="${activeType === type ? "is-active" : ""}" data-talk-type="${escapeHtml(type)}">${escapeHtml(type)}</button>`,
    ),
  ].join("");
}

function renderTalksPage() {
  const list = document.querySelector("[data-talks-list]");
  const count = document.querySelector("[data-talk-count]");
  if (!list) return;

  const search = document.querySelector("[data-talk-search]");
  let activeType = "";

  const applyFilters = () => {
    const query = (search?.value || "").trim().toLowerCase();
    const filtered = sortTalks(talks).filter((talk) => {
      const haystack = [
        talk.title,
        talk.event,
        talk.location,
        talk.type,
        talk.description,
        (talk.tags || []).join(" "),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return (!query || haystack.includes(query)) && (!activeType || talk.type === activeType);
    });

    list.innerHTML = filtered.length ? renderTalkYears(filtered) : `<p class="empty-state">No talks match the current filters.</p>`;
    if (count) count.textContent = `${filtered.length} ${filtered.length === 1 ? "talk" : "talks"}`;
    renderTalkTypeFilters(activeType);
    renderIcons();
  };

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-talk-type]");
    if (!button) return;
    activeType = button.dataset.talkType || "";
    applyFilters();
  });

  search?.addEventListener("input", applyFilters);
  applyFilters();
}

renderHome();
renderPublicationsPage();
renderNewsPage();
renderTalksPage();
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
