# PDF Table Extraction Toolkit

This repository contains a set of Python scripts for extracting tables from PDF documents using various tools and performing performance analysis. The toolkit is modular, with each extraction method implemented in a separate script and utilities to clean and visualize the extracted data.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Scripts](#scripts)
  - [pdfplumber_extractor.py](#pdfplumber_extractorpy)
  - [tabula_extractor.py](#tabula_extractorpy)
  - [camelot_extractor.py](#camelot_extractorpy)
  - [helper_functions.py](#helper_functionspy)
  - [Visualization.py](#visualizationpy)
  - [table_extraction.py](#table_extractionpy)
- [Performance Analysis](#performance-analysis)
- [Directory Structure](#directory-structure)
- [License](#license)

## Overview

This toolkit supports extracting tables from PDFs using the following tools:
- [PDFPlumber](https://github.com/jsvine/pdfplumber)
- [Tabula](https://tabula.technology/)
- [Camelot](https://camelot-py.readthedocs.io/)

Additionally, it includes:
- Table cleaning and processing utilities.
- Performance analysis and visualization for the extraction methods.

## Requirements

Ensure you have the following dependencies installed:
- Python 3.7 or later
- pandas
- matplotlib
- seaborn
- pdfplumber
- tabula-py
- camelot-py
- psutil


## Usage

### Extract Tables
1. Place your PDF files in a folder (e.g., `ESG REPORTS`) and update it in line 101.
2. Run the `table_extraction.py` script:

   ```bash
   python table_extraction.py 
   ```

### Analyze Performance
Performance metrics (e.g., extraction time, memory, CPU usage) will be saved in the `performance_metrics` folder and visualized in plots.

## Scripts

### pdfplumber_extractor.py
Extracts tables using the PDFPlumber library.
- **Functions:**
  - `extract_with_pdfplumber(input_folder, output_folder)`
  - `extract_with_pdfplumber_single(pdf_path, output_folder)`
- Outputs cleaned tables as CSV files.

### tabula_extractor.py
Extracts tables using Tabula.
- **Functions:**
  - `extract_with_tabula(input_folder, output_folder)`
  - `extract_with_tabula_single(pdf_path, output_folder)`
- Requires Java to be installed on your system (Optional).

### camelot_extractor.py
Extracts tables using Camelot with the `stream` flavor.
- **Functions:**
  - `extract_with_camelot(input_folder, output_folder)`
  - `extract_with_camelot_single(pdf_path, output_folder)`

### helper_functions.py
Utility functions for cleaning and processing extracted tables.
- **Functions:**
  - `clean_table(df)`
  - Includes utilities like `remove_empty_rows_cols`, `standardize_headers`, `handle_merged_cells`, etc.

### Visualization.py
Analyzes and visualizes the performance of extraction methods.
- **Generates plots such as:**
  - Boxplots for extraction time and memory usage.
  - Heatmaps comparing performance across methods.
- Outputs summary statistics in a text file.

### table_extraction.py
Coordinates table extraction using all methods and tracks performance.
- **Functions:**
  - `measure_extraction_performance_parallel(extraction_func, pdf_file)`
  - `extract_tables(input_folder, performance_file)`

## Performance Analysis

The `Visualization.py` script processes the performance metrics saved in `performance_metrics/table_extraction_performance.csv`. It generates visualizations such as:
- Boxplots for memory and CPU usage.
- Scatterplots of tables extracted vs. extraction time.

Run the visualization script to analyze the performance:
```bash
python Visualization.py
```

## Directory Structure

```
.
├── helper_functions.py      # Table cleaning utilities
├── pdfplumber_extractor.py  # PDFPlumber extraction script
├── tabula_extractor.py      # Tabula extraction script
├── camelot_extractor.py     # Camelot extraction script
├── table_extraction.py      # Main script for parallel extraction
├── Visualization.py         # Performance analysis and visualization
├── ESG REPORTS/              # Folder containing PDF files (to be created)
├── performance_metrics/     # Folder for performance results (generated)
```

## License

This project is licensed under the MIT License.

