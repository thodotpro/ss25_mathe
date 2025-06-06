import pytest
from tools.gemini_formatter import GeminiFormatter

def test_format_messages_prepends_system_prompt():
    messages = [
        {"role": "user", "content": "Hello!"}
    ]
    system_prompt = "You are a helpful assistant."
    formatted = GeminiFormatter.format_messages(messages, system_prompt)
    assert formatted[0]["role"] == "user"
    assert system_prompt in formatted[0]["parts"][0]["text"]
    assert "Hello!" in formatted[0]["parts"][0]["text"]

def test_format_messages_multiple_user_and_assistant():
    messages = [
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hello! How can I help you?"},
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "2+2 is 4."}
    ]
    system_prompt = "System prompt."
    formatted = GeminiFormatter.format_messages(messages, system_prompt)
    assert formatted[0]["role"] == "user"
    assert "System prompt." in formatted[0]["parts"][0]["text"]
    assert formatted[1]["role"] == "model"
    assert formatted[1]["parts"][0]["text"] == "Hello! How can I help you?"
    assert formatted[2]["role"] == "user"
    assert formatted[2]["parts"][0]["text"] == "What is 2+2?"
    assert formatted[3]["role"] == "model"
    assert formatted[3]["parts"][0]["text"] == "2+2 is 4."

def test_format_messages_no_system_prompt():
    messages = [
        {"role": "user", "content": "Test message."}
    ]
    formatted = GeminiFormatter.format_messages(messages)
    assert "Test message." in formatted[0]["parts"][0]["text"]
    assert "You are a helpful assistant." not in formatted[0]["parts"][0]["text"]
