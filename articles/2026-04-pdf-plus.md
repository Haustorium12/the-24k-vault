# PDF++

> 24K Featured -- April 2026
>
> [**PDF++**](https://github.com/RyotaUshio/obsidian-pdf-plus) by [@RyotaUshio](https://github.com/RyotaUshio)
> 528K+ downloads · 2,178 stars · MIT licensed · Active since December 2023

---

## What we tested

Spent ~45 minutes on the home PC driving PDF++ in a real Obsidian vault. We installed it from the community plugin browser, opened Vannevar Bush's "As We May Think" (the 1945 essay that conceptually invented hyperlinked knowledge work), and put it through enough of the workflow to form an honest opinion.

What we exercised hands-on:

- Backlink highlighting in two colors (yellow + blue)
- The color palette → copy-link → paste-into-note workflow
- Reading-mode rendering of the resulting callouts
- Bidirectional hover preview (Ctrl+hover on a highlight pops up the source note over the PDF)
- Round-trip click navigation (note callout → opens PDF, PDF highlight → opens note)
- Rectangular selection embed (clipped the title block as a live image into a note)
- Backlinks pane integration with bidirectional hover sync (color-coded feedback in both directions)

What we read but did not drive: the Vim mode, smart tab management for PDF wikilinks, the `Toggle select-text-to-copy` ribbon mode, citation extraction (which depends on an external `AnyStyle` binary), PDF page composer (add/remove/extract pages with auto-link-updating), outline editing, page label editing, custom link copy templates with JavaScript expressions.

That's the scope. Now the review.

---

## Walk-around

PDF++ is not a polite plugin. It does not introduce itself. It installs from the community browser in two clicks, immediately drops a row of colored dots into the toolbar of every PDF you open, and gets out of the way -- which is the problem.

A new user opens a PDF, sees the colored dots, selects some text, clicks yellow. Nothing visible happens in the note that they think should receive an annotation. They try red. They try blue. They get only red, because they're triggering Obsidian's *native* one-color highlight tool by accident (PDF++ added a separate experimental "edit PDF directly" mode that mostly stays out of the way until you stumble into it). They conclude PDF++ is broken.

It isn't broken. It's just not what they think.

The colored dots are not highlight buttons. They are **link-copy buttons.** The PDF++ workflow is:

1. Open the PDF in one pane.
2. Open or create a target note in another pane.
3. Select text in the PDF.
4. Click a color dot. **A wikilink is copied to your clipboard** -- something like `[[as_we_may_think.pdf#page=1&selection=45,19,47,56&color=yellow]]`.
5. Paste the link into the note.
6. PDF++ now renders the highlight virtually in the PDF, in the color you picked, based on the link in the note.

The PDF file itself is never modified. The annotation lives entirely in your markdown notes. Delete the wikilink, the highlight disappears. Move the note to another vault, the highlight goes with it. **The vault is the source of truth; the PDF is read-only.**

This is the design choice that makes PDF++ different from every other PDF tool we know of. Annotator (PDF++'s closest competitor at 564K downloads) uses sidecar files in a custom format that the author of PDF++ politely calls "`.md` files that are actually not markdown at all." PDF++ keeps everything in real wikilinks that survive the plugin getting uninstalled, abandoned, or replaced.

If PDF++ stops working tomorrow, your highlights still exist as wikilinks in your notes. They just stop *rendering visually*. That's the durability promise. It is, as far as we can tell, unmatched in this category.

---

## Cabin & ergonomics

The toolbar is unobtrusive once you understand it. Five colored dots (in our default install: yellow, red, blue, purple, plus an empty/no-color circle), a dotted-rectangle icon for region selection, an edit/annotation icon, and a couple of dropdown chevrons for additional actions. Clean.

Reading mode reveals the polish that editing mode hides: pasted wikilinks render as styled callouts with a colored left border matching the highlight color, a link header showing the source PDF and page number, and the quoted text body. Color-coded end-to-end: yellow link in note → yellow highlight in PDF → yellow border on callout. Consistent visual language.

The settings panel is where things get vertiginous. We counted roughly 35 toggles in 4 of perhaps 10 settings sections we sampled -- the plugin has on the order of **150-200 settings** in total. There are sub-sections for backlinks pane behavior, PDF embed rendering, opening links, citations, rectangular embeds, miscellaneous edge-case fixes (more on that), Vim keybindings, and more.

Most settings have meaningful defaults. Many have descriptions like "see the GitHub docs for more details." Which brings us to the friction.

---

## Documentation -- the friction point

The PDF++ documentation is **circular.**

- The README points you to the GitHub Pages docs site
- The docs site says "this documentation is pretty much a work in progress and thus incomplete. **More complete instructions can be found in the plugin settings.**"
- The plugin settings, in many cases, link back to the README or wiki on GitHub

None of the three sources is complete on its own. To understand a non-obvious setting, you triangulate across the README, the docs site, the in-app description, and sometimes a relevant GitHub issue. For a "set it and forget it" user, this is a wall. For a power user willing to invest, it's manageable but real.

This is not a code problem. It is a documentation problem. But the documentation problem shapes the user experience enormously, and any honest review has to surface it.

---

## Road test

After clearing the conceptual hurdle (the dots copy links, they don't highlight), the workflow is genuinely satisfying.

We highlighted the editor's note from "As We May Think":

> *"instruments are at hand which, if properly developed, will give man access to and command over the inherited knowledge of the ages."*

Selected the line, clicked yellow, switched to a fresh empty note, pasted. The note now had a styled callout with the link header and the quoted text. The PDF, on the other side, now rendered that line in a soft yellow band. Same color end-to-end.

We did it again with a second line ("This has not been a scientist's war...") in blue. Two callouts in the note, two highlights in the PDF, two colors, immediately scannable.

Then we Ctrl+hovered over the yellow highlight in the PDF. A popup appeared over the PDF showing the **entire source note** -- both callouts, plus a third item we'll get to in a second -- with a small expand icon to open the full note. The hover preview is not a tooltip; it is a live, scrollable, interactive preview of the related note content. From inside the PDF, without leaving it, we could see all the related context.

We then tested the rectangular selection embed: clicked the dotted rectangle icon, drew a box around the "AS WE MAY THINK / by VANNEVAR BUSH" title block, pasted into the note. The note now had a clean live-rendered image of the title block embedded inline -- not a screenshot file in the vault, not an attachment, but a *live reference to that PDF region*. Edit the source PDF, the embed updates.

Finally we opened the Backlinks pane. It listed all three links to the PDF in the note -- the yellow text selection (`&selection=...&color=yellow`), the blue text selection, and the rectangular embed (`&rect=146,547,355,611`). Hovering a backlink turned its entry red AND made the corresponding PDF text glow green. Reverse worked the same. The integration with Obsidian's built-in backlinks pane is total.

---

## Test data

| Metric | Value |
|---|---|
| Install time (browser → enabled) | Under 1 minute |
| Toolbar footprint | Compact (1 row of icons in PDF view) |
| Settings count (estimated) | 150-200 across ~10 sections |
| Highlight colors registered (default) | 4 colors + empty (yellow, red, blue, purple) |
| Backlink rendering | Markdown wikilink with optional `&color=` and `&rect=` params |
| File modification by default | None (backlink mode is the default) |
| Direct PDF annotation mode | Available but experimental, gated behind explicit setting |
| Vim mode | Full implementation, opt-in (off by default) |
| External dependencies | None for core; `AnyStyle` binary needed for best citation extraction |

---

## What we liked

**The architectural choice.** Backlink-as-annotation is the right design for a PKM-grounded PDF workflow. It survives plugin abandonment, vault migration, and version conflicts. Most plugins make their data dependent on themselves; PDF++ does the opposite.

**Bidirectional integration.** The hover preview popping up over the PDF, the round-trip navigation, the backlinks pane sync with color-coded feedback in both directions -- the level of integration with the rest of Obsidian goes well beyond what we expected.

**The rectangular embed.** For papers with figures, diagrams, equations, or scanned tables, being able to clip exactly the region you want as a live image embed -- without a separate file -- is a real workflow upgrade. We've never seen this done as cleanly anywhere else.

**The maintainer's commitment to weird real-world cases.** The Misc settings section contains, among other things, a workaround for a text selection bug in *Obsidian itself*, special handling for iOS Markup rubber-stamp annotations, half-width whitespace removal between Chinese and Japanese characters when copying text from OCR'd PDFs, and hyphenation fixes for words split across line breaks on copy. This is craftsmanship. Most plugins do not sweat this.

**The Vim story.** PDF++ has a full Vim implementation -- not "vim-like," actual Vim with counts (`2j`, `10G`, `150=`), search (`/` `?`), hint mode (`f`, borrowed from Tridactyl, lets you follow links without the mouse), command-line mode (`:`), and `.vimrc`-style customization. The maintainer originally said *"I personally don't use Vim... priority is not very high"* when the feature was requested. Then -- midway through the implementation thread -- mentioned *"I've started learning vim myself and found it very attractive."* Then went on to ship counts, modal editing, and the rest, eventually pushing Obsidian's `Scope` class beyond its intended use to make multi-character bindings work. That arc -- a maintainer learning a new paradigm to better serve a userbase he doesn't belong to -- is the kind of thing you don't see often.

---

## What needs work

**The mental model is opaque on first contact.** The colored dots in the toolbar copy links; they do not highlight. The native Obsidian PDF tool ALSO offers highlighting in red as a default, and a new user can easily mistake that for PDF++'s output. The plugin desperately needs a 30-second "this is how it works" explainer at first launch, or at minimum a tooltip on the color dots that says "click to copy a wikilink with this color."

**The documentation is fragmented.** Three sources (README, docs site, in-app settings) all defer to each other and none is complete. For a 150-setting plugin, this is the single biggest barrier to entry.

**Text-extraction artifacts are passed through faithfully.** When we highlighted the second line of the essay, the drop-cap "T" was selected as a separate text element from "his," producing `T h i s` with extra spaces in the resulting wikilink and callout. PDF++ preserves the literal selection rather than cleaning it up. There's a "Override the default copy behavior" toggle that does some normalization (concatenating hyphenated words, stripping line breaks), but drop-cap handling specifically is unaddressed. For older scanned documents this is a recurring papercut.

**Smart tab management only fires for wikilinks.** The "Open PDF links next to an existing PDF tab" setting is real and useful, but it ONLY triggers when you click a wikilink to a PDF in a note -- not when you click a PDF in the file tree. The documentation does not make this distinction clearly.

**Direct PDF annotation mode is a trap for new users.** PDF++ offers two annotation modes: backlink-based (the killer feature) and direct PDF modification (experimental). The experimental mode looks identical to the killer feature on the surface but does something completely different (writes into the PDF file, no backlink). New users stumbling into it conflate the two and get confused about what they actually have.

**Last release was 8 months ago.** Stable release 0.40.31 dropped August 2025; the v1.0.0 refactor has been promised but is in progress. Code activity continues on main (latest push April 2026), so the project isn't dead -- but stable users are running an 8-month-old build. The README acknowledges this: *"this release involves extensive refactoring, you probably won't see any major updates for a few months."*

---

## Compared to...

**vs. Obsidian's native PDF viewer:** native gives you read + one-color highlight. PDF++ gives you backlink-based annotation, multi-color, hover preview, rectangular embeds, page composer, citation extraction, Vim mode, and a hundred other things. Not really a contest if you take PDFs seriously.

**vs. Annotator (564K downloads, our other featured PDF & Annotation plugin):** Annotator stores annotations in a custom format inside `.md` files that aren't really markdown. PDF++ keeps annotations as actual wikilinks. If you want your annotations to survive long-term plugin churn, PDF++ wins. If you want a more traditional "PDF in one pane, annotation toolbar on the side" experience without learning a new mental model, Annotator may feel more familiar.

**vs. external tools (Zotero + plugins, Marginnote, Highlights for macOS):** PDF++ keeps everything inside Obsidian. No app switching. No data living in a separate database. The tradeoff is that external tools have years of UX polish and broader feature sets specific to PDF workflows; PDF++ has Obsidian integration that none of them can match.

---

## The verdict

PDF++ is not "set it and forget it." It is the opposite of that. It is a configuration playground built by a maintainer who quietly does the kind of work most open-source projects skip -- the edge cases, the bug workarounds for the host platform, the features for users they don't personally identify with.

For users who want to take notes on PDFs in Obsidian and never think about it again: install Obsidian's native viewer, accept its limitations, move on. PDF++ will frustrate you within the first ten minutes.

For users who keep research papers, technical documentation, books, or any serious long-form PDF material in their vault and care about the annotations being part of their knowledge graph rather than a separate database: install PDF++ tonight, expect to spend an hour learning the workflow, then never look back.

**Tier:** Strong recommend with caveats. The caveats are real (documentation, mental model, last release was 8 months ago). The strong recommend is also real (the architecture is right, the integration is excellent, the maintainer is genuinely committed).

We picked PDF++ as April's 24K Featured because it represents what Obsidian plugins can be when someone takes them seriously: not a feature checklist, but an opinionated extension of the host platform that makes the platform itself better. It also does something genuinely novel -- backlink-as-annotation -- in a way that no other tool we've seen has matched.

If you've been holding off on PDFs in your vault because the native experience felt thin, this is the plugin that fixes it. Just be ready to read the docs.

---

**Plugin:** [PDF++](https://github.com/RyotaUshio/obsidian-pdf-plus)
**Author:** [@RyotaUshio](https://github.com/RyotaUshio) ([the hobbyist dev](https://ryotaushio.github.io/the-hobbyist-dev/))
**Docs:** [ryotaushio.github.io/obsidian-pdf-plus](https://ryotaushio.github.io/obsidian-pdf-plus/) (work in progress per author)
**Discussions:** [github.com/RyotaUshio/obsidian-pdf-plus/discussions](https://github.com/RyotaUshio/obsidian-pdf-plus/discussions)
**Issues:** [github.com/RyotaUshio/obsidian-pdf-plus/issues](https://github.com/RyotaUshio/obsidian-pdf-plus/issues)
**License:** MIT
**Featured:** April 2026

*The 24K Vault Featured Pick for April 2026. Selection criteria are documented in [CONTRIBUTING.md](../CONTRIBUTING.md#featured-pick-monthly). Past picks are archived in [FEATURED.md](../FEATURED.md). Tested hands-on by 24K Labs in a real Obsidian vault on 2026-04-25.*
