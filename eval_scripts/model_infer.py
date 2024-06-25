import argparse
import json
import logging
import os.path
from pathlib import Path

import torch
from tqdm import tqdm
from BaseNews import BaseNews
from vllm import LLM, SamplingParams
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    BloomForCausalLM,
    AutoModel,
    LlamaForCausalLM
)

XINHUA_OBJECT = "xinhua_object"
XINHUA_SUBJECT = "xinhua_subject"
SAFE_OBJECT = "safe_object"
SAFE_SUBJECT = "safe_subject"


class SafeNews(BaseNews):
    r"""
    :param model_path:str model path
    :param model_name:str  model name
    :param model_type:str   model type
    :param output_dir:str   output dir of result
    :param data_path:str    dataset path
    :param temperature:float
    :param top_k:float
    :param top_p:float
    :param vllm:bool    Whether to use vLLM acceleration
    """

    def __init__(self,
                 model_path,
                 model_name,
                 model_type,
                 output_dir,
                 data_path,
                 temperature: float,
                 top_k: int,
                 top_p: float,
                 vllm: bool,
                 tensor_parallel_size,
                 max_num_batched_tokens):
        super().__init__()
        assert os.path.exists(model_path), "Model does not exist."
        self.model_path = model_path
        self.model_name = model_name
        self.model_type = model_type
        self.output_dir = output_dir
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.vllm = vllm
        self.object_result = []
        self.subject_result = []
        self.xinhua_object_data = []
        self.xinhua_subject_data = []
        self.safe_object_data = []
        self.safe_subject_data = []
        self.is_load_model = self.model_type not in self.not_load_model_types
        if tensor_parallel_size is None:
            self.tensor_parallel_size = 8
        else:
            self.tensor_parallel_size = min(8, tensor_parallel_size)
        if max_num_batched_tokens is None:
            self.max_num_batched_tokens = 8192
        else:
            self.max_num_batched_tokens = max_num_batched_tokens
        self.all_data = {
            SAFE_OBJECT: self.safe_object_data,
            SAFE_SUBJECT: self.safe_subject_data,
            XINHUA_OBJECT: self.xinhua_object_data,
            XINHUA_SUBJECT: self.xinhua_subject_data
        }
        # Initialize model.
        if self.is_load_model:
            if vllm:
                self.llm, self.sampling_params = self.getModel()
            else:
                self.model, self.tokenizer = self.getModel()
        # Initialize dataset.
        if data_path is not None:
            assert os.path.exists(data_path), "Dataset does not exist."
            with open(data_path, "r", encoding='utf-8') as f:
                self.eval_data = json.load(f)
        self.processData()

    def getModel(self):
        r"""
        This function returns an instance of the model used for evaluation.
        If vllm is used, return llm, sampling_params.
        Otherwise, return the original model, tokenizer.
        :return:
        """
        if self.vllm:
            if self.model_type.lower() == "self-70b":
                tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                added_tokens = {'cls_token': '<CLS>', 'sep_token': '<SEP>', 'additional_special_tokens': ['<EOD>'],
                                'mask_token': '<MASK>', 'pad_token': '<PAD>'}
                tokenizer.add_special_tokens(added_tokens)
                llm = LLM(model=self.model_path, tokenizer=self.model_path, tensor_parallel_size=self.tensor_parallel_size)
                llm.set_tokenizer(tokenizer)
                sampling_params = SamplingParams(temperature=self.temperature, top_p=0.7, max_tokens=100,
                                                 stop_token_ids=[2, 60301])
            else:
                llm = LLM(model=self.model_path, trust_remote_code=True,
                          max_num_batched_tokens=self.max_num_batched_tokens,
                          tokenizer_mode='auto', tensor_parallel_size=self.tensor_parallel_size)
                sampling_params = SamplingParams(max_tokens=8192, temperature=self.temperature, top_k=20, top_p=0.7)
            return llm, sampling_params
        model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True
        )
        return model, tokenizer

    def processData(self):
        for t in self.eval_data:
            assert t['type'] in self.type_to_dict.keys(), f"Unknown type exists in the data: {t['type']}"
            if self.type_to_dict[t['type']] == SAFE_OBJECT:
                self.safe_object_data.append(t)
            elif self.type_to_dict[t['type']] == SAFE_SUBJECT:
                self.safe_subject_data.append(t)
            elif self.type_to_dict[t['type']] == XINHUA_OBJECT:
                self.xinhua_object_data.append(t)
            elif self.type_to_dict[t['type']] == XINHUA_SUBJECT:
                self.xinhua_subject_data.append(t)

    def eval(self):
        r"""
        :return:
        """
        if self.is_load_model:
            if self.vllm:
                self.inferenceByVllm()
            else:
                self.inference()
            self.saveResult()

    def inference(self):
        if self.model_type == "qwen":
            gen_kwargs = {
                "do_sample": "True",
                "eos_token_id": [
                    151645
                ],
                "max_new_tokens": 2048,
                "pad_token_id": 151643,
                "repetition_penalty": 1.2,
                "temperature": 0.5,
                "top_k": 40,
                "top_p": 0.7
            }
        else:
            gen_kwargs = {
                "temperature": self.temperature,
                "top_k": self.top_k,
                "top_p": self.top_p,
                "repetition_penalty": 1.0,
                "max_new_tokens": 4096,
            }
        with tqdm(total=len(self.eval_data)) as pbar:
            pbar.set_description('inference:')
            for key, value in self.all_data.items():
                template = self.getTemplate(self.model_type, key)
                for i in value:
                    prompt = template.format_map(i)
                    i["prompt"] = prompt
                    if self.model_type == "chatglm":
                        self.model = self.model.eval()
                        output, history = self.model.chat(self.tokenizer, prompt, history=[])
                    elif self.model_type == "aquilaChat":
                        from aquila_predict import predict
                        output = predict(self.model, prompt, tokenizer=self.tokenizer, max_gen_len=2048, top_p=0.9,
                                         seed=123, topk=15, temperature=1.0, sft=True,
                                         model_name="AquilaChat2-34B-16K")
                    elif self.model_type == "xverse":
                        self.model = self.model.eval()
                        history = [{"role": "user", "content": prompt}]
                        output = self.model.chat(self.tokenizer, history)
                    else:
                        inputs = self.tokenizer.encode(prompt, return_tensors="pt").cuda()
                        outputs = self.model.generate(inputs, **gen_kwargs)[0]
                        output = self.tokenizer.decode(outputs[len(inputs[0]) - len(outputs):], skip_special_tokens=True)
                    i['output'] = output
                    pbar.update(1)

    def inferenceByVllm(self):
        safe_subject_prompts = []
        safe_object_prompts = []
        xinhua_object_prompts = []
        xinhua_subject_prompts = []
        all_prompts = {
            SAFE_OBJECT: safe_object_prompts,
            SAFE_SUBJECT: safe_subject_prompts,
            XINHUA_OBJECT: xinhua_object_prompts,
            XINHUA_SUBJECT: xinhua_subject_prompts
        }
        logging.info("Prepare data.")

        for key, value in all_prompts.items():
            template = self.getTemplate(self.model_type, key)
            for i in self.all_data[key]:
                prompt = template.format_map(i)
                i["prompt"] = prompt
                value.append(prompt)
        logging.info("Data preparation is complete.")
        logging.info("Model generation begins.")
        for key, value in all_prompts.items():
            outputs = self.llm.generate(value, self.sampling_params)
            cnt = 0
            for i in self.all_data[key]:
                i['output'] = outputs[cnt].outputs[0].text
                cnt += 1

    def saveResult(self):
        if self.output_dir is not None:
            output_dir = self.output_dir
        else:
            current_path = Path(__file__).resolve().parent
            # Get the root directory of the current script's project.
            root_path = current_path.parent
            output_dir = os.path.join(root_path, f"output/{self.model_name}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        save_path = os.path.join(output_dir, f"{self.model_name}_output.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, indent=2, ensure_ascii=False)


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", type=str, help="model name"
    )
    parser.add_argument(
        "--model_path", type=str, help="model path"
    )
    parser.add_argument(
        "--model_type", type=str, default="default", help="model type"
    )
    parser.add_argument(
        "--output_dir", type=str, default=None, help="output directory"
    )
    parser.add_argument(
        "--data_path", type=str, default=None, help="data directory"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.1, help="temperature"
    )
    parser.add_argument(
        "--top_k", type=int, default=20, help="top_k"
    )
    parser.add_argument(
        "--top_p", type=float, default=0.7, help="top_p"
    )
    parser.add_argument(
        "--vllm", action="store_true", help="vllm"
    )
    parser.add_argument(
        "--tensor_parallel_size", type=int, default=1, help="tensor_parallel_size"
    )
    parser.add_argument(
        "--max_num_batched_tokens", type=int, required=False, help="max_num_batched_tokens"
    )

    return parser.parse_args()


def eval_news(args):

    safe = SafeNews(model_path=args.model_path,
                    model_name=args.model_name,
                    model_type=args.model_type,
                    output_dir=args.output_dir,
                    data_path=args.data_path,
                    temperature=args.temperature,
                    top_k=args.top_k,
                    top_p=args.top_p,
                    vllm=args.vllm,
                    tensor_parallel_size=args.tensor_parallel_size,
                    max_num_batched_tokens=args.max_num_batched_tokens)
    safe.eval()


if __name__ == '__main__':
    args = parse_argument()
    eval_news(args)

