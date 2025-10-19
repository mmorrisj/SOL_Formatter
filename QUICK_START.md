# Quick Start Guide

Get up and running in 5 minutes!

## 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

## 2. Set Up OpenAI API Key (1 min)

### Get your key:
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-...`)

### Configure:
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your key:
OPENAI_API_KEY=sk-your-actual-key-here
```

## 3. Process Documents (2 min)

### Option A: Batch Process All Documents
```bash
python batch_process_openai.py
```

Output: `sol_formatter/sol_documents/output/all_structured_documents.json`

### Option B: Web Interface
```bash
streamlit run app.py
```

1. Check "Use OpenAI for Structured Extraction"
2. Upload .docx files
3. Click "Process Documents"
4. Download JSON/CSV

## 4. Use the Data (1 min)

```python
import json

# Load all processed data
with open('sol_formatter/sol_documents/output/all_structured_documents.json') as f:
    data = json.load(f)

# Get all documents
documents = data['documents']

# Filter by grade
grade_3 = [d for d in documents
           if d['document_metadata']['grade_level'] == 'Grade 3'][0]

# Get all standards
for strand in grade_3['strands']:
    for standard in strand['standards']:
        print(f"{standard['standard_id']}: {standard['standard_statement']}")
```

## What You Get

### Single Consolidated File
- **File**: `all_structured_documents.json`
- **Contains**: All 31 grade levels/courses
- **Size**: ~800-1000 standards, ~3000-5000 quiz-ready objectives

### Data Structure
```
Documents (31)
└── Strands (5-6 per grade)
    └── Standards (20-40 per grade)
        └── Objectives (2-8 per standard) ← These become quiz questions!
```

### Each Objective Includes
- ✅ Action verb (tells you what type of question)
- ✅ Constraints (numerical limits for difficulty)
- ✅ Examples (sample content)
- ✅ Tags (for filtering)
- ✅ Cognitive level (difficulty classification)
- ✅ Suggested question types

## Cost

**Total for all 31 documents:**
- gpt-4o-mini: ~$0.50-1.50
- gpt-4o: ~$3-10

## Troubleshooting

**Can't find API key?**
```bash
# Check if .env file exists
dir .env

# Make sure it contains:
OPENAI_API_KEY=sk-...
```

**Import error?**
```bash
pip install python-dotenv openai
```

**Need help?**
- See `SETUP.md` for detailed instructions
- See `EXTRACTION_GUIDE.md` for data structure details
- See `OUTPUT_FORMATS.md` for usage examples

## Next Steps

1. ✅ Process your documents
2. 🎯 Build quiz generation logic
3. 🎯 Create student progress tracking
4. 🎯 Deploy your quiz app!
