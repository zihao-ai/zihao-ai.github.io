---
layout: page
permalink: /publications/
title: Publications
description: 

nav: true
nav_order: 1
years: [2025,2024, 2023, 2022, 2021, 2020]
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->


<div class="publications">


<p>An up-to-date list is available on <a href="https://scholar.google.com/citations?user=11025211AAAAJ&hl=en">Google Scholar</a>.</p>
<br>

{% for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>