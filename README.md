# OVOS MaryTTS Plugin

TTS Plugin for [MaryTTS](https://github.com/marytts/marytts)

# Configuration:

```json
"tts": {
    "module": "ovos-tts-plugin-marytts",
    "ovos-tts-plugin-marytts": {
      "url": "http://0.0.0.0:59125",
      "voice": "cmu-slt-hsmm"
    }
}
```


## Usage

Standalone usage

```python
from ovos_tts_plugin_marytts import MaryTTS

engine = MaryTTS(config={"url": "http://0.0.0.0:59125"})
engine.get_tts("hello world", "test.wav")
```