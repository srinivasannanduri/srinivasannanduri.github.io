---
icon: fas fa-book
order: 1
---

{% assign gr = site.data.goodreads %}
{% assign hidden = site.data.goodreads_hide %}

Books that shaped how I think about systems, teams and leadership. I've logged {{ gr.read.size }} books on [Goodreads]({{ gr.profile }}); this page shows what I'm reading now, the ones I recommend, and what I finished recently.

{% assign shown = 0 %}
{% capture reading_cards %}{% for book in gr.currently_reading %}{% unless hidden contains book.id %}{% include book-card.html book=book %}{% assign shown = shown | plus: 1 %}{% endunless %}{% endfor %}{% endcapture %}
{% if shown > 0 %}
## Currently reading

<div class="bookshelf">
{{ reading_cards }}
</div>
{% endif %}

{% assign shelves = site.data.books | map: "shelf" | uniq | sort %}
{% for shelf in shelves %}
## {{ shelf }}

{% assign books = site.data.books | where: "shelf", shelf %}
<div class="bookshelf">
{% for book in books %}{% include book-card.html book=book %}{% endfor %}
</div>
{% endfor %}

## Five-star reads

<ul class="reading-log">
{% assign shown = 0 %}{% for book in gr.read %}{% if shown < 12 and book.rating == 5 %}{% unless hidden contains book.id %}{% include reading-row.html book=book %}{% assign shown = shown | plus: 1 %}{% endunless %}{% endif %}{% endfor %}
</ul>

## Recently read

<ul class="reading-log">
{% assign shown = 0 %}{% for book in gr.read %}{% if shown < 15 %}{% unless hidden contains book.id %}{% include reading-row.html book=book %}{% assign shown = shown | plus: 1 %}{% endunless %}{% endif %}{% endfor %}
</ul>

[Full reading history on Goodreads →]({{ gr.profile }})

<p class="reading-updated">Goodreads shelves last synced {{ gr.updated | date: "%-d %b %Y" }}.</p>
