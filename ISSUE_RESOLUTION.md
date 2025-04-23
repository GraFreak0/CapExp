# Issue Resolution Documentation

## Issue Description
The user reported two main issues:
1. The data being pulled by `test/main.py` and `src/main.py` used different API URLs and contained different data.
2. The date filter used in the API request was not working dynamically in the code, although it worked fine in Postman. The code was fetching all data from the dev API ignoring the date filter.

## Root Cause Analysis
- The difference in API URLs was due to `src/config_handler.py` and `test/config_handler.py` reading from different configuration files (`config/config.properties` vs `config/config-test.properties`) and different sections (`[API]` vs `[testAPI]`).
- The date filter was hardcoded in the `fetch_data` function in both `src/functions.py` and `test/functions.py`, causing the API request to always use the same fixed date range regardless of user input.

## Changes Made

### 1. `src/functions.py`
- Modified the `fetch_data` function to accept `start_date` and `end_date` parameters.
- Updated the API request payload to use these parameters instead of hardcoded dates.
- This allows dynamic date filtering when fetching data.

### 2. `src/main.py`
- Updated the call to `fetch_data` to pass example `start_date` and `end_date` parameters.
- This demonstrates how to use the updated `fetch_data` function with dynamic dates.

### 3. `test/functions.py`
- Made the same changes as in `src/functions.py` to accept date parameters and update the payload accordingly.

### 4. `test/main.py`
- Updated the call to `fetch_data` to pass example `start_date` and `end_date` parameters.

## Summary
These changes ensure that:
- The correct API URLs are used based on the environment (dev or test) via different config files.
- The date filter is applied dynamically in the API requests, matching the behavior tested in Postman.
- The user can now specify date ranges when running the data fetch scripts.

## Next Steps
- Optionally, enhance the scripts to accept date parameters from CLI arguments or configuration files for more flexibility.
- Test the changes with different date ranges to verify correct filtering of data.
