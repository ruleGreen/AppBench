# coding: utf-8
from utils import *

def compute_f1_direct(precision, recall):
    if precision + recall == 0.0 or precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score

def argus_approximate_match(prediction, labels):
    for k, v in labels.items():
        if k not in prediction:
            return False
        if v.lower() not in prediction[k].lower() and prediction[k].lower() not in v.lower():
            return False
    return True

def extract_name_params(api_results):
    pattern = r"(\w+)\((.*)\)"
    match = re.search(pattern, api_results, re.MULTILINE)

    returned_arguments = api_results.split("=")[0].strip().split(",")
    try:
        api_name = match.group(1)
        if '_' in api_name:
            api_name = api_name.split("_")[1]

        params = match.group(2)
        params = match.group(2)

        param_pattern = r"(\w+)\s*=\s*['\"](.+?)['\"]|(\w+)\s*=\s*(\[.*\])|(\w+)\s*=\s*(\w+)"
        param_dict = {}
        for m in re.finditer(param_pattern, params):
            if m.group(1):
                param_dict[m.group(1)] = m.group(2)
            elif m.group(3):
                param_dict[m.group(3)] = m.group(4)
            elif m.group(5):
                param_dict[m.group(5)] = m.group(6)
            
        ins = {"api_name": api_name, "input": param_dict, "output": returned_arguments}
        return ins
    except:
        return None

def error_analysis(results):
    optional_arguments = ["car_type", "num_passengers", "category", "additional_luggage", "date", "seating_class", "number_of_tickets", "airlines", \
    "in_unit_laundry", "has_garage", "has_laundry_service", "number_of_adults", "rating", "starring", "subtitle_language", "theater_name", \
    "show_tyoe", "genre", "artist", "year", "album", "private_visibility", "number_of_seats", "price_range", "has_vegetarian_options", "has_seating_outdoors", \
    "is_unisex", "class", "free_entry", "good_for_kids"]

# optional_arguments = [for key in optional_arguments if key not in ["private_visibility", "number_of_seats"]]
def single_argu_value_judge(v1, v2):
    v1 = v1.lower()
    v2 = v2.lower()
    if v1.strip("'") == v2.strip("'") or v2.strip("'") in v1.strip("'")or v1.strip("'") in v2.strip("'"):
        return True
    else:
        return False

def match_evaluate(preds, labels):
    # print("******",preds,labels)
    if len(preds)== 0 or preds is None:
        return 0, 0
    # evaluate the overlap of two results
    em, hit_num = 0, 0
    preds = [x.lower() for x in preds]
    labels = [l.lower() for l in labels]
    if sorted(preds) == sorted(labels):
        em += 1
    hit_num = len(set(preds) & set(labels))
    return em, hit_num

def get_sample_analysis(sample):
    user_inst, ground_truth, prediction = sample["input"], sample["output"], sample["prediction"]
    if "decided_app_matched_with_first_step" in prediction:
        decided_app, decided_api = [x for x in prediction["decided_app_matched_with_first_step"] if x is not None and len(x)>0], prediction["decided_api"]
    else:
        decided_app, decided_api = [x for x in prediction["decided_app"] if x is not None and len(x)>0], prediction["decided_api"]

    ground_app, ground_api = ground_truth["used_app"], ground_truth["api_results"]

    # app evaluation
    pred_apps = len(decided_app)
    ground_apps = len(ground_app)
    app_em, app_hit_count = match_evaluate(decided_app, ground_app)
    if len(decided_app) == 0:
        app_f1_score = 0
    else:
        app_f1_score = compute_f1_direct(app_hit_count / pred_apps, app_hit_count / ground_apps)
    
    # api evaluation
    predicted_api_arguments = [extract_name_params(api) for api in decided_api if extract_name_params(api) is not None]
    ground_api_argumetns = [extract_name_params(api) for api in ground_api]

    decided_api_names = [sample['api_name'] for sample in predicted_api_arguments]
    ground_api_names = [sample['api_name'] for sample in ground_api_argumetns]

    pred_apis = len(decided_api_names)
    ground_apis = len(ground_api_names)
    api_em, api_hit_count = match_evaluate(decided_api_names, ground_api_names)
    if len(decided_api_names) == 0:
        api_f1_score = 0
    else:
        api_f1_score = compute_f1_direct(api_hit_count / pred_apis, api_hit_count / ground_apis)

    return api_f1_score, api_em, app_f1_score, app_em

def get_metabench_analysis(results):
    pred_correction_map  = {"la":"los angeles", "lax": "los angeles", "ciudad de mexico":"mexico city'", "nyc":"new york", "sd":"san diego","sfo":"san francisco","chi-town":"chicago"}
    
    # exact match, f1
    app_ems, app_f1s = [], []
    api_ems, api_f1s = [], []
    succ_count = 0

    # arguments analysis
    depend_argument_correct_count = 0
    key_missing, depend_key_missing = 0, 0
    key_value_mismatch, depend_key_value_mismatch = 0, 0
    total_argument_count, date_related_value_error, location_related_value_error = 0, 0, 0
    key_missing_error, key_value_mismatch_error, depend_key_missing_error, depend_key_value_mismatch_error = 0, 0, 0, 0

    for sample in results:
        user_inst, ground_truth, prediction = sample["input"], sample["output"], sample["prediction"]
        if "decided_app_matched_with_first_step" in prediction:
            decided_app, decided_api = [x for x in prediction["decided_app_matched_with_first_step"] if x is not None and len(x)>0], prediction["decided_api"]
        else:
            decided_app, decided_api = [x for x in prediction["decided_app"] if x is not None and len(x)>0], prediction["decided_api"]
        intermediate_arguments = [argu for arguments in ground_truth["result_arguments"] for argu in arguments]
        user_aware_arguments_raw = ground_truth['user_aware_arguments']
        user_aware_arguments = {'#'+ k:v for k,v in user_aware_arguments_raw.items()}
        ground_app, ground_api = ground_truth["used_app"], ground_truth["api_results"]

        api_f1_score, api_em, app_f1_score, app_em = get_sample_analysis(sample)
        app_ems.append(app_em)
        app_f1s.append(app_f1_score)
        api_ems.append(api_em)
        api_f1s.append(api_f1_score)

        # arguments evaluation
        decided_api_arg_values = {extract_name_params(api)['api_name']:extract_name_params(api)['input']  for api in decided_api if extract_name_params(api) is not None}
        ground_api_arg_values = {extract_name_params(api)['api_name']:extract_name_params(api)['input'] for api in ground_api}
        
        argument_dont_match = False
        past_pred_argu_name_values = []  # store all keys and values for previous APIs

        depend_key_value_mismatch_flag, key_value_mismatch_flag, key_missing_flag, depend_key_missing_flag = False, False, False, False
        for ground_api, ground_api_arg in ground_api_arg_values.items():

            if ground_api.lower() in decided_api_arg_values: # the api is predicted to execute
                decided_api_arg = decided_api_arg_values[ground_api]
                total_argument_count += len(ground_api_arg.keys())

                for key in ground_api_arg.keys():
                    if key in decided_api_arg:
                        ground_value = ground_api_arg[key].lower()
                        pred_value = decided_api_arg[key].lower() if decided_api_arg[key] is not None else ""
                        
                        user_aware_value = None  # user aware arguments
                        if key in user_aware_arguments:
                            user_aware_value = user_aware_arguments[key].lower()

                        past_value = None
                        for past_name_v in past_pred_argu_name_values:
                            if key == past_name_v[0]:
                                past_value = past_name_v[1]
                                break
                        
                        if pred_value.strip("'") in pred_correction_map:
                            pred_value = "'" + pred_correction_map[pred_value.strip("'")] + "'"
                        
                        # user aware arguments may directly be used to call API despite it is returned by previous APIs
                        if user_aware_value is not None and single_argu_value_judge(user_aware_value, pred_value):
                            past_pred_argu_name_values.append([key, pred_value])
                            continue
                        
                        if single_argu_value_judge(ground_value, pred_value):
                            past_pred_argu_name_values.append([key, pred_value])

                            if ground_api_arg[key] in intermediate_arguments:
                                depend_argument_correct_count += 1
                            continue
                        
                        if past_value is not None and single_argu_value_judge(past_value, pred_value):
                            if ground_api_arg[key] in intermediate_arguments:
                                depend_argument_correct_count += 1
                            continue
                        
                        # finally it is not break, then the value is mismatched
                        key_value_mismatch += 1
                        key_value_mismatch_flag = True
                        argument_dont_match = True
                        if ground_api_arg[key] in intermediate_arguments:
                            depend_key_value_mismatch += 1
                            depend_key_value_mismatch_flag = True

                        # analysis specific value mismatch
                        if "date" in key or "time" in key:
                            date_related_value_error += 1

                        if any(item in key for item in ["from", "to", "city", "where_to", "destination"]):
                            location_related_value_error += 1
                                        
                    else:
                        key_missing += 1
                        argument_dont_match = True
                        key_missing_flag = True
                        if ground_api_arg[key] in intermediate_arguments:
                            depend_key_missing += 1
                            depend_key_missing_flag = True

                # if not argus_approximate_match(decided_api_arg, ground_api_arg):
                #     argument_dont_match = True
                #     break
        
        if key_missing_flag:
            key_missing_error += 1
        if depend_key_missing_flag:
            depend_key_missing_error += 1
        if key_value_mismatch_flag:
            key_value_mismatch_error += 1
        if depend_key_value_mismatch_flag:
            depend_key_value_mismatch_error += 1
        
        if not argument_dont_match and app_em == 1 and api_em == 1:
            succ_count += 1
    
    evaluation = {
        "app": {
            "em": sum(app_ems) / len(app_ems),
            "f1": sum(app_f1s) / len(app_f1s)
        },
        "api": {
            "em": sum(api_ems) / len(api_ems),
            "f1": sum(api_f1s) / len(api_f1s)
        },
        "succ": succ_count / len(results),
        "analysis": {
            "all_key_missing": key_missing/total_argument_count,
            "depend_key_missing": depend_key_missing/total_argument_count,
            "indendpent_key_missing": (key_missing-depend_key_missing)/total_argument_count,
            "all_key_value_mismatch": key_value_mismatch/total_argument_count,
            "depend_key_value_mismatch": depend_key_value_mismatch/total_argument_count,
            "independent_key_value_mismatch": (key_value_mismatch-depend_key_value_mismatch)/total_argument_count,
            "date_value_error": date_related_value_error / key_value_mismatch,
            "location_value_error": location_related_value_error / key_value_mismatch,
            "percent_key_missing": key_missing_error/len(results),
            "percent_depend_key_missing":depend_key_missing_error/len(results),
            "percent_key_value_mismatch": key_value_mismatch_error/len(results),
            "percent_depend_key_value_mismatch": depend_key_value_mismatch_error/len(results),
        }
    }

    print(evaluation)
    return evaluation

                    
                            