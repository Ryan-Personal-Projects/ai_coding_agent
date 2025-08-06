"""
File Writer for AI Coding Agent

This module provides secure file writing functionality for the AI coding agent.
It creates and overwrites files within a controlled environment with security
constraints to prevent directory traversal attacks and ensure safe file operations.

Security Features:
    - Path validation to prevent directory traversal attacks
    - Automatic directory creation for nested file paths
    - File vs directory validation to prevent overwriting directories
    - UTF-8 encoding with error handling
    - Content size reporting for transparency

Important Notes:
    - Files are created if they don't exist
    - Existing files are completely overwritten (not appended to)
    - Intermediate directories are created automatically
    - All operations are constrained to the working directory
"""

import os

from google.genai import types

def write_file(working_directory, file_path, content):
    """
    Securely write content to a file within the working directory.
    
    This function provides safe file writing with multiple security checks:
    - Validates the file path is within the working directory
    - Creates intermediate directories if needed
    - Prevents overwriting directories with files
    - Handles encoding and file system errors gracefully
    - Reports the number of characters written
    
    Args:
        working_directory (str): The base directory path that constrains file access
        file_path (str): Relative path to the file to write, relative to working_directory
        content (str): The content to write to the file (will completely replace existing content)
        
    Returns:
        str: Success message with character count, or error message if failed
    """
    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)

        # Check that file path is inside working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create intermediate directories if they don't exist
        if not os.path.exists(abs_file_path):
            try:
                os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            except Exception as e:
                return f"Error creating directory: {e}"

        # Prevent overwriting directories with files
        if os.path.isdir(abs_file_path):
            return f'Error: "{file_path}" is a directory, not a file'

        # Write content to file (creates new file or overwrites existing)
        with open(abs_file_path, "w", encoding="utf-8") as file_writer:
            file_writer.write(content)
        
        # Return success message with character count
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing file "{file_path}": {e}'
    
# Schema definition for the AI model to understand this function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that will be written to the designated file."
            ),
        },
        required=["file_path", "content"],
    )
)
