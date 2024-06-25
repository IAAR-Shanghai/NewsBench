import argparse


from calculateScore import cal_score
from BaseCallApi import call_api_model


def parse_argument():
    parser = argparse.ArgumentParser(description="NewsBench Eval")
    infer_parse = parser.add_argument_group(title="Model Inference Options")
    cal_parse = parser.add_argument_group(title="Calculate Scores Options")
    infer_parse.add_argument(
        "--api", action="store_true", help="call api get model output"
    )
    infer_parse.add_argument(
        "--model_name", type=str, help="model name"
    )
    infer_parse.add_argument(
        "--model_path", type=str, help="model path"
    )
    infer_parse.add_argument(
        "--model_type", type=str, default="default", help="model type"
    )
    infer_parse.add_argument(
        "--output_dir", type=str, default=None, help="output directory"
    )
    infer_parse.add_argument(
        "--data_path", type=str, default=None, help="data directory"
    )
    infer_parse.add_argument(
        "--temperature", type=float, default=0.1, help="temperature"
    )
    infer_parse.add_argument(
        "--top_k", type=int, default=20, help="top_k"
    )
    infer_parse.add_argument(
        "--top_p", type=float, default=0.7, help="top_p"
    )
    infer_parse.add_argument(
        "--vllm", action="store_true", help="vllm"
    )
    infer_parse.add_argument(
        "--tensor_parallel_size", type=int, default=1, help="tensor_parallel_size"
    )
    infer_parse.add_argument(
        "--max_num_batched_tokens", type=int, required=False, help="max_num_batched_tokens"
    )
    infer_parse.add_argument(
        "--workers", type=int, help="workers", default=1
    )
    infer_parse.add_argument(
        "--url", type=str, required=False, help="model api url"
    )
    infer_parse.add_argument(
        "--token", type=str, required=False, help="model api token"
    )
    infer_parse.add_argument(
        "--served_model_name", type=str, required=False, help="model api name"
    )
    cal_parse.add_argument(
        "--model_name_or_result_path", type=str, required=False, help="model name"
    )
    cal_parse.add_argument(
        "--gpt_model", type=str, default="gpt-4o", required=False,
        help="gpt model,choices[gpt-4-1106-preview,gpt-3.5-turbo,gpt-4o]"
    )
    cal_parse.add_argument(
        "--gpt_eval", action="store_true", help="call gpt for eval"
    )
    return parser.parse_args()


def eval():
    args = parse_argument()
    args.model_name_or_result_path = args.model_name
    if args.api:
        call_api_model(args)
    else:
        from model_infer import eval_news
        eval_news(args)
    cal_score(args)


if __name__ == '__main__':
    eval()
