# coding: utf-8

class Google:
    def __init__(self):
        self.desc = {
            "desc": "",
            "APIs": {
                "search_by_keyword": {
                    "additional_required_arguments": {
                        "keyword (str)": "keyword as query"
                    },
                    "results_arguments": {
                        "title": "",
                        "summary": "",
                    }
                }
            }
        }

    def search_by_keyword(self, query):
        pass
