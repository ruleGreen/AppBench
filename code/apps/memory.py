# coding: utf-8
from utils import *

class Memory:
    def __init__(self):
        self.desc = {
            "desc": "a memory database which store all personal information about the users such as preferences and personal traits",
            "base_required_arguments": {},
            "APIs": {
                "search_memory": {
                    "desc": "search related user memory/persona according to the query",
                    "is_transactional": False,
                    "additional_required_arguments": {},
                    "optional_arguments": {},
                    "result_arguments": {
                        "memory (str)": "related memory snippets of users"
                    }
                },
            }
        }

    def delete_memory(self, note):
        pass

    def add_memory(self, note):
        pass

    def search_memory(self, query):
        
        pass