from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from eleven_client import ElevenSTTClient, ElevenTTSClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_response(json_data: dict | None = None, content: bytes = b"", status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = content
    resp.json.return_value = json_data or {}
    resp.raise_for_status = MagicMock()
    return resp


# ---------------------------------------------------------------------------
# ElevenSTTClient
# ---------------------------------------------------------------------------

class TestElevenSTTClient:
    def test_raises_if_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ELEVEN_API_KEY", raising=False)
        with pytest.raises(RuntimeError, match="ELEVEN_API_KEY is required"):
            ElevenSTTClient()

    def test_transcribe_returns_text_field(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        client = ElevenSTTClient()

        mock_resp = _mock_response(json_data={"text": "hello world"})
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            result = client.transcribe(b"audio", "audio.mp3", "audio/mpeg")

        assert result == "hello world"

    def test_transcribe_falls_back_to_transcript_field(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        client = ElevenSTTClient()

        mock_resp = _mock_response(json_data={"transcript": "fallback text"})
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            result = client.transcribe(b"audio", "audio.mp3", "audio/mpeg")

        assert result == "fallback text"

    def test_transcribe_raises_on_unexpected_response_shape(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        client = ElevenSTTClient()

        mock_resp = _mock_response(json_data={"something_else": "oops"})
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            with pytest.raises(RuntimeError, match="Unexpected STT response shape"):
                client.transcribe(b"audio", "audio.mp3", "audio/mpeg")

    def test_transcribe_uses_correct_model_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        monkeypatch.setenv("ELEVEN_STT_MODEL_ID", "scribe_v2")
        client = ElevenSTTClient()

        mock_resp = _mock_response(json_data={"text": "hi"})
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_post = mock_http_cls.return_value.__enter__.return_value.post
            mock_post.return_value = mock_resp
            client.transcribe(b"audio", "audio.mp3", "audio/mpeg")
            _, kwargs = mock_post.call_args
            assert kwargs["data"]["model_id"] == "scribe_v2"

    def test_transcribe_raises_for_http_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        client = ElevenSTTClient()

        mock_resp = _mock_response(status_code=401)
        mock_resp.raise_for_status.side_effect = Exception("401 Unauthorized")
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            with pytest.raises(Exception, match="401 Unauthorized"):
                client.transcribe(b"audio", "audio.mp3", "audio/mpeg")


# ---------------------------------------------------------------------------
# ElevenTTSClient
# ---------------------------------------------------------------------------

class TestElevenTTSClient:
    def test_raises_if_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ELEVEN_API_KEY", raising=False)
        monkeypatch.delenv("ELEVEN_VOICE_ID", raising=False)
        with pytest.raises(RuntimeError, match="ELEVEN_API_KEY is required"):
            ElevenTTSClient()

    def test_raises_if_no_voice_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        monkeypatch.delenv("ELEVEN_VOICE_ID", raising=False)
        with pytest.raises(RuntimeError, match="ELEVEN_VOICE_ID is required"):
            ElevenTTSClient()

    def test_synthesize_returns_audio_bytes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        monkeypatch.setenv("ELEVEN_VOICE_ID", "voice-abc")
        client = ElevenTTSClient()

        fake_audio = b"\xff\xfb\x90\x00" * 100
        mock_resp = _mock_response(content=fake_audio)
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            result = client.synthesize("Hello there")

        assert result == fake_audio

    def test_synthesize_sends_correct_payload(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        monkeypatch.setenv("ELEVEN_VOICE_ID", "voice-abc")
        monkeypatch.setenv("ELEVEN_TTS_MODEL_ID", "eleven_flash_v2_5")
        client = ElevenTTSClient()

        mock_resp = _mock_response(content=b"audio")
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_post = mock_http_cls.return_value.__enter__.return_value.post
            mock_post.return_value = mock_resp
            client.synthesize("Say this")
            _, kwargs = mock_post.call_args

        assert kwargs["json"]["text"] == "Say this"
        assert kwargs["json"]["model_id"] == "eleven_flash_v2_5"
        assert kwargs["json"]["output_format"] == "mp3_44100_128"
        assert "voice-abc" in mock_post.call_args[0][0]

    def test_synthesize_raises_for_http_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ELEVEN_API_KEY", "test-key")
        monkeypatch.setenv("ELEVEN_VOICE_ID", "voice-abc")
        client = ElevenTTSClient()

        mock_resp = _mock_response(status_code=429)
        mock_resp.raise_for_status.side_effect = Exception("429 Too Many Requests")
        with patch("eleven_client.httpx.Client") as mock_http_cls:
            mock_http_cls.return_value.__enter__.return_value.post.return_value = mock_resp
            with pytest.raises(Exception, match="429 Too Many Requests"):
                client.synthesize("Hello")