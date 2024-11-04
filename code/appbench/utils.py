import os
import re
import json
import requests
import inspect
import numpy as np
from tqdm import tqdm
UNWANTED_STRINGS = [
    "Answer:",
    "Inferences:",
    "<s>",
    "</s>",
    "<pad>"
]

def load_prompt_from_dir(file_dir):
    result = {}
    for file_name in os.listdir(file_dir):
        raw_prompt = read_text(os.path.join(file_dir, file_name))
        result[file_name.split(".")[0]] = raw_prompt
    return result

def read_functions(file_path, app_name, api_name):
    with open(file_path, 'r') as file:
        file_content = file.read()
        exec(file_content, globals())
        class_obj = globals()[app_name]  # Replace 'ClassName' with your class name

        function_contents = {}
        for name, member in inspect.getmembers(class_obj):
            if inspect.isfunction(member) and name != "__init__":
                function_contents[name] = inspect.getsource(member)
    
    if api_name not in function_contents:
        return "the api is not defined yet"
    return function_contents[api_name]

def extract_api_from_class(api_name, class_obj):
    function_contents = {}
    for name, member in inspect.getmembers(class_obj):
        if inspect.isfunction(member) and name != "__init__":
            function_contents[name] = inspect.getsource(member)
            
    if api_name not in function_contents:
        return "the api is not defined yet"
    return function_contents[api_name]

def add_function(class_obj, function_name, function_source):
    if class_obj is not None:
        exec(function_source, globals())
        new_function = globals()[function_name]
        setattr(class_obj, function_name, new_function)
    else:
        print("Error: Class object not initialized.")

def extract_api_from_app(api_name, app_name):
    app_file = "./apps/" + app_name + ".py"
    api_content = read_functions(app_file, app_name, api_name)
    return api_content

def write_api_into_app(text, app_cls, api_name):
    # file_path = "./apps/" + app_name + ".py"
    # with open(file_path, 'r') as file:
    #     file_content = file.read()
    #     exec(file_content, globals())
    #     class_obj = globals()[app_name]
    add_function(app_cls, api_name, text)
    return app_cls

def delete_api_from_app(text, app_name):
    pass

def align_service_to_app(service):
    if "RentalCars" in service or "RideSharing" in service:
        app = "Rents"
    elif "Messaging" in service:
        app = "WeChat"
    else:
        app = service.split("_")[0]
    return app

def flat_apis_desc(apps_apis):
    all_apis_desc = {}
    for app_apis in apps_apis:
        for k,v in app_apis.items():
            all_apis_desc[k] = v

    apis_desc_text = ""
    for k,v in all_apis_desc.items():
        apis_desc_text += str(k) + ": " + str(v) + " \n "
    
    return apis_desc_text

def flat_apps_desc(apps_classes):
    apps_desc_text = ""
    for app_cls in apps_classes:
        app_name = app_cls.__class__.__name__ # name of App
        apps_desc_text += app_name + ": " + str(app_cls.desc) + " \n\n "
    
    return apps_desc_text

def flat_apps_apis(apps_list, apps_apis_list, return_only_desc=False):
    assert len(apps_list) == len(apps_apis_list)

    if return_only_desc:
        apps_desc_text = ""
        for i, app_name in enumerate(apps_list):
            apps_desc_text += app_name + ": " + str(apps_apis_list[i]["desc"]) + " \n\n "
        
        return apps_desc_text

    apps_desc_text = ""
    for i, app_name in enumerate(apps_list):
        apps_desc_text += app_name + ": " + str(apps_apis_list[i]) + " \n\n "
    
    return apps_desc_text

def flat_actions_desc(actions):
    actions_desc_text = ""
    for k,v in actions.items():
        actions_desc_text += str(k) + ": " + str(v) + " \n "

    return actions_desc_text


def extract_action_exp(action_call, action_list):
    for action_name in list(action_list.keys()):
        if action_name in action_call:
            return action_name, action_call
    
    pattern = r"\[(\w+)\((.*)\)\]"
    match = re.search(pattern, action_call, re.MULTILINE)

    try:
        action_name = match.group(1)
        exp = match.group(2)
    except:
        if ":" in action_call:
            index = action_call.find(":")
            action_name = action_call[:index]
        elif "(" not in action_call:
            action_name = action_call.strip("[").strip("]")
        elif "[" not in action_call:
            index = action_call.find("(")
            action_name = action_call[:index]
        else:
            action_name = "none"

        message = "action error: {action}".format(action=action_call)
        # print(message)
        exp = message

    return action_name, exp

def parse_function_string(function_string):
    # 提取函数名
    function_name = re.match(r'\s*(\w+)\(', function_string).group(1)
    
    # 提取所有带#的参数
    pattern = r"#(\w+)='[^']*'|#(\w+)=(\w+)"
    matches = re.finditer(pattern, function_string)
    
    result = {
        'function_name': function_name,
        'unquoted_parameters': {}
    }
    
    for match in matches:
        if match.group(1):
            # 如果匹配第一种模式（变量名被引号包围），忽略
            continue
        result['unquoted_parameters']["#"+match.group(2)] = match.group(3)
    # {'function_name': 'findevents', 'unquoted_parameters': {'date': 'date'}}
    return result
def topo_relations(datas):

    def build_graph(apps, api_results):
        nodes = []

        for app, api_result in zip(apps, api_results):
            left_side, function_call = api_result.split('=',1)
            parsing_result = parse_function_string(function_call)
            
            node_name = parsing_result['function_name']
            node_return = [arg.strip() for arg in left_side.strip().split(",")]
            needs = parsing_result["unquoted_parameters"]

            node_info = {"api-id":f"{node_name}-{len(nodes)}","name": node_name, "belong_to":app, "out_to":[], "returns": node_return, "needs": needs}
            nodes.append(node_info)
        
        # 1. 正向计算：考虑当前function/api，对后续所有的api的影响；
        # 2. 简化：同一个参数依赖于多个api，应当只考虑距离当前api最近的一个前置api的影响；
        for i in range(len(nodes)-1, 0, -1):
            for j in range(len(nodes)-2, -1, -1):
                # 逆向，看当前nodes[i]的所需要的前置参数，是否在nodes[j] 的返回参数中
                # 是的话，为nodes[j]添加到i的出边
                # print(i, j)
                for need in nodes[i]['needs'].values():
                    # print(need)
                    if need in nodes[j]['returns'] and not (nodes[j]['api-id'] == nodes[i]['api-id']):
                        # 逆序遍历，也逆序添加
                        nodes[j]['out_to'].insert(0, nodes[i]['api-id'])
                        # 有一个参数需要使用nodes[j]的返回值，则记录；记录后避免重复，直接跳出
                        break
        return nodes
    
    def dfs(node, graph, visited):
        path = []
        stack = [node]
        size = 0
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                path.append(vertex)
                visited.add(vertex)
                size += 1
                for neighbor in graph.get(vertex, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
        # print(len(path), size)
        assert len(path) == size
        return path

    def graph_sturc(graph):
        visited = set()
        components = []
        component_detail = []
        for node in graph:
            if node not in visited:
                # 只遍历未访问过的节点
                component = dfs(node, graph, visited)
                # print(component)
                component_detail.append(component)
                component_size  = len(component)
                components.append(component_size)
        
        # Include the nodes that are completely isolated and not in any adjacency list
        # isolated_nodes = set(graph.keys()).difference(visited)

        # components.extend([1] * len(isolated_nodes))

        return len(components), components,component_detail
    # component 数量，
    # +[[iso_node]for iso_node in isolated_nodes]
    
    topo_infos = []
    
    for data in datas:
        apps = data['output']['used_app']
        api_results = data['output']['api_results']
        nodes = build_graph(apps, api_results)
        # 开始统计graph的信息

        pure_graph = {node["api-id"]:node["out_to"] for node in nodes}
        
        num_components, sizes, comp_detail = graph_sturc(pure_graph)
        # 获取连通分量数量，每个连通分量大小
        topo_infos.append({"Number of components": num_components, "Sizes of the components": sizes, "component_detail": nodes})

    return topo_infos

def extract_name_params(code_line):
    import re
    # print("===extracting params from api call: {api_call}".format(api_call=code_line))
    # 使用正则表达式匹配函数调用的模式
    func_pattern = r"(\w[\w\d_]*)\s*=\s*(\w[\w\d_]*)\(([^)]*)\)"
    match = re.search(func_pattern, code_line)
    
    if match:
        # 抽取返回参数（可能是多个）
        return_params = [p.strip() for p in code_line.split("=")[0].split(",")]
        # 抽取函数名
        function_name = match.group(2).lower()
        if '_' in function_name:
            function_name = function_name.split("_")[1]
        # 抽取函数输入参数
        function_args = match.group(3).split(", ")
        
        # 处理输入参数使其更清晰
        args_dict = {}
        for arg in function_args:
            try:
                if "=" in arg:
                    key, value = arg.split("=")
                    if key.strip().startswith("#"):
                        args_dict[key.strip().lower()] = value.strip()
                    else:
                        args_dict['#'+key.strip().lower()] = value.strip()
                        
                else:
                    if key.strip().startswith("#"):
                        args_dict[key.strip().lower()] = ""
                    else:
                        args_dict['#'+key.strip().lower()] = ""
            except:
                continue
        # 返回解析结果
        return {
            "function_name": function_name,
            "return_parameters": return_params,
            "input_parameters": args_dict
        }
    else:
        return None
    # params_dict = {}

    # if "(" in api_call and ")" in api_call:
    #     start_params_index = api_call.find('(')
    #     end_params_index = api_call.find(')')
    #     params = api_call[start_params_index+1:end_params_index]
    #     params_list = params.split(",")

    #     for params in params_list:
    #         argument_key, argument_value = params.split("=")
    #         argument_key = argument_key.strip(" #")
    #         argument_value = argument_value.strip("'")
    #         if "?" in argument_value or "value" in argument_value:
    #             argument_value = "?"
    #         params_dict[argument_key] = argument_value
    
    # return params_dict

def extract_info(input_str):
    # Split the input string to get the app name, api name, and input arguments
    parts = input_str.strip('[]').split(': ')
    app_name = parts[0]
    api_name, args_str = parts[1].split('(')
    
    # Extract the input arguments
    args = {}
    for arg in args_str.strip(')').split(', '):
        if arg:
            key, value = arg.split('=')
            key = key.strip('#')
            value = value.strip("'")
            args[key.lower()] = value.lower() if value != '?' else '?'
    
    return app_name, api_name, args

def parse_api_into_function(api_call):
    # Find the index of the first '[' and ']'
    if "[" in api_call and "]" in api_call:
        start_index = api_call.find('[')
        end_index = api_call.find(']')
    
    try:
        if "(" in api_call and ")" in api_call:
            start_params_index = api_call.find('(')
            end_params_index = api_call.find(')')
            params = api_call[start_params_index+1:end_params_index]
            params_list = params.split(",")
            api_name = api_call[start_index+1:start_params_index]
            params_dict = {}

            for params in params_list:
                argument_key, argument_value = params.split("=")
                argument_key = argument_key.strip(" #")
                argument_value = argument_value.strip("'")
                if "?" in argument_value:
                    argument_value = "?"
                params_dict[argument_key] = argument_value
            
            return api_name, params_dict
        
    except:
        print("first parse plan is wrong, and then goto second plan")

    if "[" in api_call and "]" in api_call:
        api_call = api_call[start_index:end_index+1]
        
    pattern = r"\[(\w+)\((.*)\)\]"
    match = re.search(pattern, api_call, re.MULTILINE)

    try:
        api_name = match.group(1)
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
    except:
        # Find the index of the first '(' and ')'
        if "(" in api_call and "[" in api_call:
            start_params_index = api_call.find('(')
            start_index = api_call.find('[')
            api_name, param_dict = api_call[start_index+1:start_params_index], {}
        else:
            api_name, param_dict = None, {}
        
    return api_name, param_dict

def parse_api_format(api_name, filled_arguments, dont_filled_arguments=[]):
    api_call_text = "[" + str(api_name) + "("
    for k, v in filled_arguments.items():
        if isinstance(v, list):
            api_call_text += str(k) + '="' + str(";".join(v)) + '", '
        elif isinstance(v, str):
            api_call_text += str(k) + '="' + str(v) + '", '
        else:
            breakpoint
    
    for k in dont_filled_arguments:
        api_call_text += str(k) + '="?", '
    
    return api_call_text.strip().strip(",") + ")]"

def merge_filled_with_not_filled_arguments(filled_arguments, dont_filled_arguments):
    arguments = {}
    for k, v in filled_arguments.items():
        if isinstance(v, list):
            arguments[k] = str(";".join(v))
        elif isinstance(v, str):
            arguments[k] = str(v)

    for k in dont_filled_arguments:
        arguments[k] = "?"
    
    return arguments

def read_text(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    return "".join(data)

def read_json(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_jsonl(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f.readlines()]
    return data

def save_jsonl(filename, data):
    with open(filename, "w") as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False)
            f.write("\n")

def postprocess_result(result):
    index = result.find("answer is")
    # Check if the string is found
    if index != -1:
        # Extract the context after the specified string
        answer = result[index + len("answer is"):].strip()
        return answer
    else:
        # Return a message if the specified string is not found
        return result

def postprocess_confidence(result, return_probs=False):
    if return_probs:
        content = result["choices"][0]["logprobs"]["content"]
        log_probs = [token["logprob"] for token in content]
        probs = np.exp(log_probs) # Convert log probabilities to probabilities
        normalized_probs = probs / np.sum(probs) # Normalize probabilities
        confidence_score = sum(normalized_probs) / len(normalized_probs)
        return confidence_score
    else:
        try:
            if "\n\n" in result:
                answer, confidence = result.split("\n\n")
                confidence_score = float(confidence[12:].strip('%'))/100
            elif "\n" in result:
                answer, confidence = result.split("\n")
                confidence_score = float(confidence[12:].strip('%'))/100
            elif "%" in result:
                confidence_score = float(result[result.find('%')-2:result.find('%')])/100
            else:
                confidence_score = 0.0
        except:
            print("confience error", confidence)
            confidence_score = 0.0
    return confidence_score


def extract_sub_questions(text):
    # Define a regular expression pattern to match sub-questions
    pattern = r'#\d+: (.+?\?)'
    
    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, text)
    
    return matches

def get_response_according_to_model_type(output, model_type, is_code=False):
    if model_type in ["text-davinci-003", "gpt-3.5-turbo-instruct"]:
        response = output["choices"][0]["text"]
        prompt_tokens = output["usage"]["prompt_tokens"]
        completion_tokens = output["usage"]["completion_tokens"]
        total_tokens = prompt_tokens + (0 if completion_tokens is None else completion_tokens)
    elif "gpt-3.5" in model_type or "gpt-4" in model_type:
        response = output["choices"][0]["message"]["content"]
        if is_code:
            start_index = response.find("```") 
            end_index = response.rfind("```")
            response = response[start_index+10:end_index]

        prompt_tokens = output["usage"]["prompt_tokens"]
        completion_tokens = output["usage"]["completion_tokens"]
        total_tokens = prompt_tokens + completion_tokens
    elif "ours" in model_type:
        response = output["choices"][0]["message"]["content"]
        if is_code:
            start_index = response.find("```") 
            end_index = response.rfind("```")
            response = response[start_index+10:end_index]

        prompt_tokens = output["usage"]["prompt_tokens"]
        completion_tokens = output["usage"]["completion_tokens"]
        total_tokens = prompt_tokens + completion_tokens
    else:
        response = output["response"]
        if isinstance(response, dict): # chatglm3 outputs chinese in json format sometimes
            response = "".join(response.values()) 
        response = response.replace("<|im_end|>", "")
        total_tokens = len(response)

    return total_tokens, response # normalize_answer_without_lower(response)

def get_code_according_to_model_type(output, model_type):
    if model_type in ["text-davinci-003", "gpt-3.5-turbo-instruct"]:
        response = output["choices"][0]["text"]
        
        prompt_tokens = output["usage"]["prompt_tokens"]
        completion_tokens = output["usage"]["completion_tokens"]
        total_tokens = prompt_tokens + (0 if completion_tokens is None else completion_tokens)
    
    elif "gpt-3.5" in model_type or "gpt-4" in model_type:
        response = output["choices"][0]["message"]["content"]

        prompt_tokens = output["usage"]["prompt_tokens"]
        completion_tokens = output["usage"]["completion_tokens"]
        total_tokens = prompt_tokens + completion_tokens
    else:
        response = output["response"]
        if isinstance(response, dict): # chatglm3 outputs chinese in json format sometimes
            response = "".join(response.values()) 
        
        response = response.replace("<|im_end|>", "")
        total_tokens = len(response)
    
    if "```" in response:
        start_index = response.find("```")
        start_def_index = response.find("def")
        end_index = response.rfind("```")
        response = response[start_def_index:end_index]

    # start_index = response.find("def")
    return total_tokens, response # normalize_answer_without_lower(response)

def _validate_server(address):
    if not address:
        raise ValueError('Must provide a valid server for search')
    if address.startswith('http://') or address.startswith('https://'):
        return address
    PROTOCOL = 'http://'
    # print(f'No protocol provided, using "{PROTOCOL}"')
    return fPROTOCOL + address

def call_bing_search(endpoint, bing_api_key, query, count):
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}
    params = {"q": query, "textDecorations": True,
              "textFormat": "HTML", "count": count, "mkt": "en-GB"}
    try:
        server = _validate_server(endpoint) # server address
        server_response = requests.get(server, headers=headers, params=params)
        resp_status = server_response.status_code
        if resp_status == 200:
            result = server_response.json()
            return result 
    except:
        pass
    
    return None
    
def parse_bing_result(result):
    responses = []
    try:
        value = result["webPages"]["value"]
    except:
        return responses

    for i in range(len(value)):
        snippet = value[i]['snippet'] if 'snippet' in value[i] else ""
        snippet = snippet.replace("<b>", "").replace("</b>", "").strip()
        if snippet != "":
            responses.append(snippet)
        
    return responses

def approximate_match(arguement_one, argument_two, is_call=True):
    # print(arguement_one, argument_two)
    argument_two = {k.replace("\\", ""):v for k,v in argument_two.items()}
    
    if not is_call:
        # we only need to know the don't filled arguments whether or not correct 
        for argument in arguement_one:
            if argument in argument_two and argument_two[argument] == "?":
                return True
            # elif argument not in argument_two: # only one argument not in argument_one then it will ask for it
            #     return True  # this should not added since LLM do not infer it itself
        return False
    
    for k, v in arguement_one.items():
        if k not in argument_two:
            return False
        if v.lower() not in argument_two[k].lower() and argument_two[k].lower() not in v.lower():
            return False
    return True

# for meta-agent
def discompose_app_api(app_api_text):
    def find_slash_pattern(text):
        # The regular expression pattern
        # \s* allows for any number of whitespace characters (including none)
        # \= matches the equal sign
        # \s* allows for spaces before the underscore    
        # _ matches the underscore
        # \s* allows for spaces before the open parenthesis
        # \( matches the open parenthesis
        pattern = r'=\s*[a-zA-Z0-9]*_[a-zA-Z0-9]*\s*\('


        # Using findall to get all occurrences that match the pattern
        matches = re.search(pattern, text)
        if matches is None:
            return None
        return matches.group(0)
    def find_dot_pattern(text):
        # The regular expression pattern
        # \s* allows for any number of whitespace characters (including none)
        # \= matches the equal sign
        # \s* allows for spaces before the underscore    
        # _ matches the underscore
        # \s* allows for spaces before the open parenthesis
        # \( matches the open parenthesis
        pattern = r'=\s*[a-zA-Z0-9]*\.[a-zA-Z0-9]*\s*\('

        # Using findall to get all occurrences that match the pattern
        matches = re.search(pattern, text)
        if matches is None:
            return None

        return matches.group(0)
    
    
    app_api_list = app_api_text.split("\n")
    used_app_list, used_api_list = [], []
    
    for app_api in app_api_list:
        # app_api+="]"

        
        # Regular expression to match the pattern
        pattern = r"(\w+):\s*\n*(\[.*\])"

        # Use regular expression to find matches
        match = re.match(pattern, app_api)
        app = None
        api = None
        if match:
            app = match.group(1)
            api = match.group(2)
            api = api.replace("[", "").replace("]", "").strip()
            # print(app)

        elif ":" in app_api:
            if not (":" in app_api and  "[" in app_api and "]" in app_api):
                continue
            # print(app_api)
            app = app_api.split(":",1)[0].strip()
            api = app_api.split(":",1)[1].strip()
            api = api.replace("[", "").replace("]", "").strip()



            
        if app is None:
            parse_from_api_match = find_slash_pattern(app_api)
            if parse_from_api_match is None :
                parse_from_api_match= find_dot_pattern(app_api)
            if parse_from_api_match is not None:

                app = parse_from_api_match[0].lstrip("=").rstrip("(").strip().split('_')[0].strip()

        if app is not None and len(app) > 0:
            used_app_list.append(app)
        if api is not None:
            used_api_list.append(api)
            
    # print("===", used_api_list, used_app_list)
    return used_app_list, used_api_list


def discompose_app_api_with_app_first(app_selection_resp, app_api_text):
    def find_slash_pattern(text):
        # The regular expression pattern
        # \s* allows for any number of whitespace characters (including none)
        # \= matches the equal sign
        # \s* allows for spaces before the underscore    
        # _ matches the underscore
        # \s* allows for spaces before the open parenthesis
        # \( matches the open parenthesis
        pattern = r'=\s*[a-zA-Z0-9]*_[a-zA-Z0-9]*\s*\('


        # Using findall to get all occurrences that match the pattern
        matches = re.search(pattern, text)
        if matches is None:
            return None
        return matches.group(0)
    def find_dot_pattern(text):
        # The regular expression pattern
        # \s* allows for any number of whitespace characters (including none)
        # \= matches the equal sign
        # \s* allows for spaces before the underscore    
        # _ matches the underscore
        # \s* allows for spaces before the open parenthesis
        # \( matches the open parenthesis
        pattern = r'=\s*[a-zA-Z0-9]*\.[a-zA-Z0-9]*\s*\('

        # Using findall to get all occurrences that match the pattern
        matches = re.search(pattern, text)
        if matches is None:
            return None

        return matches.group(0)
    
    
    app_api_list = app_api_text.split("\n")
    used_app_list, used_api_list = [], []
    
    for app_api in app_api_list:
        # Regular expression to match the pattern
        
        pattern = r"(\w+): (\[.*\])"

        # Use regular expression to find matches
        match = re.match(pattern, app_api)
        app = None
        api = None
        
        if match:
            if":" in app_api:
                app = app_api.split(":",1)[0].strip()
                api = app_api.split(":",1)[1].strip()
                api = api.replace("[", "").replace("]", "").strip()
            else:
                app = match.group(1)
                api = match.group(2)
                api = api.replace("[", "").replace("]", "").strip()


            
        
        # for i in range(10):
        #     bad_case = f"app{i}"
        #     if bad_case == app:
        #         app = None
        if app is None:
            parse_from_api_match = find_slash_pattern(app_api)
            if parse_from_api_match is None :
                parse_from_api_match= find_dot_pattern(app_api)
            if parse_from_api_match is not None:

                app = parse_from_api_match[0].lstrip("=").rstrip("(").strip().split('_')[0].strip()

        # for i in range(10):
        #     bad_case = f"app{i}"
        #     if bad_case == app:
        #         app = None

        if app is not None and len(app) > 0:
            used_app_list.append(app)
        if api is not None:
            used_api_list.append(api)
            
    # print("===", used_api_list, used_app_list)
    return used_app_list, used_api_list


# Function to remove content inside parentheses
def remove_parentheses_content(s):
    return re.sub(r'\s*\(.*?\)', '', s)

if __name__ == "__main__":
    a, b = parse_api_into_function("Sure, based on the current date (2019-03-01) and the user's input, the API request that should be invoked to complete the user's current query is: [gettraintickets(from='Anaheim', to='Sacramento', date_of_journey='2019-03-05', journey_start_time='08:00', number_of_adults=1, trip_protection=False, class='Economy Premium')] Here's")
