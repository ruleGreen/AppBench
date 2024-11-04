# coding: utf-8
from utils import *

class Travel:
    def __init__(self):
        self.desc = {
            "desc": "the biggest database of tourist attractions and points of interest",
            "base_required_arguments": {},
            "APIs": {
                "findattractions": {
                    "desc": "browse attractions in a given city",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "location (str)": "city or town where the attraction is located"
                    },
                    "optional_arguments": {
                        "free_entry (bool)": "boolean flag indicating whether entrance to attraction is free",
                        "category (str)": "category to which the attraction belongs, value can only be one of follows: Place of Worship, Theme Park, Museum, Historical Landmark, Park, Tourist Attraction, Sports Venue, Shopping Area, Performing Arts Venue, or Nature Preserve",
                        "good_for_kids (bool)": "boolean flag indicating whether attraction is good for to take kids to"
                    },
                    "result_arguments": {
                        "location (str)": "city or town where the attraction is located",
                        "attraction_name (str)": "common name of the attraction",
                        "category (str)": "category to which the attraction belongs, value can only be one of follows: Place of Worship, Theme Park, Museum, Historical Landmark, Park, Tourist Attraction, Sports Venue, Shopping Area, Performing Arts Venue, or Nature Preserve",
                        "phone_number (str)": "phone number to contact the attraction",
                        "free_entry (bool)": "boolean flag indicating whether entrance to attraction is free",
                        "good_for_kids (bool)": "boolean flag indicating whether attraction is good for to take kids to"
                    }
                }
            }
        }

