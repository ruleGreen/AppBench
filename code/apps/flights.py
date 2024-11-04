# coding: utf-8
from utils import *

class Flights:
    def __init__(self):
        self.desc = {
            "desc": "find cheap flights in seconds and book flights",
            "base_required_arguments": {},
            "APIs": {
                "searchonewayflight": {
                    "desc": "search for one way flights to the destination",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "origin_airport (str)": "the name of the airport or city to depart from",
                        "destination_airport (str)": "the name of the airport or city to arrive at",
                        "departure_date (date)": "start date of the trip, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "seating_class (str)": "the cabin seat option, value can only be Economy or Premium Economy or Business",
                        "number_of_tickets (int)": "the number of flight tickets for the trip",
                        "airlines (str)": "the company that provides air transport services"
                    },
                    "result_arguments": {
                        "number_of_tickets (int)": "the number of flight tickets for the trip",
                        "seating_class (str)": "the cabin seat option, value can only be Economy or Premium Economy or Business",
                        "origin_airport (str)": "the name of the airport or city to depart from",
                        "destination_airport (str)": "the name of the airport or city to arrive at",
                        "departure_date (date)": "start date of the trip, the format follows yyyy-mm-dd",
                        "is_nonstop (bool)": "whether the flight is a direct one",
                        "outbound_departure_time (time)": "departure time of the flight flying to the destination, the format follows hh:mm",
                        "outbound_arrival_time (time)": "arrival time of the flight flying to the destination, the format follows hh:mm",
                        "price (float)": "the total cost of the flight tickets",
                        "airlines (str)": "the company that provides air transport services"
                    }
                },
                "searchroundtripflights": {
                    "desc": "search for roundtrip flights for the trip",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "origin_airport (str)": "the name of the airport or city to depart from",
                        "destination_airport (str)": "the name of the airport or city to arrive at",
                        "departure_date (date)": "start date of the trip, the format follows yyyy-mm-dd",
                        "return_date (date)": "end date of the trip, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "seating_class (str)": "the cabin seat option, value can only be Economy or Premium Economy or Business",
                        "number_of_tickets (int)": "the number of flight tickets for the trip",
                        "airlines (str)": "the company that provides air transport services"
                    },
                    "result_arguments": {
                        "number_of_tickets (int)": "the number of flight tickets for the trip",
                        "seating_class (str)": "the cabin seat option, value can only be Economy or Premium Economy or Business",
                        "origin_airport (str)": "the name of the airport or city to depart from",
                        "destination_airport (str)": "the name of the airport or city to arrive at",
                        "departure_date (date)": "start date of the trip, the format follows yyyy-mm-dd",
                        "return_date (date)": "end date of the trip, the format follows yyyy-mm-dd",
                        "is_nonstop (bool)": "whether the flight is a direct one",
                        "outbound_departure_time (time)": "departure time of the flight flying to the destination, the format follows hh:mm",
                        "outbound_arrival_time (time)": "arrival time of the flight flying to the destination, the format follows hh:mm",
                        "inbound_arrival_time (time)": "arrival time of the flight coming back from the trip, the format follows hh:mm",
                        "inbound_departure_time (time)": "departure time of the flight coming back from the trip, the format follows hh:mm",
                        "price (float)": "the total cost of the flight tickets",
                        "airlines (str)": "the company that provides air transport services, value can be only be one of the follows: United Airlines, American Airlines, Delta Airlines, Southwest Airlines, Alaska Airlines, British Airways, Air Canada, Air France, South African Airways, LOT Polish Airlines or LATAM Brasil"
                    }
                }
            }
        }




