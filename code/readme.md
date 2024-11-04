### Openai Keys Setting
put your openai key into conf/mine_keys.txt

if there are multiple keys, put them in different lines

### Running
run scripts/run.sh in current directory
```
bash scripts/run.sh
```

You can use the following args to control this procedure:

```
--dataset_dir: default as ../data/test/. Remember to set the dataset path if you have changed the orginal github repo.

--test_type  : the type of test datasets, can only be one of follows ss, sm, ms, mm

--setting    : zero-shot or few-shot: 1-shot, 2-shot, ...

--model_type : set the inference model

--app_first  : Whether to first select the app name and them fulfill api selectiong and arguments generation.

--model_path : If you use non-openai models, please specify the model_path

--only_test  : whether to obtain performance without inference
```

### dir information

**./apps**: preconstrcuted apps and their apis

**./models**: all of the model implementation

**./prompts**: prompts for testing the models, including app_first manner and the other.

**./results**: all of the evaluation results will be here

**./scripts**: scripts to test the model on AppBench, using the following codes.

- **./appbench/test.py**: main test file

- **./appbench/evaluation.py**: code for evaluating the model results to return the performance