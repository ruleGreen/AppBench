# coding: utf-8
from evaluation import *
from apps.mobile import *
from utils import *
from models.chatgpt_resp_cralwer import ChatgptRespCrawler


class Agent:
    def __init__(self, model, model_type="", setting="zero-shot"):
        self.model = model
        self.model_type = model_type
        self.env = Mobile()
        self.analysis = {
            "wrong_api_count": 0
        }

    def call_each_prompt(self, instruction, prompt):
        if "gpt" in self.model_type:
            response = self.model.call_openai_each(instruction, prompt)
        else:
            response = self.model.call_huggingfacea_each(instruction, prompt)
        return response
    
    def is_complete_sub_task(self, api_call, app_name):
        app_apis_desc = self.env.find_api_according_to_app(app_name)
        all_returned_arguments, all_required_input_arguments = [], []

        for api in api_call:
            # regular expression to match the returned arguments and the API call
            pattern = r"\[(.*?) = (.*?)\((.*?)\)\]"
            # Use regular expression to find matches
            match = re.search(pattern, api)
            if match:
                returned_arguments = match.group(1).split(", ")
                api_name = match.group(2)
                input_arguments_str = match.group(3)
            else:
                returned_arguments = []
                api_name = None
                input_arguments_str = ""
            
            # determine whether or not api and arguments is correct
            if api_name in app_apis_desc:
                is_transactional = app_apis_desc[api_name]["is_transactional"]
                original_result_arguments = [remove_parentheses_content(argu) for argu in list(app_apis_desc[api_name]["result_arguments"].keys())]
                original_required_arguments = [remove_parentheses_content(argu) for argu in list(app_apis_desc[api_name]["additional_required_arguments"])]

                # Regular expression to extract input arguments and their values
                input_pattern = r"#(\w+)=([^,]+)"
                # Find all input arguments and their values
                input_arguments = re.findall(input_pattern, input_arguments_str)
                # List to store input arguments whose value is '?'
                unknown_arguments = [arg for arg, value in input_arguments if value.strip() == '?']

                all_returned_arguments.extend(returned_arguments)
                all_required_input_arguments.extend(unknown_arguments)
            
            else:
                self.analysis["wrong_api_count"] += self.analysis.get("wrong_api_count", 0) + 1
    
        if len(all_required_input_arguments) == 0:
            return list(set(all_returned_arguments)), [], 1

        return list(set(all_returned_arguments)), all_required_input_arguments, 0

    


            