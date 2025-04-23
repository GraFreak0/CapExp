from datetime import datetime, timedelta
from functions_auto import fetch_data, export_to_excel

today = datetime.today()
first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d")
last_day_last_month = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")

def main():
    print("Fetching data from API...")
    start_date = first_day_last_month
    end_date = today.strftime("%Y-%m-%d")
    affiliate_code = "ENG"
    department_name = "Enterprise Report and Business Intelligence Team"
    requester = "Johnson Isaiah"
    fetch_data(start_date=start_date, end_date=end_date, affiliate_code=affiliate_code, department_name=department_name, requester=requester)
    print("Data successfully fetched and stored in SQLite.")
    export_to_excel()
    print("Data exported to data.xlsx")

if __name__ == "__main__":
    main()