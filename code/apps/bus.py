# coding: utf-8
from utils import *

class Buses:
    def __init__(self):
        self.desc = {
            "desc": "affordable and comfortable bus travel across the country",
            "base_required_arguments": {},
            "APIs": {
                "findbus": {
                    "desc": "search for a bus itinerary between two places on a certain date",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "from_city (str)": "the city to depart from",
                        "to_city (str)": "the destination city of the trip",
                        "departure_date (date)": "the date of departure, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "num_passengers (int)": "the number of tickets for the trip",
                        "category (str)": "how many stops the route has"
                    },
                    "result_arguments": {
                        "from_city (str)": "the city to depart from",
                        "to_city (str)": "the destination city of the trip",
                        "from_station (str)": "name of station of departure",
                        "to_station (str)": "name of station of arrival",
                        "departure_date (date)": "the date of departure, the format follows yyyy-mm-dd",
                        "departure_time (time)": "the time of departure, the format follows hh:mm",
                        "price (float)": "ticket price per passenger",
                        "num_passengers (int)": "the number of tickets for the trip",
                        "category (str)": "how many stops the route has"
                    }
                },
                "buybusticket": {
                    "desc": "purchase the bus tickets",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "from_city (str)": "the city to depart from",
                        "to_city (str)": "the destination city of the trip",
                        "departure_date (date)": "the date of departure, the format follows yyyy-mm-dd",
                        "departure_time (time)": "the time of departure, the format follows hh:mm",
                        "num_passengers (int)": "the number of tickets for the trip"
                    },
                    "optional_arguments": {
                        "additional_luggage (bool)": "whether to carry excess baggage in the bus"
                    },
                    "result_arguments": {
                        "from_city (str)": "the city to depart from",
                        "to_city (str)": "the destination city of the trip",
                        "from_station (str)": "name of station of departure",
                        "to_station (str)": "name of station of arrival",
                        "departure_date (date)": "the date of departure, the format follows yyyy-mm-dd.",
                        "departure_time (time)": "the time of departure, the format follows hh:mm",
                        "price (float)": "ticket price per passenger",
                        "additional_luggage (bool)": "whether to carry excess baggage in the bus",
                        "num_passengers (int)": "the number of tickets for the trip",
                        "category (str)": "how many stops the route has"
                    }
                }
            }
        }


