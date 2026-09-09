# Privacy remediation plan: contact files in the public Telo repository

Prepared 2026-09-02 by a coding agent under read-only rules. Nothing below was executed against `~/telo` or the GitHub repository except read-only git and `gh` queries; the `.gitleaks.toml` syntax alone was checked in a throwaway directory outside `~/telo` (section 4). Every command block is for the founder to run. No address or name from the outreach files is reproduced here. Change classes: (a) working-tree change the agent may make now, (b) needs founder approval, (c) public-history remediation, (d) website correction, (e) claim to remove, (f) claim to qualify.

## 1. Exposure summary

Repository state (all pointers are commands run on 2026-09-02 from `~/telo`):

| Fact | Value | Pointer |
|---|---|---|
| Remote | `git@github.com:rikhinkavuru/Telo.git` | `git remote -v` |
| Visibility | PUBLIC, `isPrivate=false`, default branch `main` | `gh repo view rikhinkavuru/Telo --json visibility,isPrivate,defaultBranchRef` |
| Created / last push | 2026-07-16T17:52:43Z / 2026-07-26T21:19:58Z | same query with `createdAt,pushedAt`; local `git reflog show --date=iso origin/main` prints `refs/remotes/origin/main@{2026-07-26 14:19:58 -0700}: update by push` |
| Forks, stars, watchers, PRs, issues, releases, tags | 0, 0, 0, 0, 0, 0, 0 | `gh repo view --json forkCount,stargazerCount,watchers`; `gh api repos/rikhinkavuru/Telo/forks`; `gh pr list --state all`; `gh issue list --state all`; `gh release list`; `git tag` |
| Traffic, last 14 days only | 4 clones by 4 unique cloners and 19 views by 2 unique visitors, all dated 2026-09-01; zero on the other 13 days | `gh api repos/rikhinkavuru/Telo/traffic/clones` and `.../views` (14 daily buckets, 2026-08-19 to 2026-09-01) |
| History | 19 commits, one branch, no stash, no other refs | `git rev-list --count --all`; `git for-each-ref`; `git stash list` |
| Local vs remote | local `main` = `origin/main` = `c3b31b9` (0 ahead, 0 behind at last fetch) | `git rev-list --left-right --count origin/main...HEAD` |

Files that carry addresses (regex `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` run over the working-tree copies of `git ls-files` paths, not over committed blobs; no binary file matched):

| File | Lines with an address | Occurrences | Distinct | Assessment | History |
|---|---|---|---|---|---|
| `outreach/lab-contacts.md` (102 lines, 14,387 bytes, blob `7fa0c89`) | 30 | 34 | 31 | all institutional addresses of named academics at 19 distinct domain strings at 18 universities (US, UK, BE, FI, SE, DK, IT); 29 people carry at least one address by entry structure (5 table rows at lines 30-34; 24 people across 23 address-bearing bullets at lines 52-91, line 58 naming two); line 48 is a second address for table row 5; line 101 repeats two strings from line 57, one of which the file marks as a wrong search-summary result, so at most 30 of the 31 distinct strings are real addresses; 27 entries are marked VERIFIED, 1 UNVERIFIED; further people are named without addresses at lines 66, 92, 93. The file also holds candid per-person notes (fit, conflicts, "deprioritized"), which are arguably more sensitive than the addresses; the file's own line 3 says every address was "read off a primary page or a paper's author record" and that anything not marked VERIFIED is a lead, not an address | added `c6e7c00` 2026-07-16 (3rd commit); modified `d479ed4` 2026-07-16; 2 commits touch it; present in 17 of 19 commit snapshots; both commits on `origin/main` (`git branch -r --contains`); no uncommitted edits (`git status --porcelain -- outreach/` empty) |
| `outreach/facilities.md` (162 lines) | 24 | 28 | 25 | 7 role mailboxes by local part (info, info.*, office, sales); 5 first.last-shaped; 13 other local parts, 3 to 23 characters, at vendor and university domains (12 .com, 12 .edu, 1 .biz), not classifiable without reading; treat at most 18 as potentially personal. Not mentioned in `HANDOFF.md` section 6 | added `ebafb11` 2026-07-16; present in 14 of 19 snapshots |
| `funding/applications.md` | 3 | 3 | 2 | two 5-character local parts at two accelerator domains; probably program mailboxes; founder to confirm | `a43b893`, `1f7c385`; present in 13 snapshots |
| `CLAUDE.md`, `graphify-out/graph.json` | 1 each | | 1 | one FDA program mailbox; generic | working tree only (uncommitted); in no commit (`git grep -l` over `git rev-list --all` finds 0 hits for these two paths); not exposed |
| `telo-web/README.md`, `telo-web/src/app/research/page.jsx`, `telo-web/src/components/sections/Footer.jsx` | 1-2 each | | 1 | one company role address at the founder's own domain | not an issue |

Not tracked, so not exposed: `paper/SUBMISSION.md` holds three address strings, one generic help mailbox (line 11) and two named editors (lines 145-146); a third editor and a possible referee are named without addresses (lines 147, 91). `paper/cover-letter.md` line 5 and `paper/release-layer-manuscript.md` line 8 also hold one address each, both at the same `.org` institute domain, not the founder's company domain; probably the author's own, but only the domain was checked. Only `paper/figures/.gitkeep` is tracked under `paper/`. If `paper/` is published as-is per `SUBMISSION.md` item 1, those addresses go public; scrub the editor addresses and confirm the other two are the author's own first (b).

Count correction: `HANDOFF.md` line 73 says "21 people's e-mails"; `docs/design_space/ASSIGNMENT.md` line 37 says "21 exposed email addresses". Both undercount: 31 distinct strings (at most 30 real addresses) for 29 people in `lab-contacts.md` alone, plus up to 18 potentially personal in `facilities.md`. Correct `HANDOFF.md`; `ASSIGNMENT.md` is stored as a verbatim record of the assignment (`HANDOFF.md` line 3), so append a dated correction note to it rather than editing the text (b).

Contradiction with `paper/SUBMISSION.md` item 1: it says the repo returned HTTP 404 on 2026-07-26 and that "the present repository holds company strategy documents that are not part of this paper and must not be published". The repo was created 2026-07-16 and is public now; the date it became public is not recorded anywhere locally (GitHub does not expose visibility history through `gh repo view`). The 404 statement is stale and should be qualified (f). Already logged as `docs/audits/05_inconsistencies.md` I-C14.

What is not knowable locally: whether anyone cloned or mirrored the file between 2026-07-16 and about 2026-08-19 (the traffic API covers 14 days); whether search engines, `web.archive.org`, or Software Heritage captured it. Git holds no record of readers. Fork count (0) comes from the GitHub API, not from local state. The founder can check by hand: `https://web.archive.org/web/*/github.com/rikhinkavuru/Telo*` and `https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/rikhinkavuru/Telo`.

Tooling on this machine: `gitleaks` 8.30.1 at `/opt/homebrew/bin/gitleaks`; `gh` 2.76.0 authenticated as `rikhinkavuru` with the `repo` scope (enough for a visibility change and a force-push); `git-filter-repo` and BFG not installed; no `.gitignore` entry for `outreach/`; no hooks; no `.pre-commit-config.yaml`; 64 uncommitted paths in the working tree (`feasibility/` is untracked, HA-05).

## 2. Options (commands for the founder; none executed)

### A. Make the repository private now (b)

```bash
gh repo edit rikhinkavuru/Telo --visibility private --accept-visibility-change-consequences
gh repo view rikhinkavuru/Telo --json visibility,isPrivate   # expect PRIVATE / true
```

Reversible: yes, one command flips it back. Fixes: all anonymous access to the file, to every commit by SHA, to raw URLs, and to the API stops within seconds. Does not fix: copies already cloned; GitHub's own caches of unreachable commits (moot while private); search-engine snapshots; `archive.org` or Software Heritage captures. Side effects: none for this repo (0 forks, 0 stars, no Pages site (`gh api repos/rikhinkavuru/Telo/pages` returns HTTP 404), no PRs). `telo-web/` holds a local `.vercel/` project link, so deploys go through the Vercel CLI, not the GitHub integration; if a GitHub-linked deploy exists it keeps working for private repos through the GitHub app. Time: one minute. HA-05 covers commits, not settings, but this is a founder-level decision and is recorded as HA-06.

### B. Remove the files from the working tree and push a deletion commit (b)

```bash
mkdir -p ~/telo-private/outreach && cp ~/telo/outreach/lab-contacts.md ~/telo/outreach/facilities.md ~/telo-private/outreach/
cd ~/telo && git rm outreach/lab-contacts.md outreach/facilities.md
git commit -m "Remove contact lists from the repository" -- outreach/lab-contacts.md outreach/facilities.md
git push origin main
```

Reversible: the files are still in history, so yes. Fixes: the file is gone from `main` at `HEAD`, from `blob/main/...` and `raw/.../main/...` URLs. Does not fix: `https://github.com/rikhinkavuru/Telo/blob/c3b31b9/outreach/lab-contacts.md` and every one of the 17 earlier snapshots still serve the file; clones, caches, archives untouched. Needs HA-05 (commit authorization) and a path-limited commit because the tree holds 64 unrelated uncommitted paths. Alone, this is the weakest option and should not be mistaken for remediation.

### C. Rewrite history (c, b; `CLAUDE.md` line 14, `HANDOFF.md` section 3 item 9 and `ASSIGNMENT.md` line 36 forbid this without explicit approval)

Preferred tool is `git filter-repo`, which is not installed. Work in a fresh clone; `filter-repo` refuses a non-fresh one.

```bash
brew install git-filter-repo
git clone --no-local git@github.com:rikhinkavuru/Telo.git ~/telo-rewrite && cd ~/telo-rewrite
git filter-repo --invert-paths --path outreach/lab-contacts.md --path outreach/facilities.md   # add --path funding/applications.md if HA-07 says so
git log --all --oneline -- outreach/            # expect no output
for c in $(git rev-list --all); do git grep -l -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' $c -- ':!*.png' ':!*.jpg' ':!*.mp4'; done | sed 's/^[0-9a-f]*://' | sort -u   # expect only telo-web/README.md, telo-web/src/app/research/page.jsx, telo-web/src/components/sections/Footer.jsx, and funding/applications.md if kept; the CLAUDE.md and graph.json addresses are uncommitted and never appear
git remote add origin git@github.com:rikhinkavuru/Telo.git
git push --force --all origin
```

Then ask GitHub to purge cached views and unreachable commits: open a support request under "Remove sensitive data" (docs page "Removing sensitive data from a repository"); until they act, the old SHAs such as `c6e7c00` and `c3b31b9` may still resolve. Then re-point the working repository without losing the uncommitted `feasibility/` work:

```bash
cd ~/telo && git branch backup/pre-rewrite main      # local only; never push
git fetch origin && git checkout -B main origin/main  # untracked feasibility/ survives; outreach/ files disappear from the tree, so copy them out first (option B line 1)
git log --all --not backup/pre-rewrite -- outreach/   # expect no output; plain --all would always print the backup/pre-rewrite commits
```

BFG alternative: `java -jar bfg.jar --delete-files '{lab-contacts.md,facilities.md}' --no-blob-protection ~/telo-mirror.git` on a `git clone --mirror`, then `git reflog expire --expire=now --all && git gc --prune=now --aggressive && git push --force`. BFG protects `HEAD` by default, hence the flag. BFG is not installed here; this line is from memory and was not run.

Reversible: no. Every commit from `c6e7c00` onward gets a new SHA (17 of 19), which invalidates every clone and every open PR (none exist). Fixes: the file leaves every reachable snapshot; after GitHub's purge, the old SHAs stop serving it. Does not fix: existing clones and mirrors, `archive.org`, Software Heritage, search-engine caches (request removal through Google Search Console "Remove outdated content" once the URLs return 404). If forks existed they would need the same purge; there are none.

### D. Recommended sequencing (b, c)

1. A today. Minutes, reversible, closes the live exposure. Record HA-06 as done with the `gh repo view` output.
2. Copy `outreach/` to `~/telo-private/outreach/` (HA-08), then remove it from the tree.
3. C after HA-07 approval. Alternative that avoids a rewrite: delete the repository entirely once a private mirror exists (`git clone --mirror` to `~/telo-private/Telo.git`); with 0 forks that removes the history at GitHub as well, though the same caveats on external copies apply.
4. If the paper needs a public archive, follow `paper/SUBMISSION.md` item 1: a new repository holding only `research/conformal/` and `paper/` with a fresh history, after scrubbing the editorial contacts from `SUBMISSION.md`, then a Zenodo DOI. The old repository stays private. Never re-publish the existing history.

## 3. Obligations and courtesy

No legal advice here; the founder decides, with counsel if wanted. Facts that bear on the decision: the addresses are institutional work addresses; the file's line 3 says each was "read off a primary page or a paper's author record" (27 entries marked VERIFIED, 1 UNVERIFIED; the file itself records one wrong search-summary address at lines 57 and 101); the file instructs that nothing be sent (line 5), but whether anyone was contacted is not recorded in the repository and needs the founder's confirmation; the repository shows 0 forks and 4 clones in the last 14 days; but the file also holds frank assessments of named people, and 12 of the 31 distinct addresses are at EU or UK institutions (9 domains in BE, DK, FI, IT, SE, UK; `grep -oE` per domain), where a work e-mail is personal data and where a controller weighs whether a breach is "unlikely to result in a risk" before deciding on notification. A reasonable reading is low risk with no duty to notify; a reasonable founder might still send a courtesy note to the people whose entries contain conflict or scoop language. Default recommendation: decide after A and C are done, and notify only if the founder would want to be told in their place.

Template the founder could adapt (no names; fill the bracketed fields):

> I am writing because a working document I compiled in July 2026, which listed your institutional e-mail address alongside my notes on whose research is closest to a project I am developing, sat in a code repository that was set to public on GitHub until [date]. The address came from your public faculty page or a paper's author line; [no message was ever sent from that list: keep this clause only once you have confirmed it], and the repository showed no forks. I removed the file, made the repository private on [date], and [asked GitHub to purge cached copies]. I am telling you because you would want to know, not because I need anything from you. If you would like to see what the file said about you, or want any record of you deleted from my files, reply and I will do it.

## 4. Prevention (all (b): the files sit outside this agent's write scope)

Rule: contact lists, outreach targets, and interview notes with names live in `~/telo-private/` (or a CRM), never in `~/telo`. The repository may hold counts and file paths only, the way `HANDOFF.md` section 6 (line 73) and `docs/audits/05_inconsistencies.md` I-C14 already do.

`.gitignore` additions (note: ignoring does not untrack; `git rm --cached` first):

```gitignore
# Contact lists never enter the repository (feasibility/docs/design_space/privacy_remediation_plan.md, 2026-09-02)
outreach/
**/*contacts*.md
**/*contacts*.csv
**/*.vcf
```

`gitleaks` config at `~/telo/.gitleaks.toml` (the default ruleset detects secrets, not addresses, so add a rule):

```toml
title = "telo"
[extend]
useDefault = true

[[rules]]
id = "email-address"
description = "E-mail address; contact lists live outside the repository"
regex = '''[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'''
keywords = ["@"]
[[rules.allowlists]]
regexes = ['''@telo\.ai$''', '''@fda\.hhs\.gov$''', '''@example\.com$''']
```

Hook, versioned at `~/telo/.githooks/pre-commit` and enabled with `git config core.hooksPath .githooks` (needs `chmod +x`):

```sh
#!/bin/sh
# Blocks commits that add an e-mail address. Uses gitleaks when present, a plain regex otherwise.
set -u
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks git --pre-commit --staged --redact --no-banner --config "$(git rev-parse --show-toplevel)/.gitleaks.toml" || exit 1
  exit 0
fi
pattern='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
allow='@telo\.ai|@fda\.hhs\.gov|@example\.com'
hits=$(git diff --cached -U0 --diff-filter=AM -- . ':!*.png' ':!*.jpg' ':!*.mp4' ':!*.tif' ':!*.mat' \
  | grep -E '^\+' | grep -vE '^\+\+\+' | grep -oE "$pattern" | grep -vE "$allow" | sort -u | wc -l | tr -d ' ')
if [ "$hits" -gt 0 ]; then
  echo "pre-commit: $hits e-mail address(es) in staged changes. Contact lists live outside the repository; see feasibility/docs/design_space/privacy_remediation_plan.md" >&2
  exit 1
fi
```

The `.gitleaks.toml` allowlist syntax was checked on 2026-09-02 in a throwaway repository outside `~/telo` (`gitleaks` 8.30.1: a staged non-allowlisted address exits 1, an allowlisted-only file exits 0); the hook is untested in `~/telo`; run `git commit --dry-run` with a throwaway staged file containing a fake address before relying on them. A full-history check the founder can run any time: `gitleaks git --config .gitleaks.toml --redact --no-banner` in `~/telo`.

## 5. What the agent did not do, and the decisions required

Not done: no push, no visibility change, no history rewrite, no deletion, no commit, no notification, no network call other than read-only `gh repo view`, `gh api .../forks`, `gh api .../traffic/*`, `gh api .../pages` (404), `gh pr list`, `gh issue list`, `gh release list`. The outreach files are unchanged in the working tree. This plan is the only file written (a).

Founder decisions, each yes/no with the default:

1. Make `rikhinkavuru/Telo` private today with option A? Default: yes. (HA-06)
2. Authorize the history rewrite in option C, force-push, and the GitHub support purge request? Default: yes, after A; the alternative "delete the repository after taking a private mirror" is acceptable if the founder does not intend to reuse this repository's history publicly. (HA-07)
3. Include `funding/applications.md` in the rewrite path list? Default: no, pending a read of the two addresses; include if either is a named person rather than a program mailbox. (HA-07)
4. Move `outreach/` to `~/telo-private/outreach/` and adopt the `.gitignore`, `.gitleaks.toml`, and hook above? Default: yes. (HA-08)
5. Send the courtesy note to some or all listed people? Default: no duty is asserted; decide after A and C; if yes, prioritize entries with conflict or scoop language. (HA-09)
6. Qualify `paper/SUBMISSION.md` item 1 (the 404 claim is stale; the repo is public; already logged as `05_inconsistencies.md` I-C14), correct "21 people's e-mails" in `HANDOFF.md` line 73, and append a dated correction note to `ASSIGNMENT.md` for its line 37 "21 exposed email addresses" (verbatim record; do not edit the text)? Default: yes. (f) and (b)

## 6. Rows for the human-action queue

| ID | Decision | Blocks | Where recorded | Default |
|---|---|---|---|---|
| HA-06 | Make `github.com/rikhinkavuru/Telo` private (`gh repo edit ... --visibility private --accept-visibility-change-consequences`) | closes live exposure of `outreach/lab-contacts.md` (29 people, 31 distinct strings, at most 30 real addresses) and `outreach/facilities.md` (up to 18) | this plan, section 2A; `gh repo view --json visibility` output as evidence | yes, today |
| HA-07 | Authorize history rewrite (`git filter-repo --invert-paths` on the two outreach files, optional `funding/applications.md`), force-push, and GitHub support purge request; or authorize repository deletion after a private mirror | removal of the file from 17 of 19 commit snapshots; supersedes the `CLAUDE.md` line 14 / `ASSIGNMENT.md` line 36 never-rewrite rule for this one case; also needs HA-05 for the commit | this plan, section 2C; `RESEARCH_LOG.md` | yes, after HA-06 |
| HA-08 | Relocate contact lists to `~/telo-private/` and adopt the `.gitignore` entries, `.gitleaks.toml`, and pre-commit hook | prevention; any future outreach or interview work (HA-20 to HA-25) | this plan, section 4 | yes |
| HA-09 | Decide whether to send the courtesy note (section 3) and to whom | none; courtesy only | this plan, section 3 | decide after HA-06 and HA-07 |

## 7. Facts in this plan most likely to be wrong

1. "29 people" is a structural count of table rows and address-bearing bullets, not a count of distinct people read by eye; line 48 was matched to table row 5 and line 101 to line 57 by string comparison only. The distinct-address count (31) is exact as strings; at least one is a known-wrong guess, so the real-address count is at most 30.
2. The traffic figures (4 clones, 19 views) cover only the last 14 days and may include the founder's own or agent activity; all counted activity is on 2026-09-01, the day of the feasibility session; GitHub's definition of a counted clone is not verified here.
3. The `facilities.md` split (7 role, 5 first.last, 13 other; at most 18 potentially personal) rests on local-part shape only; several of the 13 other local parts are probably vendor role mailboxes. The `applications.md` "program mailbox" guess is likewise unread.
4. The BFG command line in section 2C is written from memory; BFG is not installed here and it was not run. The `gh repo edit` flag `--accept-visibility-change-consequences` and the `[[rules.allowlists]]` form in `.gitleaks.toml` were checked on 2026-09-02 (`gh` 2.76.0 help text; a throwaway-repository run on `gitleaks` 8.30.1), but neither was executed against `rikhinkavuru/Telo`.
