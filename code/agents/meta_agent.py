# coding: utf-8
from evaluation import *
from apps.mobile import *
from utils import *
from agents.agent import *
import random
from models.chatgpt_resp_cralwer import ChatgptRespCrawler

class MetaAgent(Agent):
    def __init__(self, model, model_type="", setting="zero-shot", test_type="ss", prompt_dir=""):
        super().__init__(model, model_type, setting)
        
        # load prompts
        self.prompts = load_prompt_from_dir(prompt_dir)
        self.maximum_iterations = 5
        self.setting = setting

        if setting != "zero-shot":
            num_of_shot = int(self.setting.split("-")[0])
            self.num_of_shot = num_of_shot
            demo_path = "../data/train/" + "train_" + test_type + ".json"
            self.demo_pool = self.build_demos_from_train(demo_path)

    def build_demos_from_train(self, pth):
        raw_data = read_json(pth)
        demos = []
        for sample in raw_data:
            user_input = sample["input"]
            used_app = sample["output"]["used_app"]
            api_results = sample["output"]["api_results"]
            assert len(used_app) == len(api_results)
            
            output = ""
            for app, api in zip(used_app, api_results):
                output += app + ": [" + api + "]" + " \n"
            
            demos.append({
                "metadata": {"used_app": used_app},
                "user": user_input,
                "assistant": output
            })
            
        self.demos = demos

    def random_select_demos(self, query, num_of_shot=3):
        current_used_app = query["output"]["used_app"]
        demostrations, count = [], 0
        for demo in self.demos:
            if sorted(current_used_app) == sorted(demo["metadata"]["used_app"]):
                user_turn = {"role": "user", "content": demo["user"]}
                assistant_turn = {"role": "assistant", "content": demo["assistant"]}
                demostrations.extend([user_turn, assistant_turn])
                count += 1

                if count == num_of_shot:
                    return demostrations
        
        if count < num_of_shot:
            sampled_demos = random.sample(self.demos, num_of_shot-count)
            for demo in sampled_demos:
                user_turn = {"role": "user", "content": demo["user"]}
                assistant_turn = {"role": "assistant", "content": demo["assistant"]}
                demostrations.extend([user_turn, assistant_turn])
            return demostrations

    def call_each_prompt(self, instruction, prompt, demo=None):
        if "gpt" in self.model_type:
            response = self.model.call_openai_each(instruction, prompt, demo=demo)
        elif "ours" in self.model_type:
            response = self.model.call_ours_each(instruction, prompt, demo=demo)
        else:
            response = self.model.call_huggingfacea_each(instruction, prompt, demo=demo)
        return response

    def find_required_app(self, user_prompt):
        def check_recover_app_names(app_names):
            # 简单解决一下抽取的边界错误
            app_list = self.env.list_all_apps()
            result = []
            for app in app_names:
                if app in app_list:
                    result.append(app)
                else:
                    for true_app in app_list:
                        if app in true_app:
                            result.append(true_app)

            return result
        
        app_instruction = """Your task is to determine the required App list according the description of each App and user requirements. 
        Here is the information about all accessible Apps: {app_desc}
        Make your response short and concise. Try your best to select several (one at least) apps might be useful for fulfilling user's request. Your ONLY need to return needed app names and your output MUST follow this JSON format: [app1, app2, ...].
        User Input:"""
    
        response = self.call_each_prompt(app_instruction.format(app_desc=self.env.flat_apps_desc_test), user_prompt)
        _, decided_app = get_response_according_to_model_type(response, self.model_type)
        print("before", decided_app)

        # directly check which app in the response
        # 这样recall会好点，但是也会出现空列表
        app_list = [app_name for app_name in self.env.app_list if app_name in decided_app]

        # 优先recall后还是空，模糊匹配
        if len(app_list) == 0:
            app_list = check_recover_app_names(decided_app)

        # 
        # app_list = json.loads(decided_app)
        # app_list = [x for x in app_list]

        print("after",app_list)
        if len(app_list) == 0:
            print("ALERT!!!!! No valid app names returned.")
            return None
        return {"app_list":app_list, "app_selection_resp":decided_app}

    def generate_api_call(self, sample, is_data_isolation=False, retrieve_app_fist=True):
        # pred ONE sample
        user_prompt = sample["input"]

        if is_data_isolation:
            # 1st step: find all required agents
            app_list = self.find_required_app(user_prompt)
            all_returned_arguments, all_required_input_arguments, is_success_list = {}, {}, []
            
            # 2nd step: distribute the task into different app/agent
            for app_name in app_list:
                app_apis_desc = self.env.find_api_according_to_app(app_name)
                apis_desc_text = flat_apis_desc([app_apis_desc])
                
                api_instruction = self.prompts["api_for_single_agent"]
                response = self.call_each_prompt(api_instruction.format(app_api_list=apis_desc_text), user_prompt)
                _, decided_api = get_response_according_to_model_type(response, self.model_type)

                # the app agent only tells meta-agent the required arguments and returned arguments without details of api call
                # required arguments only for unsuccessful apis, and returned arguments only for successful apis
                returned_arguments, required_arguments, is_success = self.is_complete_sub_task(decided_api.split("\n"), app_name)
                
                all_returned_arguments[app_name] = returned_arguments
                all_required_input_arguments[app_name] = required_arguments
                is_success_list.append(is_success)
            
            # 3rd step: re-run imcompleted sub-tasks considering the order dependency without exceeds maximum iterations
            current_iterations = 0
            while current_iterations < self.maximum_iterations:
                if not all([success_flag for success_flag in is_success_list]):
                    fail_app_list = [app_list[i] for i, success_flag in enumerate(is_success_list) if success_flag == 0]
                    
                    for app_name in fail_app_list:
                        fail_api_instruction = self.prompts["dependency_api_for_single_agent"]  # TODO give all return arguments is not private and is used to test app agent
                        response = self.call_each_prompt(fail_api_instruction.format(app_api_list=apis_desc_text, returned_arguments=all_returned_arguments), user_prompt)
                        _, decided_api = get_response_according_to_model_type(response, self.model_type)
                        
                        # the app agent only tells meta-agent the required arguments and returned arguments without details of api call
                        returned_arguments, required_arguments, is_success = self.is_complete_sub_task(decided_api, app_name)
                    
                    current_iterations += 1


            decided_app_api = {
                "decided_app": decided_app,
                "decided_api": decided_api
            }

        else:
            condi_api_names = []
            if retrieve_app_fist: # retrieve app first
                # app_list = self.find_required_app(user_prompt)
                # app_api_list = self.env.list_all_app_apis(app_list)
                times = 5
                while times!=0:
                    try:
                        # {"app_list":app_list, "app_selection_resp":decided_app}
                        app_list_resp = self.find_required_app(user_prompt)
                        print(app_list_resp)
                        app_list = app_list_resp['app_list']
                        app_selection_resp = app_list_resp['app_selection_resp']

                        app_api_list = self.env.list_all_app_apis(list(set(app_list)))
                        # print(app_list, app_api_list)
                        app_apis_desc = flat_apps_apis(list(set(app_list)), app_api_list)
                        break
                    except:
                        print(f"Wrong Response Format, try again!")
                        times-=1
                        if times==0:
                            print("tried 5 times! Drop this sample.")
                            break
                
            else:
                app_apis_desc = self.env.flat_apps_apis_desc
                app_selection_resp = None

            api_instruction = self.prompts["api_for_all_agent"]
            
            if self.setting != "zero-shot":
                demo = self.random_select_demos(sample, self.num_of_shot)
                response = self.call_each_prompt(api_instruction.format(app_api_list=app_apis_desc), user_prompt, demo)
            else:
                response = self.call_each_prompt(api_instruction.format(app_api_list=app_apis_desc), user_prompt)
            
            _, decided_app_api = get_response_according_to_model_type(response, self.model_type)
            decided_app, decided_api = discompose_app_api(decided_app_api)
            decided_app_api = {
                "decided_app": decided_app,
                "decided_api": decided_api,
                "app_selection_resp":app_selection_resp,
                "decided_app_api": decided_app_api
            }
        
        return decided_app_api
    
    def revise_api_call(self, sample, is_data_isolation=False, retrieve_app_fist=True):
        def check_recover_app_names(app_names):
            # 简单解决一下抽取的边界错误
            app_list = self.env.list_all_apps()
            result = []
            for app in app_names:
                if app in app_list:
                    result.append(app)
                else:
                    for true_app in app_list:
                        if app in true_app:
                            result.append(true_app)

            return result
        
        # pred ONE sample
        user_prompt = sample["input"]

        if is_data_isolation:
            pass
        else:
            if retrieve_app_fist:
                app_first_list = []
                # print(sample['input'])
                if "app_selection_resp" in sample['prediction']:
                    app_first_list = [app_name for app_name in self.env.app_list if app_name in sample['prediction']['app_selection_resp']]

                # 优先recall后还是空，模糊匹配
                # if len(app_first_list) == 0:
                #     app_first_list = check_recover_app_names(sample['prediction']['app_selection_resp'])
                
                decided_app, decided_api = discompose_app_api(sample['prediction']['decided_app_api'])
                matched_decided_app = []
                for d_app in decided_app:
                    if d_app.lower().startswith("app"):
                        try:
                            ind = d_app.lower().replace("app", "").split("_")[0]
                            ind = int(ind) - 1
                            if ind <len(app_first_list):
                                matched_decided_app.append(app_first_list[ind])
                        except:
                            continue
                    else:
                        matched_decided_app.append(d_app)
            #     "decided_app": [
            #         "app1"
            #     ],
            #     "decided_api": [
            #         "from_city = 'San Francisco', to_city = 'Sacramento, CA', departure_date = '2023-03-14', departure_time = '06:00', num_passengers = 4"
            #     ],
            #     "app_selection_resp": "Buses: [Buses]\n<|endoftext|>",
            #     "decided_app_api": "app1: [from_city = 'San Francisco', to_city = 'Sacramento, CA', departure_date = '2023-03-14', departure_time = '06:00', num_passengers = 4]\n<|endoftext|>"
            # },
                decided_app_api = {
                    "decided_app": decided_app,
                    "decided_app_matched_with_first_step": matched_decided_app,

                    "decided_api": decided_api,
                    "decided_app_first_step":  app_first_list,
                    "decided_app_api": sample['prediction']['decided_app_api'],
                    "app_selection_resp":sample['prediction']['app_selection_resp']
                }
            else:
                decided_app, decided_api = discompose_app_api(sample['prediction']['decided_app_api'])

                decided_app_api = {
                    "decided_app": decided_app,
                    "decided_api": decided_api,
                    "decided_app_api": sample['prediction']['decided_app_api']
                }
        return decided_app_api
    
        
