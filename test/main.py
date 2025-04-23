from functions_auto import fetch_data, export_to_excel

def main():
    """Main function to fetch data and prompt for export."""
    print("Fetching data from API...")
    fetch_data()
    print("Data successfully fetched and stored in SQLite.")
    export_to_excel()
    print("Data exported to data.xlsx")

if __name__ == "__main__":
    main()