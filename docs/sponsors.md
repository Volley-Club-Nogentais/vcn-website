# Adding, removing, or editing sponsors

The scrolling "Nos sponsors" band above the footer is configured entirely in the Hugo site configuration - it is **not**
editable through the `/admin` CMS interface (there is no sponsors collection in `static/admin/config.yaml`). Changes go
directly in Git, like the gyms list (see [Adding a new gym](gyms.md)).

## Where sponsors are defined

### 1. The list - `config/_default/params.yaml`

Each sponsor is one entry in the `sponsors` list, read by
[layouts/partials/sponsors.html](../layouts/partials/sponsors.html):

```yaml
sponsors:
  - name: 'Nom du sponsor' # Displayed as the logo's alt text and as a tooltip on hover
    logo: 'mon-logo.svg' # Filename under assets/media/sponsors/ (SVG or PNG, transparent background recommended)
    url: 'https://example.com' # Optional - if present, the logo links to the sponsor's site in a new tab
```

- `name` - used for accessibility (the logo's `alt` text) and as the tooltip shown on hover.
- `logo` - **just the filename**, not a path. The file must live in `assets/media/sponsors/`.
- `url` - optional. Omit it for a sponsor without a website; the logo is then rendered without a link.

The `sponsors` key is currently commented out with placeholder entries (`logoipsum-*.svg`) in `params.yaml` - uncomment
and replace it with the real sponsors, and delete the placeholder SVGs from `assets/media/sponsors/` once done.

### 2. The logo files - `assets/media/sponsors/`

Logos are plain image files committed in this folder. The `assets` tree is mounted as static passthrough in
`config/_default/config.yaml`, so any file committed here is published as-is at `/media/sponsors/<filename>` - no build
step or upload needed, just commit the file.

## Adding a sponsor

1. Add the logo file to `assets/media/sponsors/` (SVG preferred, PNG works too; transparent background recommended -
   every logo is rendered on a fixed-size white card, so a solid background will show as a rectangle).
2. In `config/_default/params.yaml`, add an entry to the `sponsors` list (creating the list if it's still commented
   out), pointing `logo` at the filename you just added.
3. Commit the logo and the config change together and open a PR.
4. Once merged, the logo appears at the end of the band on the live site (the display order is the order of the entries
   in the list).

## Editing a sponsor

- **Name or URL** - change the corresponding field in `params.yaml`; no file to touch.
- **Logo** - either replace the file in `assets/media/sponsors/` (keeping the same filename is fine) or commit a new
  file and update the `logo` field. If you replace a file, delete the old one only if nothing else references it.

## Removing a sponsor

1. Delete the sponsor's entry from the `sponsors` list in `config/_default/params.yaml`.
2. Delete its logo file from `assets/media/sponsors/` if no other sponsor still uses it.
3. Commit both changes together and open a PR.

## Behavior worth knowing

- **Empty list** - when `sponsors` is empty or missing, the whole band (title, logos, script) is not rendered at all.
- **Missing logo file** - a `logo` pointing at a file that isn't in `assets/media/sponsors/` produces a build warning
  (`sponsors.html: logo not found for sponsor ...`) and the sponsor is silently skipped on the page. Check the CI build
  logs if a sponsor disappears.
- **Scrolling** - the band only animates when the logos together are wider than the viewport (measured at runtime by
  `assets/js/sponsors-marquee.js`); with few or narrow logos it renders as a static, centered row. That's expected, not
  a bug.
- **Fixed-size cards** - every logo is fit into a white card (roughly 80x144px on mobile, 96x176px on desktop) without
  being stretched, so wide logos are shrunk. Aim for roughly 4:3 logos to use the card space well.
