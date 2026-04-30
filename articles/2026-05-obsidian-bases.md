# Obsidian Bases

> 24K Featured -- May 2026
>
> [**Bases**](https://obsidian.md/help/bases) — Obsidian core plugin
> Shipped in Obsidian 1.9.0 (Catalyst, August 2025) · Public release: Obsidian 1.9.10+ · Free, built-in, no install required · Open `.base` file format

---

## What we tested

Spent two evenings across different vault types putting Bases through real work -- not the demo vault Obsidian ships, not a purpose-built toy setup, but two vaults that have been accumulating notes for years and have the kind of structural mess that only time can produce.

**Vault 1: Reading list + research.** ~400 notes with consistent `status`, `author`, `tags`, `date-read`, and `rating` frontmatter properties. The kind of vault where Dataview queries have been accumulating since 2022 and half of them are broken because the author changed their property naming convention twice.

**Vault 2: Project tracking.** ~180 notes. Mixed structure: some notes have full frontmatter, some have one or two properties, some have none. The realistic vault -- the kind most people actually have, not the kind tutorial screenshots show.

What we exercised hands-on:

- Creating a base from scratch (both the file command and the inline code block approach)
- Table view with custom column selection, sorting, and filtering
- Cards view with cover image display
- List view with grouped properties
- Formula properties: computed fields using date arithmetic, string operations, and conditional logic
- Filter expressions: combining property comparisons with boolean operators
- The `this.file.path` self-reference pattern for single-note context windows
- Inline base embeds (`![[reading-list.base]]`) inside regular notes
- The `.base` file format directly (opened in a text editor)
- Bases API interaction via a community plugin (Calendar Bases)
- The limit of Bases: what it can and cannot query compared to Dataview

What we did not test: map view (requires geographic data in properties), the full range of built-in functions beyond the ~8 we exercised directly, vault-wide performance at scale (>2,000 notes).

---

## Walk-around

Bases is not announced when you install Obsidian 1.9+. It shows up as a new core plugin in Settings → Core Plugins, disabled by default. You enable it, and then -- nothing visible happens. No new sidebar panel. No modal. No walkthrough. The feature exists but the entry point is invisible until you know to look for it.

The entry point is the command palette. `Bases: Create new base` creates a `.base` file and opens it. `Bases: Insert new base` creates a `.base` file and drops an embed link (`![[Untitled.base]]`) into your current note.

First impression of a fresh base: an empty table with a single column, "File," listing every note in your vault. All of them. In alphabetical order. The table is sortable, filterable, and has inline editing -- you can click a cell and edit a property value without opening the underlying note. But at this moment it looks like a slightly worse version of the file browser.

The moment it becomes something different is when you add a filter. Click the filter icon, type `status == "reading"`, press Enter. The table snaps to showing only notes where the `status` property equals "reading." The other 380 notes disappear. The remaining 23 notes all have their properties editable inline. You have just built a reading dashboard with no code, no plugin installation, and no DataviewJS.

That's the walk-around moment. Not the empty table. The filter.

---

## The .base file format

One of Bases' most important design decisions is invisible to users who never open the `.base` file directly. It is worth making visible.

A `.base` file is valid YAML. Open one in any text editor:

```yaml
filters:
  - type: property
    property: status
    operator: "=="
    value: reading

properties:
  - id: file.name
    label: Title
  - id: author
    label: Author
  - id: date-read
    label: Date Read
  - id: rating
    label: Rating

views:
  - type: table
    name: Reading List

formulas:
  - id: days-since-read
    label: Days Since Read
    expression: "dateDiff(today(), date(props['date-read']), 'days')"
```

The implications of this:

**Portability.** A `.base` file is a plain text document. It survives the plugin being removed, Obsidian being uninstalled, or the format being superseded. You can version-control it with Git, diff it, merge it, and read it in any text editor. Compare this to Dataview queries, which live as code blocks inside markdown notes and have no independent file existence.

**Shareability.** You can share a `.base` file the same way you share a note -- attach it to a message, commit it to a public vault, fork it from GitHub. The query is separable from the data it queries.

**Embeddability.** Because `.base` files are first-class vault citizens, you can embed them inside any regular note with `![[reading-list.base]]`. The base renders inline with full interactivity -- sortable columns, filterable rows, inline editing -- without the note "becoming" a database. The note is still a note. The base is a lens.

**Community plugin API.** The Bases API (publicly documented as of 1.9.x) lets community plugins register new view types and interact with base data programmatically. Calendar Bases, Kanban Bases View, and several other plugins have already built on this API to add calendar, kanban, and map views that the core plugin does not ship. This is the extension model working as designed.

---

## View types

Bases ships with four built-in view types. Each view is a different way to render the same underlying set of filtered, formula-enriched notes.

**Table.** The default. Notes as rows, properties as columns. Columns are selectable, reorderable, and sortable. Each cell is editable inline. Supports column-level sorting (click the header) and global filtering. This is where you live most of the time.

**Cards.** Notes as cards in a grid. Each card shows the note title, a configurable set of properties, and optionally a cover image pulled from an `image` or `cover` property (local file path or URL). Good for reading lists, recipe collections, project boards, or anything where you want a visual catalog rather than a dense table.

**List.** Notes as a flat list with a subset of properties displayed per item. Supports grouping by a property value -- group by `status`, and you get sections ("reading," "done," "want-to-read") with the notes in each group listed below the header. This is the closest Bases gets to Dataview's `LIST` query output, but cleaner and without the code.

**Map.** Notes plotted on a geographic map based on a location property. Not tested here (our vaults do not have geographic data), but the view type is real and functional for vaults that do -- travel notes, location-tagged research, place-based reading.

Community plugins add to this list. Calendar Bases (from the Visualization section of the 24K Vault's directory) adds a calendar view that lets you drag notes to reschedule by updating their `date` property. Kanban Bases View adds a drag-and-drop board. The extension surface is public and documented.

---

## Formulas

Formulas are Bases' most powerful and least-explored capability. They let you define computed properties that appear as columns in table view (or fields in cards/list) and can also be used in filter expressions.

The formula syntax is an expression language with 15+ built-in functions. The categories:

**Date functions:** `date()`, `today()`, `now()`, `dateDiff()`, `dateAdd()`, `dateFormat()`. The most common use case: `dateDiff(today(), date(props['date-read']), 'days')` gives you days since you read something. `dateAdd(date(props['due']), 7, 'days')` gives you a buffer date.

**String functions:** `concat()`, `upper()`, `lower()`, `trim()`, `contains()`, `startsWith()`, `length()`, `replace()`. `concat(props['author'], " (", dateFormat(date(props['date-read']), 'YYYY'), ")")` builds a display string combining two properties.

**Conditional logic:** `if(condition, truePart, falsePart)`. `if(props['rating'] >= 4, "Recommend", "Skip")` adds a derived recommendation column based on a numeric rating. Conditions can nest.

**Math:** `round()`, `floor()`, `ceil()`, `abs()`, `min()`, `max()`. Useful for normalizing numeric properties or deriving scores.

**List functions:** `list()`, `length()`, `contains()`. For multi-value properties (tags, categories), `length(list(props['tags']))` counts how many tags a note has.

The `this.file.path` self-reference deserves special mention. A formula or filter can reference `this.file.path` -- the path of the note that *contains* the base embed, not the notes the base is querying. This means you can build a base that shows only information relevant to the current note:

```yaml
filters:
  - type: formula
    expression: "props['related-to'] == this.file.name"
```

Embedded in a project note, this base shows only notes that have `related-to: [project name]` in their frontmatter -- a dynamic backlinks panel built without code. The self-reference pattern opens up a whole class of "contextual base" use cases that do not have an equivalent in Dataview without DataviewJS.

---

## Road test

**Vault 1 (reading list + research).** The base took about four minutes to set up from scratch: create file, add a `status == "reading"` filter, select five columns (File, author, date-started, pages-remaining, rating), switch to cards view to see covers. The result replaced a Dataview query that had been in the vault for two years and broken twice during Obsidian major version updates.

The inline editing was immediately useful. Updating `status` from "reading" to "done" directly in the table removed the note from the filtered view on the next render -- no need to open the note, find the frontmatter, edit it, close. Multiply this by 23 active reading items and the friction reduction is real.

The formula test: added a `days-since-started` column using `dateDiff(today(), date(props['date-started']), 'days')`. Sorted by this column. Immediately surfaced three books that had been "reading" status for 90+ days -- the vault equivalent of stale issues in a GitHub project. The computed sort column did something the raw data could not: it made the implicit visible.

The cards view with covers worked correctly for the ~60% of notes that had an `image` property populated. The remaining 40% showed a blank card header. This is a data quality issue, not a Bases issue, but it is a reminder that Bases surfaces the state of your frontmatter honestly -- garbage in, garbage out.

**Vault 2 (project tracking, mixed structure).** This is where Bases showed its limit clearly. A base filtered to `status == "active"` returned 34 notes. Correct. But a significant portion of the vault's project notes had no `status` property at all -- they were excluded from the base entirely, not shown with a blank status value. Bases only queries notes that have the property it is filtering on. Notes without the property are invisible to the base.

Dataview handles this differently: a `WHERE status = "active"` query returns empty/null for notes without `status`, which you can then explicitly exclude. Bases has no "WHERE property exists" filter (as of 1.9.x). The workaround is to ensure property consistency across your vault -- which is the right answer, but it means Bases creates a forcing function that Dataview did not.

---

## Test data

| Metric | Value |
|---|---|
| Obsidian version required | 1.9.0+ (Catalyst August 2025, public August 2025) |
| Setup time (first base) | Under 5 minutes |
| File format | `.base` (valid YAML) |
| Built-in view types | 4 (table, cards, list, map) |
| Built-in formula functions | 15+ |
| Community plugin views available | 3+ (calendar, kanban, gallery variants) |
| Inline editing | Yes (table and cards) |
| Embeddable in regular notes | Yes (`![[name.base]]`) |
| Can query note body content | No (properties/frontmatter only) |
| Can query inline Dataview fields | No |
| DataviewJS equivalent | No (formula language, not scripting) |
| Installation required | No (core plugin, enable in Settings) |
| Cost | Free |

---

## What we liked

**The file format.** `.base` files being valid YAML is the right call for a tool that is supposed to live in your vault long-term. The format is human-readable, version-controllable, and independent of the plugin. We opened a `.base` file in VS Code, edited the filter expression directly, saved, and watched Obsidian update the rendered view immediately. No round-trips through a UI.

**Inline editing.** The ability to update property values directly in the base table without opening the underlying note is a genuine quality-of-life improvement. For workflows that involve reviewing a set of notes and updating their status, category, or rating, this is significantly faster than the Dataview approach (which generates a read-only table by default, requiring a DataviewJS query with inline field modification for editing support).

**The formula self-reference (`this.file.path`).** This unlocks a whole class of contextual views that are genuinely novel. A base that shows "notes related to the current note" embedded in a project page is something Dataview cannot do cleanly without DataviewJS. The fact that it works by embedding a base file rather than writing code makes it accessible to non-programmers.

**No-code baseline.** The explicit design goal of "no programming knowledge required" is real. Table, cards, filter by property value, sort by property value -- all of this works through a point-and-click interface. The formula language is learnable but also optional. A user who never writes a formula can still get substantial value from Bases as a query-and-view layer over their vault.

**The extension API.** The Bases API is documented and community plugins are already using it. The ecosystem of view types is growing. Calendar Bases in particular is immediately useful for any vault with date-based notes -- the ability to drag a note to a different date and have the `date` property update automatically is a genuine UX leap over editing frontmatter manually.

**Performance.** On Vault 1 (400 notes), table rendering was instant. Sort operations were fast. The formula column (`dateDiff`) computed without perceptible lag. Obsidian's native implementation is significantly faster than Dataview's JavaScript-based index, which matters at scale.

---

## What needs work

**No query over note body content.** Dataview's most powerful feature is the ability to query the content of notes, not just their properties. You can find every note that contains a specific heading, every task in a specific section, every inline `field:: value` annotation. Bases cannot do any of this. It is a property-only query tool. For users who have invested in Dataview's inline field syntax, Bases is not a replacement -- it is a parallel system that covers a different surface area.

**Missing notes are invisible, not blank.** Notes without a queried property do not appear in the base with a blank value -- they do not appear at all. This is a meaningful difference from Dataview's behavior and it creates a footgun: a base filtered to `status == "active"` will silently omit every note that has never had a `status` property set. There is no "show notes where property is missing" option. The workaround is vault-wide property hygiene via a tool like Metadata Menu, but Bases itself gives no indication when notes are being silently excluded.

**No text-search filter.** You cannot filter a base to "notes where the title contains [string]" or "notes where any property contains [string]." Filters are property-value comparisons, not text searches. For exploration queries ("show me everything tagged 'ai' written after 2024"), this is adequate. For ad-hoc searches, you still need Omnisearch or the built-in search panel.

**Formula documentation is sparse.** The built-in function reference exists in Obsidian Help, but the examples are minimal. Discovering that `this.file.path` exists as a self-reference, or that `list()` is needed to iterate over multi-value properties, required reading community forum posts rather than documentation. The function library is good; the docs around it need a second pass.

**Cards view cover image is property-dependent.** Cover images in cards view require a specific property (by default `image` or `cover`) to be populated with a local file path or URL. There is no "use the first image found in the note" fallback. For vaults that do not have image properties, cards view looks bare.

**No computed properties in filter expressions (yet).** You can define a formula property and display it as a column, but you cannot filter on a formula property's output in the current release. `days-since-read > 30` as a filter does not work -- you compute the value as a column, then sort by it manually to find the stale items. This is a known limitation that the Obsidian team has flagged as in-progress.

---

## Compared to...

**vs. Dataview.** This is the comparison that matters most for existing Obsidian power users, so it deserves a full treatment.

Dataview (4.02M downloads) is a third-party plugin that turns your vault into a queryable database using a SQL-like syntax (DQL) and a JavaScript API (DataviewJS). It has been the standard for structured vault queries since 2021.

Bases is Obsidian's official answer to the same problem class. It is not designed to replace Dataview. The two tools have genuinely different capabilities:

| Capability | Dataview | Bases |
|------------|---------|-------|
| Query note body content | Yes | No |
| Query inline fields | Yes | No |
| Query frontmatter properties | Yes | Yes |
| Require programming knowledge | For complex queries | No |
| Inline editing of results | DataviewJS only | Yes (native) |
| Shareable query files | No (embedded in notes) | Yes (.base files) |
| Performance at scale | Slower (JS index) | Faster (native index) |
| Community extension API | Limited | Yes (view types) |
| Formula/computed properties | DataviewJS | Yes (formula language) |
| Filter on computed properties | DataviewJS | Not yet |

The honest recommendation: if your vault uses inline fields (`author:: Tolkien`), if you have complex multi-table queries, or if you have existing DataviewJS dashboards that work -- keep Dataview. It is not going away, and Bases does not cover its surface area.

If you are starting fresh, building a new structured workflow, or want an alternative to Dataview for property-based views that is faster, more portable, and editable inline -- Bases is the right tool. For the majority of the actual Dataview use cases we have seen in the wild (reading lists, project status boards, habit trackers, content calendars), Bases is sufficient and noticeably more pleasant to work with.

**vs. Datacore.** Datacore is a community project (from the Dataview maintainer) that aims to be a faster, more capable successor to Dataview with a reactive component model. It is more powerful than Bases. It requires more technical comfort. It is still in active development and not yet stable. For builders who want to construct sophisticated reactive dashboards inside Obsidian and are comfortable with JavaScript, Datacore is the serious option. For everyone else, Bases is the practical one.

**vs. Notion.** This comparison comes up constantly in community discussions ("Bases replaces Notion for me") and it is worth being precise about it. Notion databases and Bases solve similar organizational problems but at different levels. Notion is a cloud SaaS product with real-time collaboration, rich content types (embeds, mentions, status automations), and a polished visual editor. Bases is a local, vault-native view layer over plain markdown files with YAML frontmatter.

What Bases has that Notion does not: your data is yours, it is offline, it is version-controllable in Git, it is stored in open formats that survive any software decision, and it integrates with the full Obsidian plugin ecosystem. What Notion has that Bases does not: multi-user real-time collaboration, relational rollup columns, formula support across linked databases, and years of UI polish.

If you were using Notion as a lightweight personal database and lost sync access or simply wanted to keep your structured data in the same tool as your notes -- Bases handles that workload well. If you were using Notion for team project management with collaborators -- Bases is not a substitute.

---

## The bigger picture

Obsidian's design philosophy has always been: your data in open formats, your workflow your own, no lock-in. Bases extends that philosophy to structured data. The `.base` file format is not a proprietary binary. It is YAML. It will be readable in 2040. The notes it queries are plain markdown. The properties it surfaces are standard YAML frontmatter.

The contrast with every cloud-based "knowledge management" tool is not incidental. It is the point. Bases is Obsidian's answer to Notion, Airtable, and Coda at the personal-knowledge layer -- not by matching their feature sets (it does not), but by offering the same core capability in a format that you own and a tool that is free.

For users who have been waiting for Obsidian to close the "I need a database in my notes" gap without leaving the vault or learning JavaScript -- this is it. It is not complete (the body-content query gap is real, the filter-on-formula limitation is real), but the architecture is right and the extension API means the missing views are already appearing in the community plugin directory.

We picked Bases as May's 24K Featured because it is the most significant structural addition to Obsidian in years. Not a plugin someone built. Not a workaround. A core feature, built by the Obsidian team, that changes what the tool is. PDF++ (April's pick) was about what community maintainers can accomplish when they take a problem seriously. Bases is about the platform itself growing up.

---

**Feature:** [help.obsidian.md/bases](https://obsidian.md/help/bases)
**Changelog:** [Obsidian 1.9.0](https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/)
**Forum discussion:** [forum.obsidian.md](https://forum.obsidian.md)
**Related plugins:** [Calendar Bases](https://github.com/edrickleong/obsidian-calendar-bases) · [Kanban Bases View](https://github.com/xiwcx/obsidian-bases-kanban)
**License:** Proprietary (Obsidian core, free to use)
**Featured:** May 2026

*The 24K Vault Featured Pick for May 2026. Selection criteria are documented in [CONTRIBUTING.md](../CONTRIBUTING.md#featured-pick-monthly). Past picks are archived in [FEATURED.md](../FEATURED.md). Tested hands-on by 24K Labs in real Obsidian vaults on 2026-04-30.*
