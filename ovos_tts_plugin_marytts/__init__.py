import requests

from ovos_plugin_manager.templates.tts import RemoteTTS, TTSValidator


class MaryTTS(RemoteTTS):
    PARAMS = {
        'INPUT_TYPE': 'TEXT',
        'AUDIO': 'WAVE_FILE',
        'OUTPUT_TYPE': 'AUDIO'
    }

    def __init__(self, lang="en-us", config=None):
        config = config or {}
        url = config.get('url') or "http://0.0.0.0:59125"
        config["voice"] = config.get("voice") or "cmu-slt-hsmm"
        super(MaryTTS, self).__init__(lang, config, url,
                                      '/process', MaryTTSValidator(self))

    def build_request_params(self, sentence):
        params = self.PARAMS.copy()
        params['LOCALE'] = self.lang
        params['VOICE'] = self.voice
        params['INPUT_TEXT'] = sentence.encode('utf-8')
        return params


class MaryTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MaryTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        try:
            resp = requests.get(self.tts.url + "/version", verify=False)
            if resp.status_code == 200:
                return True
        except Exception:
            raise Exception(
                'MaryTTS server could not be verified. Check your connection '
                'to the server: ' + self.tts.url)

    def get_tts_class(self):
        return MaryTTS


if __name__ == "__main__":
    tt = MaryTTS()
    a = tt.get_tts("hello world", "test.wav")
    print(a)
