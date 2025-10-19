"""Batch processing script for SOL documents"""

import os
from pathlib import Path
from sol_formatter.parser import SOLParser
import argparse
import json
from datetime import datetime


def process_all_documents(input_dir: str = "sol_formatter/sol_documents", output_dir: str = "sol_formatter/sol_documents/output"):
    """
    Process all .docx files in the input directory

    Args:
        input_dir: Directory containing .docx files (default: current directory)
        output_dir: Directory to save processed output
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize parser
    parser = SOLParser()

    # Find all .docx files
    input_path = Path(input_dir)
    docx_files = list(input_path.glob("*.docx"))

    if not docx_files:
        print(f"No .docx files found in {input_dir}")
        return

    print(f"Found {len(docx_files)} documents to process")
    print("-" * 60)

    all_results = []
    successful = 0
    failed = 0

    # Process each document
    for idx, file_path in enumerate(docx_files, 1):
        try:
            print(f"[{idx}/{len(docx_files)}] Processing: {file_path.name}")

            # Parse document
            result = parser.parse_document(str(file_path))

            # Save individual JSON file
            output_filename = file_path.stem + ".json"
            json_path = output_path / output_filename
            parser.save_json(result, str(json_path))

            # Save individual CSV file for standards
            csv_filename = file_path.stem + "_standards.csv"
            csv_path = output_path / csv_filename
            parser.save_csv(result, str(csv_path))

            all_results.append(result)
            successful += 1

            print(f"  ✓ Extracted {len(result['content']['identified_standards'])} standards")
            print(f"  ✓ Saved to: {json_path.name}")

        except Exception as e:
            print(f"  ✗ Error processing {file_path.name}: {str(e)}")
            failed += 1

        print()

    # Save combined results
    combined_output = {
        "processed_date": datetime.now().isoformat(),
        "total_documents": len(docx_files),
        "successful": successful,
        "failed": failed,
        "documents": all_results
    }

    combined_path = output_path / "all_documents.json"
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(combined_output, f, indent=2, ensure_ascii=False)

    # Create combined CSV of all standards
    create_combined_csv(all_results, output_path / "all_standards.csv")

    # Print summary
    print("=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total documents: {len(docx_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput directory: {output_path.absolute()}")
    print(f"Combined output: {combined_path.name}")


def create_combined_csv(results, output_path):
    """Create a single CSV file with all standards from all documents"""
    import csv

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Standard', 'Source File', 'Document Type', 'Grade Level', 'Subject'])

        for result in results:
            metadata = result['metadata']
            for standard in result['content']['identified_standards']:
                writer.writerow([
                    standard,
                    result['source_file'],
                    metadata.get('type', 'Unknown'),
                    metadata.get('grade_level', 'Unknown'),
                    metadata.get('subject', 'Mathematics')
                ])

    print(f"✓ Combined CSV saved: {output_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch process Virginia SOL mathematics documents"
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

    args = parser.parse_args()

    process_all_documents(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
