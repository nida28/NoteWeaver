# NoteWeaver

Clean up raw OCR or ChatGPT dump text into neat, organized Markdown files, one per day.

NoteWeaver takes messy text dumps from OCR or ChatGPT conversations and transforms them into clean, well-formatted Markdown files organized chronologically. It handles noise removal, formatting fixes, and deduplication using AI-powered cleaning.

## Features

- **Block Parsing**: Intelligently splits raw text into screenshot-style blocks
- **Noise Removal**: Filters out OCR artifacts, headers, and formatting noise
- **AI-Powered Cleaning**: Uses OpenAI GPT to fix spacing, punctuation, and Markdown formatting
- **Deduplication**: Removes duplicate or near-duplicate paragraphs
- **Daily Organization**: Writes one Markdown file per day in chronological order
- **Concurrent Processing**: Fast parallel processing with configurable worker threads

## Installation

### Quick Install (Development)

```bash
# Clone the repository
git clone <your-repo-url>
cd NoteWeaver

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (recommended for src-layout)
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Install as Package (Recommended)

```bash
# After cloning and activating venv
pip install -e .

# This installs the package and CLI commands
```

## Usage

### Method 1: Module Style (Recommended)

```bash
python -m weave data/samples/input.txt --output data/output
```

### Method 2: After Package Installation

If you installed with `pip install -e .`, you can use:

```bash
noteweaver data/samples/input.txt --output data/output

# Or the shorter alias:
clean-md data/samples/input.txt --output data/output
```

### Command Options

```bash
python -m weave <input_file> [OPTIONS]

Arguments:
  input                  Path to input text file

Options:
  --output, -o PATH      Output folder (default: data/output)
  --max-workers N        Concurrent LLM workers (default: 4)
  -h, --help             Show help message
```

### Example

```bash
# Process a file with default settings
python -m weave data/samples/chatgpt_dump.txt

# Specify custom output directory and worker count
python -m weave data/samples/input.txt --output ./cleaned --max-workers 8
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Configurable Settings

Most settings can be modified in `weave/config.py`:

- **LLM Settings**: Model, temperature, max tokens, retry attempts
- **Parsing Settings**: Regex patterns for block splitting and noise detection
- **Deduplication**: Similarity threshold for near-duplicate detection
- **Date Formats**: Output filename and header date formatting
- **Default Paths**: Output directory and worker count defaults

## How It Works

1. **Parsing**: Splits raw text into blocks using separator patterns (default: `---`)
2. **Noise Removal**: Filters out OCR artifacts, headers, and ChatGPT UI elements
3. **LLM Cleaning**: Sends each block to OpenAI GPT-4o for intelligent cleaning:
   - Fixes OCR errors
   - Improves punctuation and spacing
   - Formats Markdown properly
   - Adds descriptive subheadings
4. **Deduplication**: Removes duplicate or near-duplicate paragraphs (96% similarity threshold)
5. **Writing**: Groups cleaned blocks by date and writes one Markdown file per day

## Project Structure

```
NoteWeaver/
├── README.md
├── .env.example              # Environment variables template
├── .gitignore
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Package metadata and entry points
│
├── data/
│   ├── samples/             # Sample input files
│   └── output/              # Generated Markdown files (gitignored)
│
├── src/                     # Source package (src-layout)
│   └── weave/               # Main package
│       ├── __init__.py
│       ├── __main__.py      # Enables: python -m weave
│       ├── cli.py           # Command-line interface
│       ├── config.py        # Configuration constants
│       ├── pipeline.py      # Main pipeline orchestration
│       ├── parsing.py       # Text parsing and block extraction
│       ├── cleaning.py      # LLM-based text cleaning
│       ├── dedup.py         # Duplicate detection and removal
│       └── writing.py       # Markdown file writing
│
└── tests/                   # Test suite
    ├── __init__.py
    └── test_parsing.py
```

## Requirements

- **Python**: 3.8 or higher
- **OpenAI API Key**: Required for LLM text cleaning
- **Dependencies**:
  - `openai>=1.40.0` - OpenAI API client
  - `python-dotenv>=1.0.1` - Environment variable management

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=weave
```

### Project Status

This project is in active development. See `pyproject.toml` for current version.

## License

MIT License 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


---

**Note**: This tool requires an OpenAI API key and will make API calls that may incur costs. Monitor your usage and set appropriate rate limits if needed.
