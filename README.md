# OVOS MaryTTS Plugin

TTS Plugin for [MaryTTS](https://github.com/marytts/marytts)

MaryTTS needs to be installed separately and may be running in a different machine


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

## Docker

[Docker](https://github.com/synesthesiam/docker-marytts) text to speech server and a collection of hidden semi-Markov model (HSMM) voices for various languages in a multi-platform Docker image.

Supported Platforms:

* `amd64` - laptops, desktops, servers
* `arm/v7` - Raspberry Pi 2/3
* `arm64` - Raspberry Pi 3+/4

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2
```

You should now be able to access the server at [http://localhost:59125](http://localhost:59125)

Beware that this may consume a lot of RAM on a Raspberry Pi!

You can control which voices are loaded with `-v` or `--voice` arguments:

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2 --voice cmu-slt-hsmm --voice cmu-rms-hsmm
```

This will only loaded the necessary JARs for the specified voices, which may help conserve RAM on a Raspberry Pi.

A list of voices can be obtained with:

```bash
$ docker run -it synesthesiam/marytts:5.2 --voices
```

## Compatible projects

A few tts server projects offer MaryTTS compatible APIs and can be used with this plugin

- [Larynx](https://github.com/rhasspy/larynx#marytts-compatible-api)
- [OpenTTS](https://github.com/synesthesiam/opentts#marytts-compatible-endpoint)