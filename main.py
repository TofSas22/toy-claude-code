import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function


def main():
    parser = argparse.ArgumentParser(description="Prompt Input")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY missing or invalid")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        response, function_responses = generate_content(client, messages, args.verbose)
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
        
        if not response.function_calls: 
            print(response.text)
            break
    else:
        print("Max iterations reached without final response")
        sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    usage = response.usage_metadata

    if usage == None:
        raise RuntimeError("failed API request")

    if verbose:
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return response, []

    function_results = []

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if not function_call_result.parts:
            raise Exception("No parts")
        
        first_part = function_call_result.parts[0]
        if first_part.function_response is None:
            raise Exception("No function_response")
        if first_part.function_response.response is None:
            raise Exception("No response in function_response")
        
        function_results.append(first_part)

        if verbose:
            print(f"-> {first_part.function_response.response}")

    return response, function_results
    


if __name__ == "__main__":
    main()



