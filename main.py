import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No valid API key detected")

    # Define a new Gemini Client
    client = genai.Client(api_key=api_key)

    # Define a parser and use it to parse user arguments
    # This makes it so that we can access "args.user_prompt"
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Defining a conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            ),
        )
        function_responses = []
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.usage_metadata is None:
            raise RuntimeError("No metadata received, invalid API request?")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError("No parts returned from function call")
                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise RuntimeError("No function response returned")
                if function_response.response is None:
                    raise RuntimeError("No response field returned")
                function_responses.append(function_call_result.parts[0])
                print(f"-> {function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            return

    print("Maximum iterations reached without a final response")
    sys.exit(1)

if __name__ == "__main__":
    main()
