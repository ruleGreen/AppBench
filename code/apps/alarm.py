class Alarm:
    def __init__(self):
        self.desc = {
            "desc": "manage alarms by getting and setting them easily",
            "base_required_arguments": {},
            "APIs": {
                "getalarms": {
                    "desc": "get the alarms user has already set",
                    "is_transactional": False,
                    "additional_required_arguments": {},
                    "optional_arguments": {},
                    "result_arguments": {
                        "alarm_time (str)": "time of the alarm",
                        "alarm_name (str)": "name of the alarm"
                    }
                },
                "addalarm": {
                    "desc": "set a new alarm",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "new_alarm_time (str)": "time to set for the new alarm"
                    },
                    "optional_arguments": {
                        "new_alarm_name (str)": "name to use for the new alarm"
                    },
                    "result_arguments": {
                        "new_alarm_time (str)": "time to set for the new alarm",
                        "new_alarm_name (str)": "name to use for the new alarm"
                    }
                }
            }
        }

    def getalarms(self):
        alarm_time, alarm_name = [], []
        return alarm_time, alarm_name
    
    def addalarm(self, new_alram_time, new_alarm_name="new alarm"):
        new_alarm_time, new_alarm_name = new_alram_time, new_alarm_name
        return new_alarm_time, new_alarm_name

