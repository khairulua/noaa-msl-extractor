"""
Created on 2025-05-28

by: Md Khairul Amin
Coastal Hydrology Lab,
The University of Alabama
"""

# Step 1: Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Step 2: User-configurable paths
EXCEL_PATH = r"path\to\stations_lat_lon.xlsx"    # input Excel with “Station Name” column
SHEET_NAME = "Gulf"                                        # Excel sheet to read
OUT_CSV_PATH = r"path\to\MSL_values_from_NOAA.csv"  # where to save results

def fetch_msl_for_station(fullname: str) -> float:
    """
    Given a full station name like 'annapolis-8575512-usa-noaa',
    extract the 7-digit ID, fetch its NOAA datum page, and return MSL value.
    Returns None if no table or no MSL row is found.
    """
    # extract station ID via regex
    m = re.search(r"-(\d+)-usa-noaa$", fullname)
    if not m:
        return None
    stnid = m.group(1)
    url = f"https://tidesandcurrents.noaa.gov/datums.html?datum=MHHW&units=1&epoch=0&id={stnid}"
    
    # fetch page
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # find all <table> elements
    tables = soup.find_all('table')
    if not tables:
        return None
    
    # loop through rows of the first table looking for 'MSL'
    for row in tables[0].find_all('tr'):
        cols = [td.get_text(strip=True) for td in row.find_all(['th','td'])]
        if cols and cols[0] == 'MSL':
            try:
                return float(cols[1])
            except ValueError:
                return None
    return None

def main():
    # 1) Load station list
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    
    # 2) Loop and collect results
    records = []
    for fullname in df["Station Name"]:
        msl = fetch_msl_for_station(fullname)
        status = "OK" if msl is not None else "Missing"
        print(f"{fullname}: MSL = {msl} → {status}")
        records.append({
            "Station Name": fullname,
            "MSL Value": msl,
            "Status": status
        })
    
    # 3) Save to CSV
    out_df = pd.DataFrame(records)
    out_df.to_csv(OUT_CSV_PATH, index=False)
    print(f"\nAll done! Results saved to:\n{OUT_CSV_PATH}")

if __name__ == "__main__":
    main()
