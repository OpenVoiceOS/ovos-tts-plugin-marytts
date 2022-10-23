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
        url = config.get('url') or "http://mary.dfki.de:59125"
        config["voice"] = config.get("voice") or "cmu-slt-hsmm"
        super(MaryTTS, self).__init__(lang, config, url,
                                      '/process', MaryTTSValidator(self))

    def build_request_params(self, sentence):
        params = self.PARAMS.copy()
        params['LOCALE'] = self.lang
        params['VOICE'] = self.voice
        params['INPUT_TEXT'] = sentence.encode('utf-8')
        return params

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(MaryTTSPluginConfig.keys())


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


# this list can be generated by querying "http://mary.dfki.de:59125/voices"
MaryTTSPluginConfig = {
    'de': [{'meta': {'display_name': 'Dfki Pavoque Styles',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'dfki-pavoque-styles'},
           {'meta': {'display_name': 'Dfki Pavoque Neutral Hsmm',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'dfki-pavoque-neutral-hsmm'},
           {'meta': {'display_name': 'Dfki Pavoque Neutral',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'dfki-pavoque-neutral'},
           {'meta': {'display_name': 'Bits4',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits4'},
           {'meta': {'display_name': 'Bits3 Hsmm',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits3-hsmm'},
           {'meta': {'display_name': 'Bits3',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits3'},
           {'meta': {'display_name': 'Bits2',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits2'},
           {'meta': {'display_name': 'Bits1 Hsmm',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits1-hsmm'},
           {'meta': {'display_name': 'Bits1',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'bits1'}],
    'en-gb': [{'meta': {'display_name': 'Dfki Spike Hsmm',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-spike-hsmm'},
              {'meta': {'display_name': 'Dfki Spike',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-spike'},
              {'meta': {'display_name': 'Dfki Prudence Hsmm',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-prudence-hsmm'},
              {'meta': {'display_name': 'Dfki Prudence',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-prudence'},
              {'meta': {'display_name': 'Dfki Poppy Hsmm',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-poppy-hsmm'},
              {'meta': {'display_name': 'Dfki Poppy',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-poppy'},
              {'meta': {'display_name': 'Dfki Obadiah Hsmm',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-obadiah-hsmm'},
              {'meta': {'display_name': 'Dfki Obadiah',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'dfki-obadiah'}],
    'en-us': [{'meta': {'display_name': 'Cmu Slt Hsmm',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-slt-hsmm'},
              {'meta': {'display_name': 'Cmu Slt',
                        'gender': 'female',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-slt'},
              {'meta': {'display_name': 'Cmu Rms Hsmm',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-rms-hsmm'},
              {'meta': {'display_name': 'Cmu Rms',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-rms'},
              {'meta': {'display_name': 'Cmu Bdl Hsmm',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-bdl-hsmm'},
              {'meta': {'display_name': 'Cmu Bdl',
                        'gender': 'male',
                        'offline': False,
                        'priority': 60},
               'url': 'http://mary.dfki.de:59125',
               'voice': 'cmu-bdl'}],
    'fr': [{'meta': {'display_name': 'Upmc Pierre Hsmm',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'upmc-pierre-hsmm'},
           {'meta': {'display_name': 'Upmc Pierre',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'upmc-pierre'},
           {'meta': {'display_name': 'Upmc Jessica Hsmm',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'upmc-jessica-hsmm'},
           {'meta': {'display_name': 'Upmc Jessica',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'upmc-jessica'},
           {'meta': {'display_name': 'Enst Dennys Hsmm',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'enst-dennys-hsmm'},
           {'meta': {'display_name': 'Enst Camille Hsmm',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'enst-camille-hsmm'},
           {'meta': {'display_name': 'Enst Camille',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'enst-camille'}],
    'it': [{'meta': {'display_name': 'Istc Lucia Hsmm',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'istc-lucia-hsmm'}],
    'lb': [{'meta': {'display_name': 'Marylux',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'marylux'}],
    'te': [{'meta': {'display_name': 'Cmu Nk Hsmm',
                     'gender': 'female',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'cmu-nk-hsmm'}],
    'tr': [{'meta': {'display_name': 'Dfki Ot Hsmm',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'dfki-ot-hsmm'},
           {'meta': {'display_name': 'Dfki Ot',
                     'gender': 'male',
                     'offline': False,
                     'priority': 60},
            'url': 'http://mary.dfki.de:59125',
            'voice': 'dfki-ot'}]}
