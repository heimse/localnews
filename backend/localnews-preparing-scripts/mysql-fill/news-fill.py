import mysql.connector
import pandas as pd
from datetime import datetime
import numpy as np

# Database connection parameters
db_config = {
    'user': 'localnews_user',
    'password': 'nudeta62',
    'host': '127.0.0.1',
    'database': 'localnews_db'
}

# Path to your CSV file
csv_file_path = '../data/news_data_output.csv'  # Replace with the path to your file

def parse_published_at(date_str):
    """
    Converts a date string from ISO format to a datetime object.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return None

def sanitize_value(value):
    """
    Replaces NaN values with None.
    """
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

def truncate_field(value, max_length):
    """
    Truncates a string to the specified length and adds an ellipsis if needed.
    """
    if value is None:
        return None
    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[:max_length - 3] + '...'
    return value_str

def import_news(csv_path):
    # Read data from the CSV file
    try:
        news_df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"File {csv_path} is empty.")
        return
    except pd.errors.ParserError as e:
        print(f"CSV parsing error: {e}")
        return

    # Check for required columns
    required_columns = ['id', 'source', 'author', 'title', 'description', 'url', 'publishedAt', 'content']
    if not all(column in news_df.columns for column in required_columns):
        print("CSV file does not contain all required columns.")
        return

    # Replace NaN values with None
    news_df = news_df.where(pd.notnull(news_df), None)

    # Establish a database connection
    try:
        cnx = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return

    cursor = cnx.cursor()

    # Define maximum field lengths
    max_lengths = {
        'source': 255,
        'author': 255,
        'title': 500,
        'url': 500
    }

    # Import data into the localnews_news table
    insert_query = """
    INSERT INTO localnews_news (id, source, author, title, description, url, published_at, content)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        source = VALUES(source),
        author = VALUES(author),
        title = VALUES(title),
        description = VALUES(description),
        url = VALUES(url),
        published_at = VALUES(published_at),
        content = VALUES(content)
    """

    records_to_insert = []
    for index, row in news_df.iterrows():
        news_id = row['id']
        source = sanitize_value(row['source'])
        author = sanitize_value(row['author'])
        title = sanitize_value(row['title'])
        description = sanitize_value(row['description'])
        url = sanitize_value(row['url'])
        published_at = parse_published_at(row['publishedAt'])
        content = sanitize_value(row['content'])

        if published_at is None:
            print(f"Invalid date format for record ID {news_id}. Skipping record.")
            continue

        # Truncate fields if necessary
        source = truncate_field(source, max_lengths['source'])
        author = truncate_field(author, max_lengths['author'])
        title = truncate_field(title, max_lengths['title'])
        url = truncate_field(url, max_lengths['url'])

        records_to_insert.append((news_id, source, author, title, description, url, published_at, content))

    try:
        cursor.executemany(insert_query, records_to_insert)
        cnx.commit()
        print(f"Successfully imported {cursor.rowcount} records into the localnews_news table.")
    except mysql.connector.Error as err:
        print(f"Data insertion error: {err}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    import_news(csv_file_path)
