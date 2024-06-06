import argparse
import json
import os
import threading
import time
from pathlib import Path

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval_scripts.BaseNews import BaseNews

XINHUA_OBJECT = "xinhua_object"
XINHUA_SUBJECT = "xinhua_subject"
SAFE_OBJECT = "safe_object"
SAFE_SUBJECT = "safe_subject"

lock = threading.Lock()


class BaseCallApi(BaseNews):
    def __init__(self, model):
        super().__init__()
        self.xinhua_object_data = []
        self.xinhua_subject_data = []
        self.safe_object_data = []
        self.safe_subject_data = []
        self.all_data = {
            SAFE_OBJECT: self.safe_object_data,
            SAFE_SUBJECT: self.safe_subject_data,
            XINHUA_OBJECT: self.xinhua_object_data,
            XINHUA_SUBJECT: self.xinhua_subject_data
        }
        self.processData()
        self.model_dict = {
            "baichuan2-53b": self.callBaichuan53B,
            "Gpt4": self.callGpt4,
            "ernie": self.callErnie,
            "GPT35-Turbo": self.callGpt3_5,
            "xinyu2-70b": self.call_xinyu70b,
            "qwen-14b": self.call_qwen_14b_chat
        }
        assert model in self.model_dict.keys(), f"模型{model}的API不存在"
        self.model = model
        # 获取当前脚本所在的目录
        current_path = Path(__file__).resolve().parent
        # 获取当前脚本所在的项目根目录
        self.root_path = current_path.parent
        self.out_dir = os.path.join(self.root_path, f"output/{self.model}")
        self.data_path = os.path.join(self.out_dir, f"{self.model}_data.json")

    def getAllResult(self):
        for key, value in self.all_data.items():
            template = self.getTemplate("default", key)
            for i in value:
                prompt = template.format_map(i)
                i["prompt"] = prompt
        out_dir = os.path.join(self.root_path, "output/" + self.model)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, f"{self.model}_data.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, indent=2, ensure_ascii=False)

    def processData(self):
        for t in self.eval_data:
            assert t['type'] in self.type_to_dict.keys(), f"Unknown type exists in the data：{t['type']}"
            if self.type_to_dict[t['type']] == SAFE_OBJECT:
                self.safe_object_data.append(t)
            elif self.type_to_dict[t['type']] == SAFE_SUBJECT:
                self.safe_subject_data.append(t)
            elif self.type_to_dict[t['type']] == XINHUA_OBJECT:
                self.xinhua_object_data.append(t)
            elif self.type_to_dict[t['type']] == XINHUA_SUBJECT:
                self.xinhua_subject_data.append(t)

    def call(self, data_path, workers=10):
        assert os.path.exists(data_path), "The data file does not exist."
        file_dict = {}
        with open(data_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            success_path = os.path.join(self.out_dir, self.model + "_" + key + f"_{self.model}_success.json")
            fail_path = os.path.join(self.out_dir, self.model + "_" + key + f"_{self.model}_fail.json")
            file_dict[key] = success_path
            self.callBatchAPI(value, success_path, fail_path, title=f"get {self.model} result for " + key,
                              workers=workers)
        for key, value in file_dict.items():
            self.all_data[key] = []
            t = self.all_data[key]
            with open(value, "r", encoding="utf-8") as file:
                for line in file:
                    s = json.loads(line.strip())
                    t.append(s)
        save_path = os.path.join(self.out_dir, f"{self.model}_output.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, indent=2, ensure_ascii=False)

    def callBatchAPI(self, json_data, success_path, fail_path, title="processing:", workers=10):
        data = set()
        if os.path.exists(success_path):
            with open(success_path, "r", encoding="utf-8") as file:
                for line in file:
                    data.add(json.loads(line.strip())['prompt'])
        res = []
        for i in json_data:
            if i['prompt'] in data:
                continue
            i['model'] = self.model
            res.append(i)
        with tqdm(total=len(res)) as pbar:
            pbar.set_description(title)
            if self.model == "ernie":
                for data in res:
                    self.getModelResult(data, success_path, fail_path)
                    pbar.update(1)
            else:
                import concurrent
                with concurrent.futures.ThreadPoolExecutor(max_workers=workers,
                                                           thread_name_prefix=self.model) as executor:
                    futures = [executor.submit(self.getModelResult, data, success_path, fail_path) for data in res]
                    total_tasks = len(futures)
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        pbar.update(1)

    def getModelResult(self, data, success_path, fail_path):
        answer = self.model_dict[self.model](data['prompt'])
        if answer is None:
            data['output'] = "failed"
            with open(fail_path, 'a', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False) + "\n")
                return
        data['output'] = answer

        with lock:
            with open(success_path, 'a', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", type=str, required=True, help="model name", default="ernie"
    )
    parser.add_argument(
        "--workers", type=int, help="workers", default=1
    )
    args = parser.parse_args()
    model = BaseCallApi(args.model_name)
    model.getAllResult()
    model.call(model.data_path, workers=args.workers)
