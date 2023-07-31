from carlo.sheet import Sheet
from carlo import keychain
import json

def projects_sheet(page):
	return Sheet(keychain.keys()["projects_sheet_id"], page=page)

def app_sheet(app_id, page):
    project_app_items = list(filter(lambda item: item["app_id"] == app_id, projects_sheet("apps").items))
    app_sheet_id = project_app_items[0]["app_sheet_url"].split("/")[-1]
    return Sheet(app_sheet_id, page=page)

def compose_app_id(project_id, platform):
    return f"{project_id}.{platform}"
