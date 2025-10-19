"""Streamlit web application for uploading and processing SOL documents"""

import streamlit as st
import tempfile
from pathlib import Path
from sol_formatter.parser import SOLParser
from sol_formatter.openai_extractor import OpenAIExtractor
import pandas as pd
import json
from datetime import datetime
import os


def main():
    st.set_page_config(
        page_title="SOL Document Processor",
        page_icon="📚",
        layout="wide"
    )

    st.title("Virginia SOL Document Processor")
    st.markdown("""
    Upload Virginia Standards of Learning (SOL) mathematics documents to extract and structure educational standards.
    """)

    # Sidebar for options
    with st.sidebar:
        st.header("Options")

        # Processing method selection
        use_openai = st.checkbox(
            "Use OpenAI for Structured Extraction",
            value=False,
            help="Extract structured data using OpenAI API (requires API key)"
        )

        if use_openai:
            st.info("OpenAI extraction provides structured output suitable for quiz generation")

            # API key input
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=os.getenv("OPENAI_API_KEY", ""),
                help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
            )

            # Model selection
            model = st.selectbox(
                "Model",
                ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
                index=0,
                help="gpt-4o-mini is recommended for cost efficiency"
            )

            if model == "gpt-4o-mini":
                st.caption("💰 ~$0.01-0.05 per document")
            elif model == "gpt-4o":
                st.caption("💰 ~$0.10-0.30 per document")

        output_format = st.multiselect(
            "Output Format",
            ["JSON", "CSV", "Preview"],
            default=["Preview", "JSON"]
        )

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload SOL Documents (.docx)",
        type=['docx'],
        accept_multiple_files=True,
        help="Upload one or more .docx files containing SOL standards"
    )

    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")

        # Process button
        if st.button("Process Documents", type="primary"):
            if use_openai:
                if not api_key:
                    st.error("Please enter your OpenAI API key")
                    return
                process_documents_with_openai(uploaded_files, output_format, api_key, model)
            else:
                process_documents(uploaded_files, output_format)


def process_documents_with_openai(uploaded_files, output_format, api_key, model):
    """Process uploaded documents using OpenAI structured extraction"""

    try:
        extractor = OpenAIExtractor(api_key=api_key, model=model)
    except ValueError as e:
        st.error(f"Error initializing OpenAI: {str(e)}")
        return

    all_results = []
    total_tokens = 0

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress = (idx + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {uploaded_file.name} with OpenAI...")

        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Extract structured data using OpenAI
            result = extractor.extract_structured_data(tmp_path)
            all_results.append(result)
            total_tokens += result["_extraction_metadata"]["tokens_used"]

            # Clean up temp file
            Path(tmp_path).unlink()

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    status_text.text("Processing complete!")

    # Display results
    display_openai_results(all_results, output_format, total_tokens)


def process_documents(uploaded_files, output_format):
    """Process uploaded documents and display results (basic extraction)"""

    parser = SOLParser()
    all_results = []

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress = (idx + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {uploaded_file.name}...")

        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Parse document
            result = parser.parse_document(tmp_path)
            all_results.append(result)

            # Clean up temp file
            Path(tmp_path).unlink()

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    status_text.text("Processing complete!")

    # Display results
    display_results(all_results, output_format)


def display_results(results, output_format):
    """Display processing results in various formats"""

    st.header("Processing Results")

    # Summary statistics
    col1, col2, col3 = st.columns(3)

    total_standards = sum(len(r['content']['identified_standards']) for r in results)
    total_paragraphs = sum(r['content']['total_paragraphs'] for r in results)
    total_tables = sum(r['content']['total_tables'] for r in results)

    with col1:
        st.metric("Documents Processed", len(results))
    with col2:
        st.metric("Standards Identified", total_standards)
    with col3:
        st.metric("Total Paragraphs", total_paragraphs)

    # Tabs for different views
    tabs = st.tabs(["Overview", "Standards", "Document Details", "Export"])

    # Overview tab
    with tabs[0]:
        st.subheader("Document Overview")

        overview_data = []
        for result in results:
            metadata = result['metadata']
            overview_data.append({
                "File": result['source_file'],
                "Type": metadata.get('type', 'Unknown'),
                "Grade Level": metadata.get('grade_level', 'Unknown'),
                "Subject": metadata.get('subject', 'N/A'),
                "Standards Found": len(result['content']['identified_standards']),
                "Paragraphs": result['content']['total_paragraphs'],
                "Tables": result['content']['total_tables']
            })

        df_overview = pd.DataFrame(overview_data)
        st.dataframe(df_overview, use_container_width=True)

    # Standards tab
    with tabs[1]:
        st.subheader("All Identified Standards")

        standards_data = []
        for result in results:
            metadata = result['metadata']
            for standard in result['content']['identified_standards']:
                standards_data.append({
                    "Standard": standard,
                    "Source": result['source_file'],
                    "Grade Level": metadata.get('grade_level', 'Unknown'),
                    "Subject": metadata.get('subject', 'Mathematics'),
                    "Type": metadata.get('type', 'Unknown')
                })

        if standards_data:
            df_standards = pd.DataFrame(standards_data)
            st.dataframe(df_standards, use_container_width=True)

            # Filter options
            st.subheader("Filter Standards")
            col1, col2 = st.columns(2)

            with col1:
                grade_filter = st.multiselect(
                    "Grade Level",
                    df_standards['Grade Level'].unique()
                )

            with col2:
                type_filter = st.multiselect(
                    "Document Type",
                    df_standards['Type'].unique()
                )

            # Apply filters
            filtered_df = df_standards
            if grade_filter:
                filtered_df = filtered_df[filtered_df['Grade Level'].isin(grade_filter)]
            if type_filter:
                filtered_df = filtered_df[filtered_df['Type'].isin(type_filter)]

            if grade_filter or type_filter:
                st.subheader("Filtered Results")
                st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No standards identified in the uploaded documents.")

    # Document Details tab
    with tabs[2]:
        st.subheader("Detailed Document Content")

        selected_doc = st.selectbox(
            "Select a document to view details",
            [r['source_file'] for r in results]
        )

        if selected_doc:
            result = next(r for r in results if r['source_file'] == selected_doc)

            # Metadata
            st.markdown("**Document Metadata:**")
            st.json(result['metadata'])

            # Content preview
            st.markdown("**Content Preview:**")

            with st.expander("View Paragraphs"):
                for idx, para in enumerate(result['content']['paragraphs'][:20], 1):
                    st.text(f"{idx}. {para['text'][:200]}...")

            with st.expander("View Tables"):
                for idx, table in enumerate(result['content']['tables'], 1):
                    st.markdown(f"**Table {idx}:**")
                    st.table(table[:5])  # Show first 5 rows

    # Export tab
    with tabs[3]:
        st.subheader("Export Data")

        # JSON export
        if "JSON" in output_format:
            json_data = {
                "processed_date": datetime.now().isoformat(),
                "total_documents": len(results),
                "documents": results
            }

            st.download_button(
                label="Download JSON",
                data=json.dumps(json_data, indent=2, ensure_ascii=False),
                file_name=f"sol_documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        # CSV export
        if "CSV" in output_format and standards_data:
            df_standards = pd.DataFrame(standards_data)

            st.download_button(
                label="Download CSV",
                data=df_standards.to_csv(index=False),
                file_name=f"sol_standards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


def display_openai_results(results, output_format, total_tokens):
    """Display OpenAI-extracted structured results"""

    st.header("Structured Extraction Results")

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)

    total_strands = sum(len(r.get('strands', [])) for r in results)
    total_standards = sum(
        sum(len(strand.get('standards', [])) for strand in r.get('strands', []))
        for r in results
    )
    total_objectives = sum(
        sum(
            sum(len(std.get('knowledge_and_skills', [])) for std in strand.get('standards', []))
            for strand in r.get('strands', [])
        )
        for r in results
    )

    with col1:
        st.metric("Documents", len(results))
    with col2:
        st.metric("Content Strands", total_strands)
    with col3:
        st.metric("Standards", total_standards)
    with col4:
        st.metric("Objectives", total_objectives)

    st.info(f"💰 API Usage: {total_tokens:,} tokens")

    # Tabs for different views
    tabs = st.tabs(["Standards", "Strands Overview", "Full Structure", "Export"])

    # Standards tab
    with tabs[0]:
        st.subheader("All Standards")

        standards_data = []
        for doc in results:
            doc_meta = doc.get('document_metadata', {})
            for strand in doc.get('strands', []):
                for standard in strand.get('standards', []):
                    standards_data.append({
                        "Standard ID": standard.get('standard_id', ''),
                        "Statement": standard.get('standard_statement', '')[:100] + "...",
                        "Strand": strand.get('strand_name', ''),
                        "Grade": doc_meta.get('grade_level', ''),
                        "Objectives": len(standard.get('knowledge_and_skills', [])),
                        "Cognitive Level": standard.get('cognitive_level', ''),
                        "Tags": ", ".join(standard.get('tags', [])[:3])
                    })

        if standards_data:
            df = pd.DataFrame(standards_data)
            st.dataframe(df, use_container_width=True)

            # Filters
            st.subheader("Filter Standards")
            col1, col2, col3 = st.columns(3)

            with col1:
                grade_filter = st.multiselect("Grade Level", df['Grade'].unique())
            with col2:
                strand_filter = st.multiselect("Strand", df['Strand'].unique())
            with col3:
                cognitive_filter = st.multiselect("Cognitive Level", df['Cognitive Level'].unique())

            filtered = df
            if grade_filter:
                filtered = filtered[filtered['Grade'].isin(grade_filter)]
            if strand_filter:
                filtered = filtered[filtered['Strand'].isin(strand_filter)]
            if cognitive_filter:
                filtered = filtered[filtered['Cognitive Level'].isin(cognitive_filter)]

            if grade_filter or strand_filter or cognitive_filter:
                st.subheader("Filtered Results")
                st.dataframe(filtered, use_container_width=True)

    # Strands Overview tab
    with tabs[1]:
        st.subheader("Content Strands Overview")

        for doc in results:
            doc_meta = doc.get('document_metadata', {})
            st.markdown(f"### {doc_meta.get('grade_level', 'Unknown')} - {doc_meta.get('course_name', 'Mathematics')}")

            for strand in doc.get('strands', []):
                with st.expander(f"{strand.get('strand_code', '')} - {strand.get('strand_name', '')}"):
                    st.markdown(f"**Standards in this strand:** {len(strand.get('standards', []))}")

                    if strand.get('strand_description'):
                        st.markdown(strand['strand_description'])

                    for std in strand.get('standards', [])[:3]:  # Show first 3
                        st.markdown(f"**{std.get('standard_id', '')}:** {std.get('standard_statement', '')[:150]}...")

    # Full Structure tab
    with tabs[2]:
        st.subheader("Complete Structured Data")

        selected_doc = st.selectbox(
            "Select Document",
            [f"{r.get('document_metadata', {}).get('grade_level', 'Unknown')} ({r.get('_extraction_metadata', {}).get('source_file', '')})"
             for r in results]
        )

        if selected_doc and results:
            idx = [f"{r.get('document_metadata', {}).get('grade_level', 'Unknown')} ({r.get('_extraction_metadata', {}).get('source_file', '')})"
                   for r in results].index(selected_doc)
            result = results[idx]

            st.json(result)

    # Export tab
    with tabs[3]:
        st.subheader("Export Structured Data")

        # JSON export
        if "JSON" in output_format:
            json_data = {
                "extracted_date": datetime.now().isoformat(),
                "total_documents": len(results),
                "total_tokens": total_tokens,
                "documents": results
            }

            st.download_button(
                label="Download Complete JSON",
                data=json.dumps(json_data, indent=2, ensure_ascii=False),
                file_name=f"sol_structured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        # CSV export of standards
        if "CSV" in output_format and standards_data:
            # Create detailed CSV
            detailed_data = []
            for doc in results:
                doc_meta = doc.get('document_metadata', {})
                for strand in doc.get('strands', []):
                    for standard in strand.get('standards', []):
                        for obj in standard.get('knowledge_and_skills', []):
                            detailed_data.append({
                                "Standard ID": standard.get('standard_id', ''),
                                "Standard Statement": standard.get('standard_statement', ''),
                                "Strand Code": strand.get('strand_code', ''),
                                "Strand Name": strand.get('strand_name', ''),
                                "Grade Level": doc_meta.get('grade_level', ''),
                                "Objective": obj.get('objective_text', ''),
                                "Action Verb": obj.get('action_verb', ''),
                                "Examples": "; ".join(obj.get('examples', [])),
                                "Constraints": "; ".join(obj.get('constraints', [])),
                                "Cognitive Level": standard.get('cognitive_level', ''),
                                "Tags": "; ".join(standard.get('tags', []))
                            })

            if detailed_data:
                df_detailed = pd.DataFrame(detailed_data)
                st.download_button(
                    label="Download Detailed CSV",
                    data=df_detailed.to_csv(index=False),
                    file_name=f"sol_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )


if __name__ == "__main__":
    main()
