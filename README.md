# SOL_Formatter

Virginia Standards of Learning (SOL) document processor with OpenAI-powered structured extraction for quiz generation.

## Overview

This project processes Virginia SOL mathematics documents (.docx) and extracts structured, quiz-ready data using OpenAI's API. The output includes standards, learning objectives, action verbs, constraints, examples, and suggested question types - everything needed to build an educational quiz and testing application.

## Features

- 🤖 **OpenAI-Powered Extraction**: Intelligent parsing of unstructured SOL documents
- 📊 **Structured Output**: Hierarchical JSON format optimized for quiz generation
- 🎯 **Quiz-Ready Data**: Action verbs, constraints, examples, cognitive levels
- 🖥️ **Dual Interface**: Command-line batch processing + Streamlit web UI
- 📈 **Progress Tracking**: Real-time processing feedback and token usage
- 💾 **Multiple Formats**: Export as JSON or detailed CSV

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
copy .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 3. Process documents
python batch_process_openai.py

# Or use web interface
streamlit run app.py
```

**Output**: Single consolidated JSON file with all standards and objectives
**Location**: `sol_formatter/sol_documents/output/all_structured_documents.json`

## Documentation

- [📖 Quick Start Guide](QUICK_START.md) - Get running in 5 minutes
- [⚙️ Setup Instructions](SETUP.md) - Detailed setup and troubleshooting
- [📋 Extraction Guide](EXTRACTION_GUIDE.md) - What data is extracted and why
- [💾 Output Formats](OUTPUT_FORMATS.md) - How to use the consolidated data
- [🏗️ Architecture](CLAUDE.md) - Complete system documentation

## What Gets Extracted

For each standard, the system extracts:

- **Standard ID** (e.g., "1.NS.1", "A.EO.1")
- **Standard Statement** (the main requirement)
- **Learning Objectives** (specific skills)
  - Action verb (identify, solve, compare, etc.)
  - Examples from document
  - Constraints (numerical limits, ranges)
  - Sub-objectives
- **Tags** (keywords for filtering)
- **Cognitive Level** (Bloom's taxonomy)
- **Suggested Question Types** (multiple choice, problem solving, etc.)

## Example Output

```json
{
  "standard_id": "1.NS.2",
  "standard_statement": "The student will identify, represent, compare, and order whole numbers up to 120.",
  "knowledge_and_skills": [
    {
      "objective_text": "Identify the place and value of each digit in a two-digit or three-digit number.",
      "action_verb": "identify",
      "examples": ["in 352, the 5 is in the tens place and has a value of 50"],
      "constraints": ["two-digit or three-digit number"]
    }
  ],
  "tags": ["place_value", "number_representation"],
  "cognitive_level": "understand",
  "suggested_question_types": ["multiple_choice", "matching"]
}
```

## Cost

Processing all 31 SOL documents:
- **gpt-4o-mini**: ~$0.50-1.50 (recommended)
- **gpt-4o**: ~$3-10 (higher quality)

## Requirements

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- See [requirements.txt](requirements.txt) for package dependencies

## Project Structure

```
SOL_Formatter/
├── sol_formatter/              # Core processing package
│   ├── parser.py              # Basic document parser
│   ├── openai_extractor.py    # OpenAI integration
│   └── schema.py              # Data structure definitions
├── batch_process_openai.py    # CLI batch processor
├── app.py                     # Streamlit web interface
├── requirements.txt           # Python dependencies
└── .env.example              # Environment variable template
```

## Support

For issues or questions, see the documentation files or check the OpenAI API documentation at https://platform.openai.com/docs
