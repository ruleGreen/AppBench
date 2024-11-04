# coding: utf-8
from utils import *

class Events:
    def __init__(self):
        self.desc = {
            "desc": "find and book tickets to any cultural events in your area",
            "base_required_arguments": {},
            "APIs": {
                "findevents": {
                    "desc": "find cultural events - concerts and plays - happening in a city",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "event_type (str)": "type of cultural event, value can only be Music or Theater",
                        "city (str)": "city where the event is taking place"
                    },
                    "optional_arguments": {
                        "date (date)": "date of event, the format follows yyyy-mm-dd"
                    },
                    "result_arguments": {
                        "event_type (str)": "type of cultural event, value can only be Music or Theater",
                        "event_name": "name of artist or play",
                        "date (date)": "date of event, the format follows yyyy-mm-dd",
                        "time (time)": "start time of event, the format follows hh:mm",
                        "price_per_ticket (float)": "price of each ticket",
                        "city (str)": "city where the event is taking place",
                        "venue (str)": "exact venue of event",
                        "venue_address (str)": "street address of event venue"
                    }
                },
                "buyeventtickets": {
                    "desc": "buy tickets for a cultural event and date in a given city",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "event_name (str)": "name of artist or play",
                        "number_of_tickets (int)": "number of tickets to reserve for the event",
                        "date (date)": "date of event, the format follows yyyy-mm-dd",
                        "city (str)": "city where the event is taking place"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "event_name (str)": "name of artist or play",
                        "date (date)": "date of event, the format follows yyyy-mm-dd",
                        "time (time)": "start time of event, the format follows hh:mm",
                        "number_of_tickets (int)": "number of tickets to reserve for the event",
                        "price_per_ticket (float)": "price of each ticket",
                        "city (str)": "city where the event is taking place",
                        "venue (str)": "exact venue of event",
                        "venue_address (str)": "street address of event venue"
                    }
                }
            }
        }




    

