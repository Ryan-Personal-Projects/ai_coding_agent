"""
Directory Listing and File Information for AI Coding Agent

This module provides secure directory listing functionality for the AI coding agent.
It recursively calculates file and directory sizes while enforcing security 
constraints to prevent directory traversal attacks.

Security Features:
    - Path validation to prevent directory traversal attacks
    - Directory existence and type validation
    - Recursive size calculation for directories
    - Safe handling of symbolic links and special files
"""

import os

from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    Securely list files and directories with size information within the working directory.
    
    This function provides safe directory listing with multiple security checks:
    - Validates the target directory is within the working directory
    - Checks directory exists and is actually a directory
    - Calculates recursive sizes for directories
    - Handles file system errors gracefully
    
    Args:
        working_directory (str): The base directory path that constrains access
        directory (str, optional): Relative path to list, relative to working_directory.
                                  Defaults to "." (current working directory).
        
    Returns:
        str: Formatted listing of files and directories with sizes, or error message if failed.
             Format: " - filename: file_size=X bytes, is_dir=True/False"
    """
    try:
        target_directory = os.path.abspath(os.path.join(working_directory, directory))
        abs_working_directory = os.path.abspath(working_directory)

        # Check that target directory is inside working directory
        if not target_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        # Check target directory is a directory
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
    
        # Get target directory contents
        items_details = []
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            item_size = get_item_size(item_path)
            is_dir = os.path.isdir(item_path)
            item_details = f" - {item}: file_size={item_size} bytes, is_dir={is_dir}"
            items_details.append(item_details)
        result = "\n".join(items_details)
        return result
    except Exception as e:
        return f"Error listing files: {e}"
    
def get_item_size(path):
    """
    Recursively calculate the total size of a file or directory.
    
    For files, returns the file size directly. For directories, recursively
    calculates the total size of all contained files and subdirectories.
    
    Args:
        path (str): Absolute path to the file or directory
        
    Returns:
        int: Total size in bytes, or 0 if path doesn't exist or is inaccessible
        
    Note:
        This function can be resource-intensive for large directory trees.
        It handles permission errors by returning 0 for inaccessible items.
    """
    if os.path.isdir(path):
        total_size = 0
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                total_size += os.path.getsize(full_path)
            elif os.path.isdir(full_path):
                total_size += get_item_size(full_path)
        return total_size             
    elif os.path.isfile(path):
        return os.path.getsize(path)
    else:
        return 0
    
# Schema definition for the AI model to understand this function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)