import json
import logging
import os.path
import time
from pathlib import Path
import erniebot
import requests

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DefaultConfig


class BaseNews:
    r"""
    Evaluation base class
    Includes：
        Dataset template: Xinhua News Agency Objective, Xinhua News Agency Subjective, Security Objective, Security Subjective
        token，url for call gpt
    """

    def __init__(self):
        config_data, self.eval_data = self.getConfigAndDataSet()
        # Model template dictionary
        self.prompt_template = config_data["prompt_template"]
        self.type_to_dict = config_data['type_to_dict']
        # gpt4 Relevant information
        gpt4_config = config_data['gpt4']
        self.gpt4_token = gpt4_config['token']
        self.gpt4_url = gpt4_config['url']
        # baichuanApi
        baichuan_config = config_data["baichuan-53b"]
        self.baichuan_token = baichuan_config["token"]
        self.baichuan_url = baichuan_config["url"]
        # Enrie APi
        ernie_config = config_data["ernie"]
        self.ernie_token = ernie_config["token"]
        self.ernie_url = ernie_config["url"]

        self.safe_system_message = config_data['safe_system_message']
        self.xinhua_system_message = config_data['xinhua_system_message']
        self.not_load_model_types = config_data["not_load_model_types"]
        self.gpt4_response = None
        self.getConfigAndDataSetUsePyConfig()
        self.logger = logging.getLogger()
    def getConfigAndDataSetUsePyConfig(self):
        # Model template dictionary
        self.prompt_template = DefaultConfig.prompt_template
        self.type_to_dict = DefaultConfig.type_to_dict
        self.api_map = DefaultConfig.api_map
        # gpt4 Relevant information
        gpt4_config = DefaultConfig.api_map['gpt4']
        self.gpt4_token = gpt4_config['token']
        self.gpt4_url = gpt4_config['url']
        # baichuanApi
        baichuan_config = DefaultConfig.api_map["baichuan-53b"]
        self.baichuan_token = baichuan_config["token"]
        self.baichuan_url = baichuan_config["url"]
        # Enrie APi
        ernie_config = DefaultConfig.api_map["ernie"]
        self.ernie_token = ernie_config["token"]
        self.ernie_url = ernie_config["url"]

        self.safe_system_message = DefaultConfig.safe_system_message
        self.xinhua_system_message = DefaultConfig.xinhua_system_message
        self.not_load_model_types = DefaultConfig.not_load_model_types
        self.gpt4_response = None

    def getConfigAndDataSet(self):
        # Get the directory of the current script
        current_path = Path(__file__).resolve().parent
        # Get the root directory of the current script's project
        root_path = current_path.parent
        # Root directory of configuration file
        config_path = os.path.join(root_path, "config/eval_config.json")
        assert os.path.exists(config_path), "Configuration file does not exist."
        with open(config_path, "r", encoding='utf-8') as f:
            config_data = json.load(f)
        # Dataset directory
        data_path = os.path.join(root_path, "dataset/news_sorted.json")
        eval_data = None
        if os.path.exists(data_path):
            with open(data_path, "r", encoding='utf-8') as f:
                eval_data = json.load(f)
        return config_data, eval_data

    def inference(self):
        pass

    def inferenceByVllm(self):
        pass

    def getTemplate(self, model_type, data_type):
        r"""
        :param model_type:
        :param data_type:Data type: general subjective and objective, security subjective and objective
        :return:
        """
        assert data_type in self.prompt_template.keys(), "Non-existent data type"
        t = self.prompt_template[data_type]
        if model_type in t.keys():
            return t[model_type]
        return t["default"]

    def callGpt4(self, query, gpt_model="gpt-4-1106-preview"):
        count = 0
        while True:
            try:
                model = gpt_model
                messages = [{"role": "user", "content": query}]
                data = {
                    "model": model,
                    "messages": messages,
                }
                headers = {
                    "Authorization": "Bearer " + self.gpt4_token,
                    "Content-Type": "application/json"
                }
                response = requests.post(self.gpt4_url, headers=headers, data=json.dumps(data))
                decoded_data = json.loads(response.text)
                self.gpt4_response = decoded_data
                result = decoded_data["choices"][0]["message"]["content"]
                return result
            except Exception as e:
                count += 1
                print(self.gpt4_response)
                print("Retry.....{}".format(count))
                time.sleep(1)
                if count > 1:
                    return None

    def callBaichuan53B(self, query):
        data = {
            "model": "Baichuan2-Turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": True
        }
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.baichuan_token
        }
        response = requests.post(self.baichuan_url, data=json_data, headers=headers, timeout=60)
        if response.status_code == 200:
            s = response.text
            ss = s.split("\n")
            res = ""
            for i in ss:
                if i == "" or i == "data: [DONE]":
                    continue
                i = i[6:]
                decoded_data = json.loads(i)
                if "choices" in decoded_data.keys():
                    res += decoded_data["choices"][0]["delta"]["content"]
            return res
        else:
            return None

    def callErnie(self, query):
        erniebot.access_token = self.ernie_token
        try:
            response = erniebot.ChatCompletion.create(
                model="ernie-4.0",
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                disable_search=True
            )
            if response.rcode == 200:
                return response.result
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def callGpt3_5(self, query):
        model = "gpt-3.5-turbo"
        return self.callGpt4(query, model)

    def call_qwen_14b_chat(self, query: str, n: int = 1, return_list: bool = False, temperature: float = 0.3,
                           top_p: float = 0.8, max_tokens: int = 4096, frequency_penalty: float = 0.05):
        url = ""
        query = "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n{}<|im_end|>\n<|im_start|>assistant\n".format(
            query)
        payload = {
            "model": "qwen14b_vllm",
            "params": {
                "request_id": "",
                "prompt": query,
                "temperature": temperature,
                "top_p": top_p,
                'n': n,
                "max_tokens": max_tokens,
                "frequency_penalty": frequency_penalty,
                "stop": ["<|im_end|>"]
            }
        }
        headers = {
            'token': ""
        }
        count = 0
        while True:
            try:
                response = requests.request("POST", url, headers=headers, json=payload)
                if return_list or n > 1:
                    result = json.loads(response.text)['text'][0]
                else:
                    result = json.loads(response.text)['text'][0][0]
                return result
            except Exception as e:
                count = count + 1
                if count > 5:
                    return None

    def call_xinyu70b(self, query: str, n: int = 1, return_list: bool = False, temperature: float = 0.3,
                      top_p: float = 0.8, max_tokens: int = 4096, frequency_penalty: float = 0.05):
        url = ""
        query = "Human:{}\nAssistant:".format(query)
        payload = {
            "model": "selfmodel_70b_vllm",
            "params": {
                "request_id": "",
                "prompt": query,
                "temperature": temperature,
                "top_p": top_p,
                'n': n,
                "max_tokens": max_tokens,
                "frequency_penalty": frequency_penalty
            }
        }
        headers = {
            'token': ""
        }
        count = 0
        while True:
            try:
                response = requests.request("POST", url, headers=headers, json=payload)
                if return_list or n > 1:
                    result = json.loads(response.text)['text'][0]
                else:
                    result = json.loads(response.text)['text'][0][0]
                return result
            except Exception as e:
                # log.info(f"retry_time :{count}" + str(e))
                count = count + 1
                if count > 5:
                    return None


if __name__ == '__main__':
    b = BaseNews()
    prompt = "Who are you?"
    model_dict = {
        "baichuan-53b": b.callBaichuan53B,
        "ernie": b.callErnie,
        "gpt35-turbo": b.callGpt3_5,
        "xinyu2-70b": b.call_xinyu70b,
        "qwen-14b": b.call_qwen_14b_chat,
        "gpt4": b.callGpt4
    }
    res = model_dict["gpt4"](prompt)
    print(res)
