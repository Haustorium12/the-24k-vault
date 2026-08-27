"""
tools/curation_audit.py

Quarterly maintenance script for The 24K Vault.

Performs two operations:

1. SYNC -- regenerate directory/plugins.md and directory/themes.md from
   obsidianmd/obsidian-releases upstream JSON files. Re-runs the same
   alphabetical, letter-grouped layout the directory was built with.

2. AUDIT -- verify every GitHub repo referenced in README.md,
   CONTRIBUTING.md, and FEATURED.md still exists, has not been archived,
   and is still on its original URL. Writes tools/audit-YYYY-MM-DD.md
   with the report.

Usage:
  python tools/curation_audit.py            # sync and audit (default)
  python tools/curation_audit.py sync       # sync only
  python tools/curation_audit.py audit      # audit only

Requires the gh CLI authenticated (for rate-limited API calls).
CP1252-safe ASCII source per project convention.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

UPSTREAM_PLUGINS = 'https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json'
UPSTREAM_PLUGIN_STATS = 'https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugin-stats.json'
UPSTREAM_THEMES = 'https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-css-themes.json'

LETTERS = '0-9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()


def fetch_json(url: str) -> object:
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fmt_dl(n: int) -> str:
    if n >= 1_000_000:
        return f'{n / 1_000_000:.2f}M'
    if n >= 1_000:
        return f'{n / 1_000:.0f}K'
    return str(n)


def clean_desc(s: str) -> str:
    if not s:
        return ''
    s = s.replace('\r', ' ').replace('\n', ' ').replace('|', '\\|')
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > 130:
        s = s[:127].rstrip() + '...'
    if not s.endswith('.'):
        s = s + '.'
    return s


def first_letter_key(name: str) -> str:
    c = name[0].upper() if name else '#'
    if c.isalpha() and c.isascii():
        return c
    return '0-9'


def name_sort_key(p: dict) -> tuple:
    n = p.get('name', '').strip().lower()
    is_alpha = bool(n and n[0].isalpha() and n[0].isascii())
    return (0 if is_alpha else 1, n)


def empty_buckets() -> OrderedDict:
    return OrderedDict((letter, []) for letter in LETTERS)


def sync_plugins(today_iso: str) -> tuple[Path, int]:
    plugins = fetch_json(UPSTREAM_PLUGINS)
    stats = fetch_json(UPSTREAM_PLUGIN_STATS)
    buckets = empty_buckets()

    for p in sorted(plugins, key=name_sort_key):
        pid = p.get('id', '')
        dl = stats.get(pid, {}).get('downloads', 0)
        name = p.get('name', '').strip() or pid
        repo = p.get('repo', '')
        desc = clean_desc(p.get('description', ''))
        safe_name = name.replace('|', '\\|')
        row = f'| [{safe_name}](https://github.com/{repo}) | {fmt_dl(dl)} | {desc} |'
        buckets[first_letter_key(name)].append(row)

    out = [
        '# Plugin Directory',
        '',
        "> The exhaustive index of every plugin in Obsidian's official "
        '`community-plugins.json` registry. Generated from upstream data, not curated.',
        '>',
        '> **Curated picks** with our notes and tag system live in the '
        '[main README](../README.md).',
        '>',
        f'> Last synced: {today_iso} from '
        '[obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases).',
        '> Source files: `community-plugins.json` + `community-plugin-stats.json`.',
        '',
        f'**{len(plugins):,} plugins indexed.**',
        '',
        '## Index',
        '',
        ' &middot; '.join(
            f'[{letter}](#{"0-9" if letter == "0-9" else letter.lower()})'
            for letter in buckets if buckets[letter]
        ),
        '',
        '---',
        '',
    ]
    for letter, rows in buckets.items():
        if not rows:
            continue
        out.append(f'## {letter}')
        out.append('')
        out.append('| Plugin | Downloads | Description |')
        out.append('|--------|-----------|-------------|')
        out.extend(rows)
        out.append('')
    out.append('---')
    out.append('')
    out.append(
        f'*Index generated {today_iso}. {len(plugins):,} plugins from '
        '`obsidianmd/obsidian-releases`. Re-sync via `tools/curation_audit.py`.*'
    )
    out.append('')

    path = REPO_ROOT / 'directory' / 'plugins.md'
    path.write_text('\n'.join(out), encoding='utf-8')
    return path, len(plugins)


def sync_themes(today_iso: str) -> tuple[Path, int]:
    themes = fetch_json(UPSTREAM_THEMES)
    buckets = empty_buckets()

    for t in sorted(themes, key=name_sort_key):
        name = t.get('name', '').strip()
        repo = t.get('repo', '')
        modes = t.get('modes', []) or []
        modes_str = ' / '.join(m.capitalize() for m in modes) if modes else '-'
        safe_name = name.replace('|', '\\|')
        row = f'| [{safe_name}](https://github.com/{repo}) | {modes_str} | `{repo}` |'
        buckets[first_letter_key(name)].append(row)

    out = [
        '# Theme Directory',
        '',
        "> The exhaustive index of every theme in Obsidian's official "
        '`community-css-themes.json` registry. Generated from upstream data, not curated.',
        '>',
        "> **Curated theme picks** with our notes live in the "
        "[main README's Themes section](../README.md#themes).",
        '>',
        f'> Last synced: {today_iso} from '
        '[obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases).',
        '> Source file: `community-css-themes.json`.',
        '',
        f'**{len(themes):,} themes indexed.**',
        '',
        '## Index',
        '',
        ' &middot; '.join(
            f'[{letter}](#{"0-9" if letter == "0-9" else letter.lower()})'
            for letter in buckets if buckets[letter]
        ),
        '',
        '---',
        '',
    ]
    for letter, rows in buckets.items():
        if not rows:
            continue
        out.append(f'## {letter}')
        out.append('')
        out.append('| Theme | Modes | Repo |')
        out.append('|-------|-------|------|')
        out.extend(rows)
        out.append('')
    out.append('---')
    out.append('')
    out.append(
        f'*Index generated {today_iso}. {len(themes):,} themes from '
        '`obsidianmd/obsidian-releases`. Re-sync via `tools/curation_audit.py`.*'
    )
    out.append('')

    path = REPO_ROOT / 'directory' / 'themes.md'
    path.write_text('\n'.join(out), encoding='utf-8')
    return path, len(themes)


def extract_curated_repos() -> list[str]:
    """Pull all unique owner/repo references from curated files."""
    repos = set()
    for fname in ('README.md', 'CONTRIBUTING.md', 'FEATURED.md'):
        path = REPO_ROOT / fname
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for match in re.findall(r'github\.com/([\w.-]+/[\w.-]+)', text):
            match = re.split(r'[?#)]', match)[0]
            if match.endswith('.git'):
                match = match[:-4]
            if match.count('/') == 1 and not match.startswith('obsidianmd/obsidian-releases'):
                repos.add(match)
    return sorted(repos)


RAW_HEAD = 'https://raw.githubusercontent.com/{repo}/HEAD/README.md'

_GH_PROXY_MSGS = (
    'not enabled for this session',
    'add_repo to request access',
)


def _gh_proxy_blocked(stderr: str) -> bool:
    return any(m in stderr for m in _GH_PROXY_MSGS)


def _raw_head_check(repo: str) -> dict:
    """
    Fallback when gh is absent or proxy-blocked.
    HEAD raw.githubusercontent.com to detect missing/moved repos.
    Cannot detect archived status -- reports ok_no_api for live repos.
    """
    url = RAW_HEAD.format(repo=repo)
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'curl/8'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                return {'full_name': repo, 'archived': None, 'pushed_at': '?',
                        '_fallback': True}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'error': 'raw HEAD 404 -- repo missing or renamed (needs manual check)'}
        return {'error': 'raw HEAD HTTP {}'.format(e.code)}
    except Exception as exc:
        return {'error': 'raw HEAD exception: {}'.format(str(exc)[:120])}
    return {'error': 'raw HEAD unexpected response'}


def gh_api_repo(repo: str) -> dict:
    """Fetch repo metadata via gh CLI; falls back to raw HEAD check if gh is
    unavailable or proxy-blocked for external repos."""
    try:
        result = subprocess.run(
            [
                'gh', 'api', f'repos/{repo}', '--jq',
                '{full_name, archived, pushed_at, stargazers_count, html_url}',
            ],
            capture_output=True, text=True, timeout=20,
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        stderr = (result.stderr or result.stdout or 'no output').strip()
        if _gh_proxy_blocked(stderr):
            return _raw_head_check(repo)
        return {'error': stderr[:200]}
    except FileNotFoundError:
        return _raw_head_check(repo)
    except Exception as exc:
        return {'error': str(exc)[:200]}


def audit(today_iso: str) -> dict:
    plugins = {p['repo'].lower() for p in fetch_json(UPSTREAM_PLUGINS)}
    themes = {t['repo'].lower() for t in fetch_json(UPSTREAM_THEMES)}

    curated = extract_curated_repos()
    print(f'  Auditing {len(curated)} curated repo references...')

    findings = {
        'ok': [],
        'ok_fallback': [],
        'stale_url': [],
        'archived': [],
        'errors': [],
    }
    cutoff_days = 365

    for i, repo in enumerate(curated, 1):
        if i % 10 == 0:
            print(f'    {i}/{len(curated)}...')
        info = gh_api_repo(repo)
        if 'error' in info:
            findings['errors'].append((repo, info['error']))
            continue
        if info.get('_fallback'):
            findings['ok_fallback'].append((repo, '?'))
            continue
        canonical = info.get('full_name', '')
        if canonical.lower() != repo.lower():
            findings['stale_url'].append((repo, canonical))
            continue
        if info.get('archived'):
            findings['archived'].append((repo, info.get('pushed_at', '?')))
            continue
        findings['ok'].append((repo, info.get('pushed_at', '?')))

    findings['_meta'] = {
        'audited': len(curated),
        'plugin_directory_size': len(plugins),
        'theme_directory_size': len(themes),
    }
    return findings


def write_audit_report(findings: dict, today_iso: str) -> Path:
    meta = findings.get('_meta', {})
    out = [
        f'# Curation Audit Report -- {today_iso}',
        '',
        f'Generated by `tools/curation_audit.py`.',
        '',
        '## Summary',
        '',
        f'- Curated repos audited: {meta.get("audited", "?")}',
        f'- Plugin directory size (upstream): {meta.get("plugin_directory_size", "?")}',
        f'- Theme directory size (upstream): {meta.get("theme_directory_size", "?")}',
        f'- OK (full API): {len(findings["ok"])}',
        f'- OK (raw HEAD fallback, archived status unknown): {len(findings.get("ok_fallback", []))}',
        f'- Stale URLs (renamed or transferred): {len(findings["stale_url"])}',
        f'- Archived repos: {len(findings["archived"])}',
        f'- Errors / needs manual check: {len(findings["errors"])}',
        '',
    ]

    if findings.get('ok_fallback'):
        out.append('## Fallback Mode Active')
        out.append('')
        out.append(
            'The `gh` CLI was unavailable or proxy-blocked for the GitHub API. '
            'Repo existence was confirmed via `raw.githubusercontent.com` HEAD checks, '
            'but **archived status and URL canonicity could not be verified**. '
            'Re-run `python tools/curation_audit.py audit` locally with `gh` authenticated '
            'for a full check.'
        )
        out.append('')

    if findings['stale_url']:
        out.append('## Stale URLs (action: update README/CONTRIBUTING)')
        out.append('')
        out.append('| Old | New canonical |')
        out.append('|-----|---------------|')
        for old, new in findings['stale_url']:
            out.append(f'| `{old}` | `{new}` |')
        out.append('')

    if findings['archived']:
        out.append('## Archived Repos (action: review for removal or fork)')
        out.append('')
        out.append('| Repo | Last push |')
        out.append('|------|-----------|')
        for repo, pushed in findings['archived']:
            out.append(f'| `{repo}` | {pushed[:10] if pushed else "?"} |')
        out.append('')

    if findings['errors']:
        out.append('## Needs Manual Check (raw HEAD 404 or other error)')
        out.append('')
        for repo, err in findings['errors']:
            out.append(f'- `{repo}` -- {err}')
        out.append('')

    all_clear = not (findings['stale_url'] or findings['archived'] or findings['errors']
                     or findings.get('ok_fallback'))
    if all_clear:
        out.append('## All Clear')
        out.append('')
        out.append('Every curated repo verified. No action required.')
        out.append('')

    out.append('---')
    out.append('')
    out.append(f'*Audit completed {today_iso}. Re-run quarterly.*')
    out.append('')

    path = REPO_ROOT / 'tools' / f'audit-{today_iso}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(out), encoding='utf-8')
    return path


def main() -> int:
    today = datetime.now().strftime('%Y-%m-%d')
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if mode not in ('sync', 'audit', 'all'):
        print(f'Unknown mode: {mode}. Use sync | audit | all.')
        return 2

    if mode in ('sync', 'all'):
        print('=== SYNC ===')
        path, count = sync_plugins(today)
        print(f'  plugins.md: {count:,} entries -> {path}')
        path, count = sync_themes(today)
        print(f'  themes.md:  {count:,} entries -> {path}')

    if mode in ('audit', 'all'):
        print('=== AUDIT ===')
        findings = audit(today)
        path = write_audit_report(findings, today)
        print(f'  Report: {path}')
        print(f'  OK={len(findings["ok"])} '
              f'ok_fallback={len(findings.get("ok_fallback", []))} '
              f'stale={len(findings["stale_url"])} '
              f'archived={len(findings["archived"])} '
              f'errors={len(findings["errors"])}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
