import requests
from ovos_utils import classproperty
from ovos_plugin_manager.templates.tts import TTS


class MaryTTS(TTS):

    def __init__(self, config=None):
        """
        Initialize the MaryTTS client from a configuration dictionary and discover available voices and languages.
        
        Parameters:
            config (dict): Configuration for the plugin. Must include the key 'url' pointing to the MaryTTS server.
                Optionally may include 'voice' to set the default voice; if omitted, "cmu-slt-hsmm" is used.
        
        Raises:
            ValueError: If 'url' is missing from the configuration.
        """
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
        """
        Refresh the internal sets of supported voices and languages by querying the MaryTTS server.
        
        Performs an HTTP GET to the server's "/voices" endpoint, expects each response line to contain whitespace-separated fields starting with `voice` and `lang`, and adds each discovered voice to `self.valid_voices` and each language to `self.valid_langs`.
        
        Raises:
            requests.HTTPError: if the HTTP response has an error status.
            requests.RequestException: on network-related errors.
            ValueError: if a response line does not contain the expected fields.
        """
        res = requests.get(self.url + "/voices")
        res.raise_for_status()
        for entry in res.text.strip().split("\n"):
            voice, lang, gender, _ = entry.split()
            self.valid_voices.add(voice)
            self.valid_langs.add(lang)

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        """
        Generate speech audio for `sentence` and save it to `wav_file`.
        
        Parameters:
            sentence (str): Text to synthesize.
            wav_file (str): Filesystem path where the resulting WAV data will be written.
            lang (str, optional): Preferred language code (e.g. "en_US" or "en-us"). If the exact code is not supported the implementation will try the language prefix (text before '_'); raises ValueError if no supported language is found.
            voice (str, optional): Preferred voice identifier. If provided and not available, a ValueError is raised.
        
        Returns:
            tuple: (`wav_file`, None) where `wav_file` is the path to the written WAV file.
        """
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
        """
        Languages supported by this TTS instance in its current state.
        
        Returns:
            set: Supported language codes discovered from the server (e.g., "en_US", "de").
        """
        # NOTE: if used as classproperty we don't know available langs
        return self.valid_langs


if __name__ == "__main__":
    url = "http://192.168.1.200:5002"
    tts = MaryTTS({"url": url, "voice": "dfki-spike-hsmm"})
    tts.get_tts("hello world", "test.wav",
                lang="en-us", voice="mary_ann;high")