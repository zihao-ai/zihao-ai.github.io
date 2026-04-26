const blogPagePosts = window.SITE_BLOG_POSTS || [];

function postUrl(post) {
  return `post.html?slug=${encodeURIComponent(post.slug)}`;
}

function sortedPosts() {
  return [...blogPagePosts].sort((a, b) => new Date(`${b.date}T00:00:00Z`) - new Date(`${a.date}T00:00:00Z`));
}

function postCard(post, options = {}) {
  const tagHtml = (post.tags || []).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("");

  return `
    <article class="${options.featured ? "blog-card blog-card-featured" : "blog-card"}">
      <a href="${postUrl(post)}" aria-label="Read ${escapeHtml(post.title)}">
        <div class="blog-card-body">
          <time datetime="${escapeHtml(post.date)}">${formatDate(post.date)}</time>
          <h2>${escapeHtml(post.title)}</h2>
          <p>${escapeHtml(post.description || "")}</p>
          <div class="blog-card-tags">${tagHtml}</div>
        </div>
      </a>
    </article>
  `;
}

function renderBlogTags(activeTag = "") {
  const target = document.querySelector("[data-blog-tags]");
  if (!target) return;

  const tags = [...new Set(blogPagePosts.flatMap((post) => post.tags || []))].sort((a, b) => a.localeCompare(b));
  target.innerHTML = [
    `<button type="button" class="${activeTag ? "" : "is-active"}" data-blog-tag="">All</button>`,
    ...tags.map(
      (tag) =>
        `<button type="button" class="${activeTag === tag ? "is-active" : ""}" data-blog-tag="${escapeHtml(tag)}">${escapeHtml(tag)}</button>`,
    ),
  ].join("");
}

function renderBlogPage() {
  const featuredTarget = document.querySelector("[data-featured-post]");
  const listTarget = document.querySelector("[data-blog-list]");
  if (!featuredTarget || !listTarget) return;

  const search = document.querySelector("[data-blog-search]");
  let activeTag = "";

  const applyFilters = () => {
    const query = (search?.value || "").trim().toLowerCase();
    const posts = sortedPosts().filter((post) => {
      const tags = post.tags || [];
      const haystack = [post.title, post.description, tags.join(" ")].join(" ").toLowerCase();
      return (!query || haystack.includes(query)) && (!activeTag || tags.includes(activeTag));
    });

    const featured = posts.find((post) => post.featured) || posts[0];
    const rest = featured ? posts.filter((post) => post.slug !== featured.slug) : posts;

    featuredTarget.innerHTML = featured ? postCard(featured, { featured: true }) : "";
    listTarget.innerHTML = rest.length
      ? rest.map((post) => postCard(post)).join("")
      : featured
        ? ""
        : `<p class="empty-state">No posts match the current filters.</p>`;
    renderBlogTags(activeTag);
    renderIcons();
  };

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-blog-tag]");
    if (!button) return;
    activeTag = button.dataset.blogTag || "";
    applyFilters();
  });

  search?.addEventListener("input", applyFilters);
  applyFilters();
}

function stripFrontMatter(markdown) {
  return markdown.replace(/^---[\s\S]*?---\s*/, "");
}

function slugifyHeading(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/<[^>]+>/g, "")
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function rewriteRelativeImages(container, markdownPath) {
  const basePath = markdownPath.split("/").slice(0, -1).join("/");
  container.querySelectorAll("img").forEach((image) => {
    const src = image.getAttribute("src") || "";
    if (!src || /^(https?:|data:|\/)/i.test(src)) return;
    image.setAttribute("src", `${basePath}/${src}`);
    image.loading = "lazy";
  });
}

function buildTableOfContents(container) {
  const toc = document.querySelector("[data-post-toc]");
  if (!toc) return;

  const headings = [...container.querySelectorAll("h2, h3")];
  if (!headings.length) {
    toc.innerHTML = "";
    toc.hidden = true;
    return;
  }

  headings.forEach((heading) => {
    if (!heading.id) heading.id = slugifyHeading(heading.textContent || "");
  });

  toc.hidden = false;
  toc.innerHTML = `
    <p>On this page</p>
    <nav>
      ${headings
        .map((heading) => `<a class="toc-${heading.tagName.toLowerCase()}" href="#${escapeHtml(heading.id)}">${escapeHtml(heading.textContent || "")}</a>`)
        .join("")}
    </nav>
  `;
}

async function renderPostPage() {
  const body = document.querySelector("[data-post-body]");
  if (!body) return;

  const slug = new URLSearchParams(window.location.search).get("slug");
  const post = blogPagePosts.find((item) => item.slug === slug) || sortedPosts()[0];

  if (!post) {
    body.innerHTML = `<p class="empty-state">No blog posts are available yet.</p>`;
    return;
  }

  document.title = `${post.title} | Zihao Zhu`;
  document.querySelector("[data-post-title]").textContent = post.title;
  document.querySelector("[data-post-date]").textContent = formatDate(post.date);
  document.querySelector("[data-post-description]").textContent = post.description || "";
  document.querySelector("[data-post-tags]").innerHTML = (post.tags || []).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("");

  try {
    const response = await fetch(post.file);
    if (!response.ok) throw new Error(`Could not load ${post.file}`);

    const markdown = stripFrontMatter(await response.text());
    marked.setOptions({ gfm: true, breaks: false });
    body.innerHTML = DOMPurify.sanitize(marked.parse(markdown), {
      ADD_ATTR: ["target", "loading"],
    });

    rewriteRelativeImages(body, post.file);
    buildTableOfContents(body);

    renderMathInElement(body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false },
        { left: "$", right: "$", display: false },
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
      throwOnError: false,
    });

    body.querySelectorAll("pre code").forEach((block) => hljs.highlightElement(block));
    body.querySelectorAll("a[href^='http']").forEach((link) => {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    });
  } catch (error) {
    body.innerHTML =
      window.location.protocol === "file:"
        ? `<p class="empty-state">Markdown posts cannot be loaded from a file:// URL. Please run <code>python3 -m http.server 8000</code> in the site folder and open <code>http://localhost:8000/post.html?slug=${escapeHtml(post.slug)}</code>.</p>`
        : `<p class="empty-state">This post could not be loaded. Please try again later.</p>`;
    console.error(error);
  }
}

renderBlogPage();
renderPostPage();
