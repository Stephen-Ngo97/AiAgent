from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import argparse

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not available")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt to be passed into the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    if content.usage_metadata is None:
        raise RuntimeError("Request Failed")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        print(content.text)

if __name__ == "__main__":
    main()
