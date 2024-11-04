# coding: utf-8
from utils import *

class Music:
    def __init__(self) -> None:
        self.desc = {
            "desc": "a free, personalized platform that plays music you'll love. discover new music and enjoy old favorites.",
            "base_required_arguments": {},
            "APIs": {
                "playmedia": {
                    "desc": "play the music",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "track (str)": "name of the song"
                    },
                    "optional_arguments": {
                        "artist (str)": "performer's name",
                        "device (str)": "place or name of the media player to play the song selected, value can only be one of follows: Living room, Kitchen or Patio",
                        "album (str)": "collection of the song"
                    },
                    "result_arguments": {
                        "track (str)": "name of the song",
                        "artist (str)": "performer's name",
                        "album (str)": "collection of the song",
                        "genre (str)": "type of the music",
                        "year (str)": "year when the song was first released, the format follows yyyy",
                        "device (str)": "place or name of the media player to play the song selected, value can only be one of follows: Living room, Kitchen or Patio"
                    }
                },
                "lookupmusic": {
                    "desc": "discover songs matching your taste",
                    "is_transactional": False,
                    "additional_required_arguments": {},
                    "optional_arguments": {
                        "artist (str)": "performer's name",
                        "album (str)": "collection of the song",
                        "genre (str)": "type of the music",
                        "year (str)": "year when the song was first released, the format follows yyyy"
                    },
                    "result_arguments": {
                        "track (str)": "name of the song",
                        "artist (str)": "performer's name",
                        "album (str)": "collection of the song",
                        "genre (str)": "type of the music",
                        "year (str)": "year when the song was first released, the format follows yyyy"
                    }
                }
            }
        }


