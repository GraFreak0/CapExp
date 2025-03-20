import json
import sqlite3
import requests
import pandas as pd
from fpdf import FPDF
from configparser import ConfigParser

# API Handler: Fetch Data
def fetch_data():
    config = ConfigParser()
    config.read('config.properties')
    username = config.get('API', 'username')
    password = config.get('API', 'password')
    
    url = "https://api.example.com/data"
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

# Database Handler: Store Data
def store_data(data):
    conn = sqlite3.connect('temp_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            response_data TEXT
        )
    """)
    cursor.execute("INSERT INTO transactions (response_data) VALUES (?)", (json.dumps(data),))
    conn.commit()
    conn.close()

# Exporter Functions
def export_to_csv():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT response_data FROM transactions", conn)
    df.to_csv('data.csv', index=False)
    conn.close()

def export_to_excel():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT response_data FROM transactions", conn)
    df.to_excel('data.xlsx', index=False)
    conn.close()

def export_to_pdf():
    conn = sqlite3.connect('temp_data.db')
    df = pd.read_sql_query("SELECT response_data FROM transactions", conn)
    conn.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index, row in df.iterrows():
        pdf.multi_cell(200, 10, txt=row["response_data"], align='L')
    pdf.output("data.pdf")

# Main Execution
def main():
    """Main function to fetch data and export in chosen format."""
    print("Fetching data from API...")
    fetch_data()
    print("Data successfully fetched and stored in SQLite.")
    
    while True:
        print("Choose an export format:")
        print("1 - CSV")
        print("2 - Excel")
        print("3 - PDF")
        choice = input("Enter the number corresponding to your choice: ")
        
        if choice == "1":
            export_to_csv()
            print("Data exported to data.csv")
            break
        elif choice == "2":
            export_to_excel()
            print("Data exported to data.xlsx")
            break
        elif choice == "3":
            export_to_pdf()
            print("Data exported to data.pdf")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
