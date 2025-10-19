# SOL Document Extraction Guide

## What Information to Extract for Quiz Generation

This guide explains what data should be extracted from Virginia SOL documents to create an effective quiz and testing application.

## Document Structure Analysis

Virginia SOL documents follow a consistent hierarchical structure:

```
Document
├── Title & Grade Level
├── Introduction/Overview
└── Content Strands (Major Domains)
    └── Standards (Individual SOL Requirements)
        └── Knowledge and Skills (Specific Objectives)
```

## Essential Fields to Extract

### 1. Document Metadata
**Purpose:** Categorize and filter content appropriately

```json
{
  "title": "Mathematics Standards of Learning for Virginia Public Schools",
  "grade_level": "Grade 1",
  "course_name": "Mathematics",
  "year": "2023",
  "state": "Virginia"
}
```

**Why it matters:** Ensures quizzes are appropriate for the student's grade level

### 2. Introduction Text
**Purpose:** Provides context about the grade level's focus

```json
{
  "introduction": "In Grade 1, instructional time focuses on developing an understanding of addition, subtraction, place value, and linear measurement..."
}
```

**Why it matters:** Helps explain the "big picture" to students and teachers

### 3. Content Strands
**Purpose:** Organize standards by mathematical domain

```json
{
  "strand_code": "NS",
  "strand_name": "Number and Number Sense",
  "strand_description": "Optional introductory text"
}
```

**Examples by Grade Level:**
- Elementary (K-5): Number Sense (NS), Computation (CE), Measurement & Geometry (MG), Probability & Statistics (PS), Patterns & Algebra (PFA)
- High School: Expressions & Operations (EO), Equations & Inequalities (EI), Functions (F), Statistics (ST)

**Why it matters:** Allows quiz filtering by content area (e.g., "Give me geometry questions")

### 4. Standards
**Purpose:** The actual learning requirements

```json
{
  "standard_id": "1.NS.1",
  "standard_statement": "The student will utilize flexible counting strategies to determine and describe quantities up to 120."
}
```

**Standard ID Format:**
- Elementary: `[Grade].[Strand].[Number]` (e.g., `1.NS.1`)
- High School: `[Course Code].[Strand].[Number]` (e.g., `A.EO.1` for Algebra 1)

**Why it matters:** Direct mapping to curriculum requirements for progress tracking

### 5. Knowledge and Skills (Learning Objectives)
**Purpose:** The specific skills that can be turned into quiz questions

```json
{
  "objective_text": "Count forward by ones to 120, starting at any number.",
  "sub_objectives": [],
  "action_verb": "count",
  "examples": [],
  "constraints": ["up to 120", "by ones"]
}
```

**Critical Components:**

#### Action Verbs
The first word of each objective indicates the type of assessment needed:
- **identify, recognize, name** → Multiple choice, matching
- **solve, calculate, compute** → Problem-solving, computational
- **compare, contrast, order** → Comparison questions, ranking
- **represent, model, illustrate** → Visual/graphical questions
- **explain, describe, justify** → Short answer, explanation
- **determine, find, estimate** → Problem-solving

#### Examples
Parenthetical examples provide concrete instances:
- "(e.g., pictorial, concrete, symbolic)" → Use these in question stems
- "(e.g., place value mats, base-10 blocks)" → Specify tools for questions
- "(e.g., skip counting by fives and tens)" → Sample question content

#### Constraints
Numerical limits and ranges for appropriate difficulty:
- "within 20" → Questions should use numbers ≤ 20
- "up to 120 objects" → Maximum quantity for counting questions
- "two-digit and three-digit numbers" → Range specification
- "using grids or coordinate planes limited to quadrant I" → Scope limitation

**Why it matters:** Directly translates to quiz question generation parameters

### 6. Tags (Derived)
**Purpose:** Keyword-based filtering and search

```json
{
  "tags": ["counting", "number_sense", "skip_counting", "sequences"]
}
```

**How to generate:**
- Extract key mathematical concepts from standard and objectives
- Include mathematical operations mentioned
- Add common educational terms
- Include tools or representations mentioned

**Why it matters:** Enables searching like "show me all addition questions" or "fractions practice"

### 7. Cognitive Level (Derived)
**Purpose:** Difficulty classification based on Bloom's Taxonomy

```json
{
  "cognitive_level": "apply"
}
```

**Levels:**
- **remember:** Recall facts, definitions (lowest complexity)
- **understand:** Explain concepts, summarize
- **apply:** Use in new situations, solve problems
- **analyze:** Break down, examine relationships
- **evaluate:** Judge, critique, defend
- **create:** Design, construct, produce (highest complexity)

**Mapping Guide:**
- "identify", "recall", "recognize" → remember
- "explain", "describe", "summarize" → understand
- "solve", "calculate", "model" → apply
- "compare", "contrast", "analyze" → analyze
- "justify", "evaluate", "critique" → evaluate
- "create", "design", "develop" → create

**Why it matters:** Adjust quiz difficulty, scaffold learning, track mastery progression

### 8. Suggested Question Types (Derived)
**Purpose:** Guide quiz generation on appropriate formats

```json
{
  "suggested_question_types": ["multiple_choice", "fill_in_blank", "problem_solving"]
}
```

**Question Type Options:**
- `multiple_choice` - Select from options
- `true_false` - Binary verification
- `fill_in_blank` - Complete the statement
- `short_answer` - Brief written response
- `problem_solving` - Multi-step solution
- `matching` - Connect related items
- `graphical` - Plot, draw, or interpret visuals
- `computational` - Calculate a numerical answer

**Why it matters:** Provides variety and matches assessment to skill type

## Example: Complete Extraction

**Source Text:**
> **1.NS.2** The student will identify, represent, compare, and order whole numbers up to 120.
>
> Students will demonstrate the following Knowledge and Skills:
> - Identify the place and value of each digit in a two-digit or three-digit number (e.g., in 352, the 5 is in the tens place and has a value of 50).
> - Use place value understanding to compare and order whole numbers within 100.
> - Represent numbers using concrete objects, pictures, and numerals (e.g., base-10 blocks, place value mats).

**Extracted Structure:**
```json
{
  "standard_id": "1.NS.2",
  "standard_statement": "The student will identify, represent, compare, and order whole numbers up to 120.",
  "knowledge_and_skills": [
    {
      "objective_text": "Identify the place and value of each digit in a two-digit or three-digit number.",
      "sub_objectives": [],
      "action_verb": "identify",
      "examples": ["in 352, the 5 is in the tens place and has a value of 50"],
      "constraints": ["two-digit or three-digit number"]
    },
    {
      "objective_text": "Use place value understanding to compare and order whole numbers within 100.",
      "sub_objectives": [],
      "action_verb": "use",
      "examples": [],
      "constraints": ["within 100"]
    },
    {
      "objective_text": "Represent numbers using concrete objects, pictures, and numerals.",
      "sub_objectives": [],
      "action_verb": "represent",
      "examples": ["base-10 blocks", "place value mats"],
      "constraints": []
    }
  ],
  "tags": ["place_value", "number_representation", "comparing_numbers", "ordering_numbers", "whole_numbers"],
  "cognitive_level": "understand",
  "suggested_question_types": ["multiple_choice", "matching", "graphical", "short_answer"]
}
```

## How This Enables Quiz Generation

### Example 1: Multiple Choice Question
Using objective: "Identify the place and value of each digit in a two-digit or three-digit number"
- **Action verb** "identify" → multiple choice format
- **Constraint** "two-digit or three-digit" → use numbers like 47 or 352
- **Example** from text → model question after "the 5 in 352"

**Generated Question:**
> In the number 284, what is the value of the digit 8?
> A) 8  B) 80  C) 800  D) 8,000

### Example 2: Problem-Solving Question
Using objective: "Use place value understanding to compare and order whole numbers within 100"
- **Action verb** "order" → sorting/ranking question
- **Constraint** "within 100" → use numbers ≤ 100
- **Cognitive level** "understand" → requires conceptual understanding

**Generated Question:**
> Order these numbers from least to greatest: 67, 42, 89, 51

### Example 3: Graphical Question
Using objective: "Represent numbers using concrete objects, pictures, and numerals"
- **Action verb** "represent" → visual representation
- **Examples** "base-10 blocks" → use in question
- **Question type** "graphical" → show/draw representation

**Generated Question:**
> Draw base-10 blocks to represent the number 34.

## Summary: Why Each Field Matters

| Field | Purpose | Quiz Application |
|-------|---------|------------------|
| Standard ID | Curriculum alignment | Track student progress against standards |
| Standard Statement | Overall goal | Provide context for question sets |
| Action Verb | Question format | Determine how to assess (select, solve, explain) |
| Examples | Question content | Model questions after provided examples |
| Constraints | Difficulty parameters | Ensure age-appropriate problem difficulty |
| Tags | Categorization | Filter and search questions |
| Cognitive Level | Complexity | Adjust difficulty, scaffold learning |
| Question Types | Format variety | Provide diverse assessment methods |

## Implementation Recommendation

The OpenAI extraction (`batch_process_openai.py` or Streamlit app with OpenAI enabled) is **strongly recommended** because:

1. **Unstructured text handling:** SOL documents vary in formatting and don't always follow rigid patterns
2. **Context understanding:** AI can infer action verbs, examples, and constraints from natural language
3. **Semantic extraction:** Can identify concepts even when worded differently
4. **Relationship mapping:** Understands hierarchy and how objectives relate to standards
5. **Automated tagging:** Generates relevant keywords without manual classification

The structured output is immediately usable for quiz generation without additional processing.
