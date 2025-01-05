import pandas as pd


def clean_table(df):
    """Comprehensive table cleaning function"""
    if df is None or len(df) <= 1 or len(df.columns) <= 1:
        return None
        
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Basic cleaning
    df = remove_empty_rows_cols(df)
    df = standardize_headers(df)
    df = handle_merged_cells(df)
    df = remove_duplicate_rows(df)
    df = fix_data_types(df)
    
    return df if len(df) > 1 and len(df.columns) > 1 else None

def remove_empty_rows_cols(df):
    """Remove empty or nearly empty rows and columns"""
    # Remove rows where most values (>90%) are NaN
    df = df.dropna(thresh=len(df.columns) * 0.1)
    
    # Remove columns where most values (>90%) are NaN
    df = df.dropna(axis=1, thresh=len(df) * 0.1)
    
    # Remove columns with only repeated values
    cols_to_drop = []
    for col in df.columns:
        if df[col].nunique() <= 1:
            cols_to_drop.append(col)
    return df.drop(columns=cols_to_drop)


def standardize_headers(df):
    """Clean and standardize column headers"""
    df.columns = df.columns.astype(str)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(r'[\n\r\t]', ' ')
    df.columns = df.columns.str.replace(r'\s+', '_')
    df.columns = df.columns.str.replace(r'[^a-z0-9_]', '')
    
    # Handle duplicate column names
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    df.columns = new_cols
    return df


def handle_merged_cells(df):
    """Handle merged cells by forward-filling values"""
    # Check for "Unnamed" columns and forward-fill
    if df.iloc[0].astype(str).str.contains(r'^Unnamed:', na=True).any():
        df.iloc[0] = df.iloc[0].fillna(method='ffill')

    # Forward fill within columns
    df = df.fillna(method='ffill')
    return df

def remove_duplicate_rows(df):
    """Remove duplicate rows while handling near-duplicates"""
    # Remove exact duplicates
    df = df.drop_duplicates()

    # Remove rows with whitespace variations, safely handling object types
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Drop duplicates again after stripping
    df = df.drop_duplicates()
    
    return df


def fix_data_types(df):
    """Convert columns to appropriate data types"""
    for col in df.columns:
        # Apply string operations only to object-type columns
        if df[col].dtype == 'object':
            # Remove currency symbols and commas
            cleaned = df[col].str.replace(r'[,$€£]', '', regex=True)
            cleaned = cleaned.str.replace(',', '')

            # Try converting to numeric
            try:
                df[col] = pd.to_numeric(cleaned)
            except ValueError:
                # Try converting to datetime
                try:
                    df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
                except ValueError:
                    pass
    return df
