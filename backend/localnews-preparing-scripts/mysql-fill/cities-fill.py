import mysql.connector
import pandas as pd

# Database connection parameters
db_config = {
    'user': 'localnews_user',
    'password': 'nudeta62',
    'host': '127.0.0.1',
    'database': 'localnews_db'
}

# Connect to the database
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

# Read data from CSV file
cities_df = pd.read_csv('../data/cities_data_output.csv')

# Import data into the localnews_cities table
for index, row in cities_df.iterrows():
    insert_query = """
    INSERT INTO localnews_cities (id, name, state, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (
        int(row['id']),
        row['city'],       # Mapping CSV 'city' to DB 'name'
        row['state'],
        float(row['latitude']),
        float(row['longitude'])
    )
    cursor.execute(insert_query, data)

# Commit changes and close the connection
cnx.commit()
cursor.close()
cnx.close()
