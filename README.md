# Zihao Zhu 的个人主页

基于 [al-folio](https://github.com/alshedivat/al-folio) 模板搭建的学术个人主页。

**网站地址**: https://zihao-ai.github.io

---

## 目录

- [快速开始](#快速开始)
- [内容修改指南](#内容修改指南)
  - [修改个人简介](#修改个人简介)
  - [添加新闻动态](#添加新闻动态)
  - [添加/修改论文](#添加修改论文)
  - [修改个人简历 (CV)](#修改个人简历-cv)
  - [修改社交链接](#修改社交链接)
  - [添加项目展示](#添加项目展示)
  - [新建博客文章](#新建博客文章)

---

## 快速开始

### 使用 Docker 启动（推荐）

**macOS 用户**: 推荐使用 [Colima](https://github.com/abiosoft/colima) 作为 Docker 运行时，相比 Docker Desktop 更轻量。

```bash
# 安装 Colima（如未安装）
brew install colima docker docker-compose

# 启动 Colima
colima start

# 设置 Docker 环境变量（首次使用需要，或添加到 ~/.zshrc 永久生效）
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"

# 拉取 Docker 镜像
docker-compose pull

# 启动本地开发服务器
docker-compose up
```

启动后访问: http://localhost:8080

支持热重载，修改文件后页面会自动刷新。

> **提示**: 下次使用时只需 `colima start` 然后 `docker-compose up` 即可。

### 本地手动启动（需要 Ruby 环境）

```bash
# 安装依赖
bundle install

# 启动开发服务器
bundle exec jekyll serve --port=8080

# 生产环境构建
JEKYLL_ENV=production bundle exec jekyll build
```

---

## 内容修改指南

### 修改个人简介

编辑 `_pages/about.md` 文件：

```yaml
---
layout: about
title: About
permalink: /
profile:
  align: right
  image: me.jpeg          # 头像图片，放在 assets/img/ 目录下
  image_circular: false   # 是否裁剪为圆形
  more_info: >
    <p>zihaozhu@link.cuhk.edu.cn</p>
selected_papers: true     # 是否显示精选论文
social: true              # 是否显示社交图标
announcements:
  enabled: true           # 是否显示新闻动态
  scrollable: true        # 新闻超过3条时是否滚动
  limit: 5                # 显示新闻条数限制
---

在这里写个人简介正文...
```

### 添加新闻动态

在 `_news/` 目录下创建新的 Markdown 文件，格式如下：

**文件名**: `announcement_X.md`（X 为数字）

```markdown
---
layout: post
date: 2025-01-15 10:00:00+0800
inline: true
related_posts: false
---

这里写新闻内容。支持 **Markdown** 格式和 <strong>HTML</strong> 标签。
```

**参数说明**:
- `date`: 新闻日期，格式为 `YYYY-MM-DD HH:MM:SS+时区`
- `inline: true`: 新闻直接显示在首页（推荐）
- `inline: false`: 新闻有单独页面，需要在正文中添加更多内容

### 添加/修改论文

编辑 `_bibliography/papers.bib` 文件，使用 BibTeX 格式：

```bibtex
@inproceedings{zhu2024vdc,
  title={VDC: Versatile Data Cleanser...},
  author={Zhu, Zihao and Zhang, Mingda and ...},
  booktitle={International Conference on Learning Representations},
  year={2024},

  % === al-folio 特殊字段 ===
  abbr={ICLR},                    % 会议/期刊缩写标签
  pdf={https://arxiv.org/pdf/...},  % PDF 链接
  code={https://github.com/...},    % 代码链接
  website={https://...},            % 项目主页
  preview={vdc.png},              % 缩略图，放在 assets/img/publication_preview/
  selected={true},                % 是否显示在首页精选论文
  bibtex_show={true},             % 是否显示 BibTeX 引用按钮

  % 可选字段
  arxiv={2309.16211},             % arXiv ID
  video={https://...},            % 视频链接
  poster={poster.pdf},            % 海报文件
  slides={slides.pdf},            % 幻灯片文件
  award={Best Paper},             % 获奖信息
  annotation={备注信息},           % 附加说明
}
```

**作者高亮**: 在 `_config.yml` 中配置你的姓名，论文列表中会自动高亮：

```yaml
scholar:
  last_name: [Zhu]
  first_name: [Zihao]
```

### 修改个人简历 (CV)

编辑 `assets/json/resume.json` 文件（JSON Resume 格式）：

```json
{
  "basics": {
    "name": "Zihao Zhu",
    "label": "Ph.D. Candidate",
    "email": "zihaozhu@link.cuhk.edu.cn",
    "summary": "简介..."
  },
  "education": [
    {
      "institution": "The Chinese University of Hong Kong, Shenzhen",
      "studyType": "Ph.D.",
      "startDate": "2021-09-01",
      "endDate": "2026-06-01",
      "courses": ["School of Data Science", "Advisor: Baoyuan Wu"]
    }
  ],
  "experience": [
    {
      "name": "Tencent AI Lab",
      "position": "Research Intern",
      "startDate": "2024-03-01",
      "endDate": "2024-07-01"
    }
  ],
  "awards": [
    {
      "title": "Guotai Junan Scholarship",
      "date": "2024-01-01",
      "awarder": "CUHK-Shenzhen"
    }
  ],
  "interests": [
    {
      "name": "Large Language Model Safety",
      "icon": "fa-solid fa-shield-halved",
      "keywords": ["Jailbreak", "Safety Alignment"]
    }
  ]
}
```

**支持的字段**: `basics`, `education`, `experience`, `awards`, `interests`, `skills`, `publications`, `languages`, `certificates`, `references`

### 修改社交链接

编辑 `_data/socials.yml` 文件：

```yaml
email: zihaozhu@link.cuhk.edu.cn
github_username: zihao-ai
scholar_userid: PnLq3EwAAAAJ      # Google Scholar ID
wechat_qr: wechat-qr.png          # 微信二维码图片，放在 assets/img/
rss_icon: true                     # 是否显示 RSS 图标

# 其他可选社交链接（取消注释即可启用）
# linkedin_username: your-linkedin
# x_username: your-twitter-handle
# orcid_id: 0000-0000-0000-0000
```

### 添加项目展示

在 `_projects/` 目录下创建新的 Markdown 文件：

**文件名**: `X_project.md`（X 为数字，决定排序）

```markdown
---
layout: page
title: 项目名称
description: 项目简介
img: assets/img/project-cover.jpg    # 封面图片
importance: 1                         # 重要性排序（数字越小越靠前）
category: work                        # 分类：work, fun 等
related_publications: true            # 是否关联相关论文
---

项目详细介绍内容...

<!-- 插入图片 -->
{% include figure.liquid path="assets/img/example.jpg" class="img-fluid rounded z-depth-1" %}
```

---

### 新建博客文章

在 `_posts/` 目录下创建新的 Markdown 文件：

**文件名格式**: `YYYY-MM-DD-文章标题.md`（如 `2025-06-01-my-first-post.md`）

```markdown
---
layout: post
title: 文章标题
date: 2025-06-01 10:00:00+0800
description: 文章简介（显示在博客列表中）
tags: tag1 tag2                  # 标签，空格分隔
categories: category-name         # 分类
featured: false                   # 是否置顶
thumbnail: assets/img/thumb.jpg   # 可选：缩略图
related_posts: true               # 是否显示相关文章
---

文章正文，支持 Markdown 格式...

<!-- 插入图片 -->
{% include figure.liquid path="assets/img/example.jpg" class="img-fluid rounded z-depth-1" %}
```

**注意事项**:
- 文件名中的日期决定文章排序，标题部分用英文和短横线（不要用空格）
- 如果 `_config.yml` 中 `collections: posts: output: false`，需要改为 `true` 才能生成博客页面

---

## 文件结构速查

```
├── _pages/about.md          # 首页个人简介
├── _news/                   # 新闻动态
├── _bibliography/papers.bib # 论文列表
├── _data/
│   └── socials.yml         # 社交链接
├── _projects/              # 项目展示
├── _posts/                 # 博客文章
├── assets/
│   ├── img/                # 图片资源
│   │   └── publication_preview/ # 论文缩略图
│   └── json/resume.json    # 个人简历（JSON Resume 格式）
└── _config.yml             # 网站配置
```

---

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

---

## 致谢

本网站基于 [al-folio](https://github.com/alshedivat/al-folio) 模板构建，感谢原作者的开源贡献。
