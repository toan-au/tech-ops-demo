# Import our deps
from dotenv import load_dotenv
import gspread
from pyairtable import Api
import os

# Load our secret keys / environment variables
load_dotenv()

dataset = "spotify_alltime_top100_songs"

# Authenticate gspread
gc = gspread.service_account()

# Open sheet
spread_sheet_name = "tech-ops-test-sheet"
work_sheet_name = dataset

sh = gc.open(spread_sheet_name)
work_sheet = sh.worksheet(work_sheet_name)

# Test connection
print(work_sheet.get('A1'))

# Authenticate pyairtable
api = Api(os.environ['AIRTABLE_ACCESS_TOKEN'])
base_id = os.environ['AIRTABLE_BASE_ID']


table_name = dataset
base = api.base(base_id)
table_exists = False

for table in base.tables():
    if table_name == table.name:
        table_exists = True
        
# Migrate dataset to airtable if the table doesn't exist
if table_exists:
    raise SystemExit("Stop here: Table already exists")


# Create an Airtable schema for our dataset
fields = [
    {"name": "alltime_rank", "type": "number", "options": {"precision": 0}},
    {"name": "song_title", "type": "singleLineText"},
    {"name": "artist", "type": "singleLineText"},
    {"name": "total_streams_billions", "type": "number", "options": {"precision": 2}},
    {"name": "primary_genre", "type": "singleLineText"},
    {"name": "bpm", "type": "number", "options": {"precision": 0}},
    {"name": "release_year", "type": "number", "options": {"precision": 0}},
    {"name": "artist_country", "type": "singleLineText"},
    {"name": "explicit", "type": "checkbox", "options": {"icon": "check", "color": "redBright"}},
    {"name": "danceability", "type": "number", "options": {"precision": 2}},
    {"name": "energy", "type": "number", "options": {"precision": 2}},
    {"name": "valence", "type": "number", "options": {"precision": 2}},
    {"name": "acousticness", "type": "number", "options": {"precision": 2}},
    {"name": "dataset_part", "type": "singleLineText"},
]

table = base.create_table(name=table_name, fields=fields)

# Since we know our dataset only has 100 rows we'll just grab them all at once
records = work_sheet.get_all_records()

# Clean the 'explicit' column to be python True False instead of string
for record in records:
    record['explicit'] = True if record['explicit'] == 'TRUE'else False

# Migrate!
table.batch_create(records)
    