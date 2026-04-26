# Contributing to The 24K Vault

The 24K Vault is curated, not exhaustive. Every entry earns its place.

## What We List

**Plugins and themes must meet one of:**

1. **Official** — Published in the Obsidian community directory (merged into [`community-plugins.json`](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json) or [`community-css-themes.json`](https://github.com/obsidianmd/obsidian-releases/blob/master/community-css-themes.json) at `obsidianmd/obsidian-releases`).
2. **Notable (pre-review)** — Submitted to the official queue with a `Ready for review` label (passed Obsidian's automated bot validation) and worth surfacing while the backlog clears.

**Plugins must have:** GitHub repo, `manifest.json`, `README`, `LICENSE`, semver GitHub release with `main.js` attached.

**Themes must have:** GitHub repo, `manifest.json`, `README`, `LICENSE`, screenshot (512x288 recommended).

**Tools and resources** must be publicly accessible, actively maintained, and directly useful to Obsidian users.

## Entry Format

```
[Name](url) - One sentence description starting uppercase, ending with period.
```

- Dash separator (single hyphen, not em dash, not colon).
- Description is factual. No "powerful", "amazing", "best", "revolutionary".
- URL: direct GitHub link or `obsidian.md/plugins` page.
- No trailing whitespace.

## Acceptance Criteria

ALL must be true:

- Active: last commit within 12 months AND repo not archived or deprecated on GitHub. (Exception: see [Stable Tier](#stable-tier-24k-verified) below.)
- Plugin or theme has `manifest.json` plus a semver GitHub release.
- Not a duplicate of an existing entry without meaningful differentiation.
- Description is one line, factual, with no marketing language.
- Link is live and working.

## Rejection Criteria

ANY fails the submission:

- Repo archived, deprecated, or last commit older than 12 months without qualifying for the `[24K Stable]` tier.
- Missing `manifest.json` or no GitHub release.
- Duplicates the functionality of an existing entry.
- Description uses marketing language.
- Broken or redirected link.

## Stable Tier (24K Verified)

A `[24K Stable · YYYY-MM]` tag on an entry means: last commit is older than 12 months, **but as of the date shown** the maintainers verified it remains in active service. To carry the tag, an entry must satisfy ALL of the following at the time of verification:

1. Still listed in the official Obsidian directory ([`community-plugins.json`](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json) or [`community-css-themes.json`](https://github.com/obsidianmd/obsidian-releases/blob/master/community-css-themes.json)).
2. Has a published GitHub release with `main.js` attached (plugins) or a valid `manifest.json` (themes).
3. Repo not archived or deprecated on GitHub.
4. No critical "doesn't work in current Obsidian" issues at the top of the issue tracker.

The tag is re-verified each quarter as part of the maintenance audit. If any criterion fails, the entry is either removed or replaced with an actively maintained fork.

Stable entries appear in their natural categories alongside actively developed entries — the tag exists to be transparent about provenance, not to segregate the list.

## Closed Source Tag

A `[Closed Source]` tag on an entry means the plugin's source code is not publicly available. The entry is still considered for inclusion if it passes the same acceptance criteria, but the tag exists so users can make an informed choice.

Closed-source plugins are evaluated more strictly: we require active maintenance (12-month rule, no Stable exception), a clear privacy policy if the plugin transmits data off-device, and no known unresolved security incidents.

## Featured Pick (Monthly)

Each month the maintainers select one plugin, theme, or tool to spotlight in the README's Featured section. The pick rotates on the 1st of every month.

Selection criteria, in roughly this order:

1. **Quality of execution** — design, polish, and reliability stand out within the category.
2. **Active maintenance** — the maintainer is responsive and the project shows recent activity.
3. **Distinct value** — solves a real problem or fills a gap that was not well-served before.
4. **Underexposure** — preference for excellent work that has not yet hit the famous-plugin tier.

Past picks are archived in [FEATURED.md](FEATURED.md) with the original write-up and the month featured. The Featured section is editorial: a Featured pick is not a substitute for the curated category lists, and a plugin can earn a Featured slot whether or not it appears elsewhere in the README.

## How to Submit

1. Open a Pull Request titled `Add [Name]`.
2. Add the entry to the bottom of the correct section.
3. Use the format: `[Name](url) - Description.`
4. Verify the link is live before submitting.
5. One entry per PR.

Alternatively, open an [issue](https://github.com/Haustorium12/the-24k-vault/issues/new?template=suggest_addition.md) using the suggestion template.

## Maintenance Cadence

The maintainers run a quarterly audit:

- Check every entry: archived/deprecated status and last commit date.
- Remove entries with last commit older than 12 months.
- Verify each plugin still appears in `community-plugins.json` (not removed by the Obsidian team).
- Refresh download counts in the Essential Plugins section.
- Scan the `obsidianmd/obsidian-releases` PR queue for breakout new plugins.

Sources for the audit: [obsidianstats.com](https://www.obsidianstats.com) and [obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases).
