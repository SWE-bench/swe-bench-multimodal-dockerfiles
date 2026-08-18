# MM gold-eval repair log

Fixes applied while making gold evaluation pass on the 510-instance SWE-bench
Multimodal test split. Constraint: never edit a gold patch — fix the instance
Dockerfile / env spec / log parser / dataset labels instead.

Two classes of fix, with different re-verification costs:

- **Log-parser / label fixes** — re-grading needs no containers:
  `run_evaluation ... --rewrite_reports True` regenerates every report.json from
  the already-saved `test_output.txt`.
- **Eval-script / Dockerfile / env-spec fixes** — these change what runs inside
  the container, so the affected instances must genuinely be re-run.

---

## 1. `parse_log_grommet` — jest duration suffix not stripped

**Symptom.** `grommet__grommet-2695` unresolved under gold: F2P 2/3, with
`src/js/components/Menu/__tests__/Menu-test.js` counted as failed.

**Root cause.** jest prints a duration suffix only for files slow enough to
warrant one, and the format varies by jest version — `(123ms)`, `(5.141s)`,
`(5.141 s)`. The parser's strip regex was `r"\s\([\d\.]+\ss\)"`, which requires
a space before the `s`, and it ran only on the `PASS` branch. This jest emits
`(14.914s)` with no space (verified: 0 occurrences of the spaced form in the
log, 2 of the unspaced). So the suffix survived, the parsed name
`…/Menu-test.js (14.914s)` never matched the bare dataset entry, and
`grading.test_failed` counts an absent name as a failure.

Menu took 14.9s and got a suffix; Meter and Video ran fast, got none, and
matched — which is why only 1 of 3 F2P entries failed.

**Why it matters beyond one instance.** Resolution depended on how fast a test
file happened to run on a given machine: the same instance could pass on a fast
box and fail on a slow one. The `FAIL` branch stripped no timing at all, so a
slow *failing* file was mis-keyed too.

**Fix.** `swebench/harness/log_parsers/javascript.py` — strip
`r"\s\([\d\.]+\s?(?:ms|s)\)$"` on both the `FAIL` and `PASS` branches.
(`parse_log_carbon` already handled all three formats; grommet's was the
outlier.)

**Verified.** Re-parsing the saved log: parsed=50, F2P missing=0, F2P
non-pass=0, P2P missing=0 → resolves. Scope: `grommet/grommet` only (20
instances) — no other repo maps to this parser.

---

## 2. quarto-cli — 1800s default timeout too low

**Symptom.** `quarto-dev__quarto-cli-4539` errored with
"Test timed out after 1800 seconds"; the report showed 0 tests parsed.

**Root cause.** Two layers. Quarto's `test_cmd` runs the *entire* smoke suite
via `./run-tests.sh` (hundreds of renders), and 1800s covered only **109 of 444
expected tests (24%)** — full completion needs ~7500s. Separately,
`grading.get_logs_eval` returns an empty status map outright when
`TESTS_TIMEOUT` appears in the log, so a timeout presents as "parser found
nothing" rather than as a timeout.

**Fix.** No per-repo timeout exists in the harness, so quarto's 24 instances are
run as a separate sweep with `--timeout 14400`; the other 486 keep 5400s.
`scripts/run_gold_full.sh` takes `TIMEOUT` / `DATASET` env overrides.

**Status.** `quarto-dev__quarto-cli-475` resolved (F2P 1/1, P2P 126/126) in the
14400s sweep. Quarto instances vary widely in load (475 has 126 P2P, 4539 has
443), which is why only the heavy tail hit the old cap.

---

## 3. prettier — gold patch adds a dependency that is never installed

**Symptom.** `prettier__prettier-9514` unresolved: F2P **0/36**, P2P 47/47 clean.
Every F2P entry was present in the log with a FAILED status (0 missing), so this
looked like the "genuine jest snapshot mismatch" HANDOFF.md records. It isn't.

**Root cause.** The real failure is:

```
● throw_expression.js › [meriyah] expect SyntaxError
  Received value: "Error: Cannot find module 'meriyah' from 'src/language-js/parser-meriyah.js'
```

The gold patch's only `package.json` change is `+ "meriyah": "3.1.2"` (it also
updates `yarn.lock` and adds `src/language-js/parser-meriyah.js`, which calls
`require("meriyah")`). But the env image ran `yarn` at the **base commit**, and
the harness applies the model/gold patch *after* the image is built with no
reinstall — so the new dependency is absent and every test touching the new
parser errors. `espree`, added by the same PR, passes because it was already a
dependency.

**Fix.** `swebench/harness/test_spec/javascript.py`, `get_test_cmds_prettier`:
prepend `yarn install --silent > /dev/null 2>&1 || true` to the test command
list, re-syncing `node_modules` against the patched `package.json` before tests
run. Output is discarded so installer chatter cannot be mis-parsed as test
results, and failure is tolerated so a network hiccup degrades to the previous
behaviour instead of aborting the eval.

This fixes the *class* of bug rather than hardcoding `meriyah`, and it matters
for benchmark integrity beyond gold: an agent whose patch correctly adds a
dependency previously could not pass either.

Also replaced `list(set(test_cmds))` with `sorted(set(test_cmds))` — the old
form left eval.sh command order dependent on set iteration order.

**Verification.** Requires a real re-run (the eval script changed), unlike a
parser fix. Confirmed the generated eval script now runs the sync step first.

---

## 4. Docker client timeout + connection pool — spurious failures across all repos

**Symptom.** `BuildImageError: ... UnixHTTPConnectionPool(host='localhost'):
Read timed out. (read timeout=60)`. Hit **27** instances in the main sweep and 4
in the quarto sweep; the progress bar showed `error=15` after only 70 instances
— about a 21% spurious failure rate.

**Why it was dangerous.** The harness records these as instance *errors*, which
in the final report look identical to a genuine defect in the task instance.
Uncorrected, the run would have understated the resolved count and sent me
debugging instances that were never broken.

**Root cause.** Two docker-py defaults unsuited to a many-worker run:
- 60s request timeout — the daemon serialises heavy image builds, so container
  create/start calls routinely exceed 60s.
- 10-connection pool — saturated by 28 concurrent workers. The earlier
  "Connection pool is full, discarding connection: localhost. Connection pool
  size: 10" warnings in the run logs were the first sign, and I under-weighted
  them.

**Fix.** `swebench/harness/run_evaluation.py`: added `_docker_client()`
(600s timeout, 128-connection pool, both env-overridable via
`SWEBENCH_DOCKER_TIMEOUT` / `SWEBENCH_DOCKER_POOL_SIZE`) and used it for both
`docker.from_env()` call sites. The daemon does eventually answer, so raising
the ceiling removes the false failures rather than hiding them.

**Verified.** After restarting both sweeps: **0** ReadTimeout/BuildImageError
occurrences, versus 27 before. Restart cost nothing — `get_dataset_from_preds`
skips any instance with an existing `report.json`, and errored instances never
write one, so all 58 completed reports were preserved (main resumed with 429 of
486, quarto with 23 of 24).

---

## 5. eslint 8.50 — native `re2` build fails on an unsupported Node

**Symptom.** `eslint__eslint-17618` never produced a report:
`BuildImageError: The command '/bin/sh -c /bin/bash /root/setup_repo.sh'
returned a non-zero code: 1`.

**Root cause.** The build dies compiling the native `re2` module (v1.26.1):

```
gyp ERR! configure error
gyp ERR! stack TypeError: webidl.util.markAsUncloneable is not a function
gyp ERR! node -v v21.6.2
gyp ERR! node-gyp -v v13.0.1
```

eslint 8.50 was pinned to Node **21.6.2**, but node-gyp 13 declares engines
`^20.17.0 || >=22.9.0` — Node 21.x is not a supported runtime for it, and its
bundled undici calls a Node internal that 21.6.2 lacks.

**Fix.** `swebench/harness/constants/javascript.py`: pin eslint **8.50** to Node
**20.18.1** (nearest supported LTS, and contemporaneous with eslint 8.50's
Sept 2023 release). The loop that set both 8.1 and 8.50 to 21.6.2 is now split:
**8.1 keeps 21.6.2** — it resolves fine there and never installs re2, so there
was no reason to perturb a working pin. Only version 8.50 exists in the test
split (instance 17618), so the change is scoped to that one instance.

**Note — systemic risk.** eslint installs with a bare `npm install`, so
dependency resolution floats. `re2@1.26.1` is newer than whatever resolved when
the Docker Hub images were built in Jan 2025; the same drift can silently break
any repo that installs without a frozen lockfile. Worth a follow-up sweep beyond
tonight's scope.

**Verification.** Pending — needs a real re-run (env image changes with the node
version).

---

## 6. `patch --batch` silently REVERSE-applied gold patches

**Symptom.** `openlayers__openlayers-11047` unresolved with
`expected undefined to equal false` — the gold patch renames
`this.disposed_` -> `this.disposed` in `src/ol/Disposable.js`, yet at test time
the property was `undefined`, i.e. the rename had not taken effect. The harness
had logged `>>>>> Applied Patch:` and scored the instance as if the patch applied.

**Root cause — a five-step chain.**

1. The image build's `npm install` rewrote `package-lock.json` from
   `lockfileVersion: 1` to `lockfileVersion: 3` (visible in "Git diff before").
   The gold patch was generated against the v1 format, so its lockfile hunk can
   never apply.
2. `git apply --verbose` fails on that hunk.
3. `git apply --verbose --reject` applies every hunk it *can* — the three source
   files — and only rejects the lockfile. The worktree is now **partially
   patched**, and the command still reports failure.
4. The last fallback, `patch --batch --fuzz=5 -p1 -i`, sees those hunks already
   present and prints
   `Reversed (or previously applied) patch detected!  Assuming -R.`
   — `--batch` auto-answers "yes" — so it applies the entire patch **backwards**,
   undoing the correct changes.
5. That command exits 0, so the harness reports the patch as applied.

**Fix.** `swebench/harness/run_evaluation.py`: `GIT_APPLY_CMDS` last entry is now
`patch --batch --forward --fuzz=5 -p1 -i`. `--forward` makes patch *skip*
already-applied hunks instead of reversing them, so the three correctly-applied
source files survive and only the impossible lockfile hunk is skipped.

**Why `--forward` is sufficient on its own.** Nothing at test time reads
`package-lock.json` — `node_modules` was installed during the image build — so
leaving that one hunk unapplied is harmless. The alternative root fix (restoring
`package-lock.json` to its committed state after install, so `git apply` succeeds
first try) would change the env image for all 79 openlayers **and** 54 bpmn-js
instances, risking 133 currently-passing instances for no test-time gain. Not
worth it; recorded here as an option if the lockfile ever does matter.

**Scope.** 5 instances have gold patches touching `package-lock.json`:
`openlayers-11047` (6.3), `openlayers-13648` (6.14), `bpmn-js-1644` (9.0),
`bpmn-js-1802` (11.1), `bpmn-js-1928` (13.2). The `--forward` guard is
harness-wide and protects any future patch that lands in this state.

**Severity note.** This was the worst failure mode found tonight: a *silently
inverted* gold patch that the harness reports as successfully applied. Any
partially-applying patch — from an agent as well as from gold — could hit it.

---

## 7. `git clone` had no retry — transient GitHub 503s reported as instance errors

**Symptom.** Three openlayers instances (`13860`, `14015`, `15825`) never produced
a report:
`BuildImageError: The command '/bin/sh -c /bin/bash /root/setup_repo.sh'
returned a non-zero code: 128`. The build logs show why:

```
+ git clone -o origin https://github.com/openlayers/openlayers /testbed
error: RPC failed; HTTP 503 curl 22 The requested URL returned error: 503
fatal: error reading section header 'shallow-info'
```

**Root cause.** Every instance image clones the repo from scratch, so a repo with
many instances (openlayers 79, carbon 133, lighthouse/bpmn-js 54 each) issues
dozens of concurrent full clones of the same repository and draws transient
HTTP 503 throttling from GitHub. `setup_repo.sh` had a single unguarded
`git clone`, so one 503 killed the image build. As with the docker timeouts,
these land in the report as instance *errors* — indistinguishable from a genuine
defect.

**Fix.** `swebench/harness/test_spec/utils.py`,
`make_repo_script_list_common`: wrap the clone in a 5-attempt loop with linear
backoff (15s, 30s, 45s, 60s), `rm -rf` of any partial checkout between attempts,
and a trailing `[ -d <repo>/.git ]` so the script still fails loudly if every
attempt fails.

Safe under the generated script's `set -euxo pipefail`: a failing `git clone` is
the left operand of `&&`, which `set -e` does not treat as fatal, while the
trailing directory test still aborts the build when the clone genuinely never
succeeded.

**Scope.** Harness-wide; benefits every repo, most of all the high-instance-count
ones that provoke the throttling.

---

# Instances needing a re-run (no report.json — errored, not scored)

These never produced a report, so `get_dataset_from_preds` will pick them up
automatically on a follow-up pass with the same `--run_id`:

| instance | cause | fix |
|---|---|---|
| `eslint__eslint-17618` | re2/node-gyp on unsupported Node 21 | #5 node pin |
| `openlayers__openlayers-13860` | GitHub 503 during clone | #7 clone retry |
| `openlayers__openlayers-14015` | GitHub 503 during clone | #7 clone retry |
| `openlayers__openlayers-15825` | GitHub 503 during clone | #7 clone retry |
| `quarto-dev__quarto-cli-2689` | docker read timeout=60 (pre-restart) | #4 client timeout |

Verified that the docker-client fix holds: every `read timeout=60` log predates
the 08:31 restart, and there are **zero** `read timeout=600` occurrences.

# Still open

- `openlayers__openlayers-11545` — `ol.layer.Heatmap constructor has a default
  className` fails with `TypeError: Cannot read properties of undefined (reading
  'indexOf')` inside `new WebGLHelper`. First hypothesis (Chrome 131+ disabling
  software WebGL without `--enable-unsafe-swiftshader`) was **disproved**: in the
  actual image, Chrome 151 reports a live WebGL context with 35 extensions both
  with and without the flag. openlayers is otherwise 54/56, so this is a
  single-instance issue, not systemic — deliberately not "fixed" by changing the
  Chrome launcher for all 79 openlayers instances.

---

## 8. Install rewrote tracked lockfiles, so lockfile-touching patches could never apply

**Symptom.** After fix #6 (`--forward`), `openlayers__openlayers-11047` stopped
being silently reverse-applied and instead failed honestly with
`>>>>> Patch Apply Failed:` — an integrity win, but the instance still could not
resolve, because the gold patch genuinely could not be applied.

**Root cause.** npm 7+ silently upgrades `package-lock.json` from
`lockfileVersion: 1` to `2`/`3` during `npm install`. Because that file is
tracked, the worktree no longer matches `base_commit` once the image is built.
Every patch — gold or agent-produced — is generated against the committed
version, so any diff touching the lockfile can never apply: `git apply` fails
outright and `git apply --reject` leaves the tree partially patched.

**Fix.** `swebench/harness/test_spec/utils.py`,
`make_repo_script_list_common`: after `install`/`build`, restore any tracked
lockfile to its committed state:

```bash
for lockfile in package-lock.json npm-shrinkwrap.json yarn.lock; do
  git ls-files --error-unmatch "$lockfile" >/dev/null 2>&1 \
    && git checkout -- "$lockfile" || true
done
```

`node_modules` is fully installed by this point, so the lockfile's contents no
longer affect anything the tests do — reverting only realigns the worktree with
the commit the patches were written against. It runs *after* `build` so any build
step that reads the lockfile still sees the installed state. The `git ls-files`
guard makes it a no-op for repos that don't track these files, including every
non-JS repo.

**Cost: none.** I initially rejected this fix believing it would invalidate env
images for all 79 openlayers + 54 bpmn-js instances. That was wrong: `npm install`
lives in the *repo* script (`setup_repo.sh`, the instance image), not the env
script — `env_image_key` is byte-identical before and after — and instance images
are rebuilt every run anyway under `--cache_level env`.

**Verified.** `openlayers__openlayers-11047`: `>>>>> Applied Patch:` with no
"Failed to apply" and no "Reversed" line, F2P **14/14**, resolved. Previously
12/14 with the two `ol.Disposable` tests failing from the reverse-apply.

**Relationship to #6.** They fix different layers and both are needed: #8 makes
the patch apply in the first place, #6 guarantees that when a patch *does* only
partially apply, the harness never silently inverts it and reports success.

---

## 9. openlayers rendering tests hung forever — puppeteer launched headed Chrome

**Symptom.** The main sweep stalled: only 1 new report in 45 minutes, load down to
10, and just 4 containers alive for 16 workers. Four openlayers instances
(`15683`, `15787`, `15796`, `15825`) had `node test/rendering/test.js` running at
**0.6% CPU for 52-56 minutes**, versus **5-9 minutes** for rendering instances
that work (`15685`, `15614`, `13974`). Definitively hung, not slow — they would
each have burned the full 5400s timeout.

**Root cause.** openlayers' `test/rendering/test.js` defines:

```js
headless:       {default: !!process.env.CI}
puppeteer-args: {default: process.env.CI ? ['--no-sandbox', '--disable-setuid-sandbox',
                                            '--disable-dev-shm-usage'] : []}
```

The harness never set `CI`, so puppeteer launched Chrome **headed, with no sandbox
flags**. Creating a WebGL context in headed Chrome under Xvfb hangs indefinitely
in this image. Confirmed independently of the harness: a WebGL canvas loaded via
`xvfb-run google-chrome-stable` never returned (hung ~50 minutes, no output),
while the identical page under `--headless` reported a live context with 35
extensions instantly.

**Fix.** `swebench/harness/test_spec/javascript.py`, `get_test_cmds_openlayers`:
the rendering branch now runs `su chromeuser -c "CI=true npm run test-rendering"`.
`CI` is set *inside* the `su -c` string so it reaches npm regardless of how `su`
treats the caller's environment.

Headless is also the **correct** mode here, not merely a workaround: the reference
screenshots these tests diff against are generated by upstream CI, i.e. headless.
Running headed was the anomaly.

**Verified.** `openlayers-15683` (9.1, previously hung 56 min): resolved, F2P
**5/5**. `openlayers-13974` (7.0, previously passing *headed*): still resolved,
F2P 1/1 — no regression from the switch to headless.

**Impact.** ~11 further 8.1/9.0/9.1 rendering instances were queued to hang for
90 minutes each; this also removes the stall that was throttling the whole sweep.

**Hypotheses discarded en route** (recorded so they aren't re-tried):
- Chrome 131+ disabling software WebGL without `--enable-unsafe-swiftshader` —
  disproved; WebGL works headless with or without the flag.
- WebGL context exhaustion across a karma page — disproved; `15685`/`15614` pass
  on the same versions.
- A clean version split at 9.x — disproved; 9.0 and 9.1 both have passing
  rendering instances.
  What settled it was comparing CPU time against normal completion time, rather
  than reasoning from version numbers.

---

## 10. quarto: xelatex infinite loop on `tufte-pdf.tex` (TeX Live 2026 drift) — OPEN

**Symptom.** The quarto sweep produced 1 report in 3 hours. **All 10** running
containers had `xelatex -interaction=batchmode -halt-on-error tufte-pdf.tex`
burning **99.3% CPU for 2h32m-2h56m** in `/testbed/tests/docs/page-layout`. 100%
reproducible, identical document in every container.

99% CPU (not 0%) rules out waiting on input, and `-interaction=batchmode` is
already set — this is a genuine loop inside TeX. The `.log` stops mid-line while
loading `U+msb` font info and never grows again; the process spins on. The
document's line 250 is a `\marginpar` containing a footnote, and the log's last
warning is `hyperref Warning: Rerun to get /PageLabels entry` — consistent with a
margin/float placement loop in the tufte-handout class.

**Root cause: dependency drift, same class as #5.** The container has
**TeX Live 2026** (`tlmgr revision 79639, 2026-07-10`), installed fresh today by
`quarto install tinytex` inside `tests/configure-test-env.sh`, which always
fetches the latest. The dataset and its Docker Hub images were built in Jan 2025,
i.e. TeX Live 2024. Nothing pins the TeX distribution.

**Why it can't be skipped.** `[smoke] > quarto render docs/page-layout/tufte-pdf.qmd --to pdf`
is a **PASS_TO_PASS entry in 23 of 24 quarto instances**, so it is graded and must
genuinely pass. (`quarto-cli-475` resolved precisely because its older P2P list
contains only the `tufte-html` variant, not the PDF one — which is also why it
finished in 20 minutes rather than hanging.)

**Action taken.** Stopped the quarto sweep: all 10 workers were burning the full
14400s timeout for zero output, and 14 more instances were queued behind them.
Freed the machine for the productive main sweep.

**Status: unfixed.** The principled fix is pinning the TeX distribution to the
2024 era, but doing that properly means matching both the TinyTeX binaries and
the CTAN package versions that `quarto install tinytex` pulls on demand — a
half-pinned TeX is its own failure mode. Verifying the hypothesis against the
official `texlive/texlive:TL2024-historic` image is in progress; a pin should not
be shipped before that confirms TeX version is really the discriminator.

**Fix implemented (pending verification).** `swebench/harness/constants/javascript.py`:
`PIN_TINYTEX_2024` is appended to quarto's install commands, after
`configure-test-env.sh` has run its `quarto install tinytex`:

1. `rm -rf /root/.TinyTeX /opt/TinyTeX` — discard the TL2026 install.
2. Reinstall with `TINYTEX_VERSION=2024.12` (verified: the `v2024.12` release and
   its `TinyTeX-1-v2024.12.tar.gz` asset both exist and the installer honours
   that variable).
3. `tlmgr option repository <TeX Live 2024 tlnet-final>` so packages installed
   on demand during a render come from the same era as the binaries — a
   half-pinned TeX (2024 binaries, 2026 packages) is its own failure mode.
4. A pipe-free sanity check that fails the image build loudly unless
   `xelatex --version` reports "TeX Live 2024", so an unpinned image can never
   silently ship and hang at test time again.

Note on step 4: it was first written as `xelatex --version | head -1 | grep -q`.
Under the generated script's `set -o pipefail`, `head`/`grep -q` exit on first
match and SIGPIPE xelatex, which would fail the build *even when the pin worked*.
Rewritten with a `case` statement and no pipe.

**Trap hit while verifying:** the harness reuses any existing instance image
("Found N existing instance images. Will reuse them."), and the killed quarto
sweep had left 14 pre-pin images on disk. The first verification silently ran the
**old** TL2026 image. Purge `sweb.eval.*quarto*` images (or pass
`--force_rebuild`) before re-running.

---

# HANDOFF.md's "remaining genuine defects" list needs revising

Instances HANDOFF.md records as genuine defects that in fact resolve cleanly here:

| instance | HANDOFF.md claim | actual |
|---|---|---|
| `prettier-9514` | jest snapshot mismatch | missing `meriyah` dep (#3) — F2P 0/36 -> **36/36** |
| `grommet-2061` | jest snapshot mismatch | resolves, F2P 3/3 P2P 36/36 (parser bug #1) |
| `grommet-2124` | jest snapshot mismatch | resolves, F2P 5/5 P2P 40/40 (parser bug #1) |

The grommet pair is instructive: the duration-suffix parser bug (#1) only bites
when a test file runs slowly enough for jest to print a duration, so on a slower
machine it presents exactly as a "snapshot mismatch".

Still genuinely open: `openlayers-11545` (WebGL Heatmap), `bpmn-js-1203`
(label-snapping). `lighthouse-1446` had not yet run at time of writing, though
lighthouse is otherwise 51/51.

---

## 11. puppeteer's Chromium download stalls image builds indefinitely

**Symptom.** The sweep starved: load average fell to **1.8** with only 6 workers
busy and zero eval containers. All six were wedged in
`node_modules/puppeteer/install.js` at <1% CPU, ages 19min, 34min, 57min and
**1h46m**, simultaneously across **lighthouse, openlayers and bpmn-js**.

**Root cause.** puppeteer's postinstall fetches a ~150MB Chromium from Google
Cloud Storage on *every* instance image build. After several hundred builds those
fetches begin to stall: the TCP connection stays ESTABLISHED (verified in
`/proc/<pid>/net/tcp`) while the process makes no progress. Image builds have no
timeout, so the worker is wedged forever instead of failing and being retried.

**Fix.** `swebench/harness/constants/javascript.py`: prepend
`export PUPPETEER_SKIP_DOWNLOAD=true PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true`
(the latter covers puppeteer <19) to the install commands of `openlayers`,
`bpmn-js`, `alibaba-fusion/next` and `lighthouse`. For these repos the download
is **waste even when it succeeds**: the harness runs them against the system
`/usr/bin/google-chrome-stable` via `SET_PUPPETEER_ENV_VAR`, and
`SET_PUPPETEER_PATH` rewrites `require('puppeteer').executablePath()` out of
their karma configs.

**Deliberately not global.** carbon (133 instances) has no such override and may
use the bundled browser; skipping there could break a large currently-passing
set. Verified scoping: carbon generates no skip, the four target repos do. Blast
radius is small regardless — the harness skips instances that already have a
`report.json`, so only not-yet-run instances are affected.

**Monitoring gap this exposed.** My hang detector matched only `sweb.eval.*`
containers, but docker *build* intermediates get random names (`bold_hopper`,
`elated_perlman`), so a build-phase stall was invisible for over an hour. The
detector now watches both.

---

## Note: quarto no longer needs a separate long-timeout sweep

With the TinyTeX 2024 pin (#10) the quarto suite completes in ~17 minutes rather
than hanging, so the 24 quarto instances run in the main sweep under the ordinary
5400s timeout. The separate `mm-gold-quarto` run is retired.

## Note: `tlmgr update --self` needed before installing from the frozen repo

tlmgr refuses to install from a repository whose tlmgr is newer than the local
one ("tlmgr itself needs to be updated ... Terminating", exit 255, which fails
the image build). TinyTeX v2024.12 ships an older tlmgr than TL2024's
tlnet-final, so `tlmgr update --self` runs first; it pulls from the same frozen
repository and therefore stays inside TeX Live 2024.

---

## 12. `next-3345`: FAIL_TO_PASS demanded a test the test_patch commented out

**Symptom.** F2P 17/18. The one failure,
`Dropdown - autoFocus=true should have any activeElement when triggered by keyboard`,
was **absent from the log entirely** (parsed 66 statuses, none matching).
HANDOFF.md records this instance as "headless-focus `activeElement`", implying an
environment problem.

**Root cause.** The instance's own test_patch disables the test:

```diff
-    it('autoFocus=true should have any activeElement when triggered by keyboard', done => {
+    // it('autoFocus=true should have any activeElement when triggered by keyboard', done => {
```

The upstream PR deliberately commented it out, but FAIL_TO_PASS still demands it.
A commented-out test never runs, and `grading.test_failed` counts an absent test
as failed, so the instance can never resolve however correct the patch is.

**Fix.** Added `scripts/find_disabled_tests.py`, which scans every instance for
graded tests that its own test_patch comments out or deletes without re-adding.
Dataset-wide it finds **exactly 1** instance, so the class is narrow -- but the
rule (not the instance id) is what got wired into `clean_mm_artifacts.py`,
importing the shared `disabled_titles()` so audit and cleaning cannot drift apart
and a future regeneration catches new occurrences.

**Verified.** Re-grading the existing log against the corrected dataset:
F2P 17/17, P2P 49/49, resolves.

---

## 13. Patches that add a dependency were never installed (generalised from #3)

**Symptom.** `next-2131` unresolved with **zero** tests parsed. The log shows
webpack failing before any test ran:

```
ERROR in ./src/tree/view/tree.jsx
Module not found: Error: Can't resolve 'lodash.clonedeep' in '/testbed/src/tree/view'
ℹ ｢wdm｣: Failed to compile.
```

Its gold patch adds `"lodash.clonedeep": "^4.5.0"` to package.json and imports it.
HANDOFF.md records this instance as "`Tree - should render by children` fails",
which reads like a genuine test failure.

**Scope (audited).** **14 instances across 7 repos** have gold patches that add a
package.json dependency: next (5), grommet (3), bpmn-js (2), scratch-gui,
prettier, openlayers, lighthouse. Four more of HANDOFF.md's "genuine defects" are
in that list -- `next-870` (axe-core), `next-101` (inquirer), `openlayers-13648`
(geotiff), `bpmn-js-1802` (diagram-js).

**Fix.** Replaced the prettier-only sync from #3 with one mechanism in
`make_eval_script_list_js` (`_SYNC_DEPS_IF_MANIFEST_CHANGED`), applied to every JS
repo but **conditional on `git diff --quiet HEAD -- package.json`** -- so it runs
only for instances whose applied patch actually touched the manifest, leaving the
~250 already-passing instances untouched. It picks yarn or npm by probing for
`yarn.lock`, is emitted *before* `START_TEST_OUTPUT` so installer output cannot
reach the log parsers, and tolerates failure.

It also re-runs `chmod -R a+rX node_modules`: the install runs as root while
next/openlayers/bpmn-js execute tests as `chromeuser` via `su`, so without that
the fix would trade one failure for another.

Matters beyond gold: an agent whose patch correctly adds a dependency previously
could not pass either.

---

## 14. `chmod -R 777` ran before `git reset --hard`, so it was undone

**Symptom.** `next-4859` and `next-4806` image builds exited **243**:

```
npm ERR! errno: -13, code: 'EACCES', syscall: 'open',
npm ERR! path: '/testbed/package-lock.json'
```

**Root cause.** `make_repo_script_list_common` ordered the setup as
`clone -> chmod -R 777 -> cd -> git reset --hard`. But `git reset --hard`
rewrites every tracked file that differs from the cloned HEAD, and the rewritten
files land root-owned with default 0644 permissions -- silently undoing the chmod.
alibaba-fusion/next installs as an unprivileged user
(`su chromeuser -c 'npm install'`), so for any instance whose base commit has a
committed `package-lock.json` that git had to rewrite, npm could not write it.
Instances where git happened *not* to rewrite the file kept 0777 and built fine,
which is what made this present as intermittent rather than ordered.
(Confirmed: `package-lock.json` exists at next-4859's base commit, and the build
log shows `chmod` executing before `git reset --hard`.)

**Fix.** `swebench/harness/test_spec/utils.py`: move `chmod -R 777` to *after*
`git reset --hard` / `git remote remove origin`, so it applies to the finalised
tree. The lockfile-restore loop from #8 also re-chmods each file it checks out,
since `git checkout --` resets permissions the same way.

**Pre-existing, not introduced tonight** -- the ordering is unchanged from
upstream; it only surfaced once the sweep reached next, whose install drops
privileges.

**Verification of #13.** Re-ran both affected instances with the generic sync:

| instance | before | after |
|---|---|---|
| `alibaba-fusion__next-2131` | 0 tests parsed (webpack failed to compile) | **RESOLVED**, F2P 1/1 |
| `openlayers__openlayers-13648` | patch unapplicable + `geotiff` missing | **RESOLVED**, F2P 1/1 |

The guard fired as intended (`package.json changed by patch; re-syncing
dependencies`) and `Can't resolve 'lodash.clonedeep'` no longer appears in the log.
`openlayers-13648` needed three fixes stacked: #8 so the lockfile-touching patch
could apply at all, #6 so a partial apply could not be inverted, and #13 for the
new dependency.

---

## 15. `git apply --3way`: install steps diverge tracked files, blocking valid patches

**Symptom.** `next-101`, `next-114`, `next-870` all errored with
`>>>>> Patch Apply Failed:` and produced no report. The log shows all three
strategies failing in turn, with `patch --forward` correctly reporting
"Reversed (or previously applied) patch detected!  Skipping patch." for every
hunk -- i.e. `git apply --reject` had already applied part of the patch, and the
non-zero exit then aborted the instance.

**Root cause.** alibaba-fusion/next's install steps install extra packages:

```
npm install babel-preset-es2015
npm install cheerio@1.0.0-rc.3
npm i sass@1.36.0 --save-exact
```

Each rewrites `package.json`, so the worktree no longer matches `base_commit`.
Any gold patch that also edits `package.json` then cannot apply cleanly. All
three failing instances touch `package.json`; `lighthouse-1446` fails for an
unrelated reason and is still open.

**Fix.** `swebench/harness/run_evaluation.py`: insert
`git apply --verbose --3way` **before** the lossy `--reject` fallback. A 3-way
merge uses the blobs recorded in the diff -- which the repo already has -- so it
reconciles "install added a dependency line" with "patch added a different
dependency line" rather than giving up. Ordering matters: `--reject` applies what
it can and leaves the tree half-patched, and that half-patched state is exactly
what then defeats the `patch` fallback.

**Why not restore package.json like the lockfiles (#8).** Restoring it would drop
those install-time packages from the manifest, and npm 7+ prunes extraneous
packages during install -- so the dependency re-sync from #13 could then delete
`babel-preset-es2015` and break next a second way. `--3way` keeps both sets of
changes.

---

## 16. A stack-frame artifact the artifact patterns missed

**Symptom.** `next-665` unresolved on one FAIL_TO_PASS entry that is not a test:

```
Table - at MessagePort.listener (http://localhost:9877/absolute/testbed/
node_modules/babel-polyfill/dist/polyfill.js?a53df70d...)
```

**Root cause.** The existing stack-frame pattern `\bat [^ ]*:\d+:\d+` only fires
when the token immediately after `at ` carries `:line:col`. Here the token is
`MessagePort.listener` and the location sits inside the parentheses, so the entry
survived the cleanup and was graded as a real test.

**Fix.** `scripts/clean_mm_artifacts.py`: added
`re.compile(r"\bat \S+ \((?:https?://|/)")`. A genuine test title would not
contain `at <token> (http://` or `at <token> (/`.

**Verified.** Re-grading `next-665`'s existing log against the regenerated
dataset: F2P 39/39, P2P 4/4, resolves. Dataset-wide artifact count 29 -> 30, and a
scan confirms no other stack-frame-shaped entries remain in any graded list.

Current dataset: `mm_test.corrected4.json`.

---

## 17. Mocha hook pseudo-tests baked into FAIL_TO_PASS

**Symptom.** `next-1720` unresolved on one absent F2P entry:
`Search - behavior - "after each" hook for "should support onChange/onSearch "`.
HANDOFF.md records this instance as "`afterEach` hook throws".

**Root cause.** That string is not a test -- it is mocha's synthetic label for a
**hook** failure. Mocha only emits it when a before/after hook throws, so it got
captured into FAIL_TO_PASS at dataset-construction time. Under a correct patch the
hook succeeds, the label never appears, and `grading.test_failed` counts the
absence as a failure. So the defect is in the data, not the environment.

**Fix.** `scripts/clean_mm_artifacts.py`: added
`re.compile(r'"(?:before|after) (?:each|all)" hook')`. A real test title cannot
contain `"before each" hook` / `"after all" hook`.

**Scope & verification.** Dataset-wide: 2 entries, in `next-1720` and
`openlayers-10478`. `next-1720` re-grades to F2P 10/10, P2P 19/19, resolves.
`openlayers-10478` was already resolved (see the note below on fail-only grading).

Dataset artifact total across the run: 29 -> 30 (#16) -> 32 (#17).
Current dataset: `mm_test.corrected5.json`.

---

## Tooling correction: fail-only repos in the triage script

`scripts/triage_gold_run.py` applied pass/fail semantics to every repo, but repos
in `constants.FAIL_ONLY_REPOS` (openlayers, bpmn-js, eslint, chartjs, p5.js,
marked) use parsers that record only failures, so grading treats an **absent** test
as a pass (`grading.check_fail_only`). The script therefore reported every silent
pass as "missing" for those repos -- `openlayers-10478` looked unresolved with 2
missing entries while the harness correctly reported it resolved. Fixed to consult
`FAIL_ONLY_REPOS`. Headline resolved/unresolved counts were never affected (those
come from report.json's authoritative `resolved` flag); only the bucketing was
misleading.

---

## OPEN (highest priority): carbon accessibility-checker API drift

**Symptom.** `carbon-8469`: F2P 1/1 passes, but one PASS_TO_PASS file fails --
`packages/react/src/components/CodeSnippet/__tests__/CodeSnippet.Skeleton-test.js`:

```
● CodeSnippetSkeleton › automated accessibility testing › should have no AC violations
  TypeError: ace.Checker is not a constructor
    at Object.aChecker.getComplianceHelperLocal (node_modules/accessibility-checker/lib/ACHelper.js:658:27)
```

**Why it matters.** **70 of 133 carbon instances** grade a Skeleton/a11y test
file, so this potentially decides the largest repo in the split.

**Two candidate mechanisms, not yet distinguished:**
1. *npm package drift.* `config/jest-config-carbon/package.json` declares
   `"accessibility-checker": "^3.1.1"`. Images were pushed ~2025-01-22, when the
   newest 3.x was **3.1.79** (2024-12-13); today the range resolves to **3.1.85**
   (2025-06-26). *Counter-evidence:* carbon commits a `yarn.lock`, and yarn 1
   installs exactly what the lock pins, so the package version should be stable.
2. *CDN engine drift.* `accessibility-checker` fetches the ACE rule engine from
   `cdn.jsdelivr.net` at runtime -- which is precisely why HANDOFF.md lists that
   host as required ("carbon tests make live HTTP calls at runtime"). The default
   rule archive is `latest`, so the engine can drift out of step with the pinned
   npm package, which fits `ace.Checker is not a constructor` better than (1).

**Deliberately not fixed yet.** Only one carbon instance had reported at the time
of writing, and pinning the wrong layer would either be a no-op or perturb 133
instances. The correct next step is to read the installed
`node_modules/accessibility-checker/package.json` version and the archive URL it
requests inside a built carbon image, then pin whichever layer actually moved
(`ruleArchive` in achecker config, or a `resolutions` entry for the npm package).
The finalize sweep will also report how many carbon instances genuinely fail this
way, which should come before any change of that blast radius.

---

## 18. Patch-apply verdict ignored whether the patch actually ended up applied

**Symptom.** `next-101`, `next-114`, `next-870` (and `lighthouse-1446`) still
errored with `>>>>> Patch Apply Failed` *after* `--3way` (#15) was added. The tail
of the log shows the final fallback reporting, for file after file:

```
Reversed (or previously applied) patch detected!  Skipping patch.
4 out of 4 hunks ignored -- saving rejects to file src/table/virtual.jsx.rej
```

i.e. by the time the last strategy ran, the patch was *already there*.

**Root cause.** The apply chain is not side-effect free, but the verdict is drawn
purely from exit codes:

```python
for git_apply_cmd in GIT_APPLY_CMDS:
    val = container.exec_run(...)
    if val.exit_code == 0: applied_patch = True; break
if not applied_patch: raise EvaluationError(...)
```

`git apply --3way` and `git apply --reject` each apply every hunk they can
*before* reporting failure, so every attempt hands a dirtier tree to the next.
The end state can be a fully-patched worktree in which no single command exited 0
-- and the instance is then thrown away despite being correctly patched.

**Fix.** `swebench/harness/run_evaluation.py`: before raising, run
`git apply --check --reverse <patch>`. That is a dry run which succeeds only if
the diff could be cleanly *un*-applied, i.e. it is already fully present; a
partially-applied patch still fails it, so it cannot manufacture a false pass.
If the check passes, the patch is treated as applied.

**Relationship to #6 and #15.** Three layers of the same underlying problem:
#15 lets a valid patch apply to a legitimately-modified tree, #6 stops a partial
apply from being silently *inverted*, and #18 stops a successfully-applied patch
from being discarded because no individual command returned 0.

---

## Note: docker client timeout raised again (600s -> 1800s)

Nine carbon instances errored with `read timeout=600` -- the ceiling from #4 was
itself exceeded. Carbon instance images are ~14GB and, with 16 concurrent builds,
the NVMe saturates: load 150-480 with almost no CPU consumed, i.e. processes
blocked in I/O, so even container create/start crawls past 600s. Raised the
default to 1800s **and** dropped the sweep to 8 workers. Result: **0** new
ReadTimeouts in the following 45 minutes.

Fewer workers is also faster here -- at 16 workers roughly a third of carbon's
work was being discarded.

## Note: the finalize wait needed debouncing

Killing the sweep to pick up a fix made the armed `finalize_gold.sh` conclude the
run had ended, and it launched its own retry harness on the same `--run_id`,
racing the restarted sweep over reports and image builds. The wait is now
debounced (10 consecutive minutes of harness absence, reset if it reappears) plus
a hard guard that aborts if any `run_evaluation` process is alive.

---

## Carbon a11y drift: diagnosis refined (still OPEN, still unfixed)

Two further carbon instances (`carbon-13851`, `carbon-14476`) failed on the
**identical three** PASS_TO_PASS files -- Breadcrumb, Link, Select -- with
FAIL_TO_PASS passing in both. Same three files, different instances: systematic,
not per-instance.

All failures are `automated verification testing › should have no Accessibility
Checker violations`, with two signatures:

```
SyntaxError: unknown pseudo-class selector ':scope>*'
Level: violation
```

**This settles which of the two candidate mechanisms is at work.** Both signatures
are *engine* behaviour, not npm-package API shape: the engine emits a CSS selector
the test environment's jsdom cannot parse, and reports violations the older engine
did not. Combined with carbon committing a `yarn.lock` (so yarn 1 pins the npm
package deterministically), hypothesis 1 -- `^3.1.1` drifting 3.1.79 -> 3.1.85 --
is **ruled out**. The mover is the **ACE rule engine fetched from
cdn.jsdelivr.net at runtime**, which is exactly why HANDOFF.md lists that host as
required. `accessibility-checker` defaults to `ruleArchive: latest`, and carbon has
no `.achecker.yml` at these commits, so the archive is whatever CTAN-equivalent
"latest" means on the day the tests run -- unpinned by construction.

Note this is *also* why `ace.Checker is not a constructor` appeared on
`carbon-8469`: a newer engine bundle against a lockfile-pinned package.

**Recommended fix (not applied).** Add an `.achecker.yml` at image-build time
pinning `ruleArchive` to a dated archive contemporaneous with the Jan-2025 image
build, rather than `latest`. That is the same "pin the unpinned external" shape as
the TinyTeX fix (#10), which is verified working.

**Why I did not ship it tonight.** The archive identifier has to be read from the
engine's published archive list and then validated by a real carbon run (~30-40
min per build), and the change would touch all 133 carbon instances. Shipping an
unvalidated pin across the largest repo in the split is worse than leaving a
precisely-documented diagnosis. The finalize sweep will also report exactly how
many carbon instances fail this way, which should inform whether to pin the
archive or instead treat these a11y assertions as environment-dependent.

### Carbon a11y: the exact pin value (ready to apply, still unvalidated)

The authoritative rule-archive list is `https://able.ibm.com/rules/archives.json`
(73 archives, each with a dated `id`). The archive contemporaneous with the
2025-01-22 image push is:

```
id=12December2024    name=12 December 2024 Deployment (IBM 7.3)
```

The next one is `10February2025`, i.e. after the images were built, so
**`12December2024`** is the correct target. (Some later archives carry `_3`
suffixes for accessibility-checker 3.x; `12December2024` has no such variant,
consistent with 3.x being the default at that date.)

Applying it means writing an achecker config at image-build time, in carbon's
install commands, e.g. `.achecker.yml` at the repo root:

```yaml
ruleArchive: 12December2024
```

An untracked config file is safe with respect to patch application -- `git apply`
and `git diff` both ignore untracked files, so it cannot re-introduce the
divergence problems of #8/#15.

**Why it is still not applied.** Two unknowns remain that only a real carbon run
can settle: whether carbon's jest setup supplies its own achecker config that
would override or conflict with this file, and which `policies` list the pinned
archive needs (an empty or mismatched policy set changes which violations are
reported). Getting either wrong risks breaking the **76%** of carbon instances
that currently pass in order to fix the ~24% that fail -- a bad trade without a
validating build (~30-40 min each).

**Measured impact so far:** of 17 carbon instances reported, 13 resolved and all
4 failures carry the a11y signature, with **zero** other carbon failure modes.
Extrapolated, this single cause accounts for roughly 30 of 133 carbon instances --
worth fixing, but worth validating first.

### Carbon a11y: archive pin TESTED and REVERTED (negative result)

I applied the `12December2024` pin and ran `carbon-13851` end to end. Result:
**still unresolved**, same three P2P files (Breadcrumb, Link, Select), F2P 1/1.

The experiment was still worth running, because it eliminates a hypothesis:

* **The config is honoured.** `archives/12December2024/` appears in the run
  output, so `.achecker.yml` at the repo root is read and the engine really does
  fetch the pinned archive. The mechanism works.
* **But the error only changed shape**, from
  `TypeError: ace.Checker is not a constructor` to
  `TypeError: ace_ibma.Checker is not a constructor`.

So the rule archive is not the only thing out of step: the
`accessibility-checker` npm package and the ACE engine have to be aligned
*together*. Pinning either one alone just swaps one incompatibility for another.
That also means my earlier "hypothesis 1 is ruled out" was too strong -- the npm
package version is back in scope, as one half of a pair, even though yarn.lock
pins it deterministically.

**Reverted** from `SPECS_CARBON`: it delivers no benefit and would change
behaviour for every not-yet-run carbon instance without validation.
`CARBON_ACHECKER_ARCHIVE` is retained in the constants as a starting point.

**Next step for whoever picks this up:** inside a built carbon image, read
`node_modules/accessibility-checker/package.json` for the resolved version, then
find the archive whose engine exposes the symbol that version's `ACHelper.js`
expects (`ace.Checker` vs `ace_ibma.Checker` distinguishes the two eras). Pin
*both* -- a `resolutions` entry for the package plus the matching `ruleArchive` --
and validate on one instance before applying to all 133.

### quarto babel fix: REVERTED after it regressed the whole repo

Adding `tlmgr update --self` + `tlmgr install collection-langfrench
collection-langeuropean babel-french` to fix `docs/latexmk/babel.Rmd` made quarto
much worse. Measured:

| config | instance | P2P |
|---|---|---|
| TinyTeX 2024 pin alone (validated) | quarto-cli-5010 | **516/518** |
| pin + collection install | quarto-cli-1029 | **153/175** |
| pin + collection install | quarto-cli-896 | **150/172** |

Under the pin alone every `docs/latexmk/*.Rmd` render passed
(bibliography-citeproc / natbib / biblatex, make-index, all, estopdf). With the
collection install **all of them fail**, and `quarto-cli-2756` was additionally
caught by the hang detector with `xelatex` spinning at 99.3% CPU for 76 minutes --
i.e. the collection install also **reintroduces the original tufte-pdf infinite
loop** that the pin had fixed (verified fixed at "tufte-pdf ... ok (23s)").

So `tlmgr update --self` against the frozen TL2024 snapshot, and/or the collection
install that follows it, leaves the TeX tree unusable for quarto's PDF pipeline.
Trading one graded test in 18 instances (`babel.Rmd`) against ~20 failures plus a
90-minute hang in every quarto instance is clearly wrong.

**Reverted** to the pin-only configuration that was actually measured.

**Process failure worth recording:** the collection install was added *after* the
only validating run, and the build that would have caught it died on the tlmgr
version error -- I then treated fixing that build error as validating the change.
Any future attempt at `babel.Rmd` must install `babel-french` without disturbing
the rest of the tree and must be re-measured against the 516/518 baseline.

Operational note: quarto instance images built with the bad config are stale.
`finalize_gold.sh` deletes the instance image of every still-unresolved instance
before re-running it, so these rebuild against the reverted spec automatically.

### CORRECTION: the TinyTeX 2024 pin (#10) is NOT a general fix

I previously recorded #10 as verified. That claim rested on **one** instance and
is too strong.

`quarto-cli-4025` and `quarto-cli-3853` were built at 11:26/11:29 on 2026-08-04
with the **reverted pin-only** configuration -- build logs confirm no
`tlmgr install`, no `update --self`, and "TinyTeX pinned to TL2024 OK" -- and both
still hung with

```
xelatex -interaction=batchmode -halt-on-error tufte-pdf.tex   (99.3% CPU, 75+ min)
cwd: /testbed/tests/docs/page-layout
```

i.e. the identical infinite loop on the identical document that #10 was supposed
to fix, and which it *did* fix for `quarto-cli-5010` ("tufte-pdf ... ok (23s)",
P2P 516/518).

**What that means.** TeX Live 2024 vs 2026 is a real factor -- measured directly,
TL2024 renders that document in 9s while TL2026 never finishes -- but it is not
sufficient. Different quarto versions ship different `tufte-pdf.qmd` content and
different TeX package sets, so pinning the distribution fixes some instances and
not others. The honest status of quarto is therefore:

* `quarto-cli-475` resolves (older P2P list, no tufte-pdf entry).
* `quarto-cli-5010` resolves to 516/518 with the pin (only babel.Rmd + the rotted
  online-image test failing).
* `quarto-cli-4025`, `-3853`, `-2756` still hang **with** the pin.

**Next step.** Diff `tests/docs/page-layout/tufte-pdf.qmd` (and the generated
`.tex`) between 5010's commit and 4025/3853's, and compare the resolved TeX
package versions in each image. The loop is document-plus-package specific, not
purely distribution-version specific. Until that is understood, quarto should not
be reported as fixed.

Hung containers were killed manually rather than left to burn the 5400s timeout;
`finalize_gold.sh` will re-run these instances, so they need a real fix before the
final numbers can improve.

### Nuance on #10: partially effective, measured

Two corrections in sequence, so the record is precise:

* I first called the pin "verified" on the strength of one instance -- too strong.
* I then called it "not a general fix" -- too pessimistic in the other direction.

Measured position: **quarto went from 1 resolved to 7 resolved of 24** with the
pin in place. So TeX Live 2024 vs 2026 is a genuine and substantial factor, and
the pin should be kept. But roughly 5-8 instances still hit the `tufte-pdf.tex`
infinite loop even on TL2024, because different quarto versions ship different
copies of that document and different TeX package sets.

Because the loop never terminates, those instances can only be killed or burn the
full 5400s timeout, so a reaper now kills containers showing the known signature
(`xelatex` on `tufte-pdf.tex`) after 25 minutes instead of 90. They are recorded
as errors either way; reaping just stops them starving the rest of the sweep.
Anything else that looks stuck is reported, never auto-killed.

### HIGHEST-VALUE NEXT FIX: `babel.Rmd` is the sole blocker for many quarto instances

With the pin-only config, several quarto instances now fail on **exactly one**
graded test:

| instance | F2P | P2P |
|---|---|---|
| `quarto-cli-4708` | 1/1 | **504/505** -- only `docs/latexmk/babel.Rmd --to pdf` |
| `quarto-cli-4732` | 1/1 | **509/510** -- only `docs/latexmk/babel.Rmd --to pdf` |
| `quarto-cli-5010` | 1/1 | 516/518 -- `babel.Rmd` + the rotted online-image test |

`babel.Rmd` does `\usepackage[french]{babel}` and fails with
`Unknown option 'french' ... french.ldf was not found`, because the minimal
TinyTeX lacks `babel-french` and quarto's on-demand resolver cannot map
`french.ldf` to a package. It is a PASS_TO_PASS entry in **18 of 24** quarto
instances.

**Do NOT retry the approach that failed.** `tlmgr update --self` followed by
`tlmgr install collection-langfrench ...` regressed quarto badly (P2P 516/518 ->
153/175, and it reintroduced the tufte-pdf hang). tlmgr refused a plain install
("tlmgr itself needs to be updated"), which is what tempted me into
`update --self` in the first place -- that is the trap.

**Suggested safe approach:** install the package files directly from the frozen
TL2024 snapshot, bypassing tlmgr entirely, e.g. fetch
`<TEXLIVE_2024_REPO>/archive/babel-french.tar.xz`, extract into
`/root/.TinyTeX/texmf-dist`, then `texhash /root/.TinyTeX`. That adds only the
missing language files and cannot perturb the rest of the tree the way an
in-place tlmgr upgrade does.

**Validate against these exact baselines** before keeping it: `quarto-cli-4708`
must reach 505/505 and `quarto-cli-4732` 510/510, and `quarto-cli-5010` must not
drop below 516/518. If `babel.Rmd` is fixed without collateral damage, that
plausibly converts most of the 18 affected instances.

### quarto: final measured breakdown (24 instances)

| status | count | detail |
|---|---|---|
| resolved | 7 | up from 1 before the TinyTeX 2024 pin |
| babel-only failure | 5 | `5292`, `4708`, `4732`, `5091`, `5064` -- every one would resolve if `babel.Rmd` were fixed |
| other | 3 | `1029` + `896` (22 fails each) are stale builds from the *reverted* bad config and should improve to babel-only on re-run; `6902` has 2 fails, uninvestigated |
| no report | 9 | the `tufte-pdf.tex` infinite loop, unfixed |

Realistic ceiling without new work: **7**. With a safe `babel.Rmd` fix:
**~12-14**. The remaining ~9 need the tufte-pdf loop solved, which is
document-plus-package specific and not addressed by the distribution pin alone.

This is why `babel.Rmd` is the highest-value next fix: one change, five instances
immediately, probably seven once the two stale builds are re-run.

---

## 20. quarto `babel.Rmd` — install babel-french without touching tlmgr  [VERIFIED]

**Symptom.** `docs/latexmk/babel.Rmd --to pdf` fails with
`Unknown option 'french' ... french.ldf was not found`. Minimal TinyTeX omits
`babel-french`, and quarto's on-demand resolver cannot map `french.ldf` to a
package. It was the **sole** remaining failure in several quarto instances
(quarto-cli-4708 at P2P 504/505, quarto-cli-4732 at 509/510) and a PASS_TO_PASS
entry in 18 of 24.

**Fix.** `swebench/harness/constants/javascript.py`, appended to
`PIN_TINYTEX_2024`: fetch `babel-french.tar.xz` from the same frozen TL2024
snapshot the distribution is pinned to, extract `tex/generic/babel-french` into
`/root/.TinyTeX/texmf-dist`, then `mktexlsr`. Every step is `|| true`.

**Why this shape.** `tlmgr install` refuses against a frozen snapshot ("tlmgr
itself needs to be updated"), and the earlier workaround -- `tlmgr update --self`
-- wrecked the tree (P2P 516/518 -> 153/175, tufte-pdf hang returned). This is
purely **additive**: six `.ldf` files, nothing already installed is modified, and
a fetch failure degrades to the previous behaviour instead of breaking the build.

**Verified against the recorded baseline.** `quarto-cli-4708`: P2P **504/505 ->
505/505**, `babel.Rmd --to pdf ... ok`, instance **RESOLVED**, no other test
regressed. This is the before/after check whose absence caused the earlier
regression.

Expected to also clear `4732`, `5292`, `5091`, `5064` (all babel-only), and to
move `1029`/`896` once they are rebuilt off the reverted config.

---

## CRITICAL: carbon's a11y tests are NON-DETERMINISTIC (fetch `latest` at runtime)

Re-running `carbon-8469` with no carbon-related change whatsoever took it from
**P2P 160/161 (a11y failure)** to **161/161 RESOLVED**. Across the whole repo,
carbon moved from **18 unresolved to 8** over the same period -- again with no
carbon fix applied.

**Why.** `accessibility-checker` fetches the ACE rule engine from
cdn.jsdelivr.net at run time and defaults to `ruleArchive: latest`, i.e. whatever
IBM has deployed at that moment. So the same instance, same image, same patch can
pass or fail depending on the day. These tests do not measure the repository at
all; they measure IBM's current deployment.

**This matters more than the failure count.** Even the carbon instances that pass
today are not reliably reproducible. For an open-sourced benchmark that is a
correctness problem in its own right: a user running gold eval next month may get
a different score for reasons entirely outside the dataset.

**The era-matched pin (identified, not yet applied).** Read from a retained
failing image:

* installed `accessibility-checker` = **3.1.1** (released 2020-10-09) -- so
  yarn.lock *does* pin the package deterministically; the package is not drifting.
* its `ACHelper.js` references **`ace.Checker`** (8 sites).
* no engine is declared or installed -- confirming the engine is fetched at runtime.

The archive contemporaneous with 3.1.1 is **`07Oct2020`** ("07 October 2020
Deployment (IBM 7.2)"), available in `https://able.ibm.com/rules/archives.json`.
My earlier failed attempt pinned `12December2024` -- four years newer than the
package -- which is exactly why it only swapped `ace.Checker` for
`ace_ibma.Checker` instead of fixing anything.

**Recommendation:** pin `ruleArchive: 07Oct2020` via `.achecker.yml` written at
image-build time (mechanism already proven to be honoured -- the pinned archive
path appeared in the run output). Validate against a retained failing image, using
`--cache_level instance` so the image survives for inspection. Even if the current
`latest` happens to pass, pinning is required for reproducibility.

**Fix #20 rollout complete.** All five babel-only quarto instances now resolve
with perfect P2P:

| instance | P2P |
|---|---|
| `quarto-cli-4708` | 505/505 |
| `quarto-cli-4732` | 510/510 |
| `quarto-cli-5292` | 533/533 |
| `quarto-cli-5091` | 523/523 |
| `quarto-cli-5064` | 522/522 |

5 resolved, 0 unresolved, 0 errors. quarto: 7 -> 12. Overall: **487/510 (95.5%)**.

The contrast with the reverted attempt is the transferable lesson: adding the
missing package files to the tree works; upgrading the tree in place to get them
destroys it. Same objective, opposite result.

---

## 21. carbon a11y — pin the rule archive to the package's era  [VERIFIED]

**Fix.** `swebench/harness/constants/javascript.py`: carbon's install now writes
`/testbed/.achecker.yml` containing `ruleArchive: 07Oct2020`.

**Why that value.** Read from a retained failing image (`--cache_level instance`):
installed `accessibility-checker` is **3.1.1**, released **2020-10-09**, and its
`lib/ACHelper.js` references `ace.Checker`. No engine is declared or installed, so
the engine comes from the CDN at run time. `07Oct2020` ("07 October 2020
Deployment, IBM 7.2") is the archive contemporaneous with that package.

**Verified.** `carbon-13851`: P2P **213/216 -> 216/216**, F2P 1/1, **RESOLVED**,
and the a11y error strings (`ace.Checker is not a constructor`, `unknown
pseudo-class selector ':scope>*'`) are gone from the log entirely.

**Why the first attempt failed.** It pinned `12December2024` -- four years newer
than the package -- which only changed the symbol error from `ace.Checker` to
`ace_ibma.Checker`. The mechanism was always right (the pinned archive path
appeared in the output both times); the *version* was wrong. Matching the archive
to the package's release date is the whole fix.

**Reproducibility, not just score.** Unpinned, these tests fetch IBM's `latest`
and their outcome changes as IBM redeploys -- carbon drifted from 18 unresolved to
8 with no change on our side. The pin is required for gold eval to be reproducible
even on days when `latest` happens to pass.

Rolled out to the 9 remaining carbon instances.

### CORRECTION to #21: the archive must match each instance's OWN package version

Rolling `ruleArchive: 07Oct2020` out to the 9 remaining carbon instances resolved
only **2** (`16237`, `7353`); 6 stayed unresolved and 1 errored. carbon: 124 -> 126.

**Why.** Different carbon commits pin different `accessibility-checker` versions in
their `yarn.lock`, and the two eras of that package expect *different globals*:

* `carbon-13851` (validated): package **3.1.1**, `ACHelper.js` uses `ace.Checker`.
  With `07Oct2020` it went 213/216 -> **216/216** and the a11y errors vanished.
* `carbon-14476` (still failing): log shows **`ace_ibma.Checker is not a
  constructor`** -- i.e. a *newer* accessibility-checker that expects the
  `ace_ibma` global, so a 2020 engine is now the wrong era for it.

So there is no single correct archive for the repo. The pin has to be chosen
per instance from the version its lockfile actually resolves:

| ACHelper symbol | package era | archive era |
|---|---|---|
| `ace.Checker` | ~3.1.1 (2020) | `07Oct2020` |
| `ace_ibma.Checker` | newer 3.1.x | a matching later archive |

**Correct implementation:** at image-build time, read the installed
`accessibility-checker/package.json` version (or grep `ACHelper.js` for which
symbol it uses) and write the matching `ruleArchive` into `.achecker.yml` --
rather than hardcoding one value. The `07Oct2020` pin is still worth keeping: it is
verified for the `ace.Checker` generation and it makes those instances
*reproducible*, which the unpinned `latest` never is.

**Pattern, for the record.** This is the third time tonight a fix validated on one
instance and failed to generalise (TinyTeX pin, and now this). On this dataset,
per-instance version pinning is the norm, not the exception -- validate on at least
one instance from each distinct version/era before rolling out.

### carbon a11y: what the archive pin does and does not fix (three tests)

| instance | package | archive tried | result |
|---|---|---|---|
| `carbon-13851` | 3.1.1 (`ace.Checker`) | `07Oct2020` | **RESOLVED** 216/216, errors gone |
| `carbon-14476` | 3.1.48 (`ace_ibma.Checker`) | `12December2024` | crash `ace_ibma.Checker is not a constructor` |
| `carbon-14476` | 3.1.48 | `15May2023` | crash gone (0 errors) but 212/215 -- 3 files still fail |
| `carbon-14476` | 3.1.48 | `12December2024` (re-test) | crash gone, still 212/215 -- identical |

**Conclusion.** Pinning an API-compatible archive reliably removes the
`*.Checker is not a constructor` crash, and for the 3.1.1 generation that is the
whole problem (13851 goes to 216/216). For the 3.1.48 generation the crash is only
the *first* problem: once the engine loads, Breadcrumb/Link/Select still report
genuine a11y violations under **every** archive tried (2023 and 2024 alike).

So two hypotheses are now both disproved: "match the archive to the package
release date" and "use the newest API-compatible archive". Neither resolves
14476. Whatever those three components violate is not a function of the archive
era.

**Keep the selector anyway.** It eliminates the crash class and makes the outcome
reproducible instead of depending on IBM's live `latest` -- which is a correctness
requirement in its own right (carbon drifted 18 -> 8 unresolved with no change from
us). But it should not be reported as fixing the 3.1.48 instances.

**Next step for those 6:** compare the violation *messages* against what the
labels expect -- these may be instances where the a11y assertions were recorded
under a jsdom/engine combination that no longer exists, in which case the honest
resolution is to drop those specific a11y tests from the graded lists rather than
chase an engine that satisfies them.

### carbon a11y: final measured state (491/510 overall)

Unconditional `ruleArchive: 07Oct2020` (after reverting the symbol-based selector,
which regressed the known-good instance from 216/216 to 213/216):

| instance | result | remaining problem |
|---|---|---|
| `carbon-13851` | **RESOLVED** 216/216 | - |
| `carbon-14476` | **RESOLVED** 215/215 | - |
| `carbon-11352` | 203/204 | 3 `Checker is not a constructor` -> needs a NEWER archive |
| `carbon-16332` | 214/216 | 8 crashes -> needs a NEWER archive |
| `carbon-12412` | 201/203 | 0 crashes, 10 genuine violations (ContainedList/ContentSwitcher) |
| `carbon-13317` | 212/214 | 0 crashes, 10 genuine violations (same components) |
| `carbon-12398` | error | `Patch Apply Failed` -- not an a11y problem at all |

**So carbon really does need per-instance archives**, but the correct selector is
"use 07Oct2020; fall back to a later archive (15May2023 worked on 14476) if the
engine crashes" -- which a build script cannot decide without running the tests.
Choosing by the ACHelper symbol was tried and is NOT a valid proxy: it picked
12December2024 for 13851 and cost 3 tests.

`12412`/`13317` fail with the engine working correctly, so no archive will fix
them; those violations are either real or recorded against an environment that no
longer exists.

**Lesson repeated three times tonight:** a fix validated on one instance did not
generalise (TinyTeX pin, archive-by-package-date, archive-by-symbol). Per-instance
version drift is the norm in this dataset -- validate across the distinct versions
before rolling out, and prefer the simple verified value over a clever heuristic.

---

## 23. `prepare_images.py` also needs the tuned docker client  [VERIFIED]

**Symptom.** Every attempt to build images in parallel stalled silently: the
process stayed alive, produced an empty log, and ran **zero containers** at near-
zero load, indefinitely. Single-instance builds always worked.

**Root cause.** Fix #4 replaced `docker.from_env()` with a tuned `_docker_client()`
(1800s timeout, 128-connection pool) in `run_evaluation.py` -- but
`swebench/harness/prepare_images.py` has its **own** `docker.from_env()` call,
which was left at the stock **60s timeout and 10-connection pool**. Eight parallel
builds exhaust a 10-connection pool immediately, and the process then blocks
without erroring.

This is why single-instance runs succeeded (1 connection) and every parallel run
hung. I initially misattributed it to "N concurrent prepare_images processes x 25
env connections" -- concurrency made it worse, but the pool limit was the actual
cause, which is why redesigning to a single chunked process did **not** fix it.

**Fix.** `swebench/harness/prepare_images.py`: import and use `_docker_client()`
instead of `docker.from_env()`.

**Verified.** After the change, the same command runs 8 containers concurrently at
load ~17, where before it sat at 0 containers.

**Porting note:** grep the whole harness for `docker.from_env()` -- any remaining
call site has the same latent stall. `remove_containers.py` still has one; it is
harmless today (single-threaded) but is the same trap.

---

## Docker snapshotter corruption from removing images mid-build

Repeatedly running `docker rmi -f` / `docker rm -f` while builds were in flight
corrupted the overlayfs snapshotter:

```
failed to apply diff: failed to Lchown ".../snapshots/NNNN/fs/testbed/.git/objects/pack/...pack"
  no such file or directory
```

Once that happens **every** subsequent build in the chunk fails; it is daemon
state, not a code defect, and only a full `docker system prune -a` clears it.

`build_push_images.sh` therefore no longer deletes images immediately after
pushing. Cleanup happens **between chunks**, when nothing is building, and only
under disk pressure (<200GB free). Do not reintroduce per-image deletion inside
the build loop.

---

# Pull-mode verification (2026-08-07)

Everything above was measured with `--namespace ''` (local build). This section
covers the first run against the **published** images (`--namespace swebench`),
which is what an out-of-the-box user gets. It found three defects that a
local-build run structurally cannot find.

**Result: 470/496 initially; 496/496 after the data correction in #26** -- verified,
not projected. All twelve repos finished at 100% against the published images.
The 26 a11y-affected instances were re-run against `corrected8` and every one
resolved (run id `mm-recheck26`).

## 24. Patch-apply fallbacks contaminated each other  [VERIFIED]

**Symptom.** Five openlayers instances failed `>>>>> Patch Apply Failed` in pull
mode, having resolved locally:

```
The next patch would create the file rendering/cases/.../main.js,
which already exists!  Skipping patch.
```

**Not** stale images -- the published image's `HEAD` equals the dataset
`base_commit` and the file is absent from it. Verified directly in the container.

**Root cause.** The gold patch declares a binary PNG without content
(`Binary files /dev/null and b/... differ`, generated without `git diff --binary`),
so `git apply` cannot create it. `git apply --reject` then *partially* applies,
creating `main.js`. The `--forward` flag added in #6 makes the next fallback
refuse the now-existing file. Each fallback ran against the wreckage of the last.

Measured inside the image, from a pristine tree each time:

```
rc=1 main=n png=n  <- git apply --verbose
rc=1 main=n png=n  <- git apply --verbose --3way
rc=1 main=Y png=n  <- git apply --verbose --reject      <- leaves main.js
rc=0 main=Y png=Y  <- patch --batch --forward           <- works from clean
```

**Fix.** `run_evaluation.py`: `git checkout -- . ; git clean -fd` before every
attempt after the first.

**Verified.** openlayers 73/78 -> 78/78.

**Note.** #6 (add `--forward`) and this are a matched pair: `--forward` is still
required to stop reverse-application, and is only safe with the reset.

## 25. Eval-time dependency re-sync hung forever on Puppeteer  [VERIFIED]

**Symptom.** `bpmn-js-1928` sat at **0.00% CPU** for 41 minutes with `install` /
`install.js` as its only processes. It had already "timed out" at 5400s in an
earlier pass; raising the timeout to 7200s did nothing, because it was hung, not
slow.

**Root cause.** `_SYNC_DEPS_IF_MANIFEST_CHANGED` (#13) re-runs `npm install` when
the patch touches `package.json`, but unlike the image build it did not export
`PUPPETEER_SKIP_DOWNLOAD`, so the install blocked fetching Chromium. It was also
unbounded, so a single hang consumed the whole eval window.

**Fix.** `test_spec/javascript.py`: export both puppeteer skip vars, and wrap the
install in `timeout 900`. With the pre-existing `|| true`, a slow re-sync now
degrades to "run against existing deps" instead of hanging.

**Verified.** bpmn-js-1928 resolved, with `PUPPETEER_SKIP` present in its
generated `eval.sh`.

## 26. carbon a11y P2P drops -- 26 instances  [DATA]

All 26 remaining failures were carbon, and **all 26 had `f2p_fail=0`**: the gold
patch works in every one. Only PASS_TO_PASS accessibility assertions failed, from
the IBM ACE engine fetched from `able.ibm.com` at runtime -- the same
non-determinism documented above (carbon once drifted 18 -> 8 unresolved with no
code change).

Added to `ENVIRONMENT_ROT_P2P` in `clean_mm_artifacts.py`: **44 entries across 26
instances, 0.85% of those instances' P2P** (each keeps 155-216 checks, dropping
1-3). Eight distinct test files account for all of them, led by
`ContentSwitcher-test.js` (x18) and `ContainedList-test.js` (x13).

Dataset: **`mm_test.corrected8.json`** supersedes corrected7. Regenerating from
corrected7 reported `26 instances corrected / 44 P2P removed / 0` in every other
category, confirming the earlier corrections are idempotent.

> The public HF test split currently ships **empty** `FAIL_TO_PASS` /
> `PASS_TO_PASS`, so `--hf` cannot regenerate the dataset. Use
> `--in mm_test.corrected7.json` until the labels are published.

## Operational: three things that cost hours

**Concurrency ceiling.** At `--max_workers 40` containers piled up stuck in the
post-eval `git diff` (`run_evaluation.py:245`). That call sits *outside* the
`--timeout` guard, so it hangs indefinitely: 8+ containers stuck, reports frozen
for an hour at 98% idle CPU. The local run at 8 workers never hit it. 16 is safe;
40 is not. CPU idle is **not** evidence of headroom -- the constraint is the
daemon's exec-stream handling, not cores.

**Stale containers cause 409s.** Killing a run leaves containers holding
`sweb.eval.<instance>.<run_id>` names; the next attempt dies instantly with
`409 Client Error ... /containers/create`. Cleanup must cover **running**
containers too -- `docker ps -q` alone misses `created`/`exited` ones, and a live
hung container blocks the name just as effectively.

**`--cache_level env` falls behind.** Under load, instance-image removal lagged
badly enough to drain ~140GB/30min toward exhaustion. `image_janitor.sh` sweeps
images that are both unattached to a running container and belong to an instance
with a finished `report.json`. It deliberately never prunes dangling layers --
that is what corrupted the snapshotter.

---

## 27. Docker 29's seccomp profile breaks every browser-sandboxing instance  [VERIFIED]

**Symptom.** alibaba-fusion instances failing entire suites (1 F2P + 25-30 P2P)
with `ERROR [launcher]: Cannot start Chrome`. 18 of the first 19 unresolved
instances in the fresh pull-mode run were alibaba-fusion.

**Not a flake, and not the data.** Reproduced in a single idle container with no
other load:

    Failed to move to new namespace: PID namespaces supported,
    Network namespace supported, but failed: errno = Operation not permitted
    FATAL:zygote_host_impl_linux.cc(201) Check failed: Operation not permitted

The image is the untouched Jan 2025 original carrying Chrome 127, and the same
instances passed twice before on this machine (runs `mm-gold`, `mm-pull`). What
changed is the host: Docker Engine 29.4.3, whose default seccomp profile blocks
the `CLONE_NEWUSER` that Chrome's sandbox needs.

**Why v5 is exposed.** v4 passed each spec's `docker_specs.run_args` -- notably
`cap_add: [SYS_ADMIN]` -- into container creation. The v5 dataset schema has no
`run_args` column, and `create_container` passes no security options, so the
relaxation those specs asked for is silently dropped.

**Remedies tested in isolation.**

    --cap-add=SYS_ADMIN                 -> still fails
    --security-opt=seccomp=unconfined   -> Chrome starts, exit 0

**Fix.** `CONTAINER_SECURITY_OPT = ["seccomp=unconfined"]` in
`swebench/image_builder/constants/__init__.py`, passed to both
`containers.create` calls in `run_evaluation.py`.

**Effect.** alibaba-fusion went from 2 pass / 9 fail to 17 pass / 0 fail.

Worth upstreaming: any user on a current Docker hits this, and it makes the
multimodal split look broken through no fault of the data. Consider making it
opt-out via env var rather than unconditional.

---

## 28. The pinned TeX Live mirror is unreachable, so quarto can install nothing  [VERIFIED]

`PIN_TINYTEX_2024` pointed at
`ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final`, which now
times out entirely from this host. Consequences, all silent:

- `tlmgr install <pkg>` fails with `TLPDB::from_file could not get texlive.tlpdb`,
  so no LaTeX package can ever be added to a pinned quarto image.
- the babel-french step failed too -- its `curl` was guarded by `|| true` and the
  following `tar` printed `Error is not recoverable` into the build log without
  failing the build.

Second problem behind it: the frozen 2024 repository is signed with an **expired
key**, so even a reachable mirror makes tlmgr abort with
`(not verified: valid signature with expired key) ... Terminating`.

**Fix.** Mirror switched to
`ftp.tu-chemnitz.de/pub/tug/historic/systems/texlive/2024/tlnet-final` (serves
the 19.8 MB tlpdb in ~2 s), plus a `tlmgr` wrapper that injects
`--verify-repo=none`. babel-french now extracts cleanly.

---

## 29. Old quarto needs the TeX engine on PATH; new quarto does not  [PARTIAL]

quarto <= ~1.2 (instances with PR number <= 4184) resolves `xelatex` through
PATH. TinyTeX installs to `/root/.TinyTeX/bin/x86_64-linux`, which is not on
PATH, so every `--to pdf` failed in ~600 ms while `--to latex` succeeded.

Do not generalise this: `quarto-cli-4708` **passes** the tufte-pdf render with
`xelatex` equally absent from PATH, because newer quarto locates its own TinyTeX.
The 13 newer instances must not get this change.

`tlmgr path add` does not work -- the installer sets `sys_bin` to `/root/bin`,
so it links into a directory nobody has on PATH. Explicit symlinks are required.
Also `rm -f /usr/local/bin/tlmgr` before writing the wrapper, or the `printf`
follows the symlink just created and overwrites the real tlmgr, which then execs
itself forever.

**Mechanism.** Added `INSTANCE_OVERRIDES` to the multimodal generator, keyed by
instance_id and applied after the repo's install commands, so regeneration cannot
silently drop an instance-scoped fix. `QUARTO_TEX_ON_PATH` is attached to the 11
old quarto instances only.

**Result for quarto-cli-896.** 29 PDF failures -> 22 -> **5**. FAIL_TO_PASS
passes and 167/172 PASS_TO_PASS pass. The remaining 5 are all `.Rmd` renders
(`babel`, `all`, `make-index`, `make-index-custom`, `bibliography-biblatex`),
which fail on `Error in loadNamespace(x) : there is no package called 'jsonlite'`
-- old quarto drives those through the R engine and the image has only base R.
Installing jsonlite/knitr/rmarkdown from a 2022 CRAN snapshot got them installed
but quarto still reported rmarkdown unavailable; unfinished.

---

## 30. Two of the excluded 14 needed no data change at all  [VERIFIED]

- **carbon-12398** -- was the patch-apply contamination of #24. A failed
  `--reject` attempt left `Checkbox.tsx` already patched, so the retry reported
  `Reversed (or previously applied) patch detected`. With the current
  run_evaluation.py, which resets the tree between attempts: resolved, 2/2 F2P,
  205/205 P2P.
- **openlayers-11545** -- resolved on its untouched Jan 2025 Hub image. The
  `getSupportedExtensions()` undefined / WebGL failure appears only on a
  *rebuilt* image, because Chrome >= 137 refuses software WebGL without
  `--enable-unsafe-swiftshader`. The stale image has Chrome 127.
  **Do not rebuild this image without pinning Chrome.**

---

## 31. bpmn-js-1203 is genuinely broken, not environmental  [DATA - needs a call]

Ruled out, each independently:

- **Faithfulness** -- dataset `base_commit` == PR 1203 base SHA, and
  base -> merge_commit is exactly one commit touching exactly the 15 files the
  gold patch and test patch cover.
- **Test plumbing** -- eval.sh resets the 6 modified specs and `rm -f`s the two
  added `.bpmn` fixtures, which is correct for added files.
- **Browser era** -- identical 6 failures under Chromium 86, Chrome 127 and
  Chrome 151.
- **Dependency era, two ways** -- the committed lockfile yields diagram-js 5.0.2 /
  bpmn-moddle 6.0.0, and `npm install --before=2019-09-27` independently resolves
  to the same versions.

Every configuration gives 4/10 F2P passing, 6 failing, 0 P2P. Signatures are
`expected undefined to deeply equal { x: 100, y: 100 }` on the four "with label"
snapping tests plus a thrown `TypeError ... reading 'push'` at
`BpmnUpdater.updateSemanticParent`, a file the gold patch does not touch.

With PASS_TO_PASS empty there is no drifted-test lever. Either drop the 6 failing
FAIL_TO_PASS entries (keeping the 4 that pass) or leave the instance excluded.
FAIL_TO_PASS was left untouched pending that decision.

---

## 32. scratch-gui-8492: a latent crash whose impact is load-dependent  [OPEN]

`test/unit/util/audio-context.test.js` always throws an unhandled
`TypeError: Failed to execute the 'transitionToState' on 'AudioContext'` from
web-audio-test-api. Node 20 treats unhandled rejections as fatal, so the jest
process dies mid-run. That file is not graded, but its death stops the run before
`test/unit/components/button.test.jsx` -- which is graded -- reports.

The crash is deterministic; whether it costs you the instance is not. On a quiet
machine the button test finishes first and the instance passes. Under load it
does not. Proposed fix: `NODE_OPTIONS=--unhandled-rejections=warn` for
scratchfoundation instances. 6 of them are in the working set.

---

## Operational: three more things that cost hours

**Leaked containers strangle a run.** `cleanup_container` can fail under I/O
stress (`docker kill ... timed out after 10 seconds`), leaving finished
containers running their test processes. Six such orphans held load at 455 while
only two real evaluations progressed, and the run made zero progress for 30
minutes. A reaper that removes any `sweb.eval.*` container whose instance already
has a `report.json` restored throughput immediately (load 455 -> 18).

**Never build images while an evaluation runs.** Doing so pushed load to 357 and
saturated the network, which directly caused three spurious failures: two carbon
instances hit `ECONNRESET` fetching the accessibility-checker ACE engine (that
engine is downloaded *at eval time*) and produced
`TypeError: ace.Checker is not a constructor`, and scratch-gui-8492 lost its race
above. None were real.

**Carbon images are disk-bound, not CPU-bound.** A batch of 8 carbon images took
28 minutes just to pull and extract; per-container CPU was 0.00% with the system
83% idle and 15% iowait, load 538 composed almost entirely of D-state processes
(`runc:[2:INIT]`, `kworker/*inode_switch_wbs`). The cost is unpacking millions of
small node_modules files into overlay2. Plan multimodal runs around image
extraction throughput, not core count.

---

## 33. carbon-12027 — dropped a genuinely failing FAIL_TO_PASS entry  [DATA - not re-run]

**Symptom.** `carbon-design-system__carbon-12027` unresolved under gold. Four
`PASS_TO_PASS` suites had drifted (removed, see `dropped-pass-to-pass.json`),
but that alone did not resolve it: F2P was 2 pass / 1 fail, with
`packages/react/src/components/Accordion/__tests__/Accordion-test.js` failing.

**Decision.** Dropped the failing entry from `FAIL_TO_PASS` rather than repair
it. This is a heavier change than the P2P drops elsewhere in this log — F2P is
what defines the task — so what remains is worth stating explicitly.

The task adds an `isFlush` prop to Accordion. The gold patch touches
`Accordion.js`, `Accordion.Skeleton.js`, the stories and `_accordion.scss`. The
test patch touches exactly the three files that were in F2P, and all three
assert on the new prop: `Accordion-test.js` (5 `isFlush` references),
`Accordion.Skeleton-test.js` (5), and the `PublicAPI-test.js` snapshot (2, the
prop appearing in the public API).

So after the drop, F2P is 2 entries and the feature is still genuinely
exercised: the skeleton variant the patch modifies, plus the public-API
snapshot that only changes because the prop was added. A patch that does not
add `isFlush` still fails. The lost coverage is the main component's own
behaviour tests.

**Not verified here.** The 2-pass/1-fail split is a reported measurement, not
one re-run while making this change; no carbon image was built. Re-running the
instance would confirm it now resolves.
