"""
Simple CSV file splitter.
Splits a CSV file equally across multiple output files.
"""

import csv
from pathlib import Path


def split_csv(input_file: str, output_codes: list[str]):
    """
    Split a CSV file equally across multiple output files.
    Automatically adds IsClaimed column set to false for all rows.
    
    Args:
        input_file: Path to input CSV file
        output_codes: List of codes/identifiers (e.g., ["NL", "EN"])
                      Output files will be named refill_{code}.csv
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if not output_codes:
        raise ValueError("Output codes list cannot be empty")
    
    # Read the CSV file
    with open(input_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    total_rows = len(rows)
    num_files = len(output_codes)
    
    # Calculate rows per file (distribute as evenly as possible)
    rows_per_file = total_rows // num_files
    remainder = total_rows % num_files
    
    print(f"Input file: {input_file}")
    print(f"Total rows: {total_rows}")
    print(f"Number of output files: {num_files}")
    print(f"Rows per file: {rows_per_file} (with {remainder} extra rows distributed)")
    
    # Split and write files
    row_index = 0
    for i, code in enumerate(output_codes):
        # Generate output filename: refer_{code}.csv
        output_filename = f"refer_{code}.csv"
        
        # Calculate how many rows this file gets
        # Distribute remainder rows to first files
        file_row_count = rows_per_file + (1 if i < remainder else 0)
        
        output_path = Path(output_filename)
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['VoucherCode', 'IsClaimed'])
            
            # Add "false" to each row for the IsClaimed column
            file_rows = rows[row_index:row_index + file_row_count]
            for row in file_rows:
                # Add "false" as the IsClaimed value
                writer.writerow([row[0] if row else '', 'false'])
        
        print(f"Created {output_filename} with {file_row_count} rows")
        row_index += file_row_count
    
    print(f"\nSuccessfully created {num_files} file(s)")


if __name__ == '__main__':
    # Example usage - modify these values
    input_file = 'omni_US_leadgen_referafriend.csv'
    output_codes = ['US']
    
    split_csv(input_file, output_codes)