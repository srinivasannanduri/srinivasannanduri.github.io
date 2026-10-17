# srinivasannanduri.github.io

Personal site of Srinivasan Nanduri: profile, blog and book recommendations.
Built with [Jekyll](https://jekyllrb.com) and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme, restyled after bloomcode.github.io (grid paper, sheets, Archivo and IBM Plex).

## Where things live

| What | Where |
|---|---|
| Site title, links, avatar | `_config.yml`, `_data/contact.yml` |
| Blog posts | `_posts/YYYY-MM-DD-title.md` |
| Unpublished drafts | `_drafts/` |
| Book picks | `_data/books.yml` |
| Goodreads shelves (synced nightly) | `_data/goodreads.json`, `tools/goodreads_sync.py` |
| Books hidden from the page | `_data/goodreads_hide.yml` |
| Hidden sections and panels | top of `_sass/sheets.scss` |
| About page | `_tabs/about.md` |
| Colours, fonts and layout styling | `_sass/sheets.scss` |

## Write a post

1. Copy `_drafts/example-book-notes.md` to `_posts/2026-10-20-my-title.md`.
2. Fill in the front matter (`title`, `date`, `categories`, `tags`, `description`) and write in Markdown.
3. Commit and push. The site rebuilds in a couple of minutes.

## Add a book

Add an entry to `_data/books.yml`. Set `recommend: true` and a `shelf` to show it on the Books page,
or `status: reading` to show it under "Currently reading". Write the `note` in your own words.

## Content rules

- Nothing confidential from IBM or past employers: no figures, team sizes, costs or internal project details.
- No copied text from books beyond a short quote. Notes are in your own words.

## Preview locally

The Mac's built-in Ruby is too old, so the site runs in a container:

```bash
podman machine start
podman run --rm -it -p 4000:4000 -v "$PWD":/srv/site -w /srv/site docker.io/library/ruby:3.4 \
  bash -c "bundle config set path vendor/bundle && bundle install && bundle exec jekyll serve -H 0.0.0.0 --drafts"
```

Then open http://localhost:4000.

## Publishing

Pushing to `master` runs `.github/workflows/pages-deploy.yml`, which builds the site and deploys it to GitHub Pages.
One-time setup: in the repository on GitHub, go to **Settings → Pages** and set **Source** to **GitHub Actions**.
