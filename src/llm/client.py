"""LLM Client for API calls."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Client for interacting with OpenAI API."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """Initialize the LLM client.

        Args:
            model: The OpenAI model to use
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_completion(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000
    ) -> str:
        """Generate a completion from the LLM.

        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            The generated text response

        Raises:
            Exception: If the API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")


# test
if __name__ == "__main__":
    client = LLMClient()
    result = client.generate_completion("Say 'Hello from LLM!'")
    print(f"✅ LLM Response: {result}")
