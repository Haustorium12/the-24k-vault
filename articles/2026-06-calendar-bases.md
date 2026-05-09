# Calendar Bases

> 24K Featured -- June 2026
>
> [**Calendar Bases**](https://github.com/edrickleong/obsidian-calendar-bases) by [@edrickleong](https://github.com/edrickleong)
> Community plugin · 61K downloads · MIT license · Requires Obsidian 1.9+ with Bases enabled

---

## What we tested

Calendar Bases is a community plugin that registers a calendar view type with the Obsidian Bases API. When you enable it, any `.base` file can be switched to a calendar view where notes appear as events on a monthly or weekly grid, positioned by a configurable date property.

We tested it across two vault configurations over several sessions:

**Vault 1: Content calendar.** ~200 notes tagged as posts, articles, and drafts, each with a `publish-date` frontmatter property. The editorial use case — you want to see what is scheduled for the next four weeks and move things around.

**Vault 2: Task and project notes.** ~350 notes with mixed property usage. Some have `due`, some have `date`, some have neither. The realistic vault, not the tutorial screenshot vault.

What we exercised hands-on:

- Installing the plugin and switching an existing base to calendar view
- Configuring which property drives date positioning (`date`, `due`, `publish-date`)
- Dragging notes between dates in monthly and weekly views
- Observing frontmatter updates after drag operations
- Creating a base with filters active and switching to calendar view
- Testing with notes that lack the configured date property
- Combining with Bases formula properties
- Weekly vs. monthly view switching

What we did not test: multi-property event display (start + end date as duration), recurring events, time-of-day positioning within weekly view.

---

## Walk-around

Installation follows the standard community plugin route: Settings → Community Plugins → Browse, search "Calendar Bases," install, enable. No additional setup. The plugin registers itself with the Bases API on startup — there is no configuration panel, no sidebar item, nothing new in the interface. The entry point is the same one Bases already has.

The calendar view appears when you open a `.base` file and click the view switcher. Before Calendar Bases, you had four options: table, cards, list, map. After installation, you have five. The calendar icon sits at the end of the row.

First click: a monthly calendar grid rendered inside the base file. Notes with a recognized date property appear as events on the correct date. Notes without the configured property do not appear — same behavior as every other Bases view, just now expressed as absence from the calendar rather than absence from a table row.

The immediate impression is that it looks right. The event blocks show the note title. The grid is clean. Dates with multiple events stack vertically. Navigation arrows move between months. The rendering is native to Obsidian's UI kit — it does not feel like an embedded web widget.

The moment the plugin earns its 61K downloads is the first drag. Click an event block, hold, drag it to a different date, release. The frontmatter `date` property of the underlying note updates immediately and silently. No modal, no confirmation dialog, no save step. The calendar reflects the new date. The frontmatter is already written.

---

## The calendar view

Calendar Bases renders two view types: monthly (the default) and weekly. Monthly shows a standard 7-column grid with all visible dates for the current month plus the trailing days of the previous month and the leading days of the next. Weekly shows a 7-column view of a single week.

Event display is minimal by design. Each event shows the note title. There is no subtitle, no property preview, no color coding by property value. If you want to see properties, you switch back to table or cards view. The calendar is for spatial overview and rescheduling — not for reading note content.

The date property that drives positioning is configurable via the base file itself. By default, Calendar Bases looks for a property named `date`. You can change this in the base settings panel (the same gear icon that controls columns in table view). Any frontmatter property that holds a valid date string will work: `due`, `publish-date`, `scheduled`, `created`.

Multi-day events are not supported in the current release. A note positions on a single date, the start of its date property value. Notes with a `start` and `end` property do not span across the calendar grid. This is a meaningful limitation for project planning use cases where duration matters.

Date properties must be in a format Bases recognizes: ISO 8601 (`2026-06-15`), or a format matching Obsidian's built-in date picker. Freeform strings ("next Tuesday," "June 15th") do not parse and the note is silently excluded from the calendar.

---

## Drag-to-reschedule

This is the feature. Everything else in Calendar Bases is presentation. Drag-to-reschedule is the reason the plugin has 61K downloads for a tool that adds one view type.

The mechanism is straightforward: dragging an event to a new date writes the new date value to the note's frontmatter and re-renders the calendar to reflect the move. The write happens synchronously — by the time your cursor lifts from the drag, the underlying markdown file has been updated.

What makes this genuinely useful rather than merely interesting: it eliminates a multi-step workflow. Without Calendar Bases, rescheduling a note in Obsidian means opening the note, finding the frontmatter, editing the date value, confirming the format is correct, closing the note, and mentally re-situating in the calendar view you were looking at. With Calendar Bases, it is a drag. The cognitive overhead of the rescheduling step drops to near zero.

For content calendars, editorial pipelines, weekly planning systems, and task management built on frontmatter properties — this single interaction is the unlock. We moved 23 items across a three-week content calendar in about four minutes. The equivalent operation in a table view (open each note, edit `publish-date`, close) would have taken significantly longer and, more importantly, would have broken spatial reasoning about the schedule mid-task.

The behavior when dragging onto a date that already has events: the note is added to that date and both events appear stacked. There is no conflict detection, no warning about overloaded dates. You can stack as many notes on a single date as you want; the calendar shows them all.

The behavior when you drag a note that has no configured date property: nothing happens. You cannot drag a propertyless note onto the calendar to assign it a date. The note must already have the property in its frontmatter. This is the one drag interaction that does not work and it is easy to run into in mixed-structure vaults.

---

## Integration with Bases

Calendar Bases inherits the full filter and formula layer from Bases. A calendar view renders the same set of notes as the active base — if the base has a `status == "scheduled"` filter, the calendar shows only scheduled notes. If the base has a `tags contains "work"` filter, the calendar shows only work-tagged notes.

This makes the calendar view composable with the rest of Bases in a way that standalone calendar plugins are not. You are not looking at all your notes on a calendar — you are looking at a filtered, formula-enriched subset of your notes on a calendar. The editorial calendar that only shows posts with `status == "draft" OR status == "scheduled"`. The project calendar that only shows notes tagged to a specific client. The personal calendar that only shows items where a computed formula property indicates the due date is within the next 14 days.

The interaction between Bases formulas and calendar positioning is the sleeper feature. You can define a formula property that computes a derived date — add 7 days to a `draft-date` to compute `review-due`, for instance — and configure Calendar Bases to position events on the formula property rather than the raw frontmatter date. The calendar then reflects derived schedules, not just raw data.

One limitation: computed formula properties are read-only. You can position events on a formula property, but drag-to-reschedule only writes to raw frontmatter properties. Dragging an event positioned by a formula property does nothing. This is the expected behavior given how Bases formulas work, but it means the drag interaction is only available when you are positioning events on a real frontmatter property.

---

## Road test

**Vault 1 (content calendar, ~200 notes).** Created a base with a `publish-date IS NOT EMPTY` filter and switched to calendar view. 34 notes appeared as events across three months. Monthly view gave an immediate spatial sense of the schedule: three weeks in April were dense, a week in May was empty.

Moved five items across the calendar to redistribute the load. Total time: under two minutes. The frontmatter updates were instantaneous and accurate. Switched back to table view to verify — all five notes showed the updated `publish-date` values. Switched back to calendar. The move was clean.

One note had `publish-date: TBD` in its frontmatter. It did not appear in the calendar. Not a Calendar Bases issue — Bases itself cannot parse `TBD` as a date value — but it is a reminder that the calendar is only as complete as your data.

**Vault 2 (project notes, mixed structure).** Created a base with a `due IS NOT EMPTY` filter. 67 notes appeared. The calendar immediately surfaced a clustering problem: 14 items were due on a single Friday, which had not been visible in table view because the table was sorted by title, not by due date.

Attempted to drag one of the 14 items to the following Monday. The drag worked and the frontmatter updated. Then discovered that three items had `due: 2026-06-5` (missing leading zero on the day) rather than `due: 2026-06-05`. These did not render in the calendar at all. Corrected the formatting manually; they appeared. Obsidian's date picker writes ISO 8601 correctly; the malformed values came from notes edited by hand in a text editor. Calendar Bases is strict about format — it is the strictest signal you will get about date property quality in your vault.

---

## Test data

| Metric | Value |
|---|---|
| Obsidian version required | 1.9.0+ (Bases must be enabled) |
| Plugin download count | 61K |
| License | MIT |
| View types added | 2 (monthly calendar, weekly calendar) |
| Date property support | Any valid ISO 8601 frontmatter property |
| Drag-to-reschedule | Yes (writes to frontmatter immediately) |
| Multi-day event support | No (single-date positioning only) |
| Integrates with Bases filters | Yes (full filter/formula inheritance) |
| Can position on formula properties | Yes (display only; drag does not write) |
| Notes without date property | Silently excluded from calendar |
| Color coding by property | No |
| Installation required | Yes (community plugin) |
| Cost | Free (MIT) |

---

## What we liked

**Drag-to-reschedule actually works.** This sounds like a low bar, but it is not. Drag interactions in Obsidian plugins have a history of being janky, losing track of cursor position, or requiring a refresh to reflect updates. Calendar Bases' drag writes immediately, re-renders immediately, and does not lose state. It feels like a native interaction because it behaves like one.

**Full Bases filter inheritance.** The calendar view is not a bolt-on calendar that shows all your notes. It shows the output of your base — filtered, formula-enriched, scoped. This makes it genuinely composable with the rest of your Bases setup. Your editorial calendar is already half-built if you have a content-tracking base; switching to calendar view is one click.

**61K downloads for good reasons.** The plugin is popular because the use case is real and the implementation is solid. There are no major stability issues, no breakage after Obsidian updates, no abandoned-plugin smell. The GitHub repository shows active maintenance.

**Zero configuration.** Install, enable, open a base, switch to calendar view. Nothing to configure before it works. The property mapping uses the Bases settings panel you already know. The plugin does not add its own settings screen.

**Correct handling of the Bases API.** Calendar Bases is one of the first community plugins to ship using the official Bases extension API rather than hacking around it. This means it inherits Bases improvements automatically as Obsidian updates. It is not going to break when Bases gets a new filter type or formula function.

---

## What needs work

**No multi-day event support.** A note has one date. It appears on one day. For tasks with a deadline, this is fine. For projects or events with a duration — a conference spanning three days, a writing sprint with a start and end date — the calendar cannot represent the span. You see the start date only. This is the most significant missing capability for project-management use cases.

**No color coding.** Every event block is the same color. You cannot configure Calendar Bases to color events by `status`, `tag`, `project`, or any other property. On a dense calendar, everything looks the same. Distinguishing scheduled posts from published posts from draft-in-progress requires switching back to table view. Color coding by a property value is table stakes for calendar tools; its absence is felt quickly on any moderately complex calendar.

**Silently excludes notes with malformed or missing date properties.** This is consistent with how Bases handles missing properties, but it means the calendar is an unreliable source of truth if your date properties are inconsistent. There is no "notes excluded from this view: 12" indicator — the exclusions are invisible. You can have a genuine scheduling gap in your calendar and not know whether it is real or an artifact of missing frontmatter.

**No time-of-day support in weekly view.** The weekly view is a date grid, not a time grid. You cannot position events at 9am vs. 2pm. For any workflow where time-of-day matters — meeting scheduling, blocked focus time, daily planning with specific time slots — the calendar cannot represent this. It is a date planner, not a time planner.

**Drag only works within the visible date range.** To move an event to a date outside the current month or week view, you have to navigate to the target period first and then drag from within memory. You cannot drag "off the edge" of the calendar and have it advance the view. In practice this means multi-month reschedules require switching to table view, editing the property, and coming back — which defeats the purpose of the drag interaction for anything beyond the current visible range.

---

## Compared to...

**vs. the Obsidian Calendar plugin (liamcain).** The original Calendar plugin (4.3M downloads) adds a sidebar calendar for navigating daily notes — clicking a date opens or creates a daily note. It does not display arbitrary notes as events. It does not drag-to-reschedule. It is a navigation tool, not a scheduling tool. The use cases do not overlap.

**vs. Full Calendar.** Full Calendar is a community plugin that embeds a full FullCalendar.js instance in the vault with support for iCal subscriptions, all-day and timed events, and real calendar protocol integration. It is the plugin for users who want a genuine calendar application inside Obsidian — synced with Google Calendar, displayed with time blocks, importable from .ics files. Calendar Bases and Full Calendar solve different problems. Calendar Bases is for organizing and scheduling notes you already have in your vault. Full Calendar is for managing a calendar that happens to live in Obsidian.

**vs. Tasks plugin with timeline view.** The Tasks plugin manages checklist tasks across the vault with a sophisticated query language and, in recent versions, a Gantt-style timeline view. Calendar Bases is not a task manager — it surfaces any note with a date property, not just tasks. The use cases overlap at the "what is due this week" level but diverge quickly. Tasks is for task management; Calendar Bases is for note scheduling.

---

## The bigger picture

Calendar Bases is a demonstration of the Bases extension API working as designed. It did not require Obsidian to ship a calendar view. A community maintainer registered a new view type against the public API, and now every base file in every Obsidian vault with the plugin installed has a calendar view. The platform grew a capability without the core team shipping a feature.

This is the pattern that makes Bases more than a Dataview alternative. Bases is a structured data layer with a public extension API. Calendar Bases, Kanban Bases View, and the plugins that follow them are building the application layer on top of that infrastructure. Each new view type makes all your existing bases more capable retroactively.

The 61K download count before the plugin is even a year old reflects something real about where Obsidian's community is going. People have been building structured vault systems for years with Dataview queries and manual table management. Calendar Bases gives them the one interaction that raw data cannot — the ability to see their notes spatially across time and reorganize them with a gesture.

We picked Calendar Bases as June's 24K Featured because it is the most compelling demonstration of what Bases enables that was not possible before Obsidian 1.9. The plugin is not the story. The API it is built on is.

---

**Plugin:** [github.com/edrickleong/obsidian-calendar-bases](https://github.com/edrickleong/obsidian-calendar-bases)
**Downloads:** 61K
**License:** MIT
**Requires:** Obsidian 1.9.0+ with Bases core plugin enabled
**Related plugins:** [Kanban Bases View](https://github.com/xiwcx/obsidian-bases-kanban) · [Bases docs](https://obsidian.md/help/bases)
**Featured:** June 2026

*The 24K Vault Featured Pick for June 2026. Selection criteria are documented in [CONTRIBUTING.md](../CONTRIBUTING.md#featured-pick-monthly). Past picks are archived in [FEATURED.md](../FEATURED.md). Tested hands-on by 24K Labs in real Obsidian vaults on 2026-05-03.*
