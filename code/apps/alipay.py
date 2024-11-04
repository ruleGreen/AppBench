import datetime
import json
import os
from utils import read_json, save_json

class Alipay:
    def __init__(self, user_name, user_password):
        """
        Initialize the AlipaySimulator with a starting balance.

        Parameters:
        - balance (float): The initial balance in the user's account.
        """
        self.desc = {
            "desc": "an APP which can transfer money  with others",
            "base_required_arguments": {
                "user_name (str)": "the name of user",
                "user_password (str)": "the password of user"
            },
            "APIs": {
                "check_bill": {
                    "desc": "check the transaction history",
                    "additional_required_arguments": {},
                    "results_arguments": {
                        "success (bool)": "True if the transaction history was retrieved successfully, False otherwise",
                        "bill (list)": "A list of transaction records,from: The sender of the bill, to: The recipient of the bill, billAmount: The amount of the bill, billPaidDate: The date and time when the bill was paid, billDeadline: The deadline for the bill payment, billStatus: The status of the bill"
                    }
                },
                "transfer": {
                    "desc": "transfer money to others",
                    "additional_required_arguments": {
                        "target_user_name (str)": "the name of the target user",
                        "transfer_amount (float)": "the amount of money to transfer"
                    },
                    "results_arguments": {
                        "success (bool)": "True if the transfer was successful, False otherwise",
                        "message (str)": "A message indicating the result of the transfer operation"
                    }
                }
            }
        }
        
        # load user name and password
        self.user_name = user_name
        self.user_password = user_password
        if self.user_name is None or self.user_password is None:
            print(f"An error occurred: user name or password is not valid")
            return False
        else:
            # load other data from database according to user name and password
            
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "alipay_data.json")
            success,data=read_json(file_path)
            # print(json_file_path)
            print(data)
            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.amount = user['amount']
                    self.bill = user['bill']
                return None

    def transfer(self, target_user_name, transfer_amount):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "alipay_data.json")
        success, data = read_json(file_path)

        for user in data["users"]:
            if user["username"] == self.user_name :
               
                msg={"from":self.user_name,"to":target_user_name,"billAmount":transfer_amount,"billPaidDate":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"billDeadline":" ","billStatus":"paid"}
                
                if self.amount >= transfer_amount:
                    self.amount =self.amount-transfer_amount
                    user["amount"] = user["amount"]-transfer_amount
                    print(f"Transfer {transfer_amount} to {target_user_name}, now the amount is {self.amount}")
                    user["bill"].append(msg)
                    for user1 in data["users"]:
                        if user1["username"] == target_user_name :
                            if  self.amount >= transfer_amount:
                                user1["amount"] =user1["amount"]+transfer_amount
                                print(f"recieve {transfer_amount} from {target_user_name}, now the amount is {user1['amount']}")
                                user1["bill"].append(msg)
                                save_json(file_path,data)
                    
                    return True, f"Transfer {transfer_amount} to {target_user_name}, now the amount is {self.amount}"
                    
                else:
                    return False, f"An error occurred: {target_user_name} is not in the contact list or the amount is not enough"

    def check_bill(self):
        """
        Check the transaction history.

        Returns:
        - success (bool): True if the transaction history was retrieved successfully, False otherwise.
        - bill (list): A list of transaction records.
        """
        print("Transaction History:")
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "alipay_data.json")
      
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name :
                for transaction in user["bill"]:
                    print(transaction)
                return True, user["bill"]


if __name__ == "__main__":
    alipay = Alipay("xiyuanhao", "123")
    #alipay.transfer("zhangsan", 10)
    alipay.check_bill()
