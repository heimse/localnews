import csv

# Name of the input file
input_file = 'cities_data.csv'
# Name of the output file
output_file = 'cities_data_output.csv'

# Open the input file for reading and the output file for writing
with open(input_file, mode='r', newline='', encoding='utf-8') as csv_in, \
     open(output_file, mode='w', newline='', encoding='utf-8') as csv_out:
    
    # Create a CSV reader object as a dictionary
    reader = csv.DictReader(csv_in)
    
    # Normalize header names by stripping whitespace and converting to lowercase
    normalized_fieldnames = [field.strip().lower() for field in reader.fieldnames]
    print("Normalized Headers:", normalized_fieldnames)

    # Create a mapping from normalized field names to original field names
    field_mapping = {field.lower(): field for field in reader.fieldnames}

    # Check if 'location' exists in normalized headers
    if 'location' not in normalized_fieldnames:
        print("Error: 'location' field not found in the CSV headers.")
        print("Available fields:", reader.fieldnames)
        exit(1)

    # Use the original field name for 'location'
    location_field = field_mapping['location']

    # Define new headers for the output file
    # Add 'id' and replace 'location' with 'latitude' and 'longitude'
    fieldnames = ['id'] + [field for field in reader.fieldnames if field != location_field] + ['latitude', 'longitude']
    
    # Create a CSV writer object with the new headers
    writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
    writer.writeheader()
    
    # Iterate over each row in the input file
    for idx, row in enumerate(reader, start=1):
        # Add the 'id' field
        row['id'] = idx
        
        try:
            # Extract and split the 'location' field into 'latitude' and 'longitude'
            location = row.pop(location_field).strip('()')  # Remove parentheses
            latitude, longitude = location.split(', ')
            row['latitude'] = latitude
            row['longitude'] = longitude
        except KeyError:
            print(f"Row {idx}: 'location' field is missing.")
            row['latitude'] = ''
            row['longitude'] = ''
        except ValueError:
            print(f"Row {idx}: 'location' field is not in the expected format.")
            row['latitude'] = ''
            row['longitude'] = ''
        
        # Order the fields for the output file
        ordered_row = {
            'id': row['id'],
            'state': row.get('state', ''),
            'city': row.get('city', ''),
            'population': row.get('population', ''),
            'latitude': row.get('latitude', ''),
            'longitude': row.get('longitude', '')
        }
        
        # Write the processed row to the output file
        writer.writerow(ordered_row)

print(f'Processing complete. The result has been saved to {output_file}.')
