import csv
import sys
import re
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import warnings

def remove_html_tags(text):
    """
    Removes HTML tags from the given text using BeautifulSoup.
    If the cleaned text is empty, returns 'NULL'.
    """
    if text is None:
        return 'NULL'
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=' ', strip=True)
    return cleaned_text if cleaned_text else 'NULL'

def remove_extra_spaces(text):
    """
    Removes sequences of more than three consecutive spaces from the text.
    """
    if text is None:
        return 'NULL'
    # Replace sequences of more than three spaces with a single space
    cleaned_text = re.sub(r'\s{4,}', ' ', text)
    return cleaned_text if cleaned_text else 'NULL'

def remove_line_breaks(text):
    """
    Removes all newline and carriage return characters from the text.
    """
    if text is None:
        return 'NULL'
    # Replace newline and carriage return characters with a space
    cleaned_text = re.sub(r'[\r\n]+', ' ', text)
    return cleaned_text if cleaned_text else 'NULL'

def process_csv(input_file, output_file):
    """
    Processes the input CSV file by adding an 'id' field, removing HTML tags,
    removing extra spaces, removing line breaks, and setting empty fields to 'NULL'.
    The processed data is written to the output CSV file.
    """
    with open(input_file, mode='r', encoding='utf-8') as csv_in, \
         open(output_file, mode='w', encoding='utf-8', newline='') as csv_out:
        
        reader = csv.DictReader(csv_in)
        # Add 'id' to the list of field names
        fieldnames = ['id'] + reader.fieldnames
        # Используем QUOTE_MINIMAL, чтобы автоматически заключать в кавычки только необходимые поля
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        
        for idx, row in enumerate(reader, start=1):
            # Assign a unique identifier
            row['id'] = idx
            
            # Process all fields except 'id'
            for field in reader.fieldnames:
                if field in row:
                    cleaned_text = remove_html_tags(row[field])
                    cleaned_text = remove_extra_spaces(cleaned_text)
                    cleaned_text = remove_line_breaks(cleaned_text)
                    row[field] = cleaned_text
                else:
                    row[field] = 'NULL'
            
            # Replace empty fields with 'NULL'
            for key, value in row.items():
                if key == 'id':
                    continue  # Не заменяем 'id'
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    row[key] = 'NULL'
            
            writer.writerow(row)

if __name__ == "__main__":
    # Suppress the MarkupResemblesLocatorWarning from BeautifulSoup
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python news_prepare.py input.csv output.csv")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    
    try:
        # Process the CSV file
        process_csv(input_csv, output_csv)
        print(f"Processing complete. Output saved to {output_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
