# coding: utf-8
from utils import *

class Trains:
    def __init__(self):
        self.desc = {
            "desc": "service to find and reserve train journeys between cities",
            "base_required_arguments": {},
            "APIs": {
                "gettraintickets": {
                    "desc": "reserve tickets for train journey",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "from (str)": "starting city for train journey",
                        "to (str)": "ending city for train journey",
                        "date_of_journey (date)": "date of train journey, the format follows yyyy-mm-dd",
                        "journey_start_time (time)": "time of start of train journey, the format follows hh:mm",
                        "number_of_adults (int)": "number of adults to reserve train tickets for",
                        "trip_protection (bool)": "whether to add trip protection to reservation, for a fee"
                    },
                    "optional_arguments": {
                        "class (str)": "fare class for train reservation, value can only be one of follows: Value, Flexible or Business"
                    },
                    "result_arguments": {
                        "from (str)": "starting city for train journey",
                        "to (str)": "ending city for train journey",
                        "from_station (str)": "name of station at starting city",
                        "to_station (str)": "name of station at ending city",
                        "date_of_journey (date)": "date of train journey, the format follows yyyy-mm-dd",
                        "journey_start_time (time)": "time of start of train journey, the format follows hh:mm",
                        "total (float)": "total price of train reservation",
                        "number_of_adults (int)": "number of adults to reserve train tickets for",
                        "class (str)": "fare class for train reservation, value can only be one of follows: Value, Flexible or Business",
                        "trip_protection (bool)": "whether to add trip protection to reservation, for a fee"
                    }
                },
                "findtrains": {
                    "desc": "find trains to a given destination city",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "from (str)": "starting city for train journey",
                        "to (str)": "ending city for train journey",
                        "date_of_journey (date)": "date of train journey, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "class (str)": "fare class for train reservation, value can only be one of follows: Value, Flexible or Business",
                        "number_of_adults (int)": "number of adults to reserve train tickets for"
                    },
                    "result_arguments": {
                        "from (str)": "starting city for train journey",
                        "to (str)": "ending city for train journey",
                        "from_station (str)": "name of station at starting city",
                        "to_station (str)": "name of station at ending city",
                        "date_of_journey (date)": "date of train journey, the format follows yyyy-mm-dd",
                        "journey_start_time (time)": "time of start of train journey, the format follows hh:mm",
                        "total (float)": "total price of train reservation",
                        "number_of_adults (int)": "number of adults to reserve train tickets for",
                        "class (str)": "fare class for train reservation, value can only be one of follows: Value, Flexible or Business",
                        "trip_protection (bool)": "whether to add trip protection to reservation, for a fee"
                    }
                }
            }
        }


