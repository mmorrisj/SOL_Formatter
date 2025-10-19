# Setup Guide

This guide will help you set up the SOL Document Processor with OpenAI integration.

## Prerequisites

- Python 3.8 or higher
- OpenAI API account
- Git (optional, for version control)

## Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)
6. **Important:** Save this key securely - you won't be able to see it again

### API Pricing (as of 2024)
- **gpt-4o-mini** (recommended): ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **gpt-4o**: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens

**Estimated cost per SOL document:**
- gpt-4o-mini: $0.01-0.05 per document
- gpt-4o: $0.10-0.30 per document

**Total cost for all 31 documents:**
- gpt-4o-mini: ~$0.50-1.50
- gpt-4o: ~$3-10

## Step 2: Set Up Environment Variables

### Option A: Using .env File (Recommended)

1. Copy the example environment file:
   ```bash
   # Windows
   copy .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```bash
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. Install python-dotenv to load environment variables:
   ```bash
   pip install python-dotenv
   ```

4. The scripts will automatically load the `.env` file

### Option B: System Environment Variables

#### Windows (Command Prompt)
```cmd
set OPENAI_API_KEY=sk-your-actual-key-here
```

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
```

#### macOS/Linux (Bash/Zsh)
```bash
export OPENAI_API_KEY=sk-your-actual-key-here
```

To make it permanent, add the export line to:
- macOS/Linux: `~/.bashrc` or `~/.zshrc`
- Windows: System Environment Variables (Control Panel)

### Option C: Pass as Command Line Argument
```bash
python batch_process_openai.py --api-key sk-your-actual-key-here
```

## Step 3: Install Dependencies

### Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```

### Install Required Packages
```bash
pip install -r requirements.txt
```

This will install:
- `python-docx` - Read .docx files
- `openai` - OpenAI API client
- `streamlit` - Web interface
- `pandas` - Data manipulation
- `openpyxl` - Excel export

## Step 4: Verify Setup

### Test OpenAI Connection

Create a test script `test_setup.py`:
```python
import os
from openai import OpenAI

# Load from .env file
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found!")
    print("Make sure you've set it in .env file or environment variables")
else:
    print(f"✓ API key found: {api_key[:10]}...")

    try:
        client = OpenAI(api_key=api_key)
        # Test API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello, SOL!'"}],
            max_tokens=10
        )
        print(f"✓ OpenAI API connection successful!")
        print(f"  Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
```

Run the test:
```bash
python test_setup.py
```

Expected output:
```
✓ API key found: sk-proj-7...
✓ OpenAI API connection successful!
  Response: Hello, SOL!
```

## Step 5: Process Your First Document

### Test with Single Document
```bash
# Create a test directory with one document
mkdir test_docs
copy "1-2023-Approved-Math-SOL.docx" test_docs\

# Process it
python batch_process_openai.py --input-dir test_docs
```

### Process All Documents
```bash
# Process all .docx files in current directory
python batch_process_openai.py
```

Expected output:
```
Processing 31 documents...
============================================================

[1/31] 1-2023-Approved-Math-SOL.docx
Extracting text from 1-2023-Approved-Math-SOL.docx...
Calling OpenAI API (gpt-4o-mini)...
  ✓ Extraction complete (8542 tokens)
  ✓ Saved to 1-2023-Approved-Math-SOL_structured.json

[2/31] 2-2023-Approved-Math-SOL.docx
...
```

## Step 6: Launch Streamlit Web Interface

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Web Interface:

1. Check "Use OpenAI for Structured Extraction"
2. Enter your API key (or leave blank if using .env)
3. Select model (gpt-4o-mini recommended)
4. Upload .docx files
5. Click "Process Documents"
6. View and export results

## Troubleshooting

### Error: "No module named 'openai'"
```bash
pip install openai
```

### Error: "OpenAI API key required"
- Make sure `.env` file exists and contains `OPENAI_API_KEY=sk-...`
- Or set environment variable: `set OPENAI_API_KEY=sk-...` (Windows)

### Error: "Incorrect API key provided"
- Verify your API key at https://platform.openai.com/api-keys
- Make sure you copied the entire key including `sk-` prefix
- Check for extra spaces or quotes in `.env` file

### Error: "Rate limit exceeded"
- You've exceeded OpenAI's rate limits
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

### Error: "Insufficient quota"
- Your OpenAI account has no credits
- Add credits at https://platform.openai.com/account/billing

### Documents processed but output is empty
- Check `sol_formatter/sol_documents/` directory
- Look for `*_structured.json` files
- Verify OpenAI extraction succeeded (check console output)

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Model to use for extraction |
| `OPENAI_TEMPERATURE` | No | `0.1` | Response randomness (0.0-1.0) |
| `OUTPUT_DIR` | No | `sol_formatter/sol_documents` | Where to save output |
| `SAVE_RAW_TEXT` | No | `false` | Save extracted text files |

## Next Steps

1. ✅ Process all SOL documents
2. ✅ Review the consolidated output: `all_structured_documents.json`
3. ✅ Explore the data in Streamlit interface
4. ✅ Export CSV for analysis
5. 🎯 Build your quiz generation application!

## Cost Monitoring

Check your OpenAI usage at:
https://platform.openai.com/usage

The batch processor displays token usage after processing:
```
Total tokens used: 265,840
```

Approximate cost calculation:
- gpt-4o-mini: 265,840 tokens ≈ $0.50-1.00
- gpt-4o: 265,840 tokens ≈ $5-8

## Getting Help

- OpenAI API Documentation: https://platform.openai.com/docs
- OpenAI Community Forum: https://community.openai.com
- Check `EXTRACTION_GUIDE.md` for data structure details
- Check `OUTPUT_FORMATS.md` for usage examples
