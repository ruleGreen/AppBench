from datetime import date
from utils import *

class Weather:
    def __init__(self):
        self.desc = {
            "desc": "check the weather for any place and any date",
            "base_required_arguments": {},
            "APIs": {
                "getweather": {
                    "desc": "get the weather of a certain location on a date",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "city (str)": "name of the city"
                    },
                    "optional_arguments": {
                        "date (date)": "date for the weather, the format follows yyyy-mm-dd"
                    },
                    "result_arguments": {
                        "precipitation (str)": "the possibility of rain or snow in percentage",
                        "humidity (str)": "percentage humidity",
                        "wind (str)": "wind speed in miles per hour",
                        "temperature (float)": "temperature in fahrenheit",
                        "city (str)": "name of the city",
                        "date (date)": "date for the weather, the format follows yyyy-mm-dd"
                    }
                }
            }
        }


        