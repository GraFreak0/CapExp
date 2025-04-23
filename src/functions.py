import os
import json
import sqlite3
import requests
import pandas as pd
from datetime import datetime
from config_handler import get_credentials, get_api_url

def fetch_data(start_date=None, end_date=None):
    username, password = get_credentials()
    url = get_api_url()
    print(url)
    
    headers = {"Content-Type": "application/json"}
    if not start_date:
        start_date = "2025-03-01"
    if not end_date:
        end_date = "2025-03-31"
    payload = {
        "data": {
            "hostHeaderInfo": {
            "affiliateCode": "ENG",
            "departmentName": "Enterprise Report and Business Intelligence Team",
            "requester": "Johnson Isaiah",
            "startDate" : start_date,
            "endDate" : end_date
            }
        }
    }
    
    response = requests.post(url, auth=(username, password), json=payload, headers=headers)
    if response.status_code == 200:
        store_data(response.json())
    else:
        print(f"Failed to fetch data: {response.status_code}")

def store_data(data):
    conn = sqlite3.connect('temp_data_prod.db')
    cursor = conn.cursor()

    # Handle different response formats
    if isinstance(data, list):  
        records = data
    elif isinstance(data, dict):
        records = data.get("data", [])
        if isinstance(records, dict):
            records = records.get("transactions", [])
    else:
        print("Unexpected API response format.")
        return

    if not records:
        print("No transaction records found in API response.")
        return

    # Extract column names dynamically
    column_names = records[0].keys()

    # Create table if not exists
    columns_def = ", ".join([f"{col} TEXT" for col in column_names])
    create_table_query = f"CREATE TABLE IF NOT EXISTS transactions ({columns_def})"
    cursor.execute(create_table_query)

    # Insert data into table
    placeholders = ", ".join(["?" for _ in column_names])
    insert_query = f"INSERT INTO transactions ({', '.join(column_names)}) VALUES ({placeholders})"

    for record in records:
        values = [str(record.get(col, '')) for col in column_names]  # Use .get(col, '') to handle missing keys
        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()


def get_output_path(filename):
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")
    
    output_dir = os.path.join("output", year, month, day)
    os.makedirs(output_dir, exist_ok=True)
    
    count = 1
    file_path = os.path.join(output_dir, filename)
    while os.path.exists(file_path):
        name, ext = os.path.splitext(filename)
        file_path = os.path.join(output_dir, f"{name}_{count}{ext}")
        count += 1
    
    return file_path

def export_to_excel():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT DISTINCT * FROM transactions", conn)
    file_path = get_output_path("data.xlsx")
    df.to_excel(file_path, index=False)
    conn.close()