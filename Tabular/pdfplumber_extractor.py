import os
import pandas as pd
from pathlib import Path
from helper_functions import *
import pdfplumber

def extract_with_pdfplumber(input_folder, output_folder="pdfplumber"):
    """Extracts tables from PDFs in a folder using PDFPlumber.

    Args:
        input_folder (str): Path to the folder containing the PDFs.
        output_folder (str, optional): Path to the folder where extracted tables
            will be saved as CSV files. Defaults to "extracted_tables".

    Returns:
        dict: A dictionary where keys are PDF filenames and values are the number of 
             tables extracted from each PDF.
    """
    Path(output_folder).mkdir(parents=True, exist_ok=True)  # Ensure output folder exists
    table_counts = {}  # Dictionary to store table counts

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_folder, filename)
        pdf_name = os.path.splitext(filename)[0]

        try:
            with pdfplumber.open(pdf_path) as pdf:
                table_count = 0  # Counter for the number of valid tables extracted
                for page_number, page in enumerate(pdf.pages, start=1):
                    try:
                        tables = page.extract_tables()  # Extract tables from the current page
                        if not tables:  # Skip if no tables are found on the page
                            continue
                        
                        for table_idx, table in enumerate(tables):
                            if not table:  # Skip empty tables
                                print(f"Empty table found on page {page_number} in {filename}")
                                continue

                            try:
                                # Convert table to DataFrame
                                df = pd.DataFrame(table[1:], columns=table[0])  # First row as header

                                # Clean the extracted table
                                cleaned_table = clean_table(df)
                                if cleaned_table is None or cleaned_table.empty:
                                    print(f"Invalid or empty table on page {page_number}, table {table_idx + 1}")
                                    continue  # Skip invalid tables

                                # Save the cleaned table to a CSV file
                                pdf_output_folder = os.path.join(output_folder, pdf_name)
                                Path(pdf_output_folder).mkdir(parents=True, exist_ok=True)
                                output_csv_path = os.path.join(
                                    pdf_output_folder, f"page_{page_number}_table_{table_idx + 1}.csv"
                                )
                                cleaned_table.to_csv(output_csv_path, index=False)
                                table_count += 1

                            except Exception as e:
                                print(f"Error processing table {table_idx + 1} on page {page_number} in {filename}: {e}")

                    except Exception as e:
                        print(f"Error processing page {page_number} in {filename}: {e}")

            table_counts[filename] = table_count
            print(f"Extracted {table_count} tables from {filename} into {os.path.join(output_folder, pdf_name)}")

        except Exception as e:
            print(f"Failed to extract tables from {filename}: {e}")
            table_counts[filename] = 0

    # Save a summary of the extraction process
    summary_path = os.path.join(output_folder, 'extraction_summary.csv')
    pd.DataFrame({
        'PDF_Filename': list(table_counts.keys()),
        'Tables_Extracted': list(table_counts.values())
    }).to_csv(summary_path, index=False)

    return table_counts

def extract_with_pdfplumber_single(pdf_path, output_folder="pdfplumber"):
    """Extract tables from a single PDF using PDFPlumber."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    Path(pdf_output_folder).mkdir(parents=True, exist_ok=True)

    table_count = 0

    try:
        # Open the PDF file and extract tables
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])  # Use first row as header
                        cleaned_table = clean_table(df)  # Apply cleaning step
                        if cleaned_table is None:
                            continue  # Skip saving if the table is invalid after cleaning

                        output_csv_path = os.path.join(
                            pdf_output_folder, f"page_{page_number}_table_{table_idx + 1}.csv"
                        )
                        cleaned_table.to_csv(output_csv_path, index=False)
                        table_count += 1

        print(f"Extracted {table_count} tables from {pdf_path}")

    except Exception as e:
        print(f"Failed to extract tables from {pdf_path}: {e}")
        table_count = 0

    return {os.path.basename(pdf_path): table_count}
