# Changing the monthly logo

The logo shown at the top-left of every page (next to "VCN" in the navbar) automatically changes depending on the
current calendar month. This is used, for example, to switch to the beach volley logo over the summer, or to a special
edition for a given month (e.g. Pink October).

## How it works

The logic lives in [layouts/partials/header.html](../layouts/partials/header.html):

```go-html-template
{{ $monthAsIndex := math.Sub (time.Now.Month | int) 1 }}
{{ $logoPath := printf "media/%s" (index .Site.Params.logo $monthAsIndex) }}
```

`time.Now.Month` returns the current month as a number (1 for January, 12 for December). The template subtracts 1 to get
a 0-based index, then picks that entry from the `logo` list in `config/_default/params.yaml`. That file is a plain,
ordered list of 12 filenames - one per month, January first:

```yaml
logo:
  # January to May
  - logo_couleur.svg
  - logo_couleur.svg
  - logo_couleur.svg
  - logo_couleur.svg
  - logo_couleur.svg
  # June to August
  - beach_logo_color.svg
  - beach_logo_color.svg
  - beach_logo_color.svg
  # September
  - logo_couleur.svg
  # October
  - logo_rose.svg
  # November
  - logo_couleur.svg
  # December
  - logo_couleur.svg
```

Each filename must exist as a static asset under `assets/media/` (e.g. `logo_rose.svg` is
[assets/media/logo_rose.svg](../assets/media/logo_rose.svg)) - the template resolves it via
`resources.Get "media/<filename>"`.

There is one exception: on any page under `/beach/`, the beach logo (`beach_logo_color.svg`) is always shown, overriding
the month-based choice. This keeps the beach volleyball section visually consistent regardless of the time of year.

## Changing the logo for a given month

1. Make sure the logo file you want exists in `assets/media/` (upload it there, or add it via a PR - this isn't exposed
   in the Sveltia CMS admin UI, since it's a site-wide setting rather than page content).
2. Edit `config/_default/params.yaml` and replace the filename at the position for that month (remember: the list is
   1-indexed by month but 0-indexed in the file - the first entry is January, the tenth is October, etc.). The inline
   comments (`# January to May`, `# October`, ...) mark the boundaries to make this easier to get right.
3. Commit and open a PR (or push directly if you have access) - this is a Hugo configuration file, not content, so it
   isn't editable through `/admin`.
4. Preview locally with `docker compose up` (see [README.md](../README.md#getting-started)) and check the navbar logo.
   To preview a month other than the current one without waiting, you can temporarily change your system clock, or
   temporarily edit the `$monthAsIndex` line in `header.html` to a fixed value and revert it before committing.

## Available logo variants

The existing files under `assets/media/` you can reuse:

- `logo_couleur.svg` - main color logo (indoor volleyball).
- `logo_rose.svg` - pink variant (currently used for October).
- `logo_black.svg` / `logo_white.svg` - monochrome variants.
- `beach_logo_color.svg` / `beach_logo_black.svg` / `beach_logo_blue.svg` / `beach_logo_white.svg` - beach volleyball
  logo variants.

Add a new SVG file to `assets/media/` if you need a variant that doesn't exist yet.
