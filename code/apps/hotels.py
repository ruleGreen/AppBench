from utils import *

class Hotels:
    def __init__(self):
        self.desc = {
            "desc": "a popular service for searching and booking houses for short term stay",
            "base_required_arguments": {},
            "APIs": {
                "bookhouse": {
                    "desc": "book the selected house for given dates and number of adults",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "where_to (str)": "location of the house",
                        "number_of_adults (int)": "number of people for the reservation",
                        "check_in_date (date)": "start date for the reservation or to find the house, the format follows yyyy-mm-dd",
                        "check_out_date (date)": "end date for the reservation or to find the house, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "where_to (str)": "location of the house",
                        "number_of_adults (int)": "number of people for the reservation",
                        "check_in_date (date)": "start date for the reservation or to find the house, the format follows yyyy-mm-dd",
                        "check_out_date (date)": "end date for the reservation or to find the house, the format follows yyyy-mm-dd",
                        "rating (float)": "review rating of the house",
                        "address (str)": "address of the house",
                        "phone_number (str)": "phone number of the house",
                        "total_price (float)": "price per night of the house",
                        "has_laundry_service (bool)": "boolean flag indicating if the house has laundry service"
                    }
                },
                "searchhouse": {
                    "desc": "find a house at a given location",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "where_to (str)": "location of the house"
                    },
                    "optional_arguments": {
                        "has_laundry_service (bool)": "boolean flag indicating if the house has laundry service",
                        "number_of_adults (int)": "number of people for the reservation",
                        "rating (float)": "review rating of the house"
                    },
                    "result_arguments": {
                        "where_to (str)": "location of the house",
                        "number_of_adults (int)": "number of people for the reservation",
                        "rating (float)": "review rating of the house",
                        "address (str)": "address of the house",
                        "phone_number (str)": "phone number of the house",
                        "total_price (float)": "price per night of the house",
                        "has_laundry_service (bool)": "boolean flag indicating if the house has laundry service"
                    }
                }
            }
        }

      