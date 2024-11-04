#!/bin/bash

setting="zero-shot"  # few-shot
# model_types="qwen1.5-7b-chat qwen1.5-14b-chat llama3-8b-instruct"
# model_types="vicuna-13b-v1.5" # "mistral-7b-v0.3 qwen1.5-72b-chat llama3-70b-instruct"
model_types="gpt-4o"
model_types="gpt-4-1106-preview"
# model_types="qwen1.5-14b-chat" # "mistral-7b-v0.3 qwen1.5-72b-chat llama3-70b-instruct"

for model_type in $model_types
do
    for setting in "zero-shot"
        do 
        for tt in "ss" 
            do
                python3 appbench/test.py \
                    --model_type $model_type \
                    --app_first \
                    --test_type $tt \
                    --setting $setting
            done
        done
done