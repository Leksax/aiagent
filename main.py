import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
import json
import sys




def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key == None:
        raise RuntimeError("no api key found")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    available_functions = [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free", 
            messages=messages,
            temperature=0,
            tools=available_functions,
        )
        if response.usage is None:
            raise RuntimeError("api response not working")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise Exception(f"Empty function response for {tool_call.function.name}")
                if args.verbose:
                    print(f" -> {result_message['content']}")
                messages.append(result_message)
        if not message.tool_calls:
            print(message.content)
            break
    else:
        print("loop finished after 20 iterations")
        sys.exit(1)


if __name__ == "__main__":
    main()
