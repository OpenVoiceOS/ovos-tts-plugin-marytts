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

This repo ships a container that serves the plugin behind
[`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server) (an
ElevenLabs-compatible HTTP API) on port `9666`, published to
`ghcr.io/openvoiceos/ovos-tts-plugin-marytts`.

> **Requires an external MaryTTS backend.** This plugin is a thin *client*: it
> forwards text to a separate MaryTTS Java server and returns the WAV it gets back.
> The plugin container **cannot synthesize on its own** and will fail to serve
> requests unless a reachable MaryTTS server URL is configured (`url` config key,
> baked via the `MARYTTS_URL` build arg, default `http://marytts:59125`).

### Compose (recommended)

`docker-compose.yml` wires both pieces together: a MaryTTS server sidecar
(`synesthesiam/marytts:5.2`, 19 HSMM voices for 8 languages, port `59125`) plus this
plugin container pointing at it.

```bash
$ docker compose up
```

The ElevenLabs-compatible API is then available at `http://localhost:9666`, backed by
the MaryTTS server at `http://localhost:59125`.

To use a different voice or point at your own MaryTTS server, rebuild the plugin image
with the `MARYTTS_URL` / `MARYTTS_VOICE` build args:

```bash
$ docker build --build-arg MARYTTS_URL=http://my-marytts:59125 \
               --build-arg MARYTTS_VOICE=dfki-spike-hsmm -t marytts-tts .
```

### The MaryTTS backend

The [`synesthesiam/marytts`](https://github.com/synesthesiam/docker-marytts) image
bundles HSMM voices for various languages and runs on `amd64`, `arm/v7` and `arm64`.

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2
```

Beware that this may consume a lot of RAM on a Raspberry Pi. Control which voices are
loaded with `--voice` to conserve RAM, and list voices with `--voices`:

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2 --voice cmu-slt-hsmm --voice cmu-rms-hsmm
$ docker run -it synesthesiam/marytts:5.2 --voices
```

## Compatible projects

A few tts server projects offer MaryTTS compatible APIs and can be used with this plugin

- [Larynx](https://github.com/rhasspy/larynx#marytts-compatible-api)
- [OpenTTS](https://github.com/synesthesiam/opentts#marytts-compatible-endpoint)