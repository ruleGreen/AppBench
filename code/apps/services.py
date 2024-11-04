# coding: utf-8
from utils import *

class Services:
    def __init__(self):
        self.desc = {
            "desc": "a widely used service for finding and reserving the hair stylist of your choice, and also discover the right therapist for you and make reservations easily",
            "base_required_arguments": {},
            "APIs": {
                "book_stylist_appointment": {
                    "desc": "book an appointment at a hair stylist",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "stylist_name (str)": "name of the hair stylist/salon",
                        "appointment_time (time)": "time of the appointment, the format follows hh:mm",
                        "appointment_date (date)": "date for the appointment, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "stylist_name (str)": "name of the hair stylist/salon",
                        "phone_number (str)": "phone number of the stylist/salon",
                        "average_rating (float)": "average review rating for the stylist/salon",
                        "is_unisex (bool)": "boolean flag indicating if the salon is unisex",
                        "street_address (str)": "address of the stylist/salon",
                        "appointment_date (date)": "date for the appointment",
                        "appointment_time (time)": "time of the appointment, the format follows hh:mm"
                    }
                },
                "find_stylist_provider": {
                    "desc": "search for a hair stylist by city and optionally other attributes",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "city (str)": "city where the salon is located"
                    },
                    "optional_arguments": {
                        "is_unisex (bool)": "boolean flag indicating if the salon is unisex"
                    },
                    "result_arguments": {
                        "stylist_name (str)": "name of the hair stylist/salon",
                        "phone_number (str)": "phone number of the stylist/salon",
                        "average_rating (float)": "average review rating for the stylist/salon",
                        "is_unisex (bool)": "boolean flag indicating if the salon is unisex",
                        "street_address (str)": "address of the stylist/salon",
                        "city (str)": "city where the salon is located"
                    }
                },
                "book_therapist_appointment": {
                    "desc": "make a reservation with the therapist based on user's wish",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "therapist_name (str)": "name of the therapist",
                        "appointment_time (time)": "time of the appointment, the format follows hh:mm",
                        "appointment_date (date)": "date of the appointment, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "therapist_name (str)": "name of the therapist",
                        "phone_number (str)": "contact number of the therapist",
                        "address (str)": "address of the therapist",
                        "appointment_date (date)": "date of the appointment, the format follows yyyy-mm-dd",
                        "appointment_time (time)": "time of the appointment, the format follows hh:mm"
                    }
                },
                "find_therapist_provider": {
                    "desc": "discover therapist according to user's conditions",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "city (str)": "area where user wants to search for a therapist",
                        "type (str)": "type of the therapist, value can only be one of follows: Psychologist, Family Counselor or Psychiatrist"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "therapist_name (str)": "name of the therapist",
                        "phone_number (str)": "contact number of the therapist",
                        "address (str)": "address of the therapist",
                        "city (str)": "area where user wants to search for a therapist",
                        "type (str)": "type of the therapist, value can only be one of follows: Psychologist, Family Counselor or Psychiatrist"
                    }
                }
            }
        }



