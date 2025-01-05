import os
import tabula
import pandas as pd
from helper_functions import *
from pathlib import Path

def extract_with_tabula(input_folder, output_folder='tabula'):
    """Extract tables using Tabula"""
    Path(output_folder).mkdir(parents=True, exist_ok=True)  # Ensure output folder exists
    table_counts = {}  # To store the number of tables extracted per PDF
    
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith('.pdf'):  # Process only PDF files
            continue
            
        pdf_path = os.path.join(input_folder, filename)
        pdf_name = os.path.splitext(filename)[0]
        pdf_output_folder = os.path.join(output_folder, pdf_name)
        Path(pdf_output_folder).mkdir(exist_ok=True)  # Create folder for each PDF
        
        try:
            # Read tables using Tabula
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            valid_tables = []
            
            for i, table in enumerate(tables):
                if table is None or table.empty:  # Skip empty tables
                    print(f"Skipping empty table {i + 1} in {filename}")
                    continue
                
                try:
                    # Clean the table
                    cleaned_table = clean_table(table)
                    if cleaned_table is not None:
                        valid_tables.append(cleaned_table)
                        
                        # Save the cleaned table to CSV
                        output_path = os.path.join(pdf_output_folder, f"table_{i + 1}.csv")
                        cleaned_table.to_csv(output_path, index=False)
                except Exception as e:
                    print(f"Error processing table {i + 1} in {filename}: {str(e)}")
            
            # Record the count of valid tables
            table_counts[filename] = len(valid_tables)
        
        except Exception as e:
            # Handle PDF-level errors (e.g., reading issues)
            print(f"Tabula error processing {filename}: {str(e)}")
            table_counts[filename] = 0
    
    # Save summary of extraction results
    summary_path = os.path.join(output_folder, 'extraction_summary.csv')
    pd.DataFrame({
        'PDF_Filename': list(table_counts.keys()),
        'Tables_Extracted': list(table_counts.values())
    }).to_csv(summary_path, index=False)
    
    return table_counts

def extract_with_tabula_single(pdf_path, output_folder='tabula'):
    """Extract tables from a single PDF using Tabula."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    Path(pdf_output_folder).mkdir(exist_ok=True)

    table_counts = 0  # To keep track of valid tables extracted

    try:
        # Read all tables from the specified PDF file
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        valid_tables = []

        # Process and clean each table
        for table in tables:
            cleaned_table = clean_table(table)
            if cleaned_table is not None:
                valid_tables.append(cleaned_table)

        # Save valid tables to output files
        for i, table in enumerate(valid_tables, 1):
            output_path = os.path.join(pdf_output_folder, f"table_{i}.csv")
            table.to_csv(output_path, index=False)

        table_counts = len(valid_tables)
        print(f"{pdf_path} processed successfully. Tables extracted: {table_counts}")

    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

    return {os.path.basename(pdf_path): table_counts}
