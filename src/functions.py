import json
import sqlite3
import requests
import pandas as pd
from fpdf import FPDF
from config_handler import get_credentials, get_api_url
import os
from datetime import datetime

# API Handler: Fetch Data
def fetch_data():
    username, password = get_credentials()
    url = get_api_url()
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "data": {
            "hostHeaderInfo": {
                "affiliateCode": "ENG",
                "departmentName": "Enterprise Report and Business Intelligence Team",
                "requester": "Johnson Isaiah"
            }
        }
    }
    
    response = requests.post(url, auth=(username, password), json=payload, headers=headers)
    if response.status_code == 200:
        store_data(response.json())
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Database Handler: Store Structured Data
def store_data(data):
    conn = sqlite3.connect('temp_data.db')
    cursor = conn.cursor()

    # Ensure data is a dictionary
    if isinstance(data, list):
        records = data  # If it's a list, assume it directly contains transaction records
    elif isinstance(data, dict):
        records = data.get("data", {}).get("transactions", [])
    else:
        print("Unexpected API response format.")
        return

    if not records:
        print("No transaction records found in API response.")
        return

    # Dynamically get column names from the first record
    column_names = records[0].keys()

    # Create table dynamically
    columns_def = ", ".join([f"{col} TEXT" for col in column_names])
    create_table_query = f"CREATE TABLE IF NOT EXISTS transactions ({columns_def})"
    cursor.execute(create_table_query)

    # Insert data
    placeholders = ", ".join(["?" for _ in column_names])
    insert_query = f"INSERT INTO transactions ({', '.join(column_names)}) VALUES ({placeholders})"

    for record in records:
        values = [str(record[col]) for col in column_names]
        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()

# Helper Function: Generate output path
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

# Exporter Functions
def export_to_csv():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    file_path = get_output_path("data.csv")
    df.to_csv(file_path, index=False)
    conn.close()

def export_to_excel():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    file_path = get_output_path("data.xlsx")
    df.to_excel(file_path, index=False)
    conn.close()

def export_to_pdf():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    file_path = get_output_path("data.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for index, row in df.iterrows():
        row_text = " | ".join(str(value) for value in row)
        pdf.multi_cell(200, 10, txt=row_text, align='L')

    pdf.output(file_path)
