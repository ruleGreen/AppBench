# coding: utf-8
import os
from utils import *

class Trip:
    def __init__(self, user_name , user_password):
        self.desc = {
            "desc": "This app is used to manage the trip of a user, including searching for flights and trains, buying and canceling tickets, etc.",
            "base_required_arguments": {  # base required arguments for almost all functions in this app
                "user_name (str)": "the name of user",
                "user_password (str)": "the password of user"
            },
            "APIs": {
                "search_flight": {
                    "desc": "search for flights based on departure, destination and departure date",
                    "additional_required_arguments": {
                        "departure (str)": "the departure of the flight",
                        "destination (str)": "the destination of the flight",
                        "departure_date (date)": "the departure date of the flight, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "flight (dict)": "the flight information"
                    }
                },
                "buy_flight_ticket": {
                    "desc": "buy a flight ticket",
                    "additional_required_arguments": {
                        "flight_number (str)": "the flight number"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "status (str)": "the status of the operation"
                    }
                },
                "cancel_flight_ticket": {
                    "desc": "cancel a flight ticket",
                    "additional_required_arguments": {
                        "flight_number (str)": "the flight number"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "status (str)": "the status of the operation"
                    }
                },
                "search_train": {
                    "desc": "search for trains based on departure, destination and departure date",
                    "additional_required_arguments": {
                        "departure (str)": "the departure of the train",
                        "destination (str)": "the destination of the train",
                        "departure_date (date)": "the departure date of the train, the format follows yyyy-mm-dd"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "train (dict)": "the train information"
                    }
                },
                "buy_train_ticket": {
                    "desc": "buy a train ticket",
                    "additional_required_arguments": {
                        "train_number (str)": "the train number"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "status (str)": "the status of the operation"
                    }
                },
                "cancel_train_ticket": {
                    "desc": "cancel a train ticket",
                    "additional_required_arguments": {
                        "train_number (str)": "the train number"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "status (str)": "the status of the operation"
                    }

                
                }
            }
        }

        self.user_name = user_name
        self.user_password = user_password
        if self.user_name is None or self.user_password is None:
            print(f"An error occurred: user name or password is not valid")
            return False
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "trip_data.json")
            success,data=read_json(file_path)
            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                   
                    self.flight_tickets = user['flight_tickets']
                    self.train_tickets = user['train_tickets']
                return None
            
    def search_flight(self, departure, destination, departure_date):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path1 = os.path.join(current_directory, "..", "database", "trip_product_data.json")
            success1,data1=read_json(file_path1)
            if success1:
                for flight in data1["flight"]:
                    if flight["from"] == departure and flight["to"] == destination and flight["date"] == departure_date:
                        print(f"Flight found: {flight}")
                        return flight
                print(f"No flight found for the given information")
                return None

    def buy_flight_ticket(self,flight_number):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data=read_json(file_path)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "trip_product_data.json")
        success1,data1=read_json(file_path1)
        if success1:
            for flight in data1["flight"]:
                if flight["flightNumber"] == flight_number:
                    self.flight_tickets.append(flight)

        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                #self.flight_tickets["status"] = "booked"
                user['flight_tickets'] = self.flight_tickets
                save_json(file_path, data)
            else:
                print(f"An error occurred: user name or password is not valid")
                return False
   
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data2=read_json(file_path)
        for user2 in data2["users"]:
            for flight in user2["flight_tickets"]:
                    if flight["flightNumber"] == flight_number:
                        index=user2["flight_tickets"].index(flight)
                        print(index)
                        user2["flight_tickets"][index]["status"]="booked"
                        save_json(file_path, data2)
                        print(f"Flight ticket bought successfully: {flight_number}")
                        return True
                   
            
        
    def cancel_flight_ticket(self, flight_number):
        index=0
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data2=read_json(file_path)
        for user2 in data2["users"]:
            for flight in user2["flight_tickets"]:
                    if flight["flightNumber"] == flight_number:
                        index=user2["flight_tickets"].index(flight)
                        user2["flight_tickets"][index]["status"]="cancelled"
                        save_json(file_path, data2)
                        print(f"Flight ticket cancelled successfully: {flight_number}")
                        return True
                    
    def search_train(self, departure, destination, departure_date):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path1 = os.path.join(current_directory, "..", "database", "trip_product_data.json")
            success1,data1=read_json(file_path1)
            if success1:
                for train in data1["train"]:
                    if train["from"] == departure and train["to"] == destination and train["date"] == departure_date:
                        print(f"Train found: {train}")
                        return train
                print(f"No train found for the given information")
                return None  
            
    def buy_train_ticket(self,train_number):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data=read_json(file_path)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "trip_product_data.json")
        success1,data1=read_json(file_path1)
        if success1:
            for train in data1["train"]:
                if train["trainNumber"] == train_number:
                    self.train_tickets.append(train)

        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                #self.flight_tickets["status"] = "booked"
                user['train_tickets'] = self.train_tickets
                save_json(file_path, data)
            else:
                print(f"An error occurred: user name or password is not valid")
                return False
        index=0
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data2=read_json(file_path)
        for user2 in data2["users"]:
            for train in user2["train_tickets"]:
                    if train["trainNumber"] == train_number:
                        index=user2["train_tickets"].index(train)
                        print(index)
                        user2["train_tickets"][index]["status"]="booked"
                        save_json(file_path, data2)
                        print(f"Train ticket bought successfully: {train_number}")
                        return True           
        
    def cancel_train_ticket(self, train_number):
        index=0
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(current_directory, "..", "database", "trip_data.json")
        success,data2=read_json(file_path)
        for user2 in data2["users"]:
            for train in user2["train_tickets"]:
                    if train["trainNumber"] == train_number:
                        index=user2["train_tickets"].index(train)
                        user2["train_tickets"][index]["status"]="cancelled"
                        save_json(file_path, data2)
                        print(f"Train ticket cancelled successfully: {train_number}")
                        return True

    
    
    
   
if __name__ == "__main__":
    trip = Trip("xiyuanhao", "123456")
    #trip.search_flight("shanghai", "beijing", "2024-04-13")
   # trip.buy_flight_ticket("MU1235")
   # trip.cancel_flight_ticket("MU1235")
   # trip.search_train("shanghai", "beijing", "2024-04-13")
   # trip.buy_train_ticket("G336")
   # trip.cancel_train_ticket("G336")