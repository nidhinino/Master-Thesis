# ESG Data Analysis Toolkit

This repository contains a suite of Jupyter notebooks and Python scripts for processing, analyzing, and visualizing ESG (Environmental, Social, and Governance) data. The tools are designed to streamline ESG report analysis through extraction, normalization, classification, and performance comparison.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Flow](#flow)
  - [Extraction and Cleaning](#extraction-and-cleaning)
  - [Normalization](#normalization)
  - [ESG Report Classification](#esg-report-classification)
  - [ESG JSON File Analysis](#esg-json-file-analysis)
- [Visualization Tools](#visualization-tools)
  - [Performance Data Analysis and Visualization](#performance-data-analysis-and-visualization)
  - [Comparison Dashboard](#comparison-dashboard)
- [Directory Structure](#directory-structure)
- [License](#license)

## Overview

The ESG Data Analysis Toolkit provides a modular approach to compare ESG data with the following capabilities:
- Extract and clean raw data from ESG reports.
- Normalize and structure the data for downstream tasks.
- Classify data into ESG categories.
- Analyze JSON-based ESG files.
- Visualize and compare ESG performance metrics.

## Requirements

Install the required dependencies using:
```bash
pip install -r requirements.txt
```
Key dependencies include:
- Python 3.7 or later
- pandas, matplotlib, seaborn
- Flask, Dash, Plotly
- scikit-learn, numpy
- Jupyter Notebook

## Usage

### Running Notebooks
1. Open Jupyter Notebook in your terminal:
   ```bash
   jupyter notebook
   ```
2. Navigate to the desired notebook (e.g., `Extraction_cleaning.ipynb`) and run the cells sequentially.

### Running Dash App
For the comparison dashboard:
1. Run the `comparision_dash.py` script:
   ```bash
   python comparision_dash.py
   ```
2. Open the app in your browser at `http://127.0.0.1:8050/`.

## Flow

### Extraction and Cleaning
Notebook: `Extraction_cleaning.ipynb`
- Extract tables and raw data from ESG reports.
- Clean the extracted data for further processing using methods like:
  - Removing empty rows/columns.
  - Standardizing headers.
  - Handling merged cells.

### Normalization
Notebook: `Normalization.ipynb`
- Normalize extracted ESG data into a structured format.
- Resolve inconsistencies across different reports.

### ESG Report Classification
Notebook: `ESG_report_classifier.ipynb`
- Classify ESG data into Environmental, Social, and Governance categories.
- Use machine learning or rule-based approaches for classification.

### ESG JSON File Analysis
Notebook: `ESG JSON File Analyzer.ipynb`
- Parse and analyze ESG JSON files.
- Generate summary statistics and visualizations.

## Visualization Tools

### Performance Data Analysis and Visualization
Notebook: `Performance Data Analysis and Visualization.ipynb`
- Visualize the performance of ESG extraction and processing.
- Generate boxplots, scatter plots, and heatmaps for extraction metrics like memory usage, extraction time, and accuracy.

### Comparison Dashboard
Script: `comparision_dash.py`
- A Dash-based web app for interactive visualization of ESG data.
- Features:
  - Individual and comparison dashboards.
  - Bar charts, pie charts, radar plots, heatmaps, and line plots.

## Directory Structure

```
.
├── Extraction_cleaning.ipynb          # Notebook for data extraction and cleaning
├── Normalization.ipynb               # Notebook for data normalization
├── ESG_report_classifier.ipynb       # Notebook for ESG report classification
├── ESG JSON File Analyzer.ipynb      # Notebook for analyzing JSON-based ESG data
├── Performance Data Analysis and Visualization.ipynb  # Notebook for visualizing performance metrics
├── comparision_dash.py               # Dash app for ESG data visualization
├── esg_counts.csv                    # Sample CSV file for Dash app
```

## License

This project is licensed under the MIT License.

