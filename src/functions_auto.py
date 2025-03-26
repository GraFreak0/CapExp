import os
import json
import sqlite3
import calendar
import requests
import pandas as pd
from config_handler import get_credentials, get_api_url
from datetime import datetime, timedelta

def fetch_data():
    username, password = get_credentials()
    url = get_api_url()
    
    # Get the first and last day of the previous month
    today = datetime.today()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d")
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    last_day_last_month = last_day_last_month.strftime("%Y-%m-%d")

    headers = {"Content-Type": "application/json"}
    payload = {
        "data": {
            "hostHeaderInfo": {
                "affiliateCode": "ENG",
                "departmentName": "Enterprise Report and Business Intelligence Team",
                "requester": "Johnson Isaiah",
                "startDate": first_day_last_month,
                "endDate": last_day_last_month,
            }
        }
    }
    
    response = requests.post(url, auth=(username, password), json=payload, headers=headers)
    if response.status_code == 200:
        store_data(response.json())
    else:
        print(f"Failed to fetch data: {response.status_code}")

def store_data(data):
    conn = sqlite3.connect('temp_data.db')
    cursor = conn.cursor()

    # Handle different response formats
    if isinstance(data, list):  
        records = data  # Direct list of records
    elif isinstance(data, dict):
        records = data.get("data", [])  # Extract list from "data"
        if isinstance(records, dict):  # Handle nested structure like {"transactions": [...]}
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
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    file_path = get_output_path("data.xlsx")
    df.to_excel(file_path, index=False)
    conn.close()