import os, argparse
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt
from functions.call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("No valid API key detected")

    #Define a new Gemini Client
    client = genai.Client(api_key=api_key)

    #Define a parser and use it to parse user arguments
    #This makes it so that we can access "args.user_prompt"
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Defining a conversation history
    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("No metadata receives, invalid API request?")

    if args.verbose:
        print(f"User prompt: {args.user_prompt} ")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(response.text)
    else:
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(response.text)

if __name__ == "__main__":
    main()
