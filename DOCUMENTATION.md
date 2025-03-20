# API Data Fetch and Export - Documentation

## Project Overview
This application fetches data from an API, stores it in SQLite, and exports it as CSV, Excel, or PDF.

## Architecture
- `config/config.properties` - Stores API credentials.
- `src/main.py` - Runs the application.
- `src/config_handler.py` - Reads credentials from the configuration file.
- `src/functions.py` - Contains API requests, SQLite operations, and export functions.

## API Request
- HTTP Method: POST
- Authorization: Basic Auth
- Payload:
  ```json
  {
      "data": {
          "hostHeaderInfo": {
              "affiliateCode": "Your Affiliate",
              "departmentName": "Your Department Name",
              "requester": "Your Name"
          }
      }
  }

## How It Works
- The application reads API credentials from config.properties.
- Sends a POST request with the predefined payload.
- Stores the API response in an SQLite table.
- Prompts the user to choose an export format.
- Generates a CSV, Excel, or PDF file.

## Running the Application
```bash
python main.py
```

