"""JSON schema and data models for structured SOL output"""

# This defines the target structure for OpenAI to extract from SOL documents

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "document_metadata": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Full document title"},
                "grade_level": {"type": "string", "description": "Grade level (e.g., 'Grade 1', 'Algebra 1')"},
                "course_name": {"type": "string", "description": "Course or subject name"},
                "year": {"type": "string", "description": "Year of standards (e.g., '2023')"},
                "state": {"type": "string", "default": "Virginia"}
            },
            "required": ["title", "grade_level", "year"]
        },
        "introduction": {
            "type": "string",
            "description": "Overview text explaining the grade level focus and approach"
        },
        "strands": {
            "type": "array",
            "description": "Major content areas/domains",
            "items": {
                "type": "object",
                "properties": {
                    "strand_code": {
                        "type": "string",
                        "description": "Abbreviated code (e.g., 'NS', 'CE', 'EO', 'F')"
                    },
                    "strand_name": {
                        "type": "string",
                        "description": "Full strand name (e.g., 'Number and Number Sense', 'Functions')"
                    },
                    "strand_description": {
                        "type": "string",
                        "description": "Optional description or introduction to the strand"
                    },
                    "standards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "standard_id": {
                                    "type": "string",
                                    "description": "Unique identifier (e.g., '1.NS.1', 'A.EO.1')"
                                },
                                "standard_statement": {
                                    "type": "string",
                                    "description": "The main standard statement"
                                },
                                "knowledge_and_skills": {
                                    "type": "array",
                                    "description": "Specific learning objectives",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "objective_text": {
                                                "type": "string",
                                                "description": "The main objective statement"
                                            },
                                            "sub_objectives": {
                                                "type": "array",
                                                "description": "Sub-bullets or additional details",
                                                "items": {"type": "string"}
                                            },
                                            "action_verb": {
                                                "type": "string",
                                                "description": "Primary action verb (identify, solve, represent, etc.)"
                                            },
                                            "examples": {
                                                "type": "array",
                                                "description": "Examples mentioned in parentheses",
                                                "items": {"type": "string"}
                                            },
                                            "constraints": {
                                                "type": "array",
                                                "description": "Numerical limits or ranges (e.g., 'within 20', 'up to 120')",
                                                "items": {"type": "string"}
                                            }
                                        },
                                        "required": ["objective_text"]
                                    }
                                },
                                "tags": {
                                    "type": "array",
                                    "description": "Keywords for categorization",
                                    "items": {"type": "string"}
                                },
                                "cognitive_level": {
                                    "type": "string",
                                    "description": "Bloom's taxonomy level",
                                    "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"]
                                },
                                "suggested_question_types": {
                                    "type": "array",
                                    "description": "Question formats based on objectives",
                                    "items": {
                                        "type": "string",
                                        "enum": ["multiple_choice", "true_false", "short_answer",
                                                "problem_solving", "matching", "fill_in_blank",
                                                "graphical", "computational"]
                                    }
                                }
                            },
                            "required": ["standard_id", "standard_statement", "knowledge_and_skills"]
                        }
                    }
                },
                "required": ["strand_code", "strand_name", "standards"]
            }
        }
    },
    "required": ["document_metadata", "strands"]
}


# Example output for reference
EXAMPLE_OUTPUT = {
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
            "strand_description": "Optional strand introduction",
            "standards": [
                {
                    "standard_id": "1.NS.1",
                    "standard_statement": "The student will utilize flexible counting strategies to determine and describe quantities up to 120.",
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
                        },
                        {
                            "objective_text": "Count forward and backward by tens to 120 from a given multiple of ten.",
                            "sub_objectives": [],
                            "action_verb": "count",
                            "examples": [],
                            "constraints": ["to 120", "by tens", "from multiple of ten"]
                        }
                    ],
                    "tags": ["counting", "number_sense", "skip_counting", "sequences"],
                    "cognitive_level": "apply",
                    "suggested_question_types": ["multiple_choice", "fill_in_blank", "short_answer"]
                }
            ]
        }
    ]
}


# OpenAI prompt template for extraction
OPENAI_EXTRACTION_PROMPT = """You are analyzing a Virginia Standards of Learning (SOL) mathematics document.

Extract the content into a structured JSON format following this schema:

DOCUMENT STRUCTURE:
- The document contains a title and grade level at the top
- An introduction/overview section explains the focus of the grade level
- Content is organized into STRANDS (major mathematical domains)
- Each strand contains multiple STANDARDS
- Each standard has a unique ID (like "1.NS.1" or "A.EO.1")
- Each standard has a statement describing what students will learn
- Under each standard is a "Knowledge and Skills" section with specific learning objectives
- Objectives are bullet points that detail specific skills students should demonstrate

EXTRACTION GUIDELINES:

1. **Document Metadata**: Extract title, grade level, course name, and year (2023)

2. **Introduction**: Capture the overview paragraph(s) at the beginning

3. **Strands**: Identify each major section/strand
   - Extract strand codes (NS, CE, MG, PS, PFA for elementary; EO, EI, F, ST for high school)
   - Extract full strand names

4. **Standards**: For each standard:
   - Extract the standard ID (e.g., "1.NS.1")
   - Extract the complete standard statement

5. **Knowledge and Skills**: For each objective under a standard:
   - Extract the main objective text
   - Extract any sub-bullets as sub_objectives
   - Identify the primary ACTION VERB (first word: identify, solve, count, represent, etc.)
   - Extract EXAMPLES from parentheses (e.g., if it says "various representations (e.g., pictorial, concrete)", extract ["pictorial", "concrete"])
   - Extract CONSTRAINTS - any numerical limits or ranges mentioned (e.g., "within 20", "up to 120 objects")

6. **Tags**: Generate relevant keyword tags based on the content (e.g., "addition", "fractions", "measurement", "algebra")

7. **Cognitive Level**: Classify based on Bloom's taxonomy:
   - "remember" - recall facts
   - "understand" - explain concepts
   - "apply" - use in new situations
   - "analyze" - break down and examine
   - "evaluate" - judge or critique
   - "create" - produce something new

8. **Suggested Question Types**: Based on action verbs, suggest appropriate quiz formats:
   - "identify", "recognize" → multiple_choice, matching
   - "solve", "calculate" → problem_solving, computational
   - "compare", "contrast" → matching, short_answer
   - "represent", "model" → graphical, short_answer
   - "explain", "describe" → short_answer
   - True/false for verification questions

Return ONLY valid JSON matching the schema. Be thorough and capture all standards and objectives."""
