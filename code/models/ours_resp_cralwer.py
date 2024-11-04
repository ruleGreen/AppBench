
import time
import json
from openai import OpenAIError
from models.resp_crawler import RespCrawlerBase
from comm.utils import ParseUtil

class OursRespCrawler(RespCrawlerBase):
    """
    数据爬取工具示例，主要有以下步骤
    1) 调用load_data()方法从input_data_path文件中获取需要爬取的prompt集合
    2) 调用load_finished()方法从output_data_path文件中获取已完成的prompt集合
    3) 调用get_all_result()方法遍历所有未完成的prompt，并调用openai api获取结果，追加写到output_data_path中，每个prompt结果占一行
    基类RespCrawlerBase包含了load_data, load_finished, get_all_result的基本实现，可在自己的爬取类中重写方法
    """

    def __init__(self, keys_path, temperature, persona='', top_p=0.95, model=""):
        self.persona = persona
        self.temperature = temperature
        self.top_p = top_p
        self.model = model
        super().__init__(keys_path, temperature)

    # TODO: add your load_data impl if needed

    # 加载txt形式的输入文件，每个query占一行
    def load_data(self, input_path):
        raw_data = ParseUtil.parse_jsonl_file(input_path)
        self.input_data = raw_data
    
    """
    # 加载json形式的输入文件
    def load_data(self):
        return ParseUtil.parse_json_file(self.input_path)
    """
    def call_ours_each(self, instruction, prompt, logprobs=False, top_logprobs=None, demo=None, stop="", max_tokens=1024):
        response = None
        while response == None:
            try:
                response = self.call_ours(instruction, prompt, logprobs, top_logprobs, demo, stop, max_tokens)
            except Exception as e:
                print("API ERROR:", e)
                if isinstance(e, OpenAIError):
                    error_obj = e.error
                    if error_obj is not None: # and error_obj['type'] == 'insufficient_quota':
                        self.openai_tool.get_one_valid_key(self.openai_tool.current_key_idx)
                time.sleep(5)
        return response
    
    def call_ours(self, instruction, prompt, logprobs=False, top_logprobs=None, demo=None, stop="", max_tokens=32):
        """
        调用openai api，不同业务基于自己的需求重写此方法
        :param prompt:
        :return:
        """
        # model = "gpt-3.5-turbo-0301"
        if demo:
            response = self.tool.client.chat.completions.create(model=self.model,
                messages=[{'role':'system','content': instruction}] + demo + [{'role':'user','content':prompt}],
                temperature=self.temperature,
                logprobs = logprobs,
                top_logprobs = top_logprobs,
                max_tokens=max_tokens,
                stop=stop,
                top_p=self.top_p)
        else:
            if self.model in ["gpt-3.5-turbo-instruct"]:
                response = self.tool.client.completions.create(model=self.model,
                    prompt=instruction+ " \n " + prompt,
                    temperature=self.temperature,
                    # logprobs = logprobs,
                    # top_logprobs = top_logprobs,  # seems not work now
                    max_tokens=max_tokens,
                    stop=stop,
                    top_p=self.top_p)
            else:
                response = self.tool.client.chat.completions.create(model=self.model,
                    messages=[
                        # {'role':'system','content': instruction},
                        {'role':'user','content': instruction + " /n" + prompt}
                        ],
                    temperature=self.temperature,
                    logprobs = logprobs,
                    top_logprobs = top_logprobs,
                    max_tokens=max_tokens,
                    stop=stop,
                    top_p=self.top_p)
        return json.loads(response.model_dump_json(indent=2))

