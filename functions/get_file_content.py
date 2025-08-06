"""
File Content Reader for AI Coding Agent

This module provides secure file reading functionality for the AI coding agent.
It reads file contents while enforcing security constraints to prevent directory
traversal attacks and limiting file size to prevent memory issues.

Security Features:
    - Path validation to prevent directory traversal attacks
    - File existence and type validation
    - Content size limiting to prevent memory exhaustion
    - UTF-8 encoding with error handling
"""

import os

from google.genai import types

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    """
    Securely read and return the contents of a file within the working directory.
    
    This function provides safe file reading with multiple security checks:
    - Validates the file path is within the working directory
    - Checks file exists and is a regular file (not directory/special file)
    - Limits content reading to MAX_CHARS to prevent memory issues
    - Handles encoding errors gracefully
    
    Args:
        working_directory (str): The base directory path that constrains file access
        file_path (str): Relative path to the file to read, relative to working_directory
        
    Returns:
        str: The file contents (up to MAX_CHARS characters) or error message if failed
    """
    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)

        # Check that file path is inside working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check that file path is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the contents of the file
        with open(abs_file_path, "r", encoding="utf-8") as file_reader:
            file_contents = file_reader.read(MAX_CHARS)
            if file_reader.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

# Schema definition for the AI model to understand this function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory."
            )
        },
        required=["file_path"],
    )
)
