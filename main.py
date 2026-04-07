from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def main():
    # Check if the API key is available
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not available")
    # Create a client
    client = genai.Client(api_key=api_key)
    # Create parser object with user_prompt and verbose arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt to be passed into the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Create messages list with user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Pass in messages list to generate content
    content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)    
    )
    if content.usage_metadata is None:
        # Assume API request failed if usage metadata is not available
        raise RuntimeError("Request Failed")
    else:
        # If verbose is enabled, print the user prompt, prompt tokens, and response tokens
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        if content.function_calls is not None:
            for function_call in content.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        print(content.text)


if __name__ == "__main__":
    main()
