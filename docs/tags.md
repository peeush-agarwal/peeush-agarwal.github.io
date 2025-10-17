---
layout: default
title: Tags
---

<h1>Tags</h1>
<ul>
  {% assign tags_list = site.pages | map: "tags" | compact | uniq | sort %}
  {% for tag in tags_list %}
    {% if tag %}
      <li><a href="#{{ tag | slugify }}">{{ tag }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
