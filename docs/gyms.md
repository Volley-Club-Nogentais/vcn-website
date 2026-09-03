# Adding a new gym for training sessions

Training sessions ("entraînements") are attached to a **gym**, and each team's schedule references a gym by a short
slug. The list of gyms is defined in exactly two places that must be kept in sync: the Hugo site configuration, and the
Sveltia CMS admin configuration. This page explains both.

## Where gyms are defined

### 1. Hugo config - `config/_default/params.yaml`

The canonical list of gyms, used by the templates to render addresses and group training sessions:

```yaml
gyms:
  - slug: 'maudry'
    name: 'Maudry'
    address: '5-7 rue Jean Monnet, 94130 Nogent-sur-Marne'
  - slug: 'watteau'
    name: 'Watteau'
    address: '37 rue Lequesne, 94130 Nogent-sur-Marne'
  - slug: 'louis-armand'
    name: 'Louis Armand'
    address: '173 Bd de Strasbourg, 94130 Nogent-sur-Marne'
```

This is what [layouts/equipes/page.html](../layouts/equipes/page.html) (a team's own training schedule) and
[layouts/partials/training-sessions.html](../layouts/partials/training-sessions.html) (the aggregated "who trains where"
list on the Contact page) use to turn a `gym: "watteau"` slug in a team's `schedule` into a display name and a "Voir sur
la carte" Google Maps link (built from `address`).

### 2. Sveltia CMS config - `static/admin/config.yaml`

The `equipes` collection's `schedule` field has a `gym` select with the same gyms **hardcoded as options**, so editors
get a dropdown instead of typing a slug by hand:

```yaml
- label: 'Gymnase'
  name: 'gym'
  widget: 'select'
  options:
    - { label: 'Maudry', value: 'maudry' }
    - { label: 'Watteau', value: 'watteau' }
    - { label: 'Louis Armand', value: 'louis-armand' }
```

This list is **not** read from `params.yaml` - Sveltia (like Decap CMS before it) can't pull select options from the
Hugo site config at build time, so it has to be duplicated by hand.

## Adding a new gym

To add a gym (say, "Marne"), update both files:

1. **`config/_default/params.yaml`** - append an entry to `gyms`:

   ```yaml
   gyms:
     - slug: 'maudry'
       name: 'Maudry'
       address: '5-7 rue Jean Monnet, 94130 Nogent-sur-Marne'
     - slug: 'watteau'
       name: 'Watteau'
       address: '37 rue Lequesne, 94130 Nogent-sur-Marne'
     - slug: 'louis-armand'
       name: 'Louis Armand'
       address: '173 Bd de Strasbourg, 94130 Nogent-sur-Marne'
     - slug: 'marne'
       name: 'Marne'
       address: '1 rue de la Marne, 94130 Nogent-sur-Marne'
   ```

2. **`static/admin/config.yaml`** - add the matching option under the `equipes` collection's `schedule.gym` field:

   ```yaml
   options:
     - { label: 'Maudry', value: 'maudry' }
     - { label: 'Watteau', value: 'watteau' }
     - { label: 'Louis Armand', value: 'louis-armand' }
     - { label: 'Marne', value: 'marne' }
   ```

   `value` **must** exactly match the `slug` used in `params.yaml` - that's the string stored in each team's
   `schedule[].gym`, and it's how the templates in step 1 look up the gym's name and address. `label` is just what
   editors see in the dropdown, and can read however you like.

3. Commit both changes together (they're two files but one logical change) and open a PR - this is site configuration,
   not content, so it's edited directly in Git rather than through `/admin`.

4. Once merged, the new gym is selectable from the **Gymnase** dropdown when editing a team's **Entraînements**
   (`schedule`) field in the CMS (see [Adding or editing a team](editing-pages.md#adding-or-editing-a-team-équipes)),
   and will appear automatically on the Contact page's training-sessions list once at least one team schedules a session
   there.

## Removing or renaming a gym

Don't change or remove a `slug` that's still referenced by a team's `schedule[].gym` - templates fall back to displaying
the raw slug (with no address or map link) if it doesn't match any entry in `gyms`. Check existing team front matter
under `content/equipes/*/index.fr.md` first, and update every reference before renaming a slug.
