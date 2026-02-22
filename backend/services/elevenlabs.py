from __future__ import annotations

import os
from dataclasses import dataclass, field

import httpx


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Settings:
    eleven_api_key: str | None = field(default_factory=lambda: os.getenv("ELEVEN_API_KEY"))
    eleven_voice_id: str | None = field(default_factory=lambda: os.getenv("ELEVEN_VOICE_ID"))
    eleven_stt_model_id: str = field(default_factory=lambda: os.getenv("ELEVEN_STT_MODEL_ID", "scribe_v2"))
    eleven_tts_model_id: str = field(default_factory=lambda: os.getenv("ELEVEN_TTS_MODEL_ID", "eleven_flash_v2_5"))


def get_settings() -> Settings:
    return Settings()


# ---------------------------------------------------------------------------
# STT
# ---------------------------------------------------------------------------

class ElevenSTTClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        if not self.settings.eleven_api_key:
            raise RuntimeError("ELEVEN_API_KEY is required")

    def transcribe(self, audio_bytes: bytes, filename: str, content_type: str) -> str:
        with httpx.Client(timeout=45.0) as http:
            response = http.post(
                "https://api.elevenlabs.io/v1/speech-to-text",
                headers={"xi-api-key": self.settings.eleven_api_key or ""},
                data={"model_id": self.settings.eleven_stt_model_id},
                files={"file": (filename, audio_bytes, content_type)},
            )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("text") or payload.get("transcript")
        if not text:
            raise RuntimeError(f"Unexpected STT response shape: {list(payload.keys())}")
        return text


# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------

class ElevenTTSClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        if not self.settings.eleven_api_key:
            raise RuntimeError("ELEVEN_API_KEY is required")
        if not self.settings.eleven_voice_id:
            raise RuntimeError("ELEVEN_VOICE_ID is required")

    def synthesize(self, text: str) -> bytes:
        with httpx.Client(timeout=45.0) as http:
            response = http.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{self.settings.eleven_voice_id}/stream",
                headers={
                    "xi-api-key": self.settings.eleven_api_key or "",
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": self.settings.eleven_tts_model_id,
                    "output_format": "mp3_44100_128",
                },
            )
        response.raise_for_status()
        return response.content