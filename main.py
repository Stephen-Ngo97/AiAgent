from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not available")
    client = genai.Client(api_key=api_key)
    content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    if content.usage_metadata is None:
        raise RuntimeError("Request Failed")
    else:
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        print(content.text)

if __name__ == "__main__":
    main()
