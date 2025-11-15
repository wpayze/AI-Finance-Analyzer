from groq import Groq
from typing import List, Dict
from src.core.config import settings

class GroqClient:
    """
    Client for interacting with the Groq API to perform AI inference.
    """
    def __init__(self):
        """
        Initializes the GroqClient, loading the API key from settings
        and setting the default model.
        """
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model: str = "llama3-8b-8192" # As decided in research.md

    async def categorize_transactions(self, descriptions: List[str]) -> List[str]:
        """
        Sends transaction descriptions to Groq API for categorization using the Llama 3 8B model.
        
        Args:
            descriptions: A list of transaction descriptions (strings) to categorize.
            
        Returns:
            A list of categories (strings) corresponding to the input descriptions.
            
        Raises:
            ValueError: If the API key is not set.
        """
        # For simplicity, we'll send all descriptions in one prompt.
        # In a real-world scenario, you might batch these or use a more sophisticated prompt.
        prompt = (
            "Categorize the following financial transaction descriptions into one of these categories: "
            "['Groceries', 'Utilities', 'Rent', 'Transport', 'Dining Out', 'Entertainment', 'Shopping', 'Salary', 'Investments', 'Healthcare', 'Education', 'Travel', 'Uncategorized']. "
            "If a description doesn't fit, use 'Uncategorized'. "
            "Return only a comma-separated list of categories, in the same order as the input descriptions. "
            "Example: 'Coffee Shop, Supermarket' -> 'Dining Out, Groceries'\n\n"
            "Descriptions:\n" + "\n".join(descriptions)
        )

        chat_completion = await self.client.chat.completions.create( # Await the API call
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
            temperature=0.0, # Keep it deterministic for categorization
            max_tokens=1024,
        )
        
        response_content: str = chat_completion.choices[0].message.content
        # Assuming the model returns a comma-separated list
        categories: List[str] = [cat.strip() for cat in response_content.split(',')]
        return categories

groq_client = GroqClient()
