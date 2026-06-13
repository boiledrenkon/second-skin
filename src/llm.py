# ------------------------------------------------------------------------------
# LLM                                                                          |
# ------------------------------------------------------------------------------
# Provider-agnostic text generation. Every model call in the project goes
# through complete(); nothing else hardcodes a model or a provider SDK.
#
# Models are named by *role* (e.g. "summarize", "reply") in src/models.toml,
# mapping each role to a litellm "provider/model" string:
#
#     summarize = "openai/gpt-4o-mini"
#     reply     = "anthropic/claude-sonnet-4-20250514"
#     local     = "ollama/llama3"
#
# Swapping providers is a one-line edit there — no code change. See
# https://docs.litellm.ai/docs/providers for the full list of prefixes.
import os

import litellm

from src.util import open_toml, robo_caller


# Short key names used in tokens.toml [keys] -> the env var litellm expects.
# Any key already written as an UPPER_SNAKE env var name (e.g. ANTHROPIC_API_KEY)
# is exported verbatim, so new providers need no code change here either.
_KEY_ALIASES = {
    "opa": "OPENAI_API_KEY",
    "ant": "ANTHROPIC_API_KEY",
    "ope": "OPENROUTER_API_KEY",
    "gem": "GEMINI_API_KEY",
}


def load_provider_keys() -> None:
    """Export API keys from tokens.toml [keys] into the environment for litellm.

    Idempotent (setdefault), so it is safe to call on every request.
    """
    for name, value in robo_caller().items():
        env = _KEY_ALIASES.get(name, name)
        if env.isupper():  # looks like a real provider env var; export it
            os.environ.setdefault(env, value)
        # lowercase aliases with no mapping (e.g. "eln" for ElevenLabs) are
        # not LLM-provider keys and are handled by their own caller.


def resolve_model(role: str) -> str:
    models = open_toml("models")
    model = models.get(role)
    if not model:
        raise KeyError(f"No model configured for role '{role}' in src/models.toml")
    return model


def complete(
    prompt: str = None,
    *,
    role: str = None,
    model: str = None,
    messages: list = None,
    **params,
) -> str:
    """Run a chat completion and return the assistant's text.

    Provide a `role` (resolved via models.toml) or an explicit litellm `model`.
    Pass either a `prompt` string or a full `messages` list. Extra keyword args
    (temperature, max_tokens, stop, ...) are forwarded to litellm unchanged.
    """
    load_provider_keys()
    target = model or resolve_model(role)
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    response = litellm.completion(model=target, messages=messages, **params)
    return response.choices[0].message.content
