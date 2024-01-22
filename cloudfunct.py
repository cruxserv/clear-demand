import csv
import os
from datetime import datetime
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
    
    # Validate and insert each row into the database
    for row in reader:
        try:
            cursor.execute("BEGIN;")  # Start a new transaction for each row
            if validate_row(row, file_name, cursor):
                insert_into_db(cursor, row, file_name)
            else:
                invalid_records.append(row)
                raise ValueError("Validation Failed")
            cursor.execute("COMMIT;")  # Commit if everything was successful
        except Exception as e:
            # Log or store the error and the invalid row
            print(f"Error processing row {row}: {e}")
            invalid_records.append(row)
            cursor.execute("ROLLBACK;")  # Rollback transaction on error

    # Close the connection
    cursor.close()
    conn.close()

    # Optionally, handle the invalid records (e.g., log them, store in another file)
    # handle_invalid_records(invalid_records)

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
    required_fields = ['UPC', 'Cost', 'RegularPrice']

    if not all(field in row and row[field] for field in required_fields):
        return False

    try:
        cost = float(row['Cost'])
        regular_price = float(row['RegularPrice'])
        if cost < 0 or regular_price < 0:
            return False
    except ValueError:
        return False

    return True

def validate_inventory_row(row):
    required_fields = ['ProductID', 'QuantityOnHand', 'Date']

    if not all(field in row and row[field] for field in required_fields):
        return False

    try:
        quantity_on_hand = int(row['QuantityOnHand'])
        if quantity_on_hand < 0:
            return False
    except ValueError:
        return False

    try:
        datetime.strptime(row['Date'], '%Y-%m-%d')
    except ValueError:
        return False

    return True


def validate_markdown_plan_row(row, cursor):
    required_fields = ['ProductID', 'StartDate', 'EndDate', 'InitialReduction', 'MidwayReduction', 'FinalReduction']

    if not all(field in row and row[field] for field in required_fields):
        return False

    try:
        datetime.strptime(row['StartDate'], '%Y-%m-%d')
        datetime.strptime(row['EndDate'], '%Y-%m-%d')
        initial_reduction = float(row['InitialReduction'])
        midway_reduction = float(row['MidwayReduction'])
        final_reduction = float(row['FinalReduction'])
        if not 0 <= initial_reduction <= 100 or not 0 <= midway_reduction <= 100 or not 0 <= final_reduction <= 100:
            return False
    except ValueError:
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
    required_fields = ['SalesDataID', 'ProductID', 'Date', 'UnitsSold', 'SellPrice']

    if not all(field in row and row[field] for field in required_fields):
        return False

    try:
        datetime.strptime(row['Date'], '%Y-%m-%d')
    except ValueError:
        return False

    try:
        units_sold = int(row['UnitsSold'])
        sell_price = float(row['SellPrice'])
        if units_sold < 0 or sell_price < 0:
            return False
    except ValueError:
        return False

    # Assuming ProductID is a numeric value
    try:
        int(row['ProductID'])
    except ValueError:
        return False

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

# Insert functions for each CSV file type

def insert_product_data(cursor, row):
    cursor.execute("INSERT INTO Product (ProductID, Description, Cost, RegularPrice) VALUES (%s, %s, %s, %s)",
                   (row['UPC'], row['Description'], row['Cost'], row['RegularPrice']))

def insert_inventory_data(cursor, row):
    cursor.execute("INSERT INTO Inventory (InventoryID, ProductID, QuantityOnHand, Date) VALUES (%s, %s, %s, %s)",
                   (row['InventoryID'], row['ProductID'], row['QuantityOnHand'], row['Date']))

def insert_markdown_plan_data(cursor, row):
    cursor.execute("INSERT INTO MarkdownPlan (MarkdownPlanID, ProductID, StartDate, EndDate, InitialReduction, MidwayReduction, FinalReduction) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (row['MarkdownPlanID'], row['ProductID'], row['StartDate'], row['EndDate'], row['InitialReduction'], row['MidwayReduction'], row['FinalReduction']))

def insert_sales_data(cursor, row):
    # Inserting SalesData and handling possible absence of MarkdownPlanID
    markdown_plan_id = row.get('MarkdownPlanID') if 'MarkdownPlanID' in row and row['MarkdownPlanID'] else None
    cursor.execute("INSERT INTO SalesData (SalesDataID, ProductID, MarkdownPlanID, Date, UnitsSold, SellPrice) VALUES (%s, %s, %s, %s, %s, %s)",
                   (row['SalesDataID'], row['ProductID'], markdown_plan_id, row['Date'], row['UnitsSold'], row['SellPrice']))
