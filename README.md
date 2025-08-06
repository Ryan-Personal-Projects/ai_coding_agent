# AI Coding Agent

A conversational AI assistant powered by Google's Gemini API that provides intelligent coding assistance through secure file operations and Python script execution. The agent can read, write, and execute code within a controlled environment while maintaining multi-turn conversations with function calling capabilities.

## Installation Instructions

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key

### Setup Process

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai_coding_agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or if using uv:
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   You can obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

4. **Verify installation:**
   ```bash
   python main.py "Hello, can you help me?"
   ```

## Usage Examples

### Basic Usage
```bash
python main.py "your prompt here"
```

### Common Use Cases

**Ask for coding help:**
```bash
python main.py "How do I create a Python function to calculate factorial?"
```

**Analyze existing code:**
```bash
python main.py "Review the code in calculator/main.py and suggest improvements"
```

**Fix bugs in your code:**
```bash
python main.py "There's a bug in my calculator app where 3 + 7 * 2 returns 20 instead of 17"
```

**Get file information:**
```bash
python main.py "List all Python files in this directory and their sizes"
```

### Verbose Mode
Enable detailed logging with token usage and function call information:
```bash
python main.py "Create a simple calculator function" --verbose
```

## Features

- **Conversational AI Assistant**: Powered by Google's Gemini 2.0 Flash model for intelligent coding assistance
- **Secure File Operations**: Read, write, and list files within a controlled working directory
- **Python Script Execution**: Execute Python scripts with timeout protection and output capture
- **Multi-turn Conversations**: Maintains conversation context across multiple interactions
- **Function Calling**: Automatically executes appropriate file operations based on user requests
- **Verbose Debugging**: Optional detailed logging for troubleshooting and development
- **Security Constraints**: All operations are sandboxed within the configured working directory
- **Error Handling**: Comprehensive error handling with informative error messages

## Requirements

### Dependencies
- **google-genai**: ^1.12.1 - Google Gemini API client
- **python-dotenv**: ^1.1.0 - Environment variable management

### System Requirements
- **Python**: 3.11 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Memory**: Minimum 512MB available RAM
- **Network**: Internet connection required for Gemini API access

### API Requirements
- Valid Google Gemini API key with sufficient quota
- API key must be set in the `GEMINI_API_KEY` environment variable

## Configuration

### Environment Variables
The following environment variables can be configured:

- **GEMINI_API_KEY** (required): Your Google Gemini API key

### Application Settings
Configuration is managed in `config.py`:

- **MAX_CHARS**: Maximum characters to read from files (default: 10,000)
- **MAX_CONV_ROUNDS**: Maximum conversation rounds to prevent infinite loops (default: 20)
- **WORKING_DIR**: Directory where file operations are permitted (default: "./calculator")

### Working Directory
By default, the agent operates within the `./calculator` directory. All file operations (read, write, list, execute) are constrained to this directory for security. To change the working directory, modify the `WORKING_DIR` setting in `config.py`.

### Function Capabilities
The agent has access to the following functions:
- `get_files_info`: List files and directories with size information
- `get_file_content`: Read file contents (up to MAX_CHARS characters)
- `write_file`: Create or overwrite files with new content
- `run_python_file`: Execute Python scripts with 30-second timeout