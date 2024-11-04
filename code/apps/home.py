# coding: utf-8
from utils import *

class Homes:
    def __init__(self):
        self.desc = {
            "desc": "service for finding properties to buy and rent",
            "base_required_arguments": {},
            "APIs": {
                "findhomebyarea": {
                    "desc": "search for a property to rent or buy in a given city",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "area (str)": "city where the property is located",
                        "intent (str)": "whether to buy or rent a property, value can only be rent or buy",
                        "number_of_beds (int)": "number of bedrooms in the property",
                        "number_of_baths (int)": "number of bathroom in the property"
                    },
                    "optional_arguments": {
                        "has_garage (bool)": "whether the property has a garage",
                        "in_unit_laundry (bool)": "whether the property has in-unit laundry facilities"
                    },
                    "result_arguments": {
                        "intent (str)": "whether to buy or rent a property, value can only be rent or buy",
                        "area (str)": "city where the property is located",
                        "address (str)": "street address of property",
                        "property_name (str)": "name of property or apartment complex",
                        "phone_number (int)": "contact number of property or apartment complex",
                        "has_garage (bool)": "whether the property has a garage",
                        "in_unit_laundry (bool)": "whether the property has in-unit laundry facilities",
                        "price (float)": "sale price or per-month rent of property",
                        "number_of_beds (int)": "number of bedrooms in the property",
                        "number_of_baths (int)": "number of bathroom in the property"
                    }
                },
                "schedulevisit": {
                    "desc": "schedule a visit to a property on a given date",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "property_name (str)": "name of property or apartment complex",
                        "visit_date (date)": "date for visit to the property, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "address (str)": "street address of property",
                        "property_name (str)": "name of property or apartment complex",
                        "phone_number (str)": "contact number of property or apartment complex",
                        "has_garage (bool)": "whether the property has a garage",
                        "in_unit_laundry (bool)": "whether the property has in-unit laundry facilities",
                        "price (float)": "sale price or per-month rent of property",
                        "visit_date (date)": "date for visit to the property, the format follows yyyy-mm-dd",
                        "number_of_beds (int)": "number of bedrooms in the property",
                        "number_of_baths (int)": "number of bathroom in the property"
                    }
                }
            }
        }


