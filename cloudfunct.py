import csv
import os
import psycopg2
from google.cloud import storage

def load_csv_to_db(event, context):
    """Triggered by a change to a Cloud Storage bucket."""
    file_name = event['name']
    bucket_name = event['bucket']

    # Initialize a storage client and connect to the database
    storage_client = storage.Client()
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST']
    )
    cursor = conn.cursor()

    # Download file from bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()

    # Read and process the CSV file
    invalid_records = []
    reader = csv.DictReader(data.splitlines())

    for row in reader:
        try:
            # Validate and insert each row into the database
            if validate_row(row, file_name, cursor):
                insert_into_db(cursor, row, file_name)
            else:
                invalid_records.append(row)
        except Exception as e:
            # Log or store the error and the invalid row
            print(f"Error processing row {row}: {e}")
            invalid_records.append(row)

    # Commit transactions and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    # Optionally, handle the invalid records (e.g., log them, store in another file)
    handle_invalid_records(invalid_records)

def validate_row(row, file_name, cursor):
    # Check for mandatory fields based on the file type
    if 'products.csv' in file_name:
        return validate_product_row(row)
    elif 'inventory.csv' in file_name:
        return validate_inventory_row(row)
    elif 'markdown_plans.csv' in file_name:
        return validate_markdown_plan_row(row, cursor)
    elif 'sales_data.csv' in file_name:
        return validate_sales_data_row(row)
    else:
        return False

def validate_product_row(row):
    return all(key in row and row[key] for key in ['UPC', 'Cost', 'RegularPrice'])

def validate_inventory_row(row):
    return all(key in row and row[key] for key in ['ProductID', 'QuantityOnHand', 'Date'])

def validate_markdown_plan_row(row, cursor):
    if not all(key in row and row[key] for key in ['ProductID', 'StartDate', 'EndDate']):
        return False

    cursor.execute("""
        SELECT COUNT(*)
        FROM MarkdownPlan
        WHERE ProductID = %s AND NOT (
            StartDate > %s OR EndDate < %s
        )
    """, (row['ProductID'], row['EndDate'], row['StartDate']))

    overlap_count = cursor.fetchone()[0]
    return overlap_count == 0

def validate_sales_data_row(row):
    # Implement the necessary validation for sales data
    # Placeholder - replace with actual validation logic
    return True

def insert_into_db(cursor, row, file_name):
    if 'products.csv' in file_name:
        insert_product_data(cursor, row)
    elif 'inventory.csv' in file_name:
        insert_inventory_data(cursor, row)
    elif 'markdown_plans.csv' in file_name:
        insert_markdown_plan_data(cursor, row)
    elif 'sales_data.csv' in file_name:
        insert_sales_data(cursor, row)

def insert_product_data(cursor, row):
    # Implement the insert logic for product data
    pass

def insert_inventory_data(cursor, row):
    # Implement the insert logic for inventory data
    pass

def insert_markdown_plan_data(cursor, row):
    # Implement the insert logic for markdown plan data
    pass

def insert_sales_data(cursor, row):
    # Implement the logic to insert sales data
    # Refer to the earlier example for detailed implementation
    pass

def handle_invalid_records(records):
    # Implement logic to handle invalid records
    # For example, log to a file or print them
    pass

# Additional helper functions can be added here
