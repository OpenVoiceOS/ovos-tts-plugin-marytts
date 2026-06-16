# ovos-tts-plugin-marytts

OVOS TTS plugin that proxies synthesis to a MaryTTS-compatible HTTP server (MaryTTS, Larynx, OpenTTS).

## Setup

```bash
pip install .
```

Runtime dependency: `ovos-plugin-manager` (and `requests`, `ovos-utils`, pulled transitively). A reachable MaryTTS server is required at runtime; this plugin is a thin client and ships no voices.

## Test

No test suite exists. There is no `test/` directory and CI runs build-only checks. The module's `__main__` block under `ovos_tts_plugin_marytts/__init__.py` is a manual smoke test that hits a hardcoded server URL.

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_marytts/__init__.py` — `MaryTTS(TTS)` class. Reads `url` (required) and `voice` (default `cmu-slt-hsmm`) from config, calls the server `/voices` endpoint at init to populate `valid_voices`/`valid_langs`, and `get_tts` GETs `/process` to fetch WAV bytes.
- `ovos_tts_plugin_marytts/version.py` — semver block consumed by `setup.py:get_version()`.
- `setup.py` — packaging. Entry point group is the legacy `mycroft.plugin.tts`: `ovos-tts-plugin-marytts = ovos_tts_plugin_marytts:MaryTTS`.
- `requirements/requirements.txt` — pins `ovos-plugin-manager>=1.0.0,<=3.0.0`.
- `scripts/bump_*.py`, `remove_alpha.py` — legacy version-bump helpers.

Entry-point group: `mycroft.plugin.tts` (OVOS OPM discovers TTS plugins here).

## Conventions

- Branches: `dev` (work) / `master` (stable). NEVER `main`.
- Never edit `version.py`; gh-automations bumps semver from conventional-commit prefixes (`feat:` / `fix:` / `feat!:`).
- New repos private by default.
- Commit identity: JarbasAi <jarbasai@mailfence.com>.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, dates, or design narration in docs/commits/PRs/code).
- CI is provided by OpenVoiceOS/gh-automations.

## Gotchas

- Network-bound: `__init__` performs a live HTTP GET to `<url>/voices`; constructing the plugin with no server reachable raises a request error, not a graceful fallback.
- `available_languages` is an instance property, not a classproperty, so OPM cannot enumerate languages without an instantiated (and connected) plugin.
- Language matching is naive (exact code, then prefix before `_`); the source itself flags this with a TODO to use the `langcodes` library.
- Release workflows reference `TigreGotico/gh-automations@master`, not `OpenVoiceOS/gh-automations@dev` — inconsistent with org convention.
