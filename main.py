import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY missing or invalid")

    parser = argparse.ArgumentParser(description="Prompt Input")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages
    )

    usage = response.usage_metadata

    if usage == None:
        raise RuntimeError("failed API request")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
