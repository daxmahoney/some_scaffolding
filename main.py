import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from call_function import available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]
    response = client.chat.completions.create(model="openrouter/free",
                                               messages=messages, tools=available_functions,)
    if args.verbose:
        print(f"User prompt: {messages[0]["content"]}")
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("response not connecting")
    print(f"Response: {response.choices[0].message.content}")
    
if __name__ == "__main__":
    main()
