import os
import camelot
import pandas as pd
from pathlib import Path
from helper_functions import *
import warnings

def extract_with_camelot(input_folder, output_folder='camelot'):
    """Extract tables using Camelot"""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    table_counts = {}

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith('.pdf'):
            continue

        pdf_path = os.path.join(input_folder, filename)
        pdf_name = os.path.splitext(filename)[0]
        pdf_output_folder = os.path.join(output_folder, pdf_name)
        Path(pdf_output_folder).mkdir(exist_ok=True)

        try:
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream') 
            valid_tables = []

            if tables:  # Check if any tables were found
                for table in tables:
                    cleaned_table = clean_table(table.df) 
                    if cleaned_table is not None:
                        valid_tables.append(cleaned_table)
            else:
                warnings.warn(f"No tables found in {filename}") 

            table_counts[filename] = len(valid_tables)

            for i, table in enumerate(valid_tables, 1):
                output_path = os.path.join(pdf_output_folder, f"table_{i}.csv")
                table.to_csv(output_path, index=False)

        except Exception as e:
            print(f"Camelot error processing {filename}: {str(e)}")
            table_counts[filename] = 0

    pd.DataFrame({
        'PDF_Filename': table_counts.keys(),
        'Tables_Extracted': table_counts.values()
    }).to_csv(os.path.join(output_folder, 'extraction_summary.csv'), index=False)

    return table_counts

def extract_with_camelot_single(pdf_path, output_folder='camelot'):
    """Extract tables from a single PDF using Camelot."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    Path(pdf_output_folder).mkdir(exist_ok=True)

    table_counts = 0

    try:
        # Extract tables using Camelot
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        valid_tables = []

        if tables:
            for table in tables:
                cleaned_table = clean_table(table.df)
                if cleaned_table is not None:
                    valid_tables.append(cleaned_table)
        else:
            print(f"No tables found in {pdf_path}")

        table_counts = len(valid_tables)

        # Save extracted tables
        for i, table in enumerate(valid_tables, 1):
            output_path = os.path.join(pdf_output_folder, f"table_{i}.csv")
            table.to_csv(output_path, index=False)

        print(f"Extracted {table_counts} tables from {pdf_path}")

    except Exception as e:
        print(f"Camelot error processing {pdf_path}: {str(e)}")
        table_counts = 0

    return {os.path.basename(pdf_path): table_counts}
