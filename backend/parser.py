# parser.py
# Parses HDFC txt statements into Python dictionaries

# parser.py
import io
import csv

def parse_hdfc_txt(file_content: bytes):
    """
    Parse HDFC txt file content and return list of expenses.
    Each expense is a dict with keys: date, narration, debit, credit, closing_balance
    """
    text_data = file_content.decode("utf-8")

    # Skip empty lines
    lines = [line for line in text_data.splitlines() if line.strip()]
    temp_file = io.StringIO("\n".join(lines))

    reader = csv.DictReader(temp_file)
    # Normalize headers
    reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

    required_cols = ["date", "narration", "debit amount", "credit amount", "closing balance"]
    for col in required_cols:
        if col not in reader.fieldnames:
            raise ValueError(f"Missing required column: {col}")

    expenses = []
    for row in reader:
        try:
            expense = {
                "date": row["date"].strip(),
                "narration": row["narration"].strip(),
                "debit": float(row["debit amount"].strip()) if row["debit amount"].strip() else 0.0,
                "credit": float(row["credit amount"].strip()) if row["credit amount"].strip() else 0.0,
                "closing_balance": float(row["closing balance"].strip()) if row["closing balance"].strip() else 0.0
            }
            expenses.append(expense)
        except Exception as e:
            print(f"Skipping row due to error: {e}, row: {row}")

    return expenses