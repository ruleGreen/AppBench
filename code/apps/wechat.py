import json
import os
from apps.utils import read_json,save_json

class WeChat:
    def __init__(self, user_name="user", user_password="password"):
        self.desc = {
            "desc": "an APP which can transfer money and chat with others",
            "base_required_arguments": {  # base required arguments for almost all functions in this app
                "user_name (str)": "the name of user",
                "user_password (str)": "the password of user"
            },
            "APIs": {
                "search_contact": {
                    "desc": "search for contacts associated with the user",
                    "additional_required_arguments": {}, # no need for base required arguments
                    "optional_arguments": {},
                    "results_arguments": {
                        "contact_list (list)": "a list of contact of current user"
                    }
                },
                "alter_contact": {
                    "desc": "change the contact of the user such as add and delete other user operations",
                    "additional_required_arguments": {
                        "action_type (str)": "the type of action to perform ('add_user', 'delete_user')",
                        "alter_user_name (str)": "the name of other user to be added or deleted"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "True if the contact list was successfully altered, False otherwise",
                        "message (str)": "A message indicating the result of the action"
                    }
                },
                "chat": {
                    "desc": "chat with specific user",
                    "additional_required_arguments": {
                        "target_user_name (str)": "the user_name of target user to initiate the chat with",
                        "msg (str)": "the message to send",
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "True if the chat was successfully initiated, False otherwise",
                        "message (str)": "a message indicating the result of the chat initiation"
                    }
                },
                "transfer": {
                    "desc": "Transfer money to a target user",
                    "required_arguments": {
                        "target_user_name (str)": "the user name of target user to transfer money to",
                        "transfer_amount (float)": "the amount of money to transfer"
                    },
                    "results_arguments": {
                        "success (bool)": "True if the money was successfully transferred, False otherwise",
                        "message (str)": "a message indicating the result of the money transfer"
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
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            # print(json_file_path)
            # print(data)
            
            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.contact = user['contact']
                    self.amount = user['amount']
                    self.chat_log = user['chat_log']
                return None

    def search_contact(self):
        # load database according to user name and password and return results TODO
        contact_list = self.contact
        if contact_list is None:
            return False
        else:
            print(f"The contact list of {self.user_name} ontains {contact_list}")
            return contact_list

    def alter_contact(self, action_type, alter_user_name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name :
                if action_type == 'add_user':
                    self.contact.append(alter_user_name)
                    print(self.contact)
                    user['contact'].append(alter_user_name)
                    save_json(file_path,data)
                    return True, f"Already add {alter_user_name} to the contact list"
                elif action_type == 'delete_user':
                    self.contact.remove(alter_user_name)
                    user['contact'].remove(alter_user_name)
                    print(self.contact)
                    save_json(file_path,data)
                    return True, f"Deleted {alter_user_name} from the contact list"
                else:
                    return False, f"An error occurred: {action_type} is not a valid action type"
        
    def search_chat_log(self, key_word):
        chat_list = self.chat_log
        if key_word in chat_list:
            index = chat_list.index(key_word)
            return index, True, f"Found {key_word} at index {index} in the chat log"
        else:
            return  -1,False, f"An error occurred: {key_word} is not in the chat log"

    def chat(self, target_user_name, msg):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            msg={"from":self.user_name,"to":target_user_name,"message":msg}
            for user in data["users"]:
                if user["username"] == self.user_name :
                    user['chat_log'].append(msg)
            for user1 in data["users"]:
                if user1["username"] == target_user_name :
                    user1['chat_log'].append(msg)        
            save_json(file_path,data)
            return True, f"Sent {msg} to {target_user_name}"
            
        else:
            return False, f"An error occurred: {target_user_name} is not in the contact list"
        
    def text_chat(self, target_user_name, msg):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            msg={"from":self.user_name,"to":target_user_name,"message":msg}
            for user in data["users"]:
                if user["username"] == self.user_name :
                    user['chat_log'].append(msg)
            for user1 in data["users"]:
                if user1["username"] == target_user_name :
                    user1['chat_log'].append(msg)    
            save_json(file_path,data)
            return True, f"Sent {msg} to {target_user_name}"
        else:
            return False, f"An error occurred: {target_user_name} is not in the contact list"

    def voice_chat(self, target_user_name, msg):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            msg={"from":self.user_name,"to":target_user_name,"message":msg}
            for user in data["users"]:
                if user["username"] == self.user_name :
                    user['chat_log'].append(msg)
            for user1 in data["users"]:
                if user1["username"] == target_user_name :
                    user1['chat_log'].append(msg)               
            save_json(file_path,data)
            return True, f"Sent {msg} to {target_user_name}"
        else:
            return False, f"An error occurred: {target_user_name} is not in the contact list"

    def image_chat(self, target_user_name, msg):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            msg={"from":self.user_name,"to":target_user_name,"message":msg}
            for user in data["users"]:
                if user["username"] == self.user_name :
                    user['chat_log'].append(msg)
            for user1 in data["users"]:
                if user1["username"] == target_user_name :
                    user1['chat_log'].append(msg)                       
            save_json(file_path,data)
            return True, f"Sent {msg} to {target_user_name}"
        else:
            return False, f"An error occurred: { target_user_name   } is not in the contact list"

    def video_chat(self, target_user_name, msg):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
            msg={"from":self.user_name,"to":target_user_name,"message":msg}
            for user in data["users"]:
                if user["username"] == self.user_name :
                    user['chat_log'].append(msg)
            for user1 in data["users"]:
                if user1["username"] == target_user_name :
                    user1['chat_log'].append(msg)                       
            save_json(file_path,data)
            return True, f"Sent {msg} to {target_user_name}"
        else:
            return False, f"An error occurred: {target_user_name} is not in the contact list"

    def transfer(self, target_user_name, transfer_amount):
        contact_list = self.search_contact()
        if target_user_name in contact_list:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")
            success,data=read_json(file_path)
           
            for user in data["users"]:
                if user["username"] == self.user_name :
                    if target_user_name in contact_list and self.amount >= transfer_amount:
                        self.amount =self.amount-transfer_amount
                        user["amount"] = user["amount"]-transfer_amount
                        print(f"Transfer {transfer_amount} to {target_user_name}, now the amount is {self.amount}")
                        for user1 in data["users"]:
                            if user1["username"] == target_user_name :
                                if target_user_name in contact_list and self.amount >= transfer_amount:
                                    user1["amount"] =user1["amount"]+transfer_amount
                                    print(f"recieve {transfer_amount} from {target_user_name}, now the amount is {user1['amount']}")
                                    save_json(file_path,data)
                        
                        return True, f"Transfer {transfer_amount} to {target_user_name}, now the amount is {self.amount}"
                        
                    else:
                        return False, f"An error occurred: {target_user_name} is not in the contact list or the amount is not enough"
                              

def main():
    # 主要逻辑代码
    # Example usage:
    # Get the directory of the current Python file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path of the example_data.json file
    json_file_path = os.path.join(current_directory, "..", "database", "wechat_data.json")

    # Load data from the JSON file
    # success, data = read_json(json_file_path)
    # print(data)
    # user = data["users"][0]

    # wechat_app1 =None
    # if success:
        # wechat_app1 = WeChat('xiyuanhao', '123')
        # wechat_app1.search_contact()
        # wechat_app1.alter_contact('add_user','xiyuanhao123')
        # #wechat_app1.chat('zhangsan','test')
        # #wechat_app1.chat('zhangsan','how are you?')
        # wechat_app1.transfer('zhangsan',100.0)
       
        
    # else:
    #     print(f"Error loading data: {data}")    
        

    # wechat_app2 = WeChat('wxid_1234567891',[], 1000, [])
    # wechat_app3 = WeChat('wxid_1234567892',[], 1000, [])

    # wechat_app1.alter_contact('add_user','wxid_1234567891','')
    # wechat_app1.alter_contact('add_user','wxid_1234567892','')
    # wechat_app1.chat('wxid_1234567891','hello world!!!','text')
    # wechat_app1.alter_contact('add_group','','groupid_1234567890')
    # wechat_app1.group_chat('groupid_1234567890','hello world!!!')
    # wechat_app1.search_contact()
    # wechat_app1.transfer('wxid_1234567891',100.0)
    # wechat_app1.search_chat_log('hello world!!!')


if __name__ == "__main__":
    main()


