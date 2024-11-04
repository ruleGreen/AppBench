# Coding: utf-8
from rouge import Rouge
import re
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from utils import *

# sys.path.append("..")
from models.chatgpt_resp_cralwer import ChatgptRespCrawler
from apps.mobile import *

class Evaluation:
    def __init__(self, use_llm=False, model="", role_play=False, quality_control=False) -> None:
        self.env = Mobile()
        self.no_tool_actions = ["req_more", "goodbye", "offer_alts", "inform", "offer_intent"]

        if use_llm:
            key_path = 'conf/mine_keys.txt'
            self.model_type = model
            self.llm_evaluator = ChatgptRespCrawler(key_path, 0, top_p=0, model=model)
        
        # if role_play:
        #     self.role_play_instruction = read_text("./role_play/prompts/evaluation.txt")
        #     self.role_pool = read_json('./role_play/prompts/role_pool.json')
        
        # if quality_control:
        #     self.quality_control = read_text("./metabench/prompts/quality.txt")


    def is_exact_match(self, prediction, labels):
        if prediction.lower() == labels.lower() or labels.lower() in prediction.lower():
            return 1
        return 0
    
    def calculate_bleu_score(self, hypothesis, reference, n=4):
        # Tokenize the hypothesis and reference
        hypothesis_tokens = nltk.word_tokenize(hypothesis.lower())
        reference_tokens = nltk.word_tokenize(reference.lower())
        
        # Calculate BLEU score
        weights = [1.0 / n] * n  # Equal weights for n-grams
        smoothing_function = SmoothingFunction().method7
        bleu_score = sentence_bleu([reference_tokens], hypothesis_tokens, weights, smoothing_function=smoothing_function)
        return bleu_score
    
    def calculate_rouge_l(self, hypothesis, reference):
        rouge = Rouge()
        scores = rouge.get_scores(hypothesis, reference, avg=True)
        rouge_l_score = scores['rouge-l']['f']
        return rouge_l_score
    
    def compute_f1_direct(self, precision, recall):
        if precision + recall == 0:
            f1_score = 0
        else:
            f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score
    
    def compute_f1(self, prediction, labels):
        # Convert the answers to sets of tokens
        predicted_tokens = set(prediction.lower().split())
        ground_truth_tokens = set(labels.lower().split())

        # Calculate precision, recall, and F1 score
        precision = len(predicted_tokens.intersection(ground_truth_tokens)) / len(predicted_tokens)
        recall = len(predicted_tokens.intersection(ground_truth_tokens)) / len(ground_truth_tokens)

        f1_score = self.compute_f1_direct(precision, recall)
        # if precision + recall == 0:
        #     f1_score = 0
        # else:
        #     f1_score = 2 * (precision * recall) / (precision + recall)

        return f1_score
    
    def is_semantic_equivalence(self, question, prediction, labels):
        if "sorry" in prediction:
            return 0
        task_definition = "In the following task, you are given a Question, a model Prediction for the Question, and a Ground-truth Answer to the Question. You should decide whether the model Prediction implies the Ground-truth Answer."
        prompt = "{task_definition} \n\n Question \n {question} \n\n Prediction \n {prediction} \n\n Ground-truth Answer \n {answer} \n\n Does the Prediction imply the Ground-truth Answer? Output Yes or No:"
        response = self.llm_evaluator.call_openai(prompt.format(task_definition=task_definition, question=question, prediction=prediction, answer=labels))
        _, results = get_response_according_to_model_type(response, self.model_type)
        if "yes" in results.lower():
            return 1
        return 0
    
    def is_success(self, state, apps):
        dialogue = ["user: " + turn + " \n " if j%2 == 0 else "system: " + turn + " \n " for j,turn in enumerate(state)]
        dialogue_text = " ".join(dialogue)
        task_instruction = "Given the dialogue between the user and system, please determine whether or not the system successfully complete the user's requirements."
        is_success_prompt = "{task_instruction} \n\n dialogue: {dialogue} \n\n Please output in the format of [Yes] or [No (Explanations and the first wrong turn)]."
        response = self.llm_evaluator.call_openai(is_success_prompt.format(task_instruction=task_instruction, dialogue=dialogue_text))
        _, results = get_response_according_to_model_type(response, self.model_type)
        
        if "yes" in results.lower():
            return 1, "success"
        return 0, "fail" # TODO

    def is_role_consistent(self, dialogue):
        role_name = dialogue["role"]
        role_config = self.role_pool[role_name]
        dialogue_context = [turn["speaker"] + ": " + turn["utterance"] for turn in dialogue["turns"]]
        role_config_text = " ".join([str(k) + ": " + str(v) for k,v in role_config.items()])
        
        is_role_consistent_prompt = "Here is a dialogue: {dialogue} \n\n Here is the role config for the system: {role_config} \n\n Score: "
        response = self.llm_evaluator.call_openai(self.role_play_instruction, is_role_consistent_prompt.format(dialogue=" \n ".join(dialogue_context), role_config=role_config_text))
        _, response = get_response_according_to_model_type(response, self.model_type)
        score = self.get_evaluation_scores(response)
        
        return score

    def is_qualified(self, instruction):
        is_qualified_prompt = "Here is the user instruction: {instruction} \n\n Score: "
        response = self.llm_evaluator.call_openai(self.quality_control, is_qualified_prompt.format(instruction=instruction))
        _, response = get_response_according_to_model_type(response, self.model_type)
        score = self.get_evaluation_scores(response)
        
        return score

    def get_appbench_analysis(self, results):

        # avoid address spelling errors
        pred_correction_map  = {"la":"los angeles", "lax": "los angeles", "ciudad de mexico":"mexico city'", "nyc":"new york", "sd":"san diego","sfo":"san francisco","chi-town":"chicago"}
        
        optional_arguments = ["car_type", "num_passengers", "category", "additional_luggage", "date", "seating_class", "number_of_tickets", "airlines", \
        "in_unit_laundry", "has_garage", "has_laundry_service", "number_of_adults", "rating", "starring", "subtitle_language", "theater_name", \
        "show_tyoe", "genre", "artist", "year", "album", "private_visibility", "number_of_seats", "price_range", "has_vegetarian_options", "has_seating_outdoors", \
        "is_unisex", "class", "free_entry", "good_for_kids"]
        
        # optional_arguments = [for key in optional_arguments if key not in ["private_visibility", "number_of_seats"]]
        def single_argu_value_judge(v1, v2):
            # determine whether the value of two arguments are equal
            v1 = v1.lower()
            v2 = v2.lower()
            if v1.strip("'") == v2.strip("'") or v2.strip("'") in v1.strip("'") or v1.strip("'") in v2.strip("'"):
                return True
            else:
                return False
            
        def match_evaluate(preds, labels):
            # print("******",preds,labels)
            # hit and exact match of two lists
            if len(preds)== 0:
                return 0,0
            
            em = 0
            hit_num = 0
            preds = [x.lower() for x in preds]
            labels = [l.lower() for l in labels]
            if sorted(preds) == sorted(labels):
                em += 1
            # 预测app的命中
            if preds is None:
                return 0,0
            while len(preds)!=0 and len(labels)!=0:
                for pred in preds:
                    if pred in labels:
                        labels = labels.remove(pred)
                        preds = preds.remove(pred)
                        if labels is None:
                            labels = []
                        if preds is None:
                            preds = []
                        hit_num+=1
                        break
                    else:
                        preds.remove(pred)
                        if preds is None:
                            preds = []
            return em, hit_num
        
        

        app_em_count, app_hit_count,total_pred_apps = 0,0,0
        total_ground_apps = 0
        api_em_count, api_hit_count,total_pred_apis = 0,0,0
        total_ground_apis = 0
        api_argu_em, api_argu_hit_count, total_pred_api_argu = 0,0,0
        total_ground_api_argu = 0
        
        depend_argu_em, depend_argu_hit, total_depend_argus = 0,0,0
        non_depend_argu_em, non_depend_argu_hit, non_total_depend_argus = 0,0,0
        
        
        total_depend_k_missing, total_k_missing = 0, 0
        total_depend_value_missing, total_value_missing = 0, 0
        total_pred_depend_args = 0
        total_pred_non_depend_args = 0
        
        pred_api_depending = 0
        total_match= 0

        total_k_missing = 0
        total_value_missing = 0

        for sample in results:
            

            user_inst, ground_truth, prediction = sample["input"], sample["output"], sample["prediction"]
            user_aware_arguments_raw = ground_truth['user_aware_arguments']
            user_aware_arguments = {'#'+k:v for k,v in user_aware_arguments_raw.items()}
            if "decided_app_matched_with_first_step" in prediction:
                decided_app, decided_api = [x for x in prediction["decided_app_matched_with_first_step"] if x is not None and len(x)>0], prediction["decided_api"]
            else:
                decided_app, decided_api = [x for x in prediction["decided_app"] if x is not None and len(x)>0], prediction["decided_api"]

            ground_app, ground_api = ground_truth["used_app"], ground_truth["api_results"]


            # evaluation app selection performance
            # em and hit rate of app
            total_pred_apps+= len(decided_app)
            total_ground_apps += len(ground_app)
            app_em, app_hit_n = match_evaluate(decided_app, ground_app)
            app_em_count += app_em
            app_hit_count += app_hit_n
                    
            # api avaluation
            # em and hit rate of api NAME
            decided_api_names = [extract_name_params(api)['function_name'] if extract_name_params(api) is not None else "" for api in decided_api ]
            ground_api_names = [extract_name_params(api)['function_name'] for api in ground_api]
            total_pred_apis += len(decided_api_names)
            total_ground_apis+= len(ground_api_names)
            api_em, api_hit_n = match_evaluate(decided_api_names, ground_api_names)
            api_em_count += api_em
            api_hit_count += api_hit_n
            
            
            decided_api = [api.replace('\\', '') for api in decided_api ]
            # print(decided_api)
            decided_api_arg_values = {extract_name_params(api)['function_name']:extract_name_params(api)['input_parameters']  for api in decided_api if extract_name_params(api) is not None}
            ground_api_arg_values = {extract_name_params(api)['function_name']:extract_name_params(api)['input_parameters'] for api in ground_api}

            past_pred_argu_name_values = []

            for decided_api_arg in decided_api_arg_values.values():
                total_pred_api_argu += len(decided_api_arg)
            
            for ground_api_arg in ground_api_arg_values.values():
                total_ground_api_argu += len(ground_api_arg)
            
            for _, pred_api_arg in decided_api_arg_values.items():
                for k in pred_api_arg:
                        if "'" not in pred_api_arg[k]:
                            total_pred_depend_args+=1

            # print(total_pred_api_argu)
            unit_api_em = 0
            # past_argu_name_values = []

            for ground_api, ground_api_arg in ground_api_arg_values.items():
                k_missing = 0
                depend_k_missing = 0
                value_missing = 0
                depend_value_missing=0
                # 评估预测输入arguments命中率
                depend_augu_length = 0
                non_depend_argu_length=0
                
                if ground_api.lower() in decided_api_arg_values:
                    # 用于记录argu匹配的比例,ground api name出现在预测的api里面
                    unit_argu_hit = 0
                    unit_depend_argu_hit =0
                    # pred中预测到了该api后，再评估预测的输入参数
                    decided_api_arg = decided_api_arg_values[ground_api]
                    # print(decided_api_arg)
                    # print(len([k for k in decided_api_arg]))
                    for k in ground_api_arg:
                        # print(ground_api_arg)

                        if "'" not in ground_api_arg[k]:
                            # count the arguments depend on other apis
                            depend_augu_length+=1
                        else:
                            non_depend_argu_length +=1
                        if k in decided_api_arg:

                            ground_value = ground_api_arg[k].lower()
      
                            pred_value = decided_api_arg[k].lower() if decided_api_arg[k] is not None else ""

                            user_aware_value = None
                            if k in user_aware_arguments:
                                user_aware_value = user_aware_arguments[k].lower()

                            
                            past_value = None
                            for past_name_v in past_pred_argu_name_values:
                                if k==past_name_v[0]:
                                    past_value = past_name_v[1]
                                    break
                            
                            if pred_value.strip("'") in pred_correction_map:
                                pred_value = "'" + pred_correction_map[pred_value.strip("'")] + "'"

                            if  single_argu_value_judge(ground_value, pred_value):
                                past_pred_argu_name_values.append([k, pred_value])
                                unit_argu_hit+=1
                                if "'" not in ground_api_arg[k]:
                                    # 命中依赖于其他api的参数
                                    unit_depend_argu_hit+=1

                                continue
                            
                            if user_aware_value is not None and single_argu_value_judge(user_aware_value, pred_value):
                                past_pred_argu_name_values.append([k, pred_value])


                                unit_argu_hit+=1
                                if "'" not in ground_api_arg[k]:
                                    unit_depend_argu_hit+=1
                                    total_pred_depend_args+=1
                                continue
                            if past_value is not None and single_argu_value_judge(past_value, pred_value):
                                unit_argu_hit+=1
                                if "'" not in ground_api_arg[k]:
                                    # 命中依赖于其他api的参数
                                    unit_depend_argu_hit+=1
                                    total_pred_depend_args+=1
                                continue

                            value_missing+=1
                            if "'" not in ground_api_arg[k]:
                                depend_value_missing+=1
                        else:
                            k_missing+=1
                            if "'" not in ground_api_arg[k]:
                                depend_k_missing+=1
                    
                    api_argu_hit_count += unit_argu_hit
                    depend_argu_hit += unit_depend_argu_hit
                    
                    total_k_missing += k_missing
                    total_value_missing+=value_missing
                    total_depend_k_missing += depend_k_missing
                    total_depend_value_missing+=depend_value_missing
                    
                    
                    total_depend_argus += depend_augu_length
                    non_total_depend_argus += non_depend_argu_length
                    
                    # print(len(ground_api_arg))
                    if depend_augu_length !=0:
                        pred_api_depending+=1
                    if unit_depend_argu_hit == depend_augu_length and depend_augu_length!=0:
                        # dependency arguments exact match
                        depend_argu_em+=1


                    if unit_argu_hit == len(ground_api_arg):
                        # arguments exact match
                        unit_api_em+=1
                        api_argu_em+=1

                total_k_missing+=k_missing
                total_value_missing+=value_missing
            # if app_em==1 and api_em==1:
            #     print(unit_api_em, len(ground_api_arg_values))
            if app_em==1 and api_em==1 and unit_api_em==len(ground_api_arg_values):
                total_match+=1
            
            


        total_pred_non_depend_args = total_pred_api_argu - total_pred_depend_args
        total_ground_non_depend_args = total_ground_api_argu - total_depend_argus
        non_depend_argu_hit = api_argu_hit_count - depend_argu_hit
        
        total_non_depend_k_missing = total_k_missing - total_depend_k_missing
        total_non_depend_value_missing = total_value_missing - total_depend_value_missing
        
        
        evaluation = {
            # "app_exact_match": app_em_count / len(results) if len(results)!=0 else 0,
            # "app_hit/ app_pred_num": app_hit_count/total_pred_apps,
            # "app_hit/ app_ground_num": app_hit_count/total_ground_apps,
            "app_hit_f1": self.compute_f1_direct(app_hit_count/total_pred_apps, app_hit_count/total_ground_apps),

            # "api_exact_match": api_em_count / len(results)  if len(results)!=0 else 0,
            # "api_hit/ api_pred_num": api_hit_count/total_pred_apis,
            # "api_hit/ api_ground_num": api_hit_count/total_ground_apis,
            "api_hit_f1": self.compute_f1_direct(api_hit_count/total_pred_apis, api_hit_count/total_ground_apis),
            
            # "argu_exact_match": api_argu_em/total_pred_apis,
            # "argu_hit/ argu_pred_num": api_argu_hit_count/total_pred_api_argu if total_pred_api_argu!=0 else 0,
            # "argu_hit/ argu_ground_num": api_argu_hit_count/total_ground_api_argu if total_pred_api_argu!=0 else 0,
            "argu_hit_f1": self.compute_f1_direct(api_argu_hit_count/total_pred_api_argu if total_pred_api_argu!=0 else 0, api_argu_hit_count/total_ground_api_argu if total_pred_api_argu!=0 else 0),
            
            "complete_match" : total_match / len(results),
            
            # "depend_argu_exact_match": (depend_argu_em )/pred_api_depending if pred_api_depending != 0 else 0,
            # "depend_argu_hit_rate/ depend_pred_num": depend_argu_hit/total_pred_depend_args if total_pred_depend_args != 0 else 1,
            # "depend_argu_hit_rate/ depend_ground_num": depend_argu_hit/total_depend_argus if total_depend_argus != 0 else 1,
            "depend_argu_hit_f1" : self.compute_f1_direct(depend_argu_hit/total_pred_depend_args if total_pred_depend_args != 0 else 1,depend_argu_hit/total_depend_argus if total_depend_argus != 0 else 1),
            # "depend_k_missing":total_depend_k_missing/total_pred_depend_args if total_pred_depend_args != 0 else 1,
            # "depend_value_missing":total_depend_value_missing/total_pred_depend_args if total_pred_depend_args != 0 else 1,
            
            # "non_depend_argu_exact_match": (non_depend_argu_em )/(total_pred_apis - pred_api_depending) if (total_pred_apis - pred_api_depending) != 0 else 0,
            # "non_depend_argu_hit_rate/ depend_pred_num": non_depend_argu_hit/total_pred_non_depend_args if total_pred_depend_args != 0 else 1,
            # "non_depend_argu_hit_rate/ depend_ground_num": non_depend_argu_hit/total_ground_non_depend_args if total_ground_non_depend_args != 0 else 1,
            "non_depend_argu_hit_f1" : self.compute_f1_direct(non_depend_argu_hit/total_pred_non_depend_args if total_pred_non_depend_args != 0 else 1,non_depend_argu_hit/total_ground_non_depend_args if total_depend_argus != 0 else 1),
            # "non_depend_k_missing":total_non_depend_k_missing / total_pred_non_depend_args if total_pred_non_depend_args != 0 else 1,
            # "non_depend_value_missing":total_non_depend_value_missing / total_pred_non_depend_args if total_pred_non_depend_args != 0 else 1,
            
            # "k_missing_rate_api_unit":total_k_missing/total_pred_apis,
            # "value_missing_rate_api_unit":total_value_missing/total_pred_apis,
            # "k_missing_rate_sample_unit":total_k_missing/len(results),
            # "value_missing_rate_sample_unit":total_value_missing/len(results),

            
        }
        print(evaluation)
        return evaluation       


    def get_evaluation_scores(self, response):
        # Regular expression to find numbers from 1 to 100
        pattern = r'\b(?!0)\d{1,2}\b|100'
        # Find all matches
        matches = re.findall(pattern, response)
        # If more than one number found, return None
        if len(matches) != 1:
            return None
        # Convert the match to integer
        number = int(matches[0])
        # Check if the number is within the range 1 to 100
        if 1 <= number <= 100:
            return number
        else:
            return None

    
    def get_turn_level_analysis(self, results):
        bleu_scores, rougel_scores = [], []
        analysis = {}
        unnecessary_api_params_calls = {}

        # action eva
        correct_act_num, all_act_num = 0, 0
        wrong_act_num_require_tool, wrong_act_num_no_tool = 0, 0

        # api eva
        api_parse_error, wrong_api_calls, correct_api_calls, have_api_but_not_call = 0, 0, 0, 0
        wrong_api_params, wrong_params_calls, correct_params_calls = 0, 0, 0
        correct_missing_params_calls, wrong_missing_params_calls = 0, 0
        unnecessary_api_calls = 0

        for sample in results:
            generation = sample["generated_sys_turn"]
            original_uttr = sample["original_sys_turn"]

            if len(original_uttr) <= 0 or generation is None:
                continue
            
            # text-based evaluation
            bleu_score = self.calculate_bleu_score(generation, original_uttr)
            rougel_score = self.calculate_rouge_l(generation, original_uttr)
            bleu_scores.append(bleu_score)
            rougel_scores.append(rougel_score)

            # intermediate evaluation
            # 1. action eva 
            all_act_num += 1
            decided_action = sample["intermediate_results"]["action"]
            if "action" not in sample["original_turn_labels"][0]: # == if ground truth actions not in self.no_tool_actions:
                # current case requires tools
                if decided_action not in self.no_tool_actions:
                    correct_act_num += 1
                else:
                    wrong_act_num_require_tool += 1
            else:
                actions = list(sample["original_turn_labels"][0]["action"].keys())
                if decided_action in actions or any([act in decided_action for act in actions]):
                    correct_act_num += 1
                elif "confirm" in actions and decided_action not in self.no_tool_actions:
                    correct_act_num += 1
                else:
                    wrong_act_num_no_tool += 1

            # 2. api eva
            if "api_name" in sample["intermediate_results"]:
                decided_api_name = sample["intermediate_results"]["api_name"]
                decided_params = sample["intermediate_results"]["params"]

                if "api_call" in sample["original_turn_labels"][0]:
                    original_api_name = sample["original_turn_labels"][0]["api_call"]["method"].lower()
                    original_api_params = sample["original_turn_labels"][0]["api_call"]["parameters"]

                    if original_api_name not in analysis:
                        analysis[original_api_name] = {}
                    analysis[original_api_name]["api_calls"] = analysis[original_api_name].get("api_calls", 0) + 1

                    if decided_api_name == None:
                        api_parse_error += 1
                        wrong_api_calls += 1
                        analysis[original_api_name]["none"] = analysis[original_api_name].get("none", 0) + 1

                    elif original_api_name == decided_api_name:
                        correct_api_calls += 1
                        analysis[original_api_name]["correct_api"] = analysis[original_api_name].get("correct_api", 0) + 1

                        if approximate_match(original_api_params, decided_params):
                            correct_params_calls += 1
                        else:
                            wrong_params_calls += 1
                    
                    else:
                        wrong_api_calls += 1
                        wrong_api_params += 1

                        analysis[original_api_name]["wrong_api"] = analysis[original_api_name].get("wrong_api", 0) + 1


                elif "progress" in sample["original_turn_labels"][0] and "dont_filled_arguments" in sample["original_turn_labels"][0]["progress"]:
                    original_api_name = sample["original_turn_labels"][0]["progress"]["active_api"].lower()
                    filled_arguments = sample["original_turn_labels"][0]["progress"]["slot_values"]
                    dont_filled_arguments = sample["original_turn_labels"][0]["progress"]["dont_filled_arguments"]
                    original_api_params = merge_filled_with_not_filled_arguments(filled_arguments, dont_filled_arguments)
                    
                    if original_api_name not in analysis:
                        analysis[original_api_name] = {}
                    analysis[original_api_name]["api_calls"] = analysis[original_api_name].get("api_calls", 0) + 1

                    if decided_api_name == None:
                        api_parse_error += 1
                        wrong_api_calls += 1
                        analysis[original_api_name]["none"] = analysis[original_api_name].get("none", 0) + 1

                    elif original_api_name == decided_api_name:
                        correct_api_calls += 1
                        analysis[original_api_name]["correct_api"] = analysis[original_api_name].get("correct_api", 0) + 1

                        if approximate_match(dont_filled_arguments, decided_params, False): # we only need to care about don't filled arguments here
                            correct_missing_params_calls += 1
                        else:
                            wrong_missing_params_calls += 1
                    
                    else:
                        wrong_api_calls += 1
                        wrong_api_params += 1

                        analysis[original_api_name]["wrong_api"] = analysis[original_api_name].get("wrong_api", 0) + 1

                elif "confirm" in actions and decided_action not in self.no_tool_actions:
                    pass

                else:
                    # there is no need to use api but the model tends to use one
                    wrong_api_calls += 1
                    unnecessary_api_calls += 1
                    unnecessary_api_params_calls[decided_api_name] = unnecessary_api_params_calls.get(decided_api_name, 0) + 1
            
            else:
                if "api_call" in sample["original_turn_labels"][0]:
                    wrong_api_calls += 1
                    have_api_but_not_call += 1
                    decided_api_name, decided_params = None, {}
                elif "progress" in sample["original_turn_labels"][0] and "dont_filled_arguments" in sample["original_turn_labels"][0]["progress"]:
                    wrong_api_calls += 1
                    have_api_but_not_call += 1
                    decided_api_name, decided_params = None, {}
                else:
                    correct_api_calls += 1

                
        # postprocess
        evaluation = {}
        evaluation["bleu_score"] = sum(bleu_scores) / len(bleu_scores)
        evaluation["rougel_score"] = sum(rougel_scores) / len(rougel_scores)

        # action scores
        evaluation["action"] = {}
        evaluation["action"]["correct_act_num"] = correct_act_num

        evaluation["action"]["wrong_act_num_require_tool"] = wrong_act_num_require_tool  / (correct_act_num + wrong_act_num_require_tool + wrong_act_num_no_tool)
        evaluation["action"]["wrong_act_num_no_tool"] = wrong_act_num_no_tool  / (correct_act_num + wrong_act_num_require_tool + wrong_act_num_no_tool)
        evaluation["action"]["acc"] = correct_act_num / (correct_act_num + wrong_act_num_require_tool + wrong_act_num_no_tool)
        
        # api scores
        evaluation["api"] = {}
    
        evaluation["api"]["correct_api_calls"] = correct_api_calls
        evaluation["api"]["wrong_api_calls"] = wrong_api_calls
        evaluation["api"]["have_api_but_not_call"] = have_api_but_not_call

        evaluation["api"]["api_parse_error"] = api_parse_error / (correct_api_calls + wrong_api_calls)
        evaluation["api"]["unnecessary_api_calls"] = unnecessary_api_calls / (correct_api_calls + wrong_api_calls)
        evaluation["api"]["acc"] = correct_api_calls / (correct_api_calls + wrong_api_calls)
        
        
        # params scores
        evaluation["api_params"] = {}
        evaluation["api_params"]["wrong_api_params"] = wrong_api_params / (correct_params_calls + wrong_api_params + wrong_params_calls + correct_missing_params_calls + wrong_missing_params_calls)
        evaluation["api_params"]["correct_params_calls"] = correct_params_calls
        evaluation["api_params"]["wrong_params_match"] = wrong_params_calls / (correct_params_calls + wrong_api_params + wrong_params_calls + correct_missing_params_calls + wrong_missing_params_calls)
        evaluation["api_params"]["correct_missing_params_calls"] = correct_missing_params_calls
        evaluation["api_params"]["wrong_missing_params_calls"] = wrong_missing_params_calls / (correct_params_calls + wrong_api_params + wrong_params_calls + correct_missing_params_calls + wrong_missing_params_calls)
        evaluation["api_params"]["acc"] = (correct_params_calls + correct_missing_params_calls) / (correct_params_calls + wrong_api_params + wrong_params_calls + correct_missing_params_calls + wrong_missing_params_calls)

        # api analysis
        evaluation["api_analysis"] = analysis
        evaluation["unnecessary_calls"] = unnecessary_api_params_calls

        api_calls, correct_apis = 0, 0
        for api_name, api_ana in analysis.items():
            api_calls += api_ana["api_calls"]
            if "correct_api" in api_ana:
                correct_apis += api_ana["correct_api"]
        evaluation["api"]["recall"] = correct_apis / api_calls

        print(evaluation)
        return evaluation


if __name__ == "__main__":
    eva = Evaluation()
    result_path = "your_result_path"
    results = read_json(result_path)
    eva.get_turn_level_analysis(results)