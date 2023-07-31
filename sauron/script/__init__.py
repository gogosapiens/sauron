import json, os, importlib
import sauron

def project():
    with open("_project-apps.json", 'r') as file:
        app_items = json.load(file)
    return Project(app_items)

def app():
    with open("_script-app.json", 'r') as file:
        app_item = json.load(file)
    return App(app_item)

def common_data():
    with open("../../common-data.json", "r") as f:
        user_input = json.load(f)
    return user_input

def input_parameters():
    with open("_script-input.json", 'r') as file:
        return json.load(file)
    
def worker():
    return input_parameters()["_worker"]
    
def set_output(output):
    with open("_script-output.json", "w") as f:
        json.dump(output, f)

def code_extensions(extensions_path):
    module_files = os.listdir(extensions_path)
    extensions_folder = extensions_path.split("/")[-1]
    modules = {}
    for file_name in module_files:
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            module = importlib.import_module(f"{extensions_folder}.{module_name}")
            modules[module_name] = module
    return modules

class App:
    app_item = {}
    id = ""

    def fields(self):
        return self.app_item
    
    def platform(self):
        return self.fields()["platform"]

    def __init__(self, app_item):
        self.app_item = app_item
        self.id = app_item["app_id"]

    def platform_fields(self):
        return json.loads(self.app_item["platform_fields"])
    
    def set_platform_fields(self, fields):
        projects_sheet = sauron.projects_sheet("apps")
        self.app_item["platform_fields"] = json.dumps(fields)
        projects_sheet.set_item_value(self.app_item, fields, key="platform_fields")

    def sheet(self, page):
        return sauron.app_sheet(self.id, page)

class Project:
    app_items = []
    id = ""

    def __init__(self, app_items):
        self.app_items = app_items
        self.id = app_items[0]["project_id"]

    def app_id(self, platform):
        return f"{self.id}.{platform}"

    def user_input(self):
        return json.loads(self.app_items[0]["user_input"])
    
    def platform_fields(self, platform):
        app_id = self.app_id(platform)
        app_item = list(filter(lambda item: item["app_id"] == app_id, self.app_items))[0]
        return json.loads(app_item["platform_fields"])
    
    def set_platform_fields(self, fields, platform):
        app_id = self.app_id(platform)
        projects_sheet = sauron.projects_sheet("apps")
        app_item = list(filter(lambda item: item["app_id"] == app_id, projects_sheet.items))[0]
        projects_sheet.set_item_value(app_item, fields, key="platform_fields")

    def apps(self):
        return self.app_items

    def app_sheet(self, platform, page):
        return sauron.app_sheet(self.app_id(platform), page)

    def store_url(self, platform, placement, source=None, campaign=None):
        if platform != "ios":
            assert(False)

        platforms = self.user_input()["platforms"]
        app_store_id = self.platform_fields()[platform]["app_store_id"]
        domain = None
        if "blog" in platforms.keys():
            domain = platforms["blog"]["domain"]
        
        url = f'https://apps.apple.com/us/app/id{app_store_id}?utm_medium={placement}'
        if source:
            url += f'&utm_source={source}'
        if domain:
            url += f'&utm_campaign={domain}'
        return url