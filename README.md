# OVOS MaryTTS Plugin

This is a text-to-speech (TTS) plugin for [OpenVoiceOS](https://github.com/OpenVoiceOS) that connects to a [MaryTTS](https://github.com/marytts/marytts) server. The plugin sends text to the MaryTTS server and returns the audio it gets back. You must install and run MaryTTS separately, on the same machine or on a different one.

## Install

```bash
$ pip install ovos-tts-plugin-marytts
```

## Configuration

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

Use the plugin directly, without OVOS, like this:

```python
from ovos_tts_plugin_marytts import MaryTTS

engine = MaryTTS(config={"url": "http://0.0.0.0:59125"})
engine.get_tts("hello world", "test.wav")
```

## Docker

This repository also builds a container that serves the plugin behind [`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server), an ElevenLabs-compatible HTTP API, on port `9666`. The image is published to `ghcr.io/openvoiceos/ovos-tts-plugin-marytts`.

This plugin is a thin client. It forwards text to a separate MaryTTS Java server and returns the WAV file it gets back. The plugin container cannot synthesize speech on its own. It fails to serve requests unless you configure a reachable MaryTTS server URL, either with the `url` config key or with the `MARYTTS_URL` build argument (default `http://marytts:59125`).

### Compose (recommended)

The `docker-compose.yml` file in this repository wires both pieces together: a MaryTTS server sidecar (`synesthesiam/marytts:5.2`, with 19 HSMM voices for 8 languages, on port `59125`) and this plugin container, pointed at that sidecar.

```bash
$ docker compose up
```

The ElevenLabs-compatible API is then available at `http://localhost:9666`, backed by the MaryTTS server at `http://localhost:59125`.

To use a different voice, or to point at your own MaryTTS server, rebuild the plugin image with the `MARYTTS_URL` and `MARYTTS_VOICE` build arguments:

```bash
$ docker build --build-arg MARYTTS_URL=http://my-marytts:59125 \
               --build-arg MARYTTS_VOICE=dfki-spike-hsmm -t marytts-tts .
```

### The MaryTTS backend

The [`synesthesiam/marytts`](https://github.com/synesthesiam/docker-marytts) image bundles HSMM voices for several languages and runs on `amd64`, `arm/v7`, and `arm64`.

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2
```

This may use a lot of RAM on a Raspberry Pi. Use the `--voice` flag to load only the voices you need, and list the available voices with `--voices`:

```bash
$ docker run -it -p 59125:59125 synesthesiam/marytts:5.2 --voice cmu-slt-hsmm --voice cmu-rms-hsmm
$ docker run -it synesthesiam/marytts:5.2 --voices
```

## Related projects

- [OpenVoiceOS/ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) — the ElevenLabs-compatible HTTP API this plugin's container serves behind.
- [MaryTTS](https://github.com/marytts/marytts) — the backend TTS engine this plugin connects to.

## Compatible projects

A few TTS server projects offer MaryTTS-compatible APIs and work with this plugin.

- [Larynx](https://github.com/rhasspy/larynx#marytts-compatible-api)
- [OpenTTS](https://github.com/synesthesiam/opentts#marytts-compatible-endpoint)

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for the full text.
