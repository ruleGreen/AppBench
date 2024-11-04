import datetime
import json
import os
from apps.utils import read_json, save_json

class Calendar:

    def __init__(self):
        """
        Initialize the CalendarApp object.
        """
        self.desc = {
            "desc": "an APP which can add and view events for a specific date",
            "base_required_arguments": {
                "date (date)": "The date to view events for in the format 'yyyy-mm-dd'"
            },
            "APIs": {
                "show_current_date": {
                    "desc": "display the current date",
                    "additional_required_arguments": {},
                    "results_arguments": {
                        "current_date (date)": "The current date in the format 'yyyy-mm-dd'"
                    }
                },
                "add_event": {
                    "desc": "add events for a specific date",
                    "additional_required_arguments": {
                        "date (date)": "The date to add events for in the format 'yyyy-mm-dd'",
                        "startTime (str)": "The start time of the event",
                        "endTime (str)": "The end time of the event",
                        "location (str)": "The location of the event",
                        "content (str)": "The content of the event"
                    },
                    "results_arguments": {
                        "success (bool)": "True if the event was added successfully, False otherwise",
                        "message (str)": "A message indicating the result of the add event operation"
                    }
                },
                "view_events": {
                    "desc": "view events for a specific date",
                    "additional_required_arguments": {
                        "date (date)": "The date to view events for in the format 'yyyy-mm-dd'"
                    },
                    "results_arguments": {
                        "success (bool)": "True if the events were retrieved successfully, False otherwise",
                        "list (list)": "A list of events for the specified date"
                    }
               
           
                }
            }
        }
        self.events = {}

    def show_current_date(self):
        """
        Display the current date.
        """
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        print(f"Current Date: {current_date}")
        return current_date

    def add_event(self, date,startTime,endTime, location, content):
     
        
        msg={"date":date,"startTime":startTime,"endTime":endTime,"location":location,"content":content}
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "calendar_data.json")
        success,data=read_json(file_path)
        #print(data)
        if startTime< datetime.datetime.now().strftime("%Y-%m-%d"):
            print("Cannot add event to a past date")
            return False, "Cannot add event to a past date"
        elif content == "":
            print("Event description cannot be empty")
            return False, "Event description cannot be empty"
        elif location == "":
            print("Event location cannot be empty")
            return False, "Event location cannot be empty"
        elif startTime == "":
            print("Date cannot be empty")
            return False, "Date cannot be empty"
        elif endTime == "":
            print("Date cannot be empty")
            return False, "Date cannot be empty"
        else:
            data["event"].append(msg)
            save_json(file_path,data)
        print(f"Event added on {startTime} to {endTime} at {location}: {content}")
        return True, f"Event added on {startTime} to {endTime} at {location}: {content}"
    


    def view_events(self, date):
        """
        View events for a specific date.

        Parameters:
        - date (str): The date to view events for in the format 'YYYY-MM-DD'.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "calendar_data.json")
        success,data=read_json(file_path)
        events = data["event"]
       # print(events)
        list=[]
        for event in events:
            #print(event["date"])
            if date == event["date"]:
                print(f"Event on {event['date']}:from {event['startTime']} to {event['endTime']} at {event['location']}: {event['content']}")
                list.append(event)
        if len(list) == 0:
            print(f"No events found for {date}")
            return False, f"No events found for {date}"
        else:
            return True, list
            
            
                
        
if __name__ == "__main__":
    # Example usage:

    calendar_app = Calendar()

    # Display the current date
    calendar_app.show_current_date()

    # Add events
    #calendar_app.add_event('2024-03-20','2024-03-20 15:08:00', '2024-03-20 16:08:00', 'Supermarket', 'To buy some food')
    #calendar_app.delete_event('2024-01-21', 'Birthday Party')

    # View events for a specific date
    calendar_app.view_events('2024-03-20')

