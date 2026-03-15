# Tech Ops Demo
## Sheets => Airtable Table migration

This Tech demo shows the migration from Google Sheet to an Airtable table using:
* Python3
* pyairtable
* gspread

## Usage

* This demo assumes there the google service account json exists in the default location
* `~/.config/gspread/service_account.json`

1. Install dependencies `pip i gspread pyairtable dotenv`
2. Create a .env file in the project root `touch .env`
3. Add these 2 keys into .env and add your keys:
```
AIRTABLE_ACCESS_TOKEN= 
AIRTABLE_BASE_ID=
```
4. run the ipynb `jupyter notebook data_migration.ipynb`
5. OR `python migrate.py`
