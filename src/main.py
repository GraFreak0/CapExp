from functions import fetch_data, export_to_csv, export_to_excel, export_to_pdf

def main():
    """Main function to fetch data and prompt for export."""
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