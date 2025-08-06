"""
Python Script Executor for AI Coding Agent

This module provides secure Python script execution functionality for the AI coding agent.
It executes Python files within a controlled environment with security constraints and
timeout protection to prevent runaway processes.

SECURITY WARNING:
    This module allows arbitrary Python code execution within the working directory.
    It should only be used in trusted environments with proper sandboxing.

Security Features:
    - Path validation to prevent directory traversal attacks
    - File existence and Python extension validation
    - Timeout protection (30 seconds) to prevent hanging processes
    - Output capture and error handling
    - Working directory constraint for subprocess execution

Limitations:
    - Only executes .py files
    - 30-second execution timeout
    - No interactive input support
    - Output size not limited (could cause memory issues with large outputs)
"""

import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    """
    Securely execute a Python file within the working directory with timeout protection.
    
    This function provides controlled Python script execution with multiple safety checks:
    - Validates the file path is within the working directory
    - Checks file exists and has .py extension
    - Executes with 30-second timeout to prevent hanging
    - Captures both stdout and stderr output
    - Returns comprehensive execution results
    
    Args:
        working_directory (str): The base directory path that constrains file access
        file_path (str): Relative path to the Python file to execute
        args (list, optional): Command line arguments to pass to the Python script.
                              Defaults to empty list.
        
    Returns:
        str: Execution results including stdout, stderr, and return code information,
             or error message if execution failed
        
    Warnings:
        - This function allows arbitrary code execution within the working directory
        - Should only be used in trusted, sandboxed environments
        - No protection against resource exhaustion or malicious code
    """
    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)

        # Check that file path is inside working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check that file path exists and is a file
        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check that file is a python file
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Run python file as a subprocess with security constraints
        subprocess_args = ["python", abs_file_path]
        if args:
            subprocess_args.extend(args)
        comp_proc_obj = subprocess.run(
            args=subprocess_args, 
            timeout=30, 
            capture_output=True, 
            cwd=abs_working_directory, 
            text=True
        )

        # Capture and format results of subprocess execution
        result = []
        if comp_proc_obj.stdout:
            result.append(f"STDOUT:\n{comp_proc_obj.stdout}")
        if comp_proc_obj.stderr:
            result.append(f"STDERR:\n{comp_proc_obj.stderr}")
        if comp_proc_obj.returncode != 0:
            result.append(f"Process exited with code {comp_proc_obj.returncode}")
        return "\n".join(result) if result else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"

# Schema definition for the AI model to understand this function    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Additional arguments to pass in for when python file is ran. If none are provided, the value defaults to an empty array.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
        required=["file_path"],
    ),
)
