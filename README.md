# Instructor Library Examples

A collection of examples and tutorials demonstrating how to use the Instructor library with OpenAI's GPT models for structured data extraction and validation.

## Overview

This repository contains practical examples of using Instructor to:
- Extract structured data from text using Pydantic models
- Validate fields and add custom validation rules
- Handle nested data structures
- Implement dynamic prompting
- Route responses based on intent classification
- Work with recursive schemas

## Getting Started

1. Clone this repository
2. Install dependencies and create venv:
```bash
uv sync
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_key_here
```

## Examples

### Basic Usage
- [basics.py](basics.py): Core concepts including data extraction, field validation, and nested models
- [beyond_basics.py](beyond_basics.py): Advanced patterns like dynamic prompting and intent-based routing
### Application Examples
- [Recursive Schemas](examples/01_recursive_schema.py): Handling nested comment trees
- [Classification with Chain of Thought](examples/02_single_classification_with_cot.py): Spam detection with reasoning

## Key Features Demonstrated

- 🔍 Structured data extraction
- ✅ Field validation and custom validators
- 🌳 Nested data handling
- 🔄 Dynamic prompting
- 🔀 Intent-based routing
- 🌿 Recursive schemas
- 💭 Chain of thought reasoning

## Requirements
- Python ≥3.13
- OpenAI API key
- Instructor ≥1.7.2

## License
MIT
