"""
AI Coding Agent - Main Application

This is the main entry point for the AI coding agent that uses Google's Gemini API
to provide conversational AI assistance for coding tasks. The agent can perform
file operations, execute Python scripts, and maintain multi-turn conversations
with function calling capabilities.

Features:
    - Interactive AI assistant powered by Gemini 2.0 Flash
    - Secure file operations (read, write, list) within working directory
    - Python script execution with timeout protection
    - Multi-turn conversations with function calling
    - Verbose mode for debugging and token usage tracking
    - Conversation round limiting to prevent infinite loops

Usage:
    python main.py "your prompt here" [--verbose]
    
Examples:
    python main.py "How do I build a calculator app?"
    python main.py "Fix the bug in my script.py" --verbose
    python main.py "List all Python files in this directory"

Requirements:
    - GEMINI_API_KEY environment variable
    - google-genai package
    - python-dotenv package
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_CONV_ROUNDS

def main():
    """
    Main entry point for the AI coding agent.
    
    Handles command-line argument parsing, initializes the Gemini client,
    and manages the conversation loop with the AI model including function
    calls and response handling.
    
    Command Line Arguments:
        prompt (str): The user's prompt/question for the AI agent
        --verbose (optional): Enable verbose output with token usage and function call details
        
    Environment Variables:
        GEMINI_API_KEY: Required API key for Google Gemini service
        
    Exits:
        1: Missing prompt, API errors, or maximum conversation rounds exceeded
        0: Successful completion with final AI response
        
    Raises:
        SystemExit: On missing arguments, API errors, or conversation limits
    """
    load_dotenv()
    print("Hello from ai-coding-agent!\n")

    # Parse command line arguments
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print('Usage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    prompt = " ".join(args)

    # Initialize Gemini client with API key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    # Initialize conversation with user's initial prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    # Main conversation loop with round limiting
    conversation_counter = 0
    while True:
        try:
            gen_content_response = generate_content(client, messages)
            final_response = handle_content(gen_content_response, messages, prompt, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
            
            conversation_counter += 1
            if conversation_counter >= MAX_CONV_ROUNDS:
                print(f"Maximum iterations ({MAX_CONV_ROUNDS}) reached.")
                sys.exit(1)

        except Exception as e:
            print(f"Error during prompt processing: {e}")
            sys.exit(1)

def generate_content(client, messages):
    """
    Generate AI response using Gemini model with function calling capabilities.
    
    Sends the current conversation history to the Gemini model and receives
    a response that may include text content and/or function calls. The model's
    response is automatically added to the message history for context continuity.
    
    Args:
        client: Initialized Gemini client instance
        messages (list): Conversation history as list of Content objects
        
    Returns:
        GenerateContentResponse: The model's response containing text and/or function calls
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )

    # Add model response to conversation history for context continuity
    for candidate in response.candidates:
        messages.append(candidate.content)

    return response

def handle_content(response, messages, prompt, verbose):
    """
    Process the AI model's response and handle any function calls.
    
    This function processes the model's response, executing any function calls
    and adding the results back to the conversation history. If the response
    contains only text (no function calls), it returns the text as the final response.
    
    Args:
        response: The GenerateContentResponse from the Gemini model
        messages (list): Conversation history to update with function results
        prompt (str): Original user prompt (used for verbose logging)
        verbose (bool): Whether to print detailed debugging information
        
    Returns:
        str or None: Final text response if no function calls, None if function calls were processed

    Raises:
        Exception: If function call results are empty or malformed
    """
    if verbose:
        print(f"User prompt: {prompt}") 
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # If no function calls, return the text response as final answer
    if not response.function_calls:
        return response.text

    # Process each function call and collect results
    function_responses = []
    for func in response.function_calls:
        function_call_result = call_function(func, verbose)

        # Validate function call result structure
        if (
            not function_call_result.parts 
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("no function responses generated, exiting")

    # Add function call results to conversation history
    messages.append(
        types.Content(
            role="tool",
            parts=function_responses
        )
    )

if __name__ == "__main__":
    main()
