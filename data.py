import os
import logging
import pandas as pd  # type: ignore


# CPI file path
CPI_PATH: str = "CPI_time_series_September_2023.xlsm"

# Path to GDP excel file
GDP_PATH: str = "R_GDP National Accounts 2022_r.xls"

# read the CPI excel file
CPI_EXCEL_FILE: pd.DataFrame | None = None
if os.path.exists(CPI_PATH):
    CPI_EXCEL_FILE = pd.read_excel(CPI_PATH, sheet_name=None)
    logging.info('CPI file loaded...')

# read the GDP excel file
GDP_EXCEL_FILE = None
if os.path.exists(GDP_PATH):
    GDP_EXCEL_FILE = pd.read_excel(GDP_PATH, sheet_name='Table A', skiprows=2,
                                   usecols=lambda x: True if 'Unnamed:' not in str(x) else False)
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.dropna()
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.set_index("Years")
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.T.reset_index()
    GDP_EXCEL_FILE.columns = [col.strip() for col in GDP_EXCEL_FILE.columns]

    # Rename the column
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.rename(columns={'index': 'Years'})
    logging.info('GDP file loaded...')


# read cpi metadata
def cpi_read_metadata(sheet_name):
    data = pd.read_excel(CPI_PATH, sheet_name=sheet_name)
    metadata = data.iloc[:3, 3].dropna().tolist()
    return metadata


# Function to load the data based on the sheet name of the cpi file
def cpi_load_data(sheet_name):
    data = pd.read_excel(CPI_PATH, sheet_name=sheet_name, skiprows=3)
    data = data.iloc[:, 3:]  # Skip the first 3 columns
    data_cleaned = data.dropna(how='all')
    items_list = data_cleaned["Unnamed: 3"].unique().tolist()
    return data_cleaned, items_list


CURRENT_LANG = "en"


# GDP for all countries
data1 = pd.read_csv("gdp_data.csv")
data2 = pd.read_csv("country_codes.csv")
GDP_FOR_ALL_COUNTRY = pd.merge(data1, data2, on="country_code")
GDP_years = sorted(GDP_FOR_ALL_COUNTRY['year'].unique())
