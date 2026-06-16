"""End-to-end TTS intelligibility test for the MaryTTS plugin.

MaryTTS requires a running MaryTTS server. The server URL is read from the
``MARYTTS_URL`` environment variable; when it is unset the test is skipped
(no server to talk to), mirroring how cloud engines gate on missing
credentials. A small fixed set of English phrases is synthesised, transcribed
back with the ovoscope reference STT, and scored with word error rate.
"""
import os
import json

import pytest

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_marytts import MaryTTS

LANG = "en-US"
PHRASES = [
    "hello world",
    "what time is it",
    "turn on the kitchen lights",
    "the weather is nice today",
    "set a timer for five minutes",
]


def test_tts_intelligibility():
    url = os.environ.get("MARYTTS_URL")
    if not url:
        pytest.skip("requires MARYTTS_URL (a running MaryTTS server)")
    tts = MaryTTS({"url": url})
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG, mode="direct")
    print("::TTS-INTELLIGIBILITY:: " + json.dumps(report.to_dict()))
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))
