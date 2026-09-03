# Managing and editing site pages

This guide is for editing the content of <https://volley-club-nogent.fr/>: pages, news, teams, and images. No coding
knowledge is required for day-to-day edits - everything below goes through the `/admin` web interface.

## The admin interface

Content is edited at <https://volley-club-nogent.fr/admin/> (or `http://localhost:1313/admin/` in local dev), powered by
**[Sveltia CMS](https://github.com/sveltia/sveltia-cms)**. Sveltia is a modern, drop-in-compatible replacement for Decap
CMS (formerly Netlify CMS): it reads the same `static/admin/config.yaml` configuration file and connects to the same
GitHub repository as its backend.

- Sign in with a GitHub account that has write access to the
  [Volley-Club-Nogentais/vcn-website](https://github.com/Volley-Club-Nogentais/vcn-website) repository.
- Every save creates a **pull request** (the "editorial workflow" - see `publish_mode: editorial_workflow` in
  `static/admin/config.yaml`) rather than writing straight to `main`. You can save a draft, come back to it later, and
  someone (or you) merges the PR on GitHub once it's ready to go live.
- Publishing a PR merges it into `main`, which triggers the production deploy (see
  [AGENTS.md](../AGENTS.md#cicd-github-actions)). There's also a preview deploy for `feat/**`/`fix/**` branches if
  you're comparing with a developer.

## What you can edit, and where it lives

The CMS collections map onto folders in `content/`. Each entry below is a Sveltia collection name, editable at
`/admin/#/collections/<name>`:

| CMS collection | What it is                                  | Source file(s)                                         |
| -------------- | ------------------------------------------- | ------------------------------------------------------ |
| `pages`        | The one-off pages (see the file list below) | `content/**/*.fr.md`                                   |
| `actualites`   | News articles                               | `content/actualites/<year>/<month>/<slug>/index.fr.md` |
| `equipes`      | Team pages (roster, schedule, gallery)      | `content/equipes/<slug>/index.fr.md`                   |

The `pages` collection groups several fixed, single-file entries - each one is a specific page rather than a list you
add to:

- **Accueil** - the homepage (`content/_index.fr.md`).
- **Le Club** - club presentation (`content/club/_index.fr.md`).
- **Histoire du club** - club history, with an image list (`content/histoire.fr.md`).
- **Mentions légales** - legal notice (`content/mentions-legales.fr.md`).
- **Contact** - contact page (`content/contact/index.fr.md`).
- **Inscriptions** - registration guide (`content/inscriptions/index.fr.md`).
- **Actualités (page d'index)** - the news section's intro text (`content/actualites/_index.fr.md`), distinct from the
  individual articles below.
- **Équipes (page d'index)** - the teams section's intro text (`content/equipes/_index.fr.md`), distinct from the
  individual team pages below.
- **Beach Volley** - the beach volley page (`content/beach/index.fr.md`).

`actualites` and `equipes` are open-ended collections: use **New actualites** / **New équipes** in the CMS to add an
entry, and each existing entry is editable individually.

## Adding a news article ("Actualités")

1. Go to `/admin/#/collections/actualites`, click **New Actualites**.
2. Fill in **Titre**, **Auteur**, **Date**, and the **Contenu** (markdown body).
3. **Résumé** is optional - if left empty, the site auto-generates one from the text before a `<!--more-->` marker in
   the body. Add `<!--more-->` in the content at the point where you want the preview/teaser to stop.
4. **Brouillon** (draft) defaults to `true` - a draft article isn't visible on the live site. Set it to `false` (or ask
   whoever reviews the PR to) once it's ready to publish.
5. Optionally add a main **Image** and **Tags**.
6. Save - this opens a PR. The article's URL is derived from its date and title (`{{year}}/{{month}}/{{slug}}`), shown
   in the CMS preview link.

## Adding or editing a team ("Équipes")

Go to `/admin/#/collections/equipes`. Each team entry has:

- **Titre**, **Résumé**, **Categories** (used for filtering/labels - FFVB, FSGT, adultes, jeunes, beach).
- **Brouillon** - like articles, a draft team isn't shown on the public teams list.
- **Positionnement** (`weight`) - controls display order on the teams list page (lower = earlier).
- **Nom du calendrier** (`calendarName`) - must exactly match an entry name in `data/calendars/` (the FFVB/FSGT match
  calendars, generated automatically - see [AGENTS.md](../AGENTS.md)) for the team's upcoming matches to show up. Leave
  empty if the team has no tracked calendar (e.g. loisir groups).
- **Image principale** and **Galerie** - team photos. If no main image is set, the site falls back to displaying the
  club's monogram instead.
- **Entraînements** (`schedule`) - one or more training sessions, each with a gym, day, and start/end time. See
  [Adding a new gym for training sessions](gyms.md) for how the gym list itself is managed - this field only lets you
  _pick_ an existing gym per session, it doesn't add new ones.
- **Contenu** - the team's markdown write-up (season recap, etc.).

## Editing images

Images uploaded through the CMS (team photos, galleries, news images) are stored under `assets/media/` in the repository
and served from `/media/`. When editing a field with an image widget, use the CMS's built-in media picker (upload
button) rather than editing files by hand.

## Editing content directly in Git (for developers)

Every field editable in the CMS is just YAML front matter plus a markdown body in a `.fr.md` file under `content/`. You
can edit these files directly and open a normal PR instead of going through `/admin` - useful for bulk changes or when
adding a field that doesn't exist in the CMS config yet. If you add or rename a front-matter field that templates in
`layouts/` rely on, update `static/admin/config.yaml` to match so the CMS keeps working for non-developer editors (see
`AGENTS.md`'s "Content editing" section).

Run the site locally to preview changes before opening a PR:

```bash
docker compose up
```

Then open <http://localhost:1313/>.
