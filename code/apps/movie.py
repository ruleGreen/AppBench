# coding: utf-8
from utils import *

class Movies:
    def __init__(self):
        self.desc = {
            "desc": "a go-to provider for finding movies, searching for show times and booking tickets",
            "base_required_arguments": {},
            "APIs": {
                "buymovietickets": {
                    "desc": "buy movie tickets for a particular show",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "movie_name (str)": "name of the movie",
                        "number_of_tickets (int)": "number of the movie tickets to be purchased",
                        "show_date (date)": "date of the show, the format follows yyyy-mm-dd",
                        "location (str)": "city where the theatre is located",
                        "show_time (time)": "time of the show, the format follows hh:mm",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax"
                    },
                    "optional_arguments": {},
                    "result_arguments": {
                        "price (float)": "price per ticket",
                        "number_of_tickets (int)": "number of the movie tickets to be purchased",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax",
                        "theater_name (str)": "name of the theatre",
                        "show_time (time)": "time of the show, the format follows hh:mm",
                        "show_date (date)": "date of the show, the format follows yyyy-mm-dd",
                        "genre (str)": "genre of the movie",
                        "street_address (str)": "address of the theatre",
                        "location (str)": "city where the theatre is located",
                        "movie_name (str)": "name of the movie"
                    }
                },
                "findmovies": {
                    "desc": "search for movies by location, genre or other attributes",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "location (str)": "city where the theatre is located"
                    },
                    "optional_arguments": {
                        "theater_name (str)": "name of the theatre",
                        "genre (str)": "genre of the movie",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax"
                    },
                    "result_arguments": {
                        "price (float)": "price per ticket",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax",
                        "theater_name (str)": "name of the theatre",
                        "genre (str)": "genre of the movie",
                        "street_address (str)": "address of the theatre",
                        "location (str)": "city where the theatre is located",
                        "movie_name (str)": "name of the movie"
                    }
                },
                "gettimesformovie": {
                    "desc": "get show times for a movie at a location on a given date",
                    "is_transactional": False,
                    "additional_required_arguments": {
                        "movie_name (str)": "name of the movie",
                        "location (str)": "city where the theatre is located",
                        "show_date (date)": "date of the show, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {
                        "theater_name (str)": "name of the theatre",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax"
                    },
                    "result_arguments": {
                        "price (float)": "price per ticket",
                        "show_type (str)": "type of show, value can only be one of follows: regular, 3d or imax",
                        "theater_name (str)": "name of the theatre",
                        "show_time (time)": "time of the show, the format follows hh:mm",
                        "show_date (date)": "date of the show, the format follows yyyy-mm-dd",
                        "genre (str)": "genre of the movie",
                        "street_address (str)": "address of the theatre",
                        "location (str)": "city where the theatre is located",
                        "movie_name (str)": "name of the movie"
                    }
                },
                "reviewmovies": {
                    "desc": "find out interesting movies that you like",
                    "is_transactional": False,
                    "additional_required_arguments": {},
                    "optional_arguments": {
                        "directed_by (str)": "director of the movie",
                        "genre (str)": "type of the movie",
                        "cast (str)": "actors in the movie"
                    },
                    "result_arguments": {
                        "movie_title (str)": "name of the movie",
                        "genre (str)": "type of the movie",
                        "percent_rating (float)": "average critic percentage rating",
                        "cast (str)": "actors in the movie",
                        "directed_by (str)": "director of the movie"
                    }
                }
            }
        }


