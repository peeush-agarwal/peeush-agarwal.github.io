---
layout: default
title: Home
---

<h1>All Pages</h1>

<label for="tag-filter">Filter by tag:</label>
<select id="tag-filter">
  <option value="">All</option>
  {% assign all_tags = site.pages | map: "tags" | join: "," | split: "," | uniq | sort %}
  {% for tag in all_tags %}
    {% if tag != "" %}
      <option value="{{ tag | strip }}">{{ tag | strip }}</option>
    {% endif %}
  {% endfor %}
</select>

<ul id="page-feed">
  {% for page in site.pages %}
    {% if page.title and page.tags %}
      <li data-tags="{{ page.tags | join: ',' }}">
        <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
        <span>Tags: {{ page.tags | join: ', ' }}</span>
      </li>
    {% endif %}
  {% endfor %}
</ul>

<script>
  const filter = document.getElementById('tag-filter');
  filter.addEventListener('change', function() {
    const selected = this.value;
    document.querySelectorAll('#page-feed li').forEach(li => {
      if (!selected || li.dataset.tags.includes(selected)) {
        li.style.display = '';
      } else {
        li.style.display = 'none';
      }
    });
  });
</script>
