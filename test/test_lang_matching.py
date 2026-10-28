"""OVOS passes BCP-47 tags (en-US); a MaryTTS server lists Java locales (en_US)."""
from unittest.mock import MagicMock, patch

import pytest

from ovos_tts_plugin_marytts import MaryTTS

# The /voices listing of an upstream MaryTTS 5.2 server
UPSTREAM_VOICES = "cmu-slt-hsmm en_US female hmm\nbits1-hsmm de female hmm\ndfki-spike-hsmm en_GB male hmm\n"


def _response(text: str = "", content: bytes = b"RIFF") -> MagicMock:
    resp = MagicMock(text=text, content=content)
    resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def tts():
    with patch("ovos_tts_plugin_marytts.requests.get", return_value=_response(UPSTREAM_VOICES)):
        yield MaryTTS({"url": "http://mary:59125"})


@pytest.mark.parametrize("lang, locale", [
    ("en-US", "en_US"),
    ("en-us", "en_US"),
    ("en_US", "en_US"),
    ("en-GB", "en_GB"),
    ("de-DE", "de"),
    ("de", "de"),
])
def test_process_gets_the_server_locale(tts, tmp_path, lang, locale):
    with patch("ovos_tts_plugin_marytts.requests.get", return_value=_response()) as get:
        tts.get_tts("hello", str(tmp_path / "out.wav"), lang=lang)
    assert get.call_args.kwargs["params"]["LOCALE"] == locale


def test_unknown_language_is_refused(tts, tmp_path):
    with pytest.raises(ValueError, match="unsupported language 'fr-FR'"):
        tts.get_tts("bonjour", str(tmp_path / "out.wav"), lang="fr-FR")


def _tts_with(locales):
    voices = "".join(f"v{n} {loc} female hmm\n" for n, loc in enumerate(locales))
    with patch("ovos_tts_plugin_marytts.requests.get", return_value=_response(voices)):
        return MaryTTS({"url": "http://mary:59125", "voice": "v0"})


@pytest.mark.parametrize("lang, locales, expected", [
    ("EN-us", ["en_US"], "en_US"),
    ("en-AU", ["en_US", "en_GB", "de"], "en_GB"),   # nearest regional variant
    ("pt", ["pt_BR", "en_US"], "pt_BR"),            # bare language, regional server locale
    ("pt-PT", ["pt_BR", "en_US"], "pt_BR"),
    ("en-US", ["en"], "en"),
    ("fr-FR", ["en_US", "de"], None),
])
def test_matching_follows_the_spec(lang, locales, expected):
    assert _tts_with(locales).match_lang(lang) == expected


def test_exact_locale_wins_over_an_equal_distance_neighbour():
    assert _tts_with(["en", "en_US"]).match_lang("en-US") == "en_US"
    assert _tts_with(["en_US", "en"]).match_lang("en") == "en"
