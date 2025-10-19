# Data Output Formats

This document explains exactly how the extracted SOL data is consolidated and formatted for use in your quiz application.

## Output Files Generated

### Batch Processing with OpenAI

When you run `python batch_process_openai.py`, the following files are created in `sol_formatter/sol_documents/output/`:

```
sol_formatter/sol_documents/
├── *.docx                                             # Source documents
└── output/                                            # Generated output files
    ├── 1-2023-Approved-Math-SOL_structured.json      # Individual document
    ├── 2-2023-Approved-Math-SOL_structured.json      # Individual document
    ├── 9-Alg1-2023-Approved-Math-SOL_structured.json # Individual document
    ├── ...                                            # One file per document
    └── all_structured_documents.json                  # CONSOLIDATED OUTPUT
```

## Primary Consolidated Format: all_structured_documents.json

This is your **main output file** containing all documents in a single JSON structure:

### File Structure

```json
{
  "total_documents": 31,
  "successful": 31,
  "failed": 0,
  "total_tokens_used": 265840,
  "documents": [
    {
      "document_metadata": {
        "title": "Mathematics Standards of Learning for Virginia Public Schools",
        "grade_level": "Grade 1",
        "course_name": "Mathematics",
        "year": "2023",
        "state": "Virginia"
      },
      "introduction": "In Grade 1, instructional time focuses on...",
      "strands": [
        {
          "strand_code": "NS",
          "strand_name": "Number and Number Sense",
          "strand_description": "Optional description",
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
                },
                {
                  "objective_text": "Count backward by ones from 30.",
                  "sub_objectives": [],
                  "action_verb": "count",
                  "examples": [],
                  "constraints": ["from 30", "by ones"]
                }
              ],
              "tags": ["counting", "number_sense", "skip_counting"],
              "cognitive_level": "apply",
              "suggested_question_types": ["multiple_choice", "fill_in_blank"]
            }
          ]
        }
      ],
      "_extraction_metadata": {
        "source_file": "1-2023-Approved-Math-SOL.docx",
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "tokens_used": 8542
      }
    },
    {
      "document_metadata": {
        "title": "Mathematics Standards of Learning for Virginia Public Schools",
        "grade_level": "Grade 2",
        "course_name": "Mathematics",
        "year": "2023"
      },
      "strands": [...],
      "_extraction_metadata": {...}
    }
    // ... continues for all 31 documents
  ]
}
```

## Data Hierarchy

The consolidated file follows this nested structure:

```
all_structured_documents.json
│
├── Metadata (processing summary)
│   ├── total_documents
│   ├── successful/failed counts
│   └── total_tokens_used
│
└── documents[] (array of all processed docs)
    │
    └── [each document]
        ├── document_metadata (grade, year, course)
        ├── introduction (overview text)
        ├── strands[] (content domains)
        │   │
        │   └── [each strand]
        │       ├── strand_code (e.g., "NS", "EO")
        │       ├── strand_name (e.g., "Number and Number Sense")
        │       └── standards[] (individual requirements)
        │           │
        │           └── [each standard]
        │               ├── standard_id (e.g., "1.NS.1")
        │               ├── standard_statement
        │               ├── knowledge_and_skills[] (objectives)
        │               │   │
        │               │   └── [each objective]
        │               │       ├── objective_text
        │               │       ├── action_verb
        │               │       ├── examples[]
        │               │       ├── constraints[]
        │               │       └── sub_objectives[]
        │               │
        │               ├── tags[] (keywords)
        │               ├── cognitive_level (Bloom's)
        │               └── suggested_question_types[]
        │
        └── _extraction_metadata (processing info)
```

## How to Use This Data in Your Quiz App

### Example 1: Load All Standards

```python
import json

# Load consolidated data
with open('sol_formatter/sol_documents/output/all_structured_documents.json', 'r') as f:
    data = json.load(f)

# Access all documents
all_documents = data['documents']

# Iterate through all standards
for doc in all_documents:
    grade = doc['document_metadata']['grade_level']

    for strand in doc['strands']:
        strand_name = strand['strand_name']

        for standard in strand['standards']:
            std_id = standard['standard_id']
            statement = standard['standard_statement']

            print(f"{grade} - {std_id}: {statement}")
```

### Example 2: Filter by Grade Level

```python
# Get all Grade 3 standards
grade_3_docs = [doc for doc in data['documents']
                if doc['document_metadata']['grade_level'] == 'Grade 3']

# Get all objectives for Grade 3
grade_3_objectives = []
for doc in grade_3_docs:
    for strand in doc['strands']:
        for standard in strand['standards']:
            for objective in standard['knowledge_and_skills']:
                grade_3_objectives.append({
                    'standard_id': standard['standard_id'],
                    'objective': objective['objective_text'],
                    'action_verb': objective['action_verb'],
                    'constraints': objective['constraints'],
                    'question_types': standard['suggested_question_types']
                })
```

### Example 3: Generate Quiz Questions by Strand

```python
# Get all "Number Sense" objectives across all grades
number_sense_objectives = []

for doc in data['documents']:
    grade = doc['document_metadata']['grade_level']

    for strand in doc['strands']:
        if strand['strand_code'] == 'NS':  # Number Sense
            for standard in strand['standards']:
                for objective in standard['knowledge_and_skills']:
                    number_sense_objectives.append({
                        'grade': grade,
                        'standard_id': standard['standard_id'],
                        'objective': objective['objective_text'],
                        'action_verb': objective['action_verb'],
                        'examples': objective['examples'],
                        'constraints': objective['constraints'],
                        'tags': standard['tags'],
                        'cognitive_level': standard['cognitive_level']
                    })

# Now you can filter by action verb to determine question type
counting_questions = [obj for obj in number_sense_objectives
                      if obj['action_verb'] == 'count']
```

### Example 4: Build a Quiz Database

```python
import sqlite3

# Create database
conn = sqlite3.connect('sol_quiz.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE standards (
        id INTEGER PRIMARY KEY,
        standard_id TEXT UNIQUE,
        grade_level TEXT,
        strand_name TEXT,
        statement TEXT,
        cognitive_level TEXT
    )
''')

cursor.execute('''
    CREATE TABLE objectives (
        id INTEGER PRIMARY KEY,
        standard_id TEXT,
        objective_text TEXT,
        action_verb TEXT,
        constraints TEXT,
        examples TEXT,
        FOREIGN KEY (standard_id) REFERENCES standards(standard_id)
    )
''')

# Populate from JSON
for doc in data['documents']:
    grade = doc['document_metadata']['grade_level']

    for strand in doc['strands']:
        for standard in strand['standards']:
            # Insert standard
            cursor.execute('''
                INSERT OR IGNORE INTO standards
                (standard_id, grade_level, strand_name, statement, cognitive_level)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                standard['standard_id'],
                grade,
                strand['strand_name'],
                standard['standard_statement'],
                standard.get('cognitive_level')
            ))

            # Insert objectives
            for obj in standard['knowledge_and_skills']:
                cursor.execute('''
                    INSERT INTO objectives
                    (standard_id, objective_text, action_verb, constraints, examples)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    standard['standard_id'],
                    obj['objective_text'],
                    obj.get('action_verb'),
                    '; '.join(obj.get('constraints', [])),
                    '; '.join(obj.get('examples', []))
                ))

conn.commit()
```

## Alternative Format: CSV Export

The Streamlit app also generates detailed CSV files with a flattened structure:

### detailed_standards.csv

One row per objective (most granular):

| Standard ID | Standard Statement | Strand Code | Strand Name | Grade Level | Objective | Action Verb | Examples | Constraints | Cognitive Level | Tags |
|-------------|-------------------|-------------|-------------|-------------|-----------|-------------|----------|-------------|-----------------|------|
| 1.NS.1 | The student will utilize flexible counting... | NS | Number and Number Sense | Grade 1 | Count forward by ones to 120... | count | | up to 120; by ones | apply | counting; number_sense |
| 1.NS.1 | The student will utilize flexible counting... | NS | Number and Number Sense | Grade 1 | Count backward by ones from 30 | count | | from 30; by ones | apply | counting; number_sense |
| 1.NS.2 | The student will identify, represent... | NS | Number and Number Sense | Grade 1 | Identify the place and value... | identify | in 352, the 5 is in tens place | two-digit or three-digit | understand | place_value |

**Use case:** Import into Excel, Google Sheets, or databases for analysis

## Data Statistics

After processing all 31 SOL documents (Grades 1-8 + 10 high school courses), you'll have approximately:

- **31 documents** (grade levels/courses)
- **~150 content strands** (5-6 per document)
- **~800-1000 standards** (unique SOL requirements)
- **~3000-5000 objectives** (specific skills for quiz questions)

## Recommended Data Storage Strategy

### Option 1: Direct JSON Usage (Simple)
- Load `all_structured_documents.json` directly in your app
- Filter and query using Python/JavaScript
- **Pros:** No database setup, easy to inspect
- **Cons:** Slower for large-scale queries

### Option 2: Database (Production)
- Import into SQLite/PostgreSQL/MongoDB
- Create indexes on grade_level, strand_code, tags
- **Pros:** Fast queries, scalable
- **Cons:** Requires database setup

### Option 3: Hybrid (Recommended)
- Keep JSON as source of truth
- Build in-memory index/cache on app startup
- Use pandas DataFrame for filtering
- **Pros:** Fast, flexible, no external database
- **Cons:** Uses memory

## Example: Building an In-Memory Index

```python
import pandas as pd
import json

def load_sol_data():
    """Load and index SOL data for fast querying"""

    with open('sol_formatter/sol_documents/output/all_structured_documents.json') as f:
        data = json.load(f)

    # Flatten to objective level
    records = []
    for doc in data['documents']:
        grade = doc['document_metadata']['grade_level']

        for strand in doc['strands']:
            for standard in strand['standards']:
                for obj in standard['knowledge_and_skills']:
                    records.append({
                        'grade_level': grade,
                        'strand_code': strand['strand_code'],
                        'strand_name': strand['strand_name'],
                        'standard_id': standard['standard_id'],
                        'standard_statement': standard['standard_statement'],
                        'objective': obj['objective_text'],
                        'action_verb': obj.get('action_verb', ''),
                        'constraints': obj.get('constraints', []),
                        'examples': obj.get('examples', []),
                        'cognitive_level': standard.get('cognitive_level', ''),
                        'tags': standard.get('tags', []),
                        'question_types': standard.get('suggested_question_types', [])
                    })

    # Create DataFrame for easy filtering
    df = pd.DataFrame(records)

    return df

# Usage
df = load_sol_data()

# Query examples
grade_3_counting = df[(df['grade_level'] == 'Grade 3') &
                      (df['action_verb'] == 'count')]

algebra_graphing = df[(df['grade_level'] == 'Algebra 1') &
                      (df['strand_name'] == 'Functions')]

easy_questions = df[df['cognitive_level'].isin(['remember', 'understand'])]
```

## Summary

**Your consolidated data format is:**
- **Single JSON file**: `all_structured_documents.json`
- **Hierarchical structure**: Documents → Strands → Standards → Objectives
- **Quiz-ready fields**: Action verbs, constraints, examples, question types
- **Easy to query**: Filter by grade, strand, cognitive level, or tags
- **Production-ready**: Can be loaded directly or imported into a database

The structure is optimized for quiz generation with all the metadata needed to create appropriate, varied, and curriculum-aligned questions!
