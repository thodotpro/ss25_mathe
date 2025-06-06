import pytest
from unittest.mock import patch, MagicMock
from agent.agent import Agent

class DummyResponse:
    def __init__(self, text):
        self.text = text

def test_agent_call_and_execute(monkeypatch):
    # Patch GeminiFormatter to just echo the messages
    with patch('agent.agent.GeminiFormatter') as MockFormatter:
        MockFormatter.format_messages = staticmethod(lambda messages, system: [{'role': 'user', 'parts': [{'text': messages[-1]['content']}]}])
        # Patch the client.models.generate_content to return a dummy response
        dummy_client = MagicMock()
        dummy_model = MagicMock()
        dummy_response = DummyResponse("Paris")
        dummy_model.generate_content.return_value = dummy_response
        dummy_client.models = MagicMock()
        dummy_client.models.generate_content = dummy_model.generate_content
        # Patch system_prompt to avoid file I/O
        with patch('agent.agent.system_prompt', return_value="You are a helpful assistant."):
            agent = Agent(client=dummy_client, system="You are a helpful assistant.")
            query = "What is the capital of France?"
            result = agent(query)
            assert result == "Paris"
            assert agent.messages[-1]['content'] == "Paris"
            assert agent.messages[0]['content'] == query

def test_agent_empty_query():
    agent = Agent(client=MagicMock(), system="sys")
    with pytest.raises(ValueError):
        agent("")
