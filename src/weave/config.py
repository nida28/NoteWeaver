"""Configuration values for the tidy-md pipeline."""
import re

# Parsing configuration
BLOCK_SPLIT_RE = re.compile(r'(?m)^\s*---\s*$')
TAKEN_RE = re.compile(r'Taken:\s*\[\[(.*?)\]\]', re.S)
TEXT_RE = re.compile(r'Text:\s*\[\[(.*?)\]\]', re.S)

NOISE_PATTERNS = [
    r'^\s*###\s*Screenshot\s*$',
    r'^\s*Taken:\s*\[\[.*?\]\]\s*$',
    r'^\s*Text:\s*$',
    r'^\s*ChatGPT\s*\d+\s*[›>»]?\s*$',
    r'^\s*\d{1,4}\)?\s*$',
]

# LLM cleaning configuration
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 2048
LLM_MAX_RETRIES = 4
LLM_MIN_SLEEP = 0.6
LLM_MAX_SLEEP = 1.2
LLM_BACKOFF_BASE = 2

SYSTEM_PROMPT = (
    "You are a careful copy editor for markdown files. "
    "Fix OCR artifacts, punctuation, and spacing without adding new content. "
    "Begin the cleaned text block with a short descriptive Markdown subheading (####) "
    "summarizing its theme, then continue with the rest of the text. "
    "Remove isolated numeric prefixes (e.g., '4.') unless they belong to a real list. "
    "Preserve paragraph boundaries and meaning."
)

# Deduplication configuration
DEDUP_SIMILARITY_THRESHOLD = 0.96

# Writing configuration
DATE_FORMAT = "%d-%m-%y"
DATE_HEADER_FORMAT = "%d %b %Y"

# Pipeline defaults
DEFAULT_MAX_WORKERS = 4
DEFAULT_OUTPUT_DIR = "data/output"

