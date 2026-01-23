import requests
from ovos_utils import classproperty
from ovos_plugin_manager.templates.tts import TTS


class MaryTTS(TTS):

    def __init__(self, config=None):
        config = config or {}
        self.url = config.get('url')
        if not self.url:
            raise ValueError("'url' missing from MaryTTS plugin config")
        config["voice"] = config.get("voice") or "cmu-slt-hsmm"
        super().__init__(config)
        self.valid_voices = set()
        self.valid_langs = set()
        self.update_voice_list()

    def update_voice_list(self):
        res = requests.get(self.url + "/voices")
        res.raise_for_status()
        for entry in res.text.strip().split("\n"):
            voice, lang, gender, _ = entry.split()
            self.valid_voices.add(voice)
            self.valid_langs.add(lang)

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        l2 = lang or self.lang
        # TODO - use langcodes library to match lang instead
        if l2 not in self.valid_langs:
            l2 = l2.split("_")[0]
            if l2 not in self.valid_langs:
                raise ValueError(f"unsupported language '{lang}' - available langs: {self.valid_langs}")

        # TODO - validate voice/lang combo
        v = voice or self.voice
        if v and v not in self.valid_voices:
            raise ValueError(f"unsupported voice '{voice}' - available voices: {self.valid_voices}")


        params = {
            "LOCALE": l2,
            "VOICE": v,
            "INPUT_TEXT": sentence,
            "INPUT_TYPE": "TEXT",
            "OUTPUT_TYPE": "AUDIO",
            "AUDIO": "WAVE"
        }
        resp = requests.get(self.url + "/process", params=params)
        resp.raise_for_status()
        with open(wav_file, "wb") as f:
            f.write(resp.content)
        return wav_file, None

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        # NOTE: if used as classproperty we don't know available langs
        return self.valid_langs


if __name__ == "__main__":
    url = "http://192.168.1.200:5002"
    tts = MaryTTS({"url": url, "voice": "dfki-spike-hsmm"})
    tts.get_tts("hello world", "test.wav",
                lang="en-us", voice="mary_ann;high")
