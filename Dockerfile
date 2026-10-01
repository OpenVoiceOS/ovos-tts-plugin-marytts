# MaryTTS voices served through ovos-tts-server's ElevenLabs-compatible API.
#
# IMPORTANT: this plugin is a THIN CLIENT. It does not synthesize speech itself; it
# forwards text to an external MaryTTS Java server (or any MaryTTS-compatible server
# such as OpenTTS / Larynx) over HTTP and returns the WAV it gets back. This image on
# its own is useless without a reachable MaryTTS server. Use the provided
# docker-compose.yml, which starts a MaryTTS server sidecar and points this container
# at it, or set MARYTTS_URL to your own server.
FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# the plugin + the OVOS TTS server. setuptools<81 keeps ovos-plugin-manager's
# pkg_resources usage working. ovos-tts-server>=1.13.5a1 carries the non-WAV transcode
# fix; the alpha floor lets pip resolve the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# URL of the external MaryTTS server and the default voice. Override MARYTTS_URL to
# point at your own server; the compose sidecar is reachable at http://marytts:59125.
ARG MARYTTS_URL=http://marytts:59125
ARG MARYTTS_VOICE=cmu-slt-hsmm
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "tts": {\n    "module": "ovos-tts-plugin-marytts",\n    "ovos-tts-plugin-marytts": {\n      "url": "%s",\n      "voice": "%s"\n    }\n  }\n}\n' "${MARYTTS_URL}" "${MARYTTS_VOICE}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-marytts", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
