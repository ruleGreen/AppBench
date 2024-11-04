# coding: utf-8
from utils import *

class Restaurants:
    def __init__(self):
        self.desc = {
            "desc": "a popular restaurant search and reservation service",
            "base_required_arguments": {},
            "APIs": {
                "reserverestaurant": {
                    "desc": "make a table reservation at a restaurant",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "restaurant_name (str)": "name of the restaurant",
                        "location (str)": "city where the restaurant is located",
                        "time (time)": "tentative time of restaurant reservation, the format follows hh:mm"
                    },
                    "optional_arguments": {
                        "number_of_seats (int)": "number of seats to reserve at the restaurant",
                        "date (date)": "tentative date of restaurant reservation, the format follows yyyy-mm-dd"
                    },
                    "result_arguments": {
                        "restaurant_name (str)": "name of the restaurant",
                        "date (date)": "tentative date of restaurant reservation, the format follows yyyy-mm-dd",
                        "time (time)": "tentative time of restaurant reservation, the format follows hh:mm",
                        "has_seating_outdoors (bool)": "whether the restaurant has outdoor seating available",
                        "has_vegetarian_options (bool)": "whether the restaurant has adequate vegetarian options",
                        "phone_number (str)": "phone number to contact restaurant",
                        "rating (float)": "average user rating for restaurant on a scale of 5",
                        "address (str)": "address of restaurant",
                        "number_of_seats (int)": "number of seats to reserve at the restaurant",
                        "price_range (str)": "price range for the restaurant, value can only be one of follows: cheap, moderate, pricey or ultra high-end",
                        "location (str)": "city where the restaurant is located",
                        "category (str)": "the category of food offered by the restaurant"
                    }
                },
                "findrestaurants": {
                    "desc": "find restaurants by location and by category",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "category (str)": "the category of food offered by the restaurant",
                        "location (str)": "city where the restaurant is located"
                    },
                    "optional_arguments": {
                        "price_range (str)": "price range for the restaurant, value can only be one of follows: cheap, moderate, pricey or ultra high-end",
                        "has_vegetarian_options (bool)": "whether the restaurant has adequate vegetarian options",
                        "has_seating_outdoors (bool)": "whether the restaurant has outdoor seating available"
                    },
                    "result_arguments": {
                        "restaurant_name (str)": "name of the restaurant",
                        "has_seating_outdoors (bool)": "whether the restaurant has outdoor seating available",
                        "has_vegetarian_options (bool)": "whether the restaurant has adequate vegetarian options",
                        "phone_number (str)": "phone number to contact restaurant",
                        "rating (float)": "average user rating for restaurant on a scale of 5",
                        "address (str)": "address of restaurant",
                        "price_range (str)": "price range for the restaurant, value can only be one of follows: cheap, moderate, pricey or ultra high-end",
                        "location (str)": "city where the restaurant is located",
                        "category (str)": "the category of food offered by the restaurant"
                    }
                }
            }
        }

