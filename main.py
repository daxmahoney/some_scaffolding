import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from call_function import available_functions
from prompts import system_prompt
from call_function import call_function
import json


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content":system_prompt},
        {"role": "user","content": args.user_prompt}
    ]
    response = client.chat.completions.create(model="openrouter/free",
                                               messages=messages, tools=available_functions,)
    if args.verbose:
        print(f"User prompt: {messages[0]['content']}")
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("response not connecting")
        
    message = response.choices[0].message

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            tool_output = call_function(tool_call, args.verbose)
            if not tool_output['content']:
                raise Exception("Error: Result is none")
            
            print(f"Calling function: {tool_call.function.name}({function_args})")
            if args.verbose:
                print(f"-> {tool_output['content']}")
    if message.tool_calls is None:
        print(f"Response: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()
