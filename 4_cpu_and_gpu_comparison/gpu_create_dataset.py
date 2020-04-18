import numpy as np
import json
import jsonlines
import time

techpowerup_gpus = None
benchmark_gpus = None
gpu_map = None

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def createMap(map_file):
    result_dict = {}
    with open(map_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            tid = cur_dict["tpowerup_gpu_id"]
            if cur_dict["max_score"] >= 0.95:
                result_dict[tid] = cur_dict["benchmark_gpu_id"]

    print("Num keys = ", len(result_dict.keys()))
    return result_dict

def createRegressionDataset():
    global techpowerup_gpus, benchmark_gpus, gpu_map

    score_col = "g3d_mark"
    feature_cols = []



def createClassificationDataset():
    pass

if __name__ == "__main__":
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    benchmark_gpu_file = "../../data_with_ids/gpu_benchmarks.jl"
    mapping_file = "../../data_er/ER_benchmark_gpus_and_techpowerup_gpus.jl"

    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)
    benchmark_gpus = constructDictfromJL(benchmark_gpu_file)
    gpu_map = createMap(mapping_file)



