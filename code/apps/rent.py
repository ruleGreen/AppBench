# coding: utf-8
from utils import *

class Rents:
    def __init__(self):
        self.desc = {
            "desc": "a leading global provider of car rental solutions",
            "base_required_arguments": {},
            "APIs": {
                "getcarsavailable": {
                    "desc": "discover cars available for rent in a certain location and period",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "city (str)": "city where you want to rent the car",
                        "start_date (date)": "the first date to start using the rental car, the format follows yyyy-mm-dd.",
                        "pickup_time (time)": "time for the pick-up, the format follows hh:mm",
                        "end_date (date)": "the date to return the car, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "car_type (str)": "type of the car, value can only be one of follows: Hatchback, Sedan or SUV"
                    },
                    "result_arguments": {
                        "car_type (str)": "type of the car, value can only be one of follows: Hatchback, Sedan or SUV",
                        "car_name (str)": "car model",
                        "pickup_location (str)": "place to pick up the car",
                        "start_date (date)": "the first date to start using the rental car, the format follows yyyy-mm-dd",
                        "pickup_time (time)": "time for the pick-up, the format follows hh:mm",
                        "city (str)": "city where you want to rent the car",
                        "end_date (date)": "the date to return the car, the format follows yyyy-mm-dd",
                        "price_per_day (int)": "the cost for renting the car per day"
                    }
                },
                "reservecar": {
                    "desc": "make a rental car reservation",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "pickup_location (str)": "place to pick up the car",
                        "start_date (date)": "the first date to start using the rental car, the format follows yyyy-mm-dd",
                        "pickup_time (time)": "time for the pick-up, the format follows hh:mm",
                        "end_date (date)": "the date to return the car, the format follows yyyy-mm-dd",
                        "car_type (str)": "type of the car, value can only be one of follows: Hatchback, Sedan or SUV",
                        "add_insurance (bool)": "whether to purchase insurance, True or False"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "car_type": "type of the car, value can only be one of follows: Hatchback, Sedan or SUV",
                        "car_name": "car model",
                        "pickup_location": "place to pick up the car",
                        "start_date": "the first date to start using the rental car",
                        "pickup_time": "time for the pick-up",
                        "end_date": "the date to return the car",
                        "price_per_day": "the cost for renting the car per day",
                        "add_insurance": "whether to purchase insurance"
                    }
                },
                "getride": {
                    "desc": "book a cab for any destination, number of seats and ride type",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "destination (str)": "destination address or location for cab",
                        "number_of_seats (int)": "number of seats to reserve in the cab",
                        "ride_type (str)": "type of cab ride"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "destination": "destination address or location for cab",
                        "ride_type": "type of cab ride, value can only be one of follows: Pool, Regular or Luxury",
                        "ride_fare": "total fare for cab ride",
                        "wait_time": "expected waiting time for pick-up by cab",
                        "number_of_seats": "number of seats to reserve in the cab"
                    }
                }
            }
        }
