from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

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

    # Call AI model in a loop with maximum of 20 iterations
    for call_loop in range(20):
        # Pass in messages list to generate content
        content = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)    
        )
        # Add response if any to messages list
        if content.candidates: 
            for response in content.candidates:
                messages.append(response.content)
        # Assume API request failed if usage metadata is not available
        if content.usage_metadata is None:  
            raise RuntimeError("Request Failed")
        else:
            # If verbose is enabled, print the user prompt, prompt tokens, and response tokens
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
            # Run all function calls if any
            if content.function_calls is not None:
                function_results = []
                for function_call in content.function_calls:
                    function_call_result = call_function(function_call, verbose=args.verbose)
                    if not function_call_result.parts:
                        raise Exception("Function call failed")
                    if function_call_result.parts[0].function_response is None:
                        raise Exception("Function call did not provide a response")
                    if function_call_result.parts[0].function_response.response is None:
                        raise Exception("Function call did not provide a response")
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                # Append results of function calls to messages
                messages.append(types.Content(role="user", parts=function_results))
            else:     
                print(content.text)
                return None 
    print("Maximum number of iterations reached - exiting program")
    sys.exit(1)
            


if __name__ == "__main__":
    main()
