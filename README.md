# srinivasannanduri.github.io

Personal site of Srinivasan Nanduri: a rolling list of writing, with tags, and an About page.
Built with [Jekyll](https://jekyllrb.com) and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme, restyled after bloomcode.github.io (grid paper, sheets, Archivo and IBM Plex).

## Where things live

| What | Where |
|---|---|
| Site title, avatar | `_config.yml` |
| Top-bar icons (LinkedIn, X, Goodreads, RSS) | `_data/contact.yml` |
| Top bar (photo, name, icons), no sidebar | `_includes/topbar.html`, `_includes/sidebar.html` |
| Blog posts | `_posts/YYYY-MM-DD-title.md` |
| Unpublished drafts | `_drafts/` |
| About page | `_tabs/about.md` |
| Colours, fonts and layout styling | `_sass/sheets.scss` |

## Write a post

1. Copy `_drafts/example-book-notes.md` to `_posts/2026-10-20-my-title.md`.
2. Fill in the front matter (`title`, `date`, `categories`, `tags`, `description`) and write in Markdown.
3. Commit and push. The site rebuilds in a couple of minutes.

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
