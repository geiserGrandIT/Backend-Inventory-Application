from .models import Item, Division, Category, Audit, Order, FlaggedItems
from oauth2client.service_account import ServiceAccountCredentials
import os, gspread
async def update_google_sheet():
    creds = await get_credentials()
    client = await create_client(creds)
    modelsData = await fetch_model_data()

    pass

async def update_db_from_sheet():
    pass

async def post_google_sheet():
    pass

async def fetch_google_sheet():
    pass

async def get_credentials() -> dict:
    result = {}
    try:
        with open("./settings.cfg") as f:
            lines = f.readlines()
            for line in lines:
                l = line.split("=")
                result[l[0]] = result[l[1]]
        return result
    except Exception as e:
        print(f"Something went wrong while fetching credentials: {e}")
        return {}
    
async def fetch_model_data() -> list:
    result = []
    header = Item._meta.fields
    print(header)
    items = []
    for instance in Item.objects.all():
        items += [getattr(instance, field.name) for field in Item._meta.fields]
    result.append(header)
    result.append(items)
    return result

async def create_client(conf: dict) -> gspread.Client:
    creds = ServiceAccountCredentials.from_json_keyfile_name(conf["CREDS"], conf["SCOPE"])
    current_directory = os.getcwd()
    filename=os.path.join(current_directory, conf["CREDS"])
    client = gspread.service_account(filename=filename)
    return client