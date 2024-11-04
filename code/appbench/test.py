# coding: utf-8
import argparse
from tqdm import tqdm
import os
import sys
sys.path.append(".")

from utils import *
from evaluation import *
from apps.mobile import *
from models.chatgpt_resp_cralwer import ChatgptRespCrawler

from agents.meta_agent import *

if __name__ == "__main__":
    ap = argparse.ArgumentParser("arguments for inference of LLMs")
    ap.add_argument('-dd', '--dataset_dir', type=str, default="../data/test/", help="the dir of dataset")
    ap.add_argument('-tt', '--test_type', type=str, default="ss", help="the type of test datasets, can only be one of follows ss, sm, ms, mm")
    ap.add_argument('-set', '--setting', type=str, default="zero-shot", help="zero-shot or few-shot: 1-shot, 2-shot, ...")
    ap.add_argument('-eva', '--evaluation_type', type=str, default="single-turn", help="the evaluation type")
    ap.add_argument('-mt', '--model_type', type=str, default="gpt-4o", help='reader type')
    ap.add_argument('-af', '--app_first', action="store_true", help='app first')
    ap.add_argument('-mp', "--model_path", type=str, default="", help='model path')
    ap.add_argument('-ot', "--only_test",  action="store_true", help='obtain performance without inference')
    
    # /kfdata03/kf_grp/hrwang/LLM/models/english/
    args = ap.parse_args()

    # init the model
    key_path = 'conf/mine_keys.txt'
    persona = "You are a helpful assistant."
    if "gpt-3.5" in args.model_type or "gpt-4" in args.model_type:
        target_model = ChatgptRespCrawler(key_path, temperature=0, top_p=0, persona=persona, model=args.model_type)
    else:
        target_model = HuggingFaceRespCrawlerBase(model_type=args.model_type, model_path=args.model_path, temperature=0, top_p=0)
    
    judge_model = Evaluation(use_llm=True, model=args.model_type) # fix evaluation model type

    # # init the dialogue agent
    agent = MetaAgent(target_model, model_type=args.model_type, setting=args.setting, test_type=args.test_type, prompt_dir="./prompts/appbench/")

    # read the data
    dataset_path = os.path.join(args.dataset_dir, "test_" + args.test_type + ".json")
    test_cases = read_json(dataset_path)
    intermeidate_results = []
    
    # args.app_first = True
    if args.app_first:
        pred_store_file = "./results/appbench/" + args.model_type + "_app_first_" + args.setting+ "_"+ args.test_type + "_results.json"
        evaluation_store_file = "./results/appbench/" + args.model_type + "_app_first_" + args.setting+ "_"+ args.test_type + "_evaluation.json"
    else:
        pred_store_file = "./results/appbench/" + args.model_type + "_" + args.setting+ "_"+ args.test_type + "_results.json"
        evaluation_store_file = "./results/appbench/" + args.model_type + "_" + args.setting+ "_"+ args.test_type + "_evaluation.json"

    # check if there exist previous results to restore
    if os.path.exists(pred_store_file):
        intermeidate_results = read_json(pred_store_file)
    if not args.only_test:
        processed = set()
        for ind in intermeidate_results:
            processed.add(ind["input"])
        
        for sample in tqdm(test_cases[:1]):
            if sample['input'] in processed:
                continue

            try:
                decided_app_api = agent.generate_api_call(sample, retrieve_app_fist=args.app_first)

                ins = {
                    "input": sample["input"],
                    "output": sample["output"],
                    "prediction": decided_app_api,
                    "formtted_pred_api":[extract_name_params(api) for api in decided_app_api['decided_api']]
                }

                intermeidate_results.append(ins)
                processed.add(sample['input'])
                # save results
                save_json(pred_store_file, intermeidate_results)  # TODO add models and times
            except Exception as e:
                print("something wrong with the data sample", e)

    # save file
    save_json(pred_store_file, intermeidate_results)  # TODO add models and times

    evaluation = judge_model.get_appbench_analysis(intermeidate_results)
    # evaluation["success_rate"] = sum(success_results) / len(success_results)
    save_json(evaluation_store_file, evaluation)  # TODO add models and times

    



