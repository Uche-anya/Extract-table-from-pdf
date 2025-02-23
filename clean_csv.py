import pandas as pd
from tabulate import tabulate

# Load the CSV file that was extracted from the PDF by Camelot
file_path = "extracted_table.csv"
df = pd.read_csv(file_path, header=None)

# Prepare an empty list to store the structured data
data = []
current_section = None  # To keep track of the current section
current_remita = None  # To keep track of the current Remita RRR number

# Iterate over every row in the CSV DataFrame
for i, row in df.iterrows():
    # We assume that all useful info is in the first cell; remove leading/trailing whitespace.
    cell = str(row[0]).strip()
    if not cell:
        continue  # Skip empty rows

    # Identify section headers (they include "Details" and "Amount")
    if "Details" in cell and "Amount" in cell:
        # Remove the trailing "Amount" part from the header if present.
        section = cell.replace("\nAmount", "").strip()
        current_section = section
        continue

    # Also treat "STUDENT COPY TRANSCRIPT" as a section header
    elif "STUDENT COPY TRANSCRIPT" in cell:
        section = cell.replace("\nAmount", "").strip()
        current_section = section
        continue

    # Identify rows that specify the Remita RRR number
    elif "Remita RRR" in cell:
        # Expect format like "Remita RRR: 180963971417"
        parts = cell.split(":")
        if len(parts) > 1:
            current_remita = parts[1].strip()
        else:
            current_remita = cell.strip()
        continue

    # Process rows that start with "TOTAL" (which also contain the amount on the same cell)
    elif cell.startswith("TOTAL"):
        # For a TOTAL row, the cell may look like: "TOTAL\n15,000.00"
        parts = cell.split("\n")
        fee_type = parts[0].strip()  # This will be "TOTAL"
        amount = parts[1].strip() if len(parts) > 1 else ""
        # The status is in the second column of the CSV row
        status = str(row[1]).strip() if (len(row) > 1 and pd.notna(row[1])) else ""
        data.append([current_section, current_remita, fee_type, amount, status])

    else:
        # For normal fee items, the cell will contain both the fee description and its amount
        # e.g., "Identity Card\n5,000.00"
        parts = cell.split("\n")
        fee_type = parts[0].strip()  # The fee description
        amount = parts[1].strip() if len(parts) > 1 else ""
        # Some rows might have a status in the second CSV column
        status = str(row[1]).strip() if (len(row) > 1 and pd.notna(row[1])) else ""
        data.append([current_section, current_remita, fee_type, amount, status])

# Create a DataFrame from the structured data
columns = ["Section", "Remita RRR", "Fee Type", "Amount", "Status"]
df_cleaned = pd.DataFrame(data, columns=columns)

# Save the cleaned data to an Excel file
df_cleaned.to_excel("formatted_payment_advice.xlsx", index=False)

# Also, print a grid-formatted table in the terminal for quick verification
print(tabulate(df_cleaned, headers="keys", tablefmt="grid"))
