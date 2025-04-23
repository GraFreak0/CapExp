from functions import fetch_data, export_to_excel

def main():
    """Main function to fetch data and prompt for export."""
    print("Fetching data from API...")
    # Example date range, can be modified or made dynamic
    start_date = "2025-03-01"
    end_date = "2025-03-31"
    fetch_data(start_date=start_date, end_date=end_date)
    print("Data successfully fetched and stored in SQLite.")
    export_to_excel()
    print("Data exported to data.xlsx")

if __name__ == "__main__":
    main()