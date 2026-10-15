from types import SimpleNamespace

import pytest

from app.utils.openai_chat_compat import (
    CLAUDE_DEFAULT_MAX_TOKENS,
    CLAUDE_JSON_INSTRUCTION,
    claude_model_config,
    create_chat_completion,
    extract_chat_completion_text,
    is_claude_model,
    is_gpt5_family,
)


class CompletionRecorder:
    def __init__(self, result=None, error=None):
        self.result = result or object()
        self.error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.result


def client_for(recorder):
    return SimpleNamespace(chat=SimpleNamespace(completions=recorder))


def test_gpt5_uses_completion_token_limit_without_temperature():
    recorder = CompletionRecorder()
    messages = [{"role": "user", "content": "hello"}]

    result = create_chat_completion(
        client_for(recorder),
        model="gpt-5-2025-08-07",
        messages=messages,
        temperature=0.2,
        max_tokens=123,
        response_format={"type": "json_object"},
    )

    assert result is recorder.result
    assert recorder.calls == [
        {
            "model": "gpt-5-2025-08-07",
            "messages": messages,
            "max_completion_tokens": 123,
            "response_format": {"type": "json_object"},
        }
    ]


def test_legacy_model_preserves_original_request_shape():
    recorder = CompletionRecorder()
    messages = [{"role": "user", "content": "hello"}]

    create_chat_completion(
        client_for(recorder),
        model="third-party-chat-model",
        messages=messages,
        temperature=0.7,
        max_tokens=456,
        response_format={"type": "json_object"},
    )

    assert recorder.calls == [
        {
            "model": "third-party-chat-model",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 456,
            "response_format": {"type": "json_object"},
        }
    ]


def test_provider_error_is_propagated_without_guessing_or_retrying():
    provider_error = RuntimeError("unsupported max_tokens due to a server outage")
    recorder = CompletionRecorder(error=provider_error)

    with pytest.raises(RuntimeError) as captured:
        create_chat_completion(
            client_for(recorder),
            model="legacy-model",
            messages=[],
            max_tokens=10,
        )

    assert captured.value is provider_error
    assert len(recorder.calls) == 1


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        ("gpt-5", True),
        (" GPT-5.1-mini ", True),
        ("gpt-4.1", False),
        ("my-gpt-5-proxy", False),
        (None, False),
    ],
)
def test_gpt5_family_detection(model, expected):
    assert is_gpt5_family(model) is expected


def test_claude_json_request_drops_unsupported_params_and_adds_instruction():
    recorder = CompletionRecorder()
    messages = [
        {"role": "system", "content": "You are a profile generator."},
        {"role": "user", "content": "hello"},
    ]
    original = [dict(m) for m in messages]

    create_chat_completion(
        client_for(recorder),
        model="claude-haiku-5-5",
        messages=messages,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    assert recorder.calls == [
        {
            "model": "claude-haiku-5-5",
            "messages": [
                *original,
                {"role": "system", "content": CLAUDE_JSON_INSTRUCTION},
            ],
            "max_tokens": CLAUDE_DEFAULT_MAX_TOKENS,
        }
    ]
    assert messages == original


def test_claude_plain_request_keeps_messages_and_explicit_token_limit():
    recorder = CompletionRecorder()
    messages = [{"role": "user", "content": "hello"}]

    create_chat_completion(
        client_for(recorder),
        model="claude-sonnet-5-5",
        messages=messages,
        temperature=0.3,
        max_tokens=4096,
    )

    assert recorder.calls == [
        {"model": "claude-sonnet-5-5", "messages": messages, "max_tokens": 4096}
    ]


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        ("claude-haiku-5-5", True),
        (" Claude-Opus-5-5 ", True),
        ("anthropic.claude-opus-5-5", False),
        ("qwen-plus", False),
        (None, False),
    ],
)
def test_claude_model_detection(model, expected):
    assert is_claude_model(model) is expected


def test_claude_model_config_only_applies_to_claude():
    assert claude_model_config("claude-haiku-5-5") == {
        "max_tokens": CLAUDE_DEFAULT_MAX_TOKENS
    }
    assert claude_model_config("gpt-4o-mini") is None


@pytest.mark.parametrize("model", ["claude-haiku-5-5", "qwen-plus"])
def test_simulation_model_request_shape(model, monkeypatch):
    """The camel model used by the simulation scripts sends no sampling params."""
    from camel.models import ModelFactory
    from camel.types import ModelPlatformType

    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used")
    backend = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=model,
        model_config_dict=claude_model_config(model),
        url="https://example.invalid/v1/",
    )
    recorder = CompletionRecorder()
    monkeypatch.setattr(backend._client.chat, "completions", recorder)

    backend._request_chat_completion([{"role": "user", "content": "hi"}])

    sent = recorder.calls[0]
    assert "temperature" not in sent
    assert "response_format" not in sent
    if is_claude_model(model):
        assert sent["max_tokens"] == CLAUDE_DEFAULT_MAX_TOKENS
    else:
        assert "max_tokens" not in sent


def test_extracts_text_from_supported_content_shapes():
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=[
                        {"text": {"value": "first"}},
                        {"content": " second"},
                        SimpleNamespace(text=" third"),
                    ]
                )
            )
        ]
    )

    assert extract_chat_completion_text(response) == "first second third"
    assert extract_chat_completion_text(SimpleNamespace(choices=[])) == ""
