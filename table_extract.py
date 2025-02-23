import camelot
from pdf_file_test import file_path


# Extract tables using the 'stream' method (good for non-ruled tables)
tables = camelot.read_pdf(file_path, pages="1", flavor="stream")

# Check the number of tables detected
print(f"Number of tables extracted: {tables.n}")

# Export the first table to CSV (or print it)
if tables.n > 0:
    tables[1].to_csv("extracted_table.csv")
    print(tables[1].df)  # Print extracted table as a DataFrame
else:
    print("No tables found. Try 'lattice' method instead.")
