# Directory Structure

This document explains the updated directory structure for the SOL_Formatter project.

## Current Structure

```
SOL_Formatter/
│
├── sol_formatter/                    # Main Python package
│   ├── __init__.py                  # Package initialization
│   ├── parser.py                    # Basic document parser (regex-based)
│   ├── openai_extractor.py          # OpenAI-powered structured extraction
│   ├── schema.py                    # JSON schema and extraction prompt
│   │
│   └── sol_documents/               # Documents directory
│       ├── *.docx                   # SOURCE: Original SOL documents
│       │                            # - Approved Math SOL Standards
│       │                            # - Instructional Guides
│       │                            # - Understanding the Standards docs
│       │
│       └── output/                  # OUTPUT: Generated files (created on first run)
│           ├── *_structured.json    # Individual document extractions
│           ├── *_standards.csv      # Per-document CSV exports
│           ├── all_structured_documents.json  # MAIN OUTPUT: All docs combined
│           └── all_standards.csv    # Combined CSV of all standards
│
├── batch_process.py                 # CLI: Basic batch processing
├── batch_process_openai.py          # CLI: OpenAI-powered batch processing
├── app.py                           # Streamlit web interface
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .env                            # Your environment variables (git-ignored)
├── .gitignore                      # Git ignore rules
│
└── Documentation/
    ├── README.md                    # Project overview
    ├── QUICK_START.md              # 5-minute quick start
    ├── SETUP.md                    # Detailed setup instructions
    ├── EXTRACTION_GUIDE.md         # What data is extracted and why
    ├── OUTPUT_FORMATS.md           # How to use the output data
    ├── CLAUDE.md                   # Architecture documentation
    └── DIRECTORY_STRUCTURE.md      # This file
```

## Key Directories

### Source Documents: `sol_formatter/sol_documents/`
- **Purpose**: Store original SOL .docx files
- **Contents**: All Virginia SOL mathematics documents (31 files)
- **When to use**: Place new SOL documents here to process them

### Output Directory: `sol_formatter/sol_documents/output/`
- **Purpose**: Store all processed/extracted data
- **Created**: Automatically on first script run
- **Contents**:
  - Individual JSON files per document
  - Combined JSON with all documents
  - CSV exports
- **When to use**: Read from here to access processed data

## File Naming Conventions

### Source Files (Input)
Located in: `sol_formatter/sol_documents/`

```
1-2023-Approved-Math-SOL.docx              # Grade 1
2-2023-Approved-Math-SOL.docx              # Grade 2
9-Alg1-2023-Approved-Math-SOL.docx         # Algebra 1
10-Geo-2023-Approved-Math-SOL.docx         # Geometry
1. Grade 1 Mathematics Instructional Guide.docx
12-AFDA-Understanding the Standards.docx
```

### Output Files (Generated)
Located in: `sol_formatter/sol_documents/output/`

```
1-2023-Approved-Math-SOL_structured.json           # Individual extraction
2-2023-Approved-Math-SOL_structured.json
9-Alg1-2023-Approved-Math-SOL_structured.json

all_structured_documents.json                      # Main consolidated file
all_standards.csv                                  # All standards in CSV
```

## Command Line Paths

All scripts now use the new structure by default:

### Process all documents
```bash
# Default: reads from sol_formatter/sol_documents/
#          writes to sol_formatter/sol_documents/output/
python batch_process_openai.py
```

### Custom directories
```bash
# Specify different directories if needed
python batch_process_openai.py \
  --input-dir path/to/your/documents \
  --output-dir path/to/your/output
```

## Accessing Output Data

### Python Code
```python
import json

# Load the main consolidated file
with open('sol_formatter/sol_documents/output/all_structured_documents.json') as f:
    data = json.load(f)

# Now you have all 31 documents in one structure
documents = data['documents']
```

### File Paths in Scripts
- **Input (source docs)**: `sol_formatter/sol_documents/`
- **Output (processed)**: `sol_formatter/sol_documents/output/`

## Why This Structure?

### Benefits:
1. **Clear Separation**: Source and output are clearly separated
2. **Git-Friendly**: Easy to commit source docs, ignore output
3. **Self-Contained**: Everything under `sol_formatter/` package
4. **Organized**: Output directory prevents clutter
5. **Scalable**: Easy to add more document types

### Migration from Old Structure:
If you had documents in the root directory:
- **Before**: Documents in project root
- **After**: Documents in `sol_formatter/sol_documents/`
- Scripts automatically updated to use new paths

## .gitignore Configuration

By default, the `.gitignore` is configured to:
- ✅ Commit source .docx files
- ✅ Commit all Python code
- ❌ Ignore .env (API keys)
- ⚠️ Optionally ignore output files (uncomment in .gitignore)

To ignore processed output files:
```bash
# Uncomment these lines in .gitignore:
sol_formatter/sol_documents/output/*.json
sol_formatter/sol_documents/output/*.csv
sol_formatter/sol_documents/output/*.txt
```

## Environment Variables

The `.env` file now reflects the updated paths:

```bash
# Where source documents are stored
INPUT_DIR=sol_formatter/sol_documents

# Where processed output should go
OUTPUT_DIR=sol_formatter/sol_documents/output
```

## Notes

- The `output/` directory will be created automatically on first run
- You can safely delete the `output/` directory to reprocess all documents
- Individual document JSON files are useful for debugging
- The main file `all_structured_documents.json` is what you'll use for your quiz app
