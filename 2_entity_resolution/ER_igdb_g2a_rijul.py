import jsonlines
import rltk
import re
import time

def create_block():
    with jsonlines.open('igdb_games.jl') as reader:
        with jsonlines.open('g2a_games_with_requirements.jl') as g2a_reader:
            block = defaultdict(lambda: [[], []])
            for igdb_obj in reader:
                for key, val in igdb_obj.items():
                    game_name = val['game_name']
                    if 'DUPLICATE' in game_name or 'duplicate' in game_name or 'Duplicate':
                        print('dup present')
                        game_name = re.sub('DUPLICATE', '', game_name)
                        game_name = re.sub('duplicate', '', game_name)
                        game_name = re.sub('Duplicate', '', game_name)
                        game_name = re.sub('\[.*?\]', '', game_name)
                        #print(game_name)
                    # game_name = re.sub('[^a-zA-Z0-9 \n\.]','',game_name)
                    if game_name.startswith(' '):
                        #print('starts with space')
                        game_name = game_name[1:]
                        #print(game_name)
                    gen_block_key = re.sub(' ', '', game_name)
                    gen_block_key = gen_block_key.lower()
                    first_word = gen_block_key[:3]
                    if first_word == 'the':
                        first_word = gen_block_key[3:6]
                    block_key = first_word
                    block[block_key][0].append({key: game_name})
                    '''else:
                      block_key = val['game_name'].split(' ')[1].lower()[:3]
                      block[block_key][0].append({key:val['game_name']})'''
            for g2a_obj in g2a_reader:
                for key, val in g2a_obj.items():
                    if val['title'].startswith(' '):
                        g2a_game_name = val['title'][1:]
                    else:
                        g2a_game_name = val['title']

                    g2a_block_key = re.sub(' ', '', g2a_game_name)
                    g2a_block_key = g2a_block_key.lower()
                    first_word = g2a_block_key[:3]
                    if first_word == 'the':
                        first_word = g2a_block_key[3:6]
                    block_key = first_word
                    block[block_key][1].append({key: g2a_game_name})
                    '''else:
                      block_key = val['title'].split(' ')[1].lower()[:3]
                      block[block_key][1].append({key:val['title']})'''
    return block

def er_task(block):
    st = time.time()
    similar = defaultdict(lambda: [])

    for i, (key, val) in enumerate(block.items()):
        if (i + 1) % 1 == 0:
            print("time taken for {} is {}".format(i, time.time() - st))
        '''if i == 1:
          continue'''
        for igdb_obj in val[0]:
            for igdb_game_key, igdb_game_name in igdb_obj.items():
                max_score = -1
                matching_key = ''
                matching_name = ''
                for g2a_obj in val[1]:
                    for g2a_game_key, g2a_game_name in g2a_obj.items():
                        score = rltk.levenshtein_similarity(igdb_game_name, g2a_game_name)
                        if score > max_score:
                            max_score = score
                            matching_key = g2a_game_key
                            matching_name = g2a_game_name
                if max_score > 0.4:
                    similar[key].append({(igdb_game_key, igdb_game_name): (matching_key, matching_name, max_score)})
                else:
                    similar[key].append({(igdb_game_key, igdb_game_name): ('', '', -1)})
    print("total time taken: ", time.time() - st)
    return similar

def write_result_to_jl(similar):
    with jsonlines.open('er_g2a_igdb_levenshtein_rijul_v2.jl', 'w') as writer:
        for key, val in similar.items():
            # print(val)
            for obj in val:
                # print(obj)
                obj_to_write = {"igdb_key": '', 'igdb_game_name': '', 'similar_g2a_key': '','similar_g2a_game_name': ''}
                # k,v = list(obj)[0][0],list(obj)[0][1]
                # obj = {list(obj)[0][0],list(obj)[0][1]}
                # obj_to_write = dict({k[0]:k[1],'similar':{v[0],v[1],v[2]}})
                # print(type(list(obj)[0][0]))
                # print(list(obj.items()))

                obj_to_write['igdb_key'] = list(obj.items())[0][0][0]
                obj_to_write['igdb_game_name'] = list(obj.items())[0][0][1]
                obj_to_write['similar_g2a_key'] = list(obj.items())[0][1][0]
                obj_to_write['similar_g2a_game_name'] = list(obj.items())[0][1][1]
                obj_to_write['similarity_score'] = list(obj.items())[0][1][2]
                writer.write(obj_to_write)


if __name__ == '__main__':
    block = create_block()
    similar = er_task(block)
    write_result_to_jl(similar)
