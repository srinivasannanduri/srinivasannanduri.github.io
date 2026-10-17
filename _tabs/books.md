---
icon: fas fa-book
order: 1
---

Books that shaped how I think about systems, teams and leadership, with a short note on who should read each one.
<!-- TODO: add "My full reading history is on [Goodreads](<profile URL>)." once the link is known -->

{% assign reading = site.data.books | where: "status", "reading" %}
{% assign recommended = site.data.books | where: "recommend", true %}
{% assign shelves = recommended | map: "shelf" | uniq | sort %}

{% if reading.size > 0 %}
## Currently reading

<div class="bookshelf">
{% for book in reading %}{% include book-card.html book=book %}{% endfor %}
</div>
{% endif %}

{% for shelf in shelves %}
## {{ shelf }}

{% assign books = recommended | where: "shelf", shelf %}
<div class="bookshelf">
{% for book in books %}{% include book-card.html book=book %}{% endfor %}
</div>
{% endfor %}
