from apps.hotels import Hotels
from apps.weather import Weather
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

import json

class App:
    def __init__(self):
        self.desc = {
            "desc": "",
            "APIs": {}
        }
        
        self.apis = self.read_all_apis()

    def get_api_by_name(self, name: str):
        """
        Gets the API with the given name.

        Parameters:
        - name (str): the name of the API to get.

        Returns:
        - api (dict): the API with the given name.
        """
        for api in self.apis:
            if api['name'] == name:
                return api
        raise Exception('invalid tool name.')
    
    def get_api_description(self, name: str):
        """
        Gets the description of the API with the given name.

        Parameters:
        - name (str): the name of the API to get the description of.

        Returns:
        - desc (str): the description of the API with the given name.
        """
        api_info = self.get_api_by_name(name).copy()
        api_info.pop('class')
        if 'init_database' in api_info:
            api_info.pop('init_database')
        return json.dumps(api_info)


    def init_tool(self, tool_name: str, *args, **kwargs):
        """
        Initializes a tool with the given name and parameters.

        Parameters:
        - tool_name (str): the name of the tool to initialize.
        - args (list): the positional arguments to initialize the tool with.
        - kwargs (dict): the parameters to initialize the tool with.

        Returns:
        - tool (object): the initialized tool.
        """
        if tool_name in self.inited_tools:
            return self.inited_tools[tool_name]
        # Get the class for the tool
        api_class = self.get_api_by_name(tool_name)['class']
        temp_args = []

        if 'init_database' in self.get_api_by_name(tool_name):
            # Initialize the tool with the init database
            temp_args.append(self.get_api_by_name(tool_name)['init_database'])
        
        if tool_name != 'CheckToken' and 'token' in self.get_api_by_name(tool_name)['input_parameters']:
            temp_args.append(self.token_checker)

        args = temp_args + list(args)
        tool = api_class(*args, **kwargs)

        self.inited_tools[tool_name] = tool
        return tool