import json
import os
from utils import read_json, save_json

class Lark:
    def __init__(self,user_name, user_password):
           # load user name and password
        self.desc = {
            "desc": " a personal productivity app for users to manage their todo list and okr list",
            "base_required_arguments": {  # base required arguments for almost all functions in this app
                "user_name (str)": "the user name of the current user",
                "user_password (str)": "the password of the current user"
            },
            "APIs": {
                "check_todo": {
                    "is_transactional": False,
                    "desc": "check the todo list of the current user",
                    "additional_required_arguments": {}, # no need for base required arguments
                    "optional_arguments": {},
                    "results_arguments": {
                        "todo_list (list)": "a list of todo items of current user"
                    }
                },
                "modify_todo": {
                    "is_transactional": True,
                    "desc": "modify a todo item of the current user",
                    "additional_required_arguments": {
                        "task_id (int)": "the id of the task to be modified",
                        "date (str)": "the date of the task",
                        "task_name (str)": "the name of the task",
                        "task_content (str)": "the content of the task",
                        "task_status (str)": "the status of the task"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "whether the modification is successful"
                    }
                },
                "add_todo": {
                    "is_transactional": True,
                    "desc": "add a todo item for the current user",
                    "additional_required_arguments": {
                        "date (str)": "the date of the task",
                        "task_name (str)": "the name of the task",
                        "task_content (str)": "the content of the task",
                        "task_status (str)": "the status of the task"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "whether the addition is successful"
                    }
                },
                "check_okr": {
                    "is_transactional": False,
                    "desc": "check the okr list of the current user",
                    "additional_required_arguments": {
                        "timestamp (str)": "the timestamp of the okr list to be checked"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "okr_list (list)": "a list of okr items of current user"
                    }
                },
                "modify_okr": {
                    "is_transactional": True,
                    "desc": "modify an okr item of the current user",
                    "additional_required_arguments": {
                        "okr_id (int)": "the id of the okr to be modified",
                        "objective (str)": "the objective of the okr",
                        "okr_status (str)": "the status of the okr",
                        "key_results (list)": "the key results of the okr"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "whether the modification is successful"
                    }
                },
                "add_okr": {
                    "is_transactional": True,
                    "desc": "add an okr item for the current user",
                    "additional_required_arguments": {
                        "objective (str)": "the objective of the okr",
                        "key_results (list)": "the key results of the okr"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "success (bool)": "whether the addition is successful"
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
            # load other data from database according to user name and password
            
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "lark_data.json")
            success,data=read_json(file_path)
            # print(json_file_path)
            #print(data)
            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.todo = user['todo_list']
                    self.okr = user['okr_list']
                  
                return None
       

    def check_todo(self):
        
        print(self.todo)
        return self.todo
        
    def modify_todo(self,task_id,date,task_name,task_content,task_status):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "lark_data.json")
        success,data=read_json(file_path)
       
        if task_id is None:
            print(f"An error occurred: task id is not valid")
            return False
      
        else:
            for task in self.todo:
                if task["task_id"] == task_id:
                    task["date"] = date
                    task["task_name"] = task_name
                    task["task_content"] = task_content
                    task["task_status"] = task_status
                    for user in data["users"]:
                        if user["username"] == self.user_name and user["password"] == self.user_password:
                            user["todo_list"]=self.todo
                            save_json(file_path,data)
                    return True
            return False
    def add_todo(self, date,task_name,task_content,task_status):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "lark_data.json")
        success,data=read_json(file_path)
        task_id = len(self.todo) + 1
        new_task = {"task_id": task_id, "date": date, "task_name": task_name, "task_content": task_content, "task_status": task_status}
        self.todo.append(new_task)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                user["todo_list"]=self.todo
                save_json(file_path,data)
        return True





    def check_okr(self, timestamp):
        print(self.okr)
        return self.okr
        
    def modify_okr(self, okr_id, objective,okr_status,key_results):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "lark_data.json")
        success,data=read_json(file_path)
       
        if okr_id is None:
            print(f"An error occurred: task id is not valid")
            return False
      
        else:
            for okr in self.okr:
                if okr["okr_id"] == okr_id:
                    okr["objective"] = objective
                    okr["okr_status"] = okr_status
                    okr["key_results"] = key_results
                    for user in data["users"]:
                        if user["username"] == self.user_name and user["password"] == self.user_password:
                            user["okr_list"]=self.okr
                            save_json(file_path,data)
                    return True

        


    def add_okr(self, objective, key_results):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "lark_data.json")
        success,data=read_json(file_path)
        okr_id = len(self.okr) + 1
        new_okr = {"okr_id": okr_id, "objective": objective, "okr_status": "on track", "key_results": key_results}
        self.okr.append(new_okr)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                user["okr_list"]=self.okr
                save_json(file_path,data)
     



if __name__ == "__main__":
    lark1 = Lark("Bruce", "123")
    #lark1.check_todo()
    #lark1.modify_todo(2, "2024-03-01", "test", "test", "done")
   # lark1.add_todo("2024-03-02", "test_add", "test_add", "done")
   # lark1.modify_okr(3, "test_modify", "done", ["test_modify1", "test_modify2"])
    lark1.add_okr("test_add", ["test_add1", "test_add2"])
  


