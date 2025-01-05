import os
import pandas as pd
import time
import psutil
import threading
from pathlib import Path
from helper_functions import *
from tabula_extractor import *
from camelot_extractor import *
from pdfplumber_extractor import *


def measure_extraction_performance_parallel(extraction_func, pdf_file):
    """Measure performance metrics for a single PDF file."""
    metrics = {
        'extraction_time': 0,
        'memory_usage': 0,
        'cpu_usage': 0
    }

    def monitor_performance():
        process = psutil.Process()
        while not stop_event.is_set():
            metrics['memory_usage'] = max(metrics['memory_usage'], process.memory_info().rss / (1024 * 1024))
            metrics['cpu_usage'] = max(metrics['cpu_usage'], psutil.cpu_percent(interval=0.1))
            time.sleep(0.1)

    stop_event = threading.Event()
    monitor_thread = threading.Thread(target=monitor_performance)
    monitor_thread.start()

    start_time = time.time()
    try:
        table_counts = extraction_func(pdf_file)
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        table_counts = {}

    metrics['extraction_time'] = time.time() - start_time

    stop_event.set()
    monitor_thread.join()

    return table_counts, metrics

def extract_tables(input_folder, performance_file="table_extraction_performance.csv"):
    """Extract tables from individual PDFs with performance tracking."""
    performance_results = []
    input_path = Path(input_folder)

    if not input_path.exists():
        raise ValueError(f"Input folder not found: {input_folder}")

    extraction_methods = [
        ("Tabula", extract_with_tabula_single),
        ("Camelot", extract_with_camelot_single),
        ("PDFPlumber", extract_with_pdfplumber_single)
    ]

    for pdf_file in input_path.glob("*.pdf"):
        for method_name, extraction_func in extraction_methods:
            try:
                table_counts, metrics = measure_extraction_performance_parallel(
                    extraction_func, 
                    str(pdf_file)
                )
                
                for filename, table_count in table_counts.items():
                    performance_results.append({
                        'Filename': filename,
                        'Extraction Method': method_name,
                        'tables_extracted': table_count,
                        **metrics
                    })
                    print(f"{filename} processed successfully with {method_name}")
                    print(f"Tables extracted: {table_count}")

            except Exception as e:
                print(f"Error processing {pdf_file.name} with {method_name}: {str(e)}")
                performance_results.append({
                    'Filename': pdf_file.name,
                    'Extraction Method': method_name,
                    'extraction_time': 0,
                    'memory_usage': 0,
                    'cpu_usage': 0,
                    'tables_extracted': 0
                })

    output_dir = Path("performance_metrics")
    output_dir.mkdir(exist_ok=True)

    performance_df = pd.DataFrame(performance_results)
    performance_file_path = output_dir / performance_file
    performance_df.to_csv(performance_file_path, index=False)
    print(f"\nPerformance metrics saved to {performance_file_path}")

    return performance_df

if __name__ == "__main__":
    try:
        performance_metrics = extract_tables('../ESG REPORTS')
        print("\nExtraction Performance Summary:")
        print(performance_metrics)
    except Exception as e:
        print(f"Error in main execution: {str(e)}")