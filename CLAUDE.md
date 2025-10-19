# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This project processes Virginia Standards of Learning (SOL) mathematics documents to create structured datasets for building a quiz and testing application. The source documents are Word files (.docx) containing approved mathematics standards and instructional guides across various grade levels and subjects.

## Document Organization

The repository contains two types of SOL documents:

1. **Approved Math SOL Standards** (numbered format: `#-Subject-2023-Approved-Math-SOL.docx`)
   - Grades 1-8: `1-2023-Approved-Math-SOL.docx` through `8-2023-Approved-Math-SOL.docx`
   - High school subjects: Algebra 1 (9), Geometry (10), AFDA (11), Algebra 2 (12), Trigonometry (13), Computational Mathematics (14), Probability & Statistics (15), Discrete Mathematics (16), Mathematical Analysis (17), Data Science (18)

2. **Instructional Guides** (format: `#. Grade # Mathematics Instructional Guide.docx`)
   - Available for Grades 1-8 and Algebra 2

3. **Understanding the Standards** documents
   - Available for high school subjects (AFDA, Trigonometry, Computational Math, etc.)

## Repository Structure

```
SOL_Formatter/
├── sol_formatter/            # Python package for document processing
│   ├── __init__.py          # Package initialization
│   ├── parser.py            # SOLParser class for .docx parsing
│   ├── openai_extractor.py  # OpenAI integration
│   ├── schema.py            # Data structure definitions
│   └── sol_documents/       # Source SOL documents + output
│       ├── *.docx           # Source documents (various formats)
│       └── output/          # Processed JSON/CSV files (created on first run)
├── batch_process.py         # CLI script for basic batch processing
├── batch_process_openai.py  # CLI script for OpenAI extraction
├── app.py                   # Streamlit web interface
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md
```

## Setup and Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or create a virtual environment first (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Common Commands

### Basic Batch Processing
Process all .docx files in the current directory (basic regex extraction):
```bash
python batch_process.py
```

Process files from a specific directory:
```bash
python batch_process.py --input-dir path/to/documents --output-dir path/to/output
```

### OpenAI-Powered Structured Extraction (Recommended for Quiz Generation)
Process documents with AI-powered structured extraction:
```bash
# Set your OpenAI API key
export OPENAI_API_KEY=sk-your-key-here  # macOS/Linux
set OPENAI_API_KEY=sk-your-key-here     # Windows

# Process all documents
python batch_process_openai.py

# Use higher quality model (more expensive)
python batch_process_openai.py --model gpt-4o

# Pass API key as parameter
python batch_process_openai.py --api-key sk-your-key-here

# Save raw text files for debugging
python batch_process_openai.py --save-raw-text
```

**Cost Estimates:**
- `gpt-4o-mini`: ~$0.01-0.05 per document (recommended)
- `gpt-4o`: ~$0.10-0.30 per document (higher quality)

### Streamlit Web Interface
Launch the local web application for uploading and processing documents:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` where you can:
- Toggle between basic extraction and OpenAI-powered structured extraction
- Upload single or multiple .docx files via drag-and-drop
- View extracted standards in interactive tables
- Filter by grade level, strand, or cognitive level
- Export results as JSON or CSV (detailed format with all objectives)
- Preview complete document structure
- Track API token usage and costs

## Architecture

### SOLParser (`sol_formatter/parser.py`)
Basic parsing engine for quick extraction:
- Reads .docx files using `python-docx`
- Extracts metadata from filenames (grade level, subject, document type)
- Parses document content (paragraphs, tables, styles)
- Identifies SOL standard identifiers using regex patterns
- Exports data to JSON and CSV formats

**Use case:** Quick scanning and basic extraction when AI processing is not needed

### OpenAIExtractor (`sol_formatter/openai_extractor.py`)
AI-powered structured extraction for quiz generation:
- Extracts complete document text from .docx files
- Sends to OpenAI API with detailed extraction prompt
- Returns structured JSON following defined schema
- Validates output against schema requirements
- Tracks token usage and costs

Key methods:
- `extract_structured_data(file_path)` - Main extraction entry point
- `extract_batch(file_paths)` - Process multiple documents
- `extract_text_from_docx(file_path)` - Extract raw text with formatting hints
- `validate_output(data)` - Validate against schema

**Use case:** Primary method for creating quiz-ready datasets

### Schema Definition (`sol_formatter/schema.py`)
Defines the target structure for extracted data:
- `EXTRACTION_SCHEMA` - JSON schema for validation
- `OPENAI_EXTRACTION_PROMPT` - Detailed instructions for OpenAI
- `EXAMPLE_OUTPUT` - Reference example of expected output

**Key extracted fields:**
- Document metadata (grade, year, course)
- Content strands (domains like Number Sense, Algebra, etc.)
- Standards with unique IDs
- Knowledge & skills (specific learning objectives)
- Action verbs, examples, constraints
- Tags, cognitive levels, suggested question types

### Batch Processing Scripts
**`batch_process.py`** - Basic regex-based extraction
**`batch_process_openai.py`** - OpenAI-powered extraction (recommended)

Both scripts:
- Scan directories for .docx files
- Process each document
- Save individual and combined output files
- Provide progress feedback and error handling

### Streamlit App (`app.py`)
Web-based interface supporting both processing methods:
- Toggle between basic and OpenAI extraction
- File upload with drag-and-drop
- Real-time progress tracking
- Interactive filtering by grade, strand, cognitive level
- Multiple export formats (JSON, CSV)
- Token usage tracking for cost monitoring
- Complete structure preview

## Output Formats

### OpenAI Structured Output (Recommended for Quiz Generation)
```json
{
  "document_metadata": {
    "title": "Mathematics Standards of Learning for Virginia Public Schools",
    "grade_level": "Grade 1",
    "course_name": "Mathematics",
    "year": "2023",
    "state": "Virginia"
  },
  "introduction": "Overview text explaining grade level focus...",
  "strands": [
    {
      "strand_code": "NS",
      "strand_name": "Number and Number Sense",
      "standards": [
        {
          "standard_id": "1.NS.1",
          "standard_statement": "The student will utilize flexible counting strategies...",
          "knowledge_and_skills": [
            {
              "objective_text": "Count forward by ones to 120, starting at any number.",
              "sub_objectives": [],
              "action_verb": "count",
              "examples": [],
              "constraints": ["up to 120", "by ones"]
            }
          ],
          "tags": ["counting", "number_sense", "sequences"],
          "cognitive_level": "apply",
          "suggested_question_types": ["multiple_choice", "fill_in_blank"]
        }
      ]
    }
  ],
  "_extraction_metadata": {
    "model": "gpt-4o-mini",
    "tokens_used": 8542
  }
}
```

### Basic Extraction Output
```json
{
  "metadata": {
    "type": "Approved SOL Standards",
    "number": "5",
    "grade_level": "Grade 5"
  },
  "content": {
    "paragraphs": [...],
    "identified_standards": ["5.1", "5.2a", "5.3"],
    "total_paragraphs": 120
  }
}
```

### CSV Exports
**Basic CSV:** Standard, Source File, Document Type, Grade Level, Subject

**Detailed CSV (OpenAI):** Standard ID, Standard Statement, Strand Code, Strand Name, Grade Level, Objective, Action Verb, Examples, Constraints, Cognitive Level, Tags

## Data Structure for Quiz Generation

The OpenAI extraction produces a hierarchical structure optimized for quiz apps:

1. **Document Level:** Metadata about grade/course
2. **Strand Level:** Major content domains (Number Sense, Algebra, etc.)
3. **Standard Level:** Individual SOL standards with IDs
4. **Objective Level:** Specific learning objectives with:
   - Action verbs (identify what type of question to ask)
   - Examples (provide sample content for questions)
   - Constraints (numerical limits for problem generation)
   - Cognitive levels (difficulty classification)
   - Question type suggestions (multiple choice, problem solving, etc.)

This structure allows quiz generation to:
- Select standards by grade level and strand
- Generate questions based on action verbs and cognitive levels
- Use constraints to create appropriate difficulty
- Tag questions for progress tracking
- Provide variety through suggested question types

## Notes for Development

- **Primary method:** Use OpenAI extraction for production quiz datasets
- **Basic extraction:** Use for quick scanning or when API costs are a concern
- All source documents are Word files (.docx) processed via `python-docx`
- SOL documents follow consistent structure: Introduction → Strands → Standards → Knowledge & Skills
- The OpenAI prompt is engineered to extract quiz-relevant details (action verbs, examples, constraints)
- Validate all extracted data before using in production
- Consider caching extracted results to avoid re-processing documents
