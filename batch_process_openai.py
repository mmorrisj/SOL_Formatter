"""Batch processing script using OpenAI for structured extraction"""

import os
from pathlib import Path
from sol_formatter.openai_extractor import OpenAIExtractor
import argparse


def process_all_documents_with_openai(
    input_dir: str = "sol_formatter/sol_documents",
    output_dir: str = "sol_formatter/sol_documents/output",
    api_key: str = None,
    model: str = "gpt-4o-mini",
    save_raw_text: bool = False
):
    """
    Process all .docx files using OpenAI for structured extraction

    Args:
        input_dir: Directory containing .docx files
        output_dir: Directory to save processed output
        api_key: OpenAI API key (or set OPENAI_API_KEY environment variable)
        model: OpenAI model to use (gpt-4o-mini recommended for cost, gpt-4o for quality)
        save_raw_text: Save raw extracted text files for debugging
    """
    # Find all .docx files
    input_path = Path(input_dir)
    docx_files = list(input_path.glob("*.docx"))

    if not docx_files:
        print(f"No .docx files found in {input_dir}")
        return

    # Initialize extractor
    try:
        extractor = OpenAIExtractor(api_key=api_key, model=model)
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your OpenAI API key:")
        print("  Option 1: Set environment variable: OPENAI_API_KEY=your_key_here")
        print("  Option 2: Pass --api-key parameter")
        return

    # Process all documents
    extractor.extract_batch(
        [str(f) for f in docx_files],
        output_dir=output_dir,
        save_raw_text=save_raw_text
    )


def main():
    parser = argparse.ArgumentParser(
        description="Batch process SOL documents with OpenAI structured extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all documents in current directory (using OPENAI_API_KEY env variable)
  python batch_process_openai.py

  # Process with API key parameter
  python batch_process_openai.py --api-key sk-...

  # Use higher quality model (more expensive)
  python batch_process_openai.py --model gpt-4o

  # Save raw text files for debugging
  python batch_process_openai.py --save-raw-text

  # Process specific directory
  python batch_process_openai.py --input-dir path/to/documents

Models:
  - gpt-4o-mini: Fast, cost-effective (~$0.15 per 1M tokens) - RECOMMENDED
  - gpt-4o: Higher quality, more expensive (~$2.50 per 1M tokens)
  - gpt-4-turbo: Previous generation, middle ground

Cost estimate per document: $0.01-0.05 for gpt-4o-mini, $0.10-0.30 for gpt-4o
        """
    )

    parser.add_argument(
        '--input-dir',
        default='sol_formatter/sol_documents',
        help='Directory containing .docx files (default: sol_formatter/sol_documents)'
    )
    parser.add_argument(
        '--output-dir',
        default='sol_formatter/sol_documents/output',
        help='Directory to save processed output (default: sol_formatter/sol_documents/output)'
    )
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY environment variable)'
    )
    parser.add_argument(
        '--model',
        default='gpt-4o-mini',
        choices=['gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo'],
        help='OpenAI model to use (default: gpt-4o-mini)'
    )
    parser.add_argument(
        '--save-raw-text',
        action='store_true',
        help='Save raw extracted text files for debugging'
    )

    args = parser.parse_args()

    process_all_documents_with_openai(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        api_key=args.api_key,
        model=args.model,
        save_raw_text=args.save_raw_text
    )


if __name__ == "__main__":
    main()
