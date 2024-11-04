import os
import time
import random
import json
from openai import OpenAIError
from models.comm.utils import ParseUtil
from models.comm.tools import Tool


class RespCrawlerBase:
    """
    回复爬取工具基类
    """

    def __init__(self, keys_path, temperature):
        self.tool = Tool(keys_path)
        self.temperature = temperature

    def load_data(self, input_path):
        """
        加载待爬取的prompts；不同业务可以实现自己的加载函数。
        :return: 返回prompt的列表
        """
        self.input_data = ParseUtil.parse_json_file(input_path)

    def load_finished(self, output_path):
        """
        读取已完成的数据；如果输出目录不存在，则创建目录
        :return: 已完成的prompt的set集合，如果没有则返回空set
        """
        ret = []
        try:
            # 如果输出目录不存在，则创建目录
            if '/' in output_path:
                output_dir = '/'.join(output_path.split('/')[:-1])
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    print("[CREATE DIRECTORY]", output_dir)
            f = open(output_path, 'r', encoding='utf-8')
            lines = f.readlines()
            ret = [json.loads(line)['prompt'] for line in lines]
        except Exception as e:
            print(e)
        return set(ret)

    def call_openai(self, prompt):
        """
        调用openai api，不同业务基于各自特点重写此函数
        :param prompt:
        :return:
        """
        response = client.completions.create(model="text-davinci-003",
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=512,
            top_p=1.0)
        return response

    def get_all_result(self, input_path, output_path):
        # 加载输入数据，初始化时已完成
        self.load_data(input_path)
        
        # 获取已完成数据
        finished_prompts = self.load_finished(output_path)

        # 遍历所有prompts，获取AIP结果
        with open(output_path, 'a', encoding='utf-8') as fo:
            idx = 0
            for instance in self.input_data:
                # 没有尾部的换行符，模型一般输出的结果为"\n\n"开头；为保持统一，每个输入之后的\n先去除
                prompt = instance["prompt"].strip()
                demo = instance["demo"] if "demo" in instance else None
                idx += 1
                if idx % 100 == 0:
                    print(f"Process {idx} prompts")
                # 跳过已完成的prompt
                if prompt in finished_prompts:
                    continue
                try:
                    response = self.call_openai(prompt, demo)
                except Exception as e:
                    print("API ERROR:", e)
                    if isinstance(e, OpenAIError):
                        error_obj = e.error
                        if error_obj is not None: # and error_obj['type'] == 'insufficient_quota':
                            self.tool.get_one_valid_key(self.tool.current_key_idx)
                            # TODO: 如果获取不到可用api，可以提早退出程序
                    time.sleep(10)
                    continue
                # 为减少报错提示，每个请求休眠1到5s
                sleep_time = random.randint(1, 5)
                time.sleep(sleep_time)
                response.to_dict_recursive()
                response['prompt'] = prompt
                json_str = json.dumps(response, indent=None, ensure_ascii=False)
                fo.write(json_str + "\n")
                fo.flush()