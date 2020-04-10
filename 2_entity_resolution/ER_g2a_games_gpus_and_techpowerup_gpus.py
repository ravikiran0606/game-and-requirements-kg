import numpy as np
import json
import jsonlines
import rltk

techpowerup_gpus = None
g2a_games = None

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def getMostSimilarGPU_Techpowerup(input_gpu):
    global techpowerup_gpus

    split_words = ["/", "or"]

    game_gpus = [input_gpu]
    for cur_word in split_words:
        if cur_word in input_gpu:
            game_gpus = input_gpu.split(cur_word)
            break

    max_score = -1
    max_match_id = None
    for tgpu_id, tgpu_val in techpowerup_gpus.items():
        try:
            cur_product_name = tgpu_val["Product Name"].lower()
            cur_game_gpu = game_gpus[0].lower()
            cur_score = rltk.levenshtein_similarity(cur_game_gpu, cur_product_name)
            if cur_score > max_score:
                max_score = cur_score
                max_match_id = tgpu_id
        except:
            pass

    return max_match_id, max_score

if __name__ == "__main__":
    g2a_games_file = "../../data_with_ids/sample_g2a_games_with_requirements.jl"
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    out_file = "ER_g2a_games_gpus_and_techpowerup_gpus.jl"

    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)
    g2a_games = constructDictfromJL(g2a_games_file)
    er_mapping_result = []

    index = 0
    for key, val in g2a_games.items():
        if index%100==0:
            print("Progress count = ", index)

        cur_dict = {}
        cur_dict["g2a_games_id"] = key
        try:
            min_req = val["min_requirements"]
            cur_gpu = min_req["Graphics"]
            tpowerup_id, score = getMostSimilarGPU_Techpowerup(cur_gpu)
            # if score >= 0.5:
            #     print(cur_gpu, "-------", techpowerup_gpus[tpowerup_id]["Product Name"])
            cur_dict["techpowerup_gpu_id"] = tpowerup_id
            cur_dict["similarity_score"] = score
        except:
            cur_dict["techpowerup_gpu_id"] = "NA"
            cur_dict["similarity_score"] = -1

        er_mapping_result.append(cur_dict)
        index = index + 1

    with jsonlines.open(out_file, "w") as f:
        f.write_all(er_mapping_result)


