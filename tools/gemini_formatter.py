class GeminiFormatter:
    @staticmethod
    def format_messages(messages, system_prompt=None):
        """
        Convert internal message history to Gemini API format.
        Prepends system prompt to the first user message if provided.
        """
        formatted_content = []
        user_count = 0
        for msg in messages:
            if msg["role"] == "user":
                user_count += 1
                if user_count == 1 and system_prompt:
                    formatted_content.append({
                        "role": "user",
                        "parts": [{"text": f"{system_prompt}\n\n{msg['content']}"}]
                    })
                else:
                    formatted_content.append({
                        "role": "user",
                        "parts": [{"text": msg["content"]}]
                    })
            elif msg["role"] == "assistant":
                formatted_content.append({
                    "role": "model",
                    "parts": [{"text": msg["content"]}]
                })
        return formatted_content
