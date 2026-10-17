---
icon: fas fa-book
order: 1
---

{% assign gr = site.data.goodreads %}
{% assign hidden = site.data.goodreads_hide %}
{% assign reading_count = 0 %}{% for book in gr.currently_reading %}{% unless hidden contains book.id %}{% assign reading_count = reading_count | plus: 1 %}{% endunless %}{% endfor %}
{% assign five_star = gr.read | where: "rating", 5 %}

<div class="eyebrow">Bookshelf · synced from Goodreads</div>

Books that shaped how I think about systems, teams and leadership. This page shows what I'm reading now, the ones I recommend, and the books I rated five stars. My full history is on [Goodreads]({{ gr.profile }}).

<div class="shelf-stats"><span><b>{{ gr.read.size }}</b>read</span><span><b>{{ reading_count }}</b>reading</span><span><b>{{ five_star.size }}</b>five-star</span></div>

{% if reading_count > 0 %}
## Currently reading

<div class="bookshelf">
{% for book in gr.currently_reading %}{% unless hidden contains book.id %}{% include book-card.html book=book %}{% endunless %}{% endfor %}
</div>
{% endif %}

{% assign shelves = site.data.books | map: "shelf" | uniq | sort %}
{% for shelf in shelves %}
## {{ shelf }} picks

{% assign books = site.data.books | where: "shelf", shelf %}
<div class="bookshelf">
{% for book in books %}{% include book-card.html book=book %}{% endfor %}
</div>
{% endfor %}

## Five-star reads

<label class="shelf-filter"><i class="fas fa-search fa-fw" aria-hidden="true"></i><input id="five-star-filter" type="search" placeholder="Filter {{ five_star.size }} books by title or author" aria-label="Filter five-star reads"></label>

<ul class="reading-log" id="five-star-log">
{% for book in five_star %}{% unless hidden contains book.id %}{% include reading-row.html book=book %}{% endunless %}{% endfor %}
</ul>
<p class="shelf-empty" id="five-star-empty" hidden>No five-star book matches that filter.</p>

## Recently read

<ul class="reading-log">
{% assign shown = 0 %}{% for book in gr.read %}{% if shown < 15 %}{% unless hidden contains book.id %}{% include reading-row.html book=book %}{% assign shown = shown | plus: 1 %}{% endunless %}{% endif %}{% endfor %}
</ul>

[Full reading history on Goodreads →]({{ gr.profile }})

<p class="reading-updated">Goodreads shelves last synced {{ gr.updated | date: "%-d %b %Y" }}.</p>

<script>
  (function () {
    var input = document.getElementById('five-star-filter');
    var rows = Array.prototype.slice.call(document.querySelectorAll('#five-star-log li'));
    var empty = document.getElementById('five-star-empty');
    var shownByDefault = 12;
    function apply() {
      var q = input.value.trim().toLowerCase();
      var hits = 0;
      rows.forEach(function (row, i) {
        var match = q ? row.textContent.toLowerCase().indexOf(q) !== -1 : i < shownByDefault;
        row.hidden = !match;
        if (match) { hits += 1; }
      });
      empty.hidden = hits > 0;
    }
    input.addEventListener('input', apply);
    apply();
  })();
</script>
