# main.py
import os
import sys
from config import MAX_ITERS
from google import genai
from google.genai import types
from dotenv import load_dotenv
from agent_instructions import SYSTEM_PROMPT
from func_calling import call_function, available_functions

def generate_content(client, messages, verbose, system_prompt):
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=messages,
            config = types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if verbose :
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response is None or response.usage_metadata is None : 
            print("No llm response...")
            return None
        
        if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                if function_call_content:
                    messages.append(function_call_content)
                
        
        if not response.function_calls:
            return response
    
        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

        messages.append(types.Content(parts=function_responses))
        return response
    
def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
            
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
                
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: LLM_PI_KEY not found in environment variables.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    system_prompt = SYSTEM_PROMPT.strip()
    user_prompt = " ".join(args)
    
        
    messages = []
    print("AI Agent activated. Type 'exit' to end the session.")
    first_prompt = True
    end = False
    while True:
        user_prompt = user_prompt if first_prompt else input("--> You... : ")
        first_prompt = False
        if verbose:
            print(f"\nUser prompt: {user_prompt}\n")
        if user_prompt.lower() == 'exit' :
            break
        messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
        for _ in range(MAX_ITERS):
            try:
                response = generate_content(client, messages, verbose, system_prompt)
                
                if response and not response.function_calls:
                    final_response = "".join(part.text for part in response.candidates[0].content.parts)
                    print(f"\n--> Agent... : {final_response}")
                    print("----------------------------------------------\n")
                    end = True
                    break
                
            except Exception as e:
                print(f"Error in generate_content: {e}")
                break
        else:
            print("Agent: I couldn't resolve the request within the maximum number of allowed steps.")
        if end: break    
    
if __name__ == "__main__":
    main()
