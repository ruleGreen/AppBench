import anthropic
from openai import OpenAI
from openai import OpenAIError
from .utils import ParseUtil


class Tool:
    def __init__(self, key_path, source="openai"):
        self.default_api_key = "your key"
        self._keys = ParseUtil.get_all_lines(key_path)
        self.key_num = len(self._keys)
        idx, valid_key = self.get_one_valid_key(0)
        self.current_key_idx = idx
        self.current_key = valid_key
        if source == "openai":
            self.client = OpenAI(api_key=self.current_key)
        elif source == "anthropic":
            self.client = anthropic.Anthropic(api_key=self.current_key)
        self.source = source
    
    def probe_query(self, prompt='早上好'):
        if self.source == "openai":
            response = self.client.completions.create(model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=16,
                top_p=1.0,
                frequency_penalty=0,
                presence_penalty=0.0)
        print('[PROBE RESP]\n', response)
        return response

    def get_one_valid_key(self, start_idx):
        """
        按序遍历所有的api key，获取第一个可用的api key
        :param start_idx: 初始时，起始位置为0；运行一段时间后要获取一个新的key，start_idx设置为上次可用的起始位置
        :return:
        """
        if len(self._keys) == 0:
            return -1, None
        elif len(self._keys) == 1:
            return 1, self._keys[start_idx].strip()
        else:
            for idx in range(self.key_num):
                if idx == start_idx:
                    continue
                self.current_key_idx = idx
                self.current_key = self._keys[idx].strip()
                try:
                    ret = self.probe_query()
                except Exception as e:
                    print(e)
                    if isinstance(e, OpenAIError):
                        error_obj = e.error
                        if error_obj is not None and (
                                error_obj['type'] == 'insufficient_quota'
                                or error_obj['type'] == 'invalid_request_error'):
                            if idx < self.key_num - 1:
                                continue
                            else:
                                return -1, None
                break
            print("[UPDATE KEY]", self.current_key)
            return self.current_key_idx, self.current_key




