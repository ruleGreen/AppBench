# coding: utf-8
import sys; sys.path.append("./")
from apps.hotels import Hotels
from apps.weather import Weather
from apps.meituan import Meituan
from apps.home import Homes
from apps.movie import Movies
from apps.train import Trains
from apps.event import Events
from apps.travel import Travel
from apps.media import Media
from apps.bus import Buses
from apps.restaurant import Restaurants
from apps.services import Services
from apps.rent import Rents
from apps.alarm import Alarm
from apps.wechat import WeChat
from apps.flights import Flights
from apps.music import Music
from apps.payment import Payment # WeChat / Alipay
from utils import *

class Mobile:
    def __init__(self):
        self.desc = {
            "Apps": self.list_all_apps,
            "base_required_arguments": {},
            "APIs": {
                "list_all_apps": {
                    "desc": "list all apps in the mobile phone",
                    "additional_required_arguments": {},
                    "optional_arguments": {},
                    "results_arguments": {
                        "app_list (list)": "a list of all apps in the mobile phone"
                    }
                },
                "search_app": {
                    "desc": "",
                    "additional_required_arguments": {},
                    "optional_arguments": {},
                    "results_arguments": {}
                }
            }
        }
        self.app_list = ["Hotels", "Rents", "Buses", "Events", "Flights", "Homes", "Media", "Movies", "Music", "Payment", "Restaurants", "Services", \
                "Trains", "Travel", "Weather"]
        self.app_api_list = self.list_all_app_apis()
        self.flat_apps_apis_desc = flat_apps_apis(self.app_list, self.app_api_list)
        self.flat_apps_desc_test = flat_apps_apis(self.app_list, self.app_api_list, True)
        
        print("Welcome to the AppBench, a virtual mobile phone environment!!!")

    def init_env(self):
        self.progress_state = {}
        self.last_api_name = ""
        self.last_api_name = ""
        self.current_api_name = ""
        self.current_app_name = ""
        self.confirmed_apis_list = {}
        self.global_arguments = {}
        self.db_path = "./database/all_database.json"
    
    def list_all_apps(self):
        # initial all apps
        return self.app_list
    
    def list_all_apis(self, apps_name=None):
        api_list = []
        if apps_name is not None:
            for app_name in apps_name:
                apis_desc = self.find_api_according_to_app(app_name)
                api_list.extend(list(apis_desc.keys()))
        else:
            for app_name in self.app_list:
                apis_desc = self.find_api_according_to_app(app_name)
                api_list.extend(list(apis_desc.keys()))
        return api_list

    def list_all_app_apis(self, apps_name=None):
        app_api_list = []
        if apps_name is not None:
            for app_name in apps_name:
                current_app = eval(app_name)()
                app_desc = current_app.desc
                app_api_list.append(app_desc)
        else:
            for app_name in self.app_list:
                current_app = eval(app_name)()
                app_desc = current_app.desc
                app_api_list.append(app_desc)
        return app_api_list

    def search_app(self, keywords):
        return []
    
    def find_app_according_to_api(self, api_name, visible_apps):
        for app_name in visible_apps:
            current_app = eval(app_name)()
            if api_name in current_app.desc["APIs"]:
                return app_name
        return "Do not find suitable App"

    def find_api_according_to_app(self, app_name):
        current_app = eval(app_name)()
        return current_app.desc["APIs"]
    
    def is_transactional_api(self, app_name, api_name):
        app = self.find_api_according_to_app(app_name)
        return app[api_name]["is_transactional"]

    def confirm_api_arguments(self, app_name, api_name, params):
        if not hasattr(self, "confirmed_apis_list"):
            self.confirmed_apis_list = {}

        if app_name not in self.confirmed_apis_list:
            self.confirmed_apis_list[app_name] = {}
        self.confirmed_apis_list[app_name][api_name] = params

    def confirmed_api_arguments(self, app_name, api_name, params):
        if not hasattr(self, "confirmed_apis_list"):
            return False
        
        if app_name in self.confirmed_apis_list:
            if api_name in self.confirmed_apis_list[app_name]:
                return params == self.confirmed_apis_list[app_name][api_name]
            else:
                return False
        else:
            return False
        
    def api_call(self, app_name, api_name, is_same=False, arguments={}):
        # is_same indicate whether or not the returned results same as returned in original SGD datasets, including the order information
        self.align_progress_state(app_name, api_name, arguments)
        self.current_app = eval(app_name)()
        if is_same:
            results = self.exact_api_call(app_name, api_name, arguments)
        else:
            results = eval("self.current_app.{api_name}".format(api_name=api_name))(**arguments)
            # results = eval("{app_name}.{api_name}".format(app_name=app_name, api_name=api_name))(**arguments)
        self.track_progress_state(app_name, api_name, results)
        if len(results) > 0:
            return results, "success"
        return results, "fail"
    
    def exact_api_call(self, app_name, api_name, arguments):
        raw_db = read_json(self.db_path)
        for sample in raw_db:
            if align_service_to_app(sample["app"]) == app_name and sample["api"]["method"].lower() == api_name and \
                approximate_match(sample["api"]["parameters"], arguments):
                return sample["database"]
        return []
    
    def track_progress_state(self, app_name, api_name, api_results):
        self.last_app_name = app_name
        self.last_api_name = api_name
        # save progress results to 1) bridge the gap between consecutive api calls; 2)
        if not hasattr(self, "progress_state"):
            self.progress_state = {}

        if app_name not in self.progress_state:
            self.progress_state[app_name] = {}
        self.progress_state[app_name][api_name] = api_results
        return self.progress_state
    
    def align_progress_state(self, app_name, api_name, arguments):
        self.current_app_name = app_name
        self.current_api_name = api_name
        global_arguments = {}  # save global arguments for debugging or future use
        
        if hasattr(self, "last_app_name") and hasattr(self, "last_api_name") and self.last_api_name != "":
            last_api_results = self.progress_state[self.last_app_name][self.last_api_name]

            if len(last_api_results) > 0:
                top1_result = last_api_results[0] # default as top-1 result
            
                for k,v in top1_result.items():
                    global_arguments[k] = v
            
                for k, v in arguments.items():
                    global_arguments[k] = v
                    if k in top1_result and (top1_result[k] in arguments[k] or arguments[k] in top1_result[k]):
                        arguments[k] = top1_result[k]
        
        else:
            for k, v in arguments.items():
                global_arguments[k] = v
            
        self.global_arguments = global_arguments
    
    def is_all_arguments_filled(self, app_name, api_name, arguments={}):
        try:
            current_app = eval(app_name)()
            apis = current_app.desc["APIs"]
            api_desc = apis[api_name]
        except:
            return True, []

        base_arguments_keys = [key.split(" ")[0] for key in current_app.desc["base_required_arguments"].keys()]
        additional_required_arguments_keys = [key.split(" ")[0] for key in api_desc["additional_required_arguments"].keys()]
        optional_arguments_keys = [key.split(" ")[0] for key in api_desc["optional_arguments"].keys()] # for personalization
        all_requried_keys = base_arguments_keys + additional_required_arguments_keys

        filled_keys, dont_filled_keys = [], []
        for key in all_requried_keys:
            if key in arguments and "?" not in arguments[key]:
                filled_keys.append(key)
            else:
                dont_filled_keys.append(key)
        
        if len(dont_filled_keys) > 0:
            return False, dont_filled_keys
        else:
            return True, dont_filled_keys

if __name__ == "__main__":
    mobile = Mobile()
    mobile.api_call("Rents", "getcarsavailable")
    

