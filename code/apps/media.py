# coding: utf-8
from utils import *

class Media:
    def __init__(self):
        self.desc = {
            "desc": "enjoy instant and unlimited access to best shows, movies, comedy, sports, documentaries and more.",
            "base_required_arguments": {},
            "APIs": {
                "findmovies": {
                    "is_transactional": False,
                    "desc": "explore movies online based on your preferences",
                    "additional_required_arguments": {
                        "genre (str)": "category of the content"
                    },
                    "optional_arguments": {
                        "starring (str)": "celebs acting in the movie"
                    },
                    "result_arguments": {
                        "title (str)": "title of the movie",
                        "genre (str)": "category of the content",
                        "subtitle_language (str)": "language of the subtitles, value can only be one of follows: English, Spanish, Hindi or French",
                        "starring (str)": "celebs acting in the movie"
                    }
                },
                "playmovie": {
                    "is_transactional": False,
                    "desc": "watch the movie instantly online with your preferred subtitles",
                    "additional_required_arguments": {
                        "title (str)": "title of the movie"
                    },
                    "optional_arguments": {
                        "subtitle_language (str)": "language of the subtitles, value can only be one of follows: English, Spanish, Hindi or French"
                    },
                    "result_arguments": {
                        "title (str)": "title of the movie",
                        "genre (str)": "category of the content",
                        "subtitle_language (str)": "language of the subtitles, value can only be one of follows: English, Spanish, Hindi or French",
                        "starring (str)": "celebs acting in the movie"
                    }
                }
            }
        }





