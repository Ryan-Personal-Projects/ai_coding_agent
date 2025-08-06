"""
Function Dispatcher for AI Coding Agent

This module provides a centralized function call dispatcher that handles execution
of various file operations and Python script execution for an AI coding agent.
All functions are constrained to operate within a specified working directory
for security purposes.

Available Functions:
    - get_files_info: List files and directories in the working directory
    - get_file_content: Read contents of specified files
    - write_file: Create or overwrite files with new content
    - run_python_file: Execute Python scripts within the working directory

Security Note:
    All function calls automatically inject the working directory parameter
    to prevent directory traversal attacks. Individual functions implement
    additional path validation.
"""

from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file
from config import WORKING_DIR

# Registry of available functions mapped to their implementations
FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}
 
# Create a list of all available functions for the model
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, verbose=False):
    """
    Execute a function call from the AI model.
    
    This function serves as the main dispatcher for handling function calls
    from the AI model. It validates the function name, injects the working
    directory parameter for security, and executes the requested function.
    
    Args:
        function_call_part: Function call object containing name and arguments
                           from the AI model's response
        verbose (bool, optional): Whether to log detailed function call 
                                 information including arguments. Defaults to False.
        
    Returns:
        types.Content: Response object containing either the function execution 
                      results or error information, formatted for the AI model
        
    """
    func_name = function_call_part.name
    func_args = function_call_part.args
    func_args["working_directory"] = WORKING_DIR

    if verbose:
        print(f" - Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    if func_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    results = FUNCTIONS[func_name](**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": results},
            )
        ],
    )
    

    