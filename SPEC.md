# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** APP-002 merged via [PR #4](https://github.com/pb392/my-app-studio/pull/4); [main CI](https://github.com/pb392/my-app-studio/actions/runs/41653406620) passed both jobs. Issue #3 closed and local main updated. APP-003 scope and learner prediction recorded; role routes and the denied-page recovery link are implemented locally. Full explicit APP-003 checks passed with a source-matching receipt; normal full rerun also passed; learner browser observations, keep decision and approved learning summary are recorded. GitHub completion remains pending.
- **Next step:** Prepare the APP-003 PR, review its latest checks, and obtain the learner merge decision. The learner reported member denial and admin access after promotion. The learner interpreted the former-admin access risk; AI clarified the distinction between the saved address and stale session permissions.
- **Implementation marker:** `implemented_through: 3`, advanced only after the full explicit APP-003 check passed. Normal full rerun after this change passed.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | A newcomer comparing Magic: The Gathering, Pokémon TCG and Elestrals and looking for an approachable way to start playing. |
| Reused IS117 brand, or name / promise / primary archetype | Name: **First Draw**. Beginner-oriented name selected by the learner; XenoSHIN TCG is their username. AI-drafted promise: **Find your game. Make your first move.** AI-proposed archetype: **Sage**, expressed as a welcoming, patient guide. These AI-supplied choices implement the learner's friendly-guide direction; the learner subsequently chose to keep the revised design. |
| One visible choice and visitor benefit | Lead with the light snowy illustration and approachable first steps. The learner predicts the character will feel welcoming to beginners; dramatic creature/strategy content is a later direction. Navy, cyan and light surfaces support this direction. |
| Supplied character artwork | The learner asked to use their existing character and supplied four illustrations. The light snowy landscape is reused unchanged as `app/static/guide-landscape.png`, framed responsively with CSS. The original asset is approximately 12 MB; web image optimization remains a performance improvement before any future deployment. The other three illustrations remain private local references. |
| Own issue / branch / PR | [APP-001 issue #1](https://github.com/pb392/my-app-studio/issues/1); `app-001-first-draw`; [PR #2](https://github.com/pb392/my-app-studio/pull/2). |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Signup → login → private dashboard → logout. Signed-out dashboard visits redirect to `/login`; top-right Sign in changes to My dashboard when signed in. New accounts are members. JSON `/api/me` rejects anonymous requests with 401 and returns public identity after login. |
| Valid and rejected cases to demonstrate | Successful signup/login; duplicate or malformed signup, role injection, wrong credentials, absent/incorrect CSRF, and revoked/expired sessions rejected. Logout revokes the server session. Local throwaway accounts only. |
| Own issue / branch / PR | [Issue #3](https://github.com/pb392/my-app-studio/issues/3); `app-002-first-draw-accounts`; [PR #4](https://github.com/pb392/my-app-studio/pull/4). |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | A small admin-only page, with ordinary members retaining their private dashboard. Learner agreed to this scope and requested an access-denied message with a homepage link for members. Server-enforced access, member-only signup and the trusted local role command stay within the prepared lesson. |
| Actual allowed/denied request evidence | Prepared contracts passed: anonymous API 401 and page redirect 303; member API/page 403; admin API/page 200; promotion/demotion affect the existing session; stale role claims cannot override the database. Full Chromium check passed in the learner terminal. |
| Own issue / branch / PR | [Issue #5](https://github.com/pb392/my-app-studio/issues/5); `app-003-first-draw-roles`; PR pending. |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | [Issue #1](https://github.com/pb392/my-app-studio/issues/1); `app/brand.json`, `app/templates/base.html`, `app/templates/home.html`, `app/static/site.css`, original `logo.svg`, supplied `guide-landscape.png` | Foundation-only baseline full check previously passed in learner terminal (98 tests + 2 Chromium). Current APP-001 fast check passed Black, Pylint, 98 foundation tests + 2 homepage contracts; Chromium omitted. AI inspected desktop 1440×1000 and mobile 390×844, loaded artwork, game anchor navigation, no missing local anchors, mobile page width 390px and primary action height 52.28px. Full APP-001 check subsequently passed in learner terminal: Black, Pylint, 98 foundation tests, 2 homepage contracts and 2 actual Chromium journeys, observed 2026-10-30T14:25:00.759721+00:00. AI verified the local receipt matched source fingerprint `db374371df5a531d90881adef6e79ce1fb57bee4f6fda22a475e61ed041e1649` before advancing the marker. Final normal full check after the marker change and logo revision passed at 2026-10-30T18:12:32.366765+00:00: Black, Pylint, 98 foundation tests, 2 homepage contracts and 2 Chromium journeys. AI verified source fingerprint `0debcb49119eb6b68949a087caf394861d539711d7b6db14cd4220aa9c052310`. Learner observed the generic symbols, requested a revision, and kept the official-logo result for ease of navigation. | Learner kept the design and approved the learning summary. [PR #2](https://github.com/pb392/my-app-studio/pull/2) merged; [main CI](https://github.com/pb392/my-app-studio/actions/runs/41646628308) passed both jobs. |
| APP-002 | [Issue #3](https://github.com/pb392/my-app-studio/issues/3); `app/features/accounts.py`, `account.html`, `dashboard.html`, `accounts.css`, account navigation and added request/browser tests | Fast cumulative check passed Black, Pylint, 104 non-browser tests and 14 APP-001/APP-002 contracts. Prepared assertions unchanged. AI inspected desktop login and 390px signup (no overflow; button 52.28px high), and confirmed a signed-out browser visit to `/dashboard` redirects to `/login`. Full explicit APP-002 check subsequently passed in the learner terminal: Black, Pylint, 104 non-browser tests, 14 cumulative contracts and 3 Chromium journeys; observed 2026-11-03T14:01:14.560000+00:00. AI verified fingerprint `44690b631993d9d9a5f730bfe18b314388a0efb40e191eee7bd552957a57733e` before advancing the marker. The normal full rerun after the marker change passed at 2026-11-03T14:11:39.849620+00:00: Black, Pylint, 104 non-browser tests, 14 contracts and 3 Chromium journeys. AI verified current source fingerprint `78229cbf697f7c824793026d0b8dfb6e055eb0ab2bef544c8dd8914523499cce`. AI also inspected a disposable local account dashboard at 1440×1000 and 390×844: profile and game links were readable, the mobile document width was 390px, and logout returned to login. Learner interpretation, browser observation and keep reason are recorded in LEARNING. | Learner kept the flow, approved the summary and authorized merge. [PR #4](https://github.com/pb392/my-app-studio/pull/4) merged; issue #3 closed; both [main CI jobs](https://github.com/pb392/my-app-studio/actions/runs/41653406620) passed. APP-002 status reported evidence ready for instructor review, not a grade. |
| APP-003 | [Issue #5](https://github.com/pb392/my-app-studio/issues/5); `app/features/roles.py`, `app/templates/admin.html`, `accounts.css`, `tests/test_role_experience.py`, browser assertions | Black and Pylint passed; 106 non-browser tests and 18 cumulative contracts passed. Chromium omitted from fast check. Initial sandbox loopback failures resolved after network permission; a formatting issue was fixed. AI inspected denied/admin pages at 1440×1000 and 390×844 (390px document width), clicked the homepage link, and confirmed promotion then demotion changed the same browser session after a fresh request. Test account restored to member and logged out. | Local draft; marker advanced to 3 after full scoped checks passed. Normal full rerun passed. Learner interpretation, member/admin browser observations, keep decision and summary approval are recorded in LEARNING. PR and CI pending. |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.

## APP-001 content and review notes

Official resources inspected on October 30, 2026; the short starter guidance is AI-drafted, not learner research:

- [Magic: official how-to-play guide](https://magic.wizards.com/en/how-to-play).
- [Pokémon TCG Live Learning Lab FAQ](https://support.pokemon.com/hc/en-us/articles/45562128423444-Pok%C3%A9mon-TCG-Live-Learning-Lab-FAQ).
- [Elestrals official site](https://www.elestrals.com/) links its Learn to Play video at `https://www.youtube.com/watch?v=ONlBgqp5HHo`; the site link was verified, video playback was not. [Official starter decks](https://www.shopelestrals.com/collections/starter-decks) are linked without price or availability claims.

AI reviewed the changes against APP-001: semantic headings, shared brand tokens, original card mark, image alternative text, visible focus styles and reduced-motion support. No account routes, security helpers, dependencies or server settings changed. Prepared checks were preserved. Browser review supplements, and does not replace, the required Chromium suite or learner observations. Screenshots are saved locally outside Git pending learner review.

### Game-card revision

The learner requested each game's logo or an iconic character after observing generic symbols. AI selected the logo option and replaced the generic symbols with unchanged official PNG assets, displayed proportionally. Matching adjacent game headings provide accessible identification, so duplicate decorative logo images have empty alternative text. The learner chose to keep this revision because it is easy to follow and navigate. Full checks of this revision passed, and the learner approved the learning summary for publication.

Asset provenance (retrieved October 30, 2026):

- `app/static/magic-logo.png`: [official Magic site](https://magic.wizards.com/en), [image](https://images.ctfassets.net/s5n2t79q9icq/3dB5uyWzUH95O1ZPBNNUX5/6cff7c65a809285755ea24b164b6ac65/magic-logo.png).
- `app/static/pokemon-tcg-logo.png`: [official Pokémon TCG image](https://tcg.pokemon.com/assets/img/global/logos/en-us/tcg-logo-2x.png).
- `app/static/elestrals-logo.png`: [official Elestrals store](https://www.shopelestrals.com/collections/starter-decks), [image](https://www.shopelestrals.com/cdn/shop/files/Official-Elestrals-Logo-Colored_0f255c66-ebd6-4ba2-a375-f8e1d2f06d14.png?v=1731089794&width=1948).

These are third-party game logos, not original First Draw artwork; the original First Draw SVG mark remains separate.

Revision verification: the first fast check passed; a later rerun caught that the stylesheet query version conflicted with the prepared foundation requirement for the original CSS URL. The original URL was restored and logo-specific styles moved to a separate local stylesheet; the final fast rerun passed Black, Pylint, all 98 foundation tests and both APP-001 contracts without changing any test. Browser inspection confirmed all three official logo files loaded, proportional `object-fit: contain` rendering and 390px document width at a 390px viewport. A dark Magic panel preserves contrast with its white wordmark. A separate `game-logos.css` handles the logo presentation, including compatibility with a previously cached shared stylesheet. The full normal rerun subsequently passed, including actual Chromium, as recorded in the evidence table.

## APP-002 implementation notes

The HTML and JSON routes in `app/features/accounts.py` reuse the prepared `security.py` services and schemas. HTML credentials are validated server-side; password fields are never repopulated. Public JSON responses are filtered to the public user schema. Bounded forms reject extra/duplicate fields, and errors remain recoverable. `account.html`, `dashboard.html` and `accounts.css` provide First Draw's member experience. The dashboard shows the signed-in username, account type and links to existing beginner guides; profile editing and saved progress are outside this slice. The original security helpers, account contracts and role routes remain unchanged.

AI consulted [FastAPI's password hashing and JWT tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) and the repository's [security notes](docs/security.md). Hashes avoid storing plaintext passwords; JWT signatures establish integrity, not secrecy. Prepared HttpOnly cookies, CSRF validation, expiry, throttles and server revocation are reused. This local feature is not a production-security certification.

## APP-003 implementation notes

Both admin routes call the prepared `security.require_admin`, which checks the current database role. The browser route translates anonymous access into a login redirect and member denial into a 403 page with the learner-requested homepage link. The admin result is a small read-only welcome page; no user-management feature or public role-changing endpoint was added. Existing security helpers and acceptance contracts are unchanged. New tests cover recovery links, member dashboard access and navigation after role changes. AI review found no blocking issues within this scope; full explicit Chromium validation passed; normal full rerun after the marker change also passed.

APP-003 full scoped verification: the learner ran Black, Pylint, 106 non-browser tests, 18 cumulative contracts and 3 actual Chromium journeys successfully. AI verified the saved receipt at 2026-11-03T21:05:43.361819+00:00 against source fingerprint `6abc503958613316be9e9b8fc386e124b9fc0c0c277b343a113af73e342663ea` before advancing the marker to 3.

APP-003 normal full verification after advancing the marker: Black, Pylint, 106 non-browser tests, 18 cumulative contracts and 3 actual Chromium journeys passed in the learner terminal. AI verified the receipt at 2026-11-03T21:09:28.534399+00:00 against current source fingerprint `ffaf8709760ec9dbd09526352939770d8c205bfe4cef978ae07ab39abaac09ff`. The learner reported the expected member-denial message. The learner also reported admin access after promotion. The learner chose to keep the behavior because it matches their intended admin access; the learner approved the summary for publication.
