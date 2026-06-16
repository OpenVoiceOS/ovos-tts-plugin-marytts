# TODO

## Open issues

- [ ] #14 Dependency Dashboard (Renovate bot)

## Gaps

- [ ] No test suite (no `test/` dir; CI is build-only).
- [ ] No coverage workflow.
- [ ] No license-check workflow.
- [ ] No `opm-check` workflow despite declaring a TTS plugin entry point.
- [ ] Release workflows reference `TigreGotico/gh-automations@master` instead of `OpenVoiceOS/gh-automations@dev`.
- [ ] Packaging uses legacy `setup.py` with no `pyproject.toml`.
- [ ] Entry-point group is legacy `mycroft.plugin.tts`.
- [ ] `requirements.txt` caps `ovos-plugin-manager<=3.0.0`, which may block newer OVOS stacks.

## Code TODOs

- [ ] `ovos_tts_plugin_marytts/__init__.py:61` — use langcodes library to match lang instead of naive prefix split.
- [ ] `ovos_tts_plugin_marytts/__init__.py:67` — validate voice/lang combo.
