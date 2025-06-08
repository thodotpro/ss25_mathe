class OllamaFormatter:
    @staticmethod
    def format_messages(messages, system_prompt=None, include_system_prompt=True):
        prompt = ""
        # Only include the system prompt in the prompt string, not for printing
        if include_system_prompt and system_prompt:
            prompt += system_prompt.strip() + "\n\n"
        # Only include the last user and assistant message to avoid recursive history
        last_user = None
        last_assistant = None
        for msg in reversed(messages):
            if not last_user and msg["role"] == "user":
                last_user = msg["content"]
            elif not last_assistant and msg["role"] == "assistant":
                last_assistant = msg["content"]
            if last_user and last_assistant:
                break
        if last_user:
            prompt += f"User: {last_user}\n"
        if last_assistant:
            prompt += f"Assistant: {last_assistant}\n"
        return prompt
