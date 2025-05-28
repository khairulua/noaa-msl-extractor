# NOAA MSL Extractor

A Python script to batch-extract **Mean Sea Level (MSL)** datum values from NOAA Tides & Currents for a list of station IDs stored in an Excel file.

## 🚀 Features

- Reads station names (and embedded NOAA IDs) from an Excel sheet  
- Fetches each station’s datum page via HTTP & parses the HTML  
- Gracefully handles missing tables or missing MSL rows  
- Outputs a CSV with station name, MSL value, and status  

## 📋 Prerequisites

- Python 3.7 or newer  
- Install Python packages:
  ```bash
  pip install pandas openpyxl requests beautifulsoup4

🔧 Installation
git clone https://github.com/<your-username>/noaa-msl-extractor.git
cd noaa-msl-extractor

⚙️ Usage
Open msl_extractor.py and update the three path constants at the top:

EXCEL_PATH   = r"path/to/stations_lat_lon.xlsx"
SHEET_NAME   = "YourSheetName"
OUT_CSV_PATH = r"path/to/output_msl.csv"

Run the script:
python msl_extractor.py
Check the generated CSV for MSL values and statuses.

🤝 Contributing
Feel free to open issues or submit pull requests!

If you need NAVD88 or other datums, you can extend the fetch_msl_for_station function.
