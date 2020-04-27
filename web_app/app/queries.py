from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from rltk.similarity import levenshtein_similarity
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import rankdata


def generate_visualization_data(class_name, property_name):
    '''
    :param class_name: Name of class in the KG
    :param property_name: Name of the property in the KG
    :return(store_result): list of tuples
    '''

    '''
        works for
        1. Game ---> hasGenre
        2. Game ---> hasTheme
        3. Game ---> hasGameMode
        4. Game ---> soldBy
        5. Game ---> developedBy
        6. Game ---> publisherBy
        7. Game ---> memory_MB
        8. Game ---> diskSpace_MB
        9. Game ---> ratingValue
        10. Enterprise ---> ratingValue
        11. Seller ---> ratingValue
        12. Game ---> datePublished
    '''
    store_result = list()
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    if (class_name == 'Game') and (
            property_name == 'hasGenre' or property_name == 'hasTheme' or property_name == 'hasGameMode'):
        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>
        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:''' + class_name + ''' .
          ?game mgns:''' + property_name + ''' ?genre .
          ?genre rdfs:label ?label
        }
        group by ?label
        order by desc(?countLabel)
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    if (class_name == 'Game') and (property_name == 'soldBy' or property_name == 'developedBy' or property_name == 'publishedBy'):
        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>

        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:Game .
          ?game mgns:''' + property_name + ''' ?s .
          ?s schema:name ?label .

        }
        group by ?label
        order by desc(?countLabel)
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    if (class_name == 'Game') and (property_name == 'memory_MB' or property_name == 'diskSpace_MB'):
        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>

        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:Game .
          ?game mgns:hasMSD ?s .
          ?s mgns:''' + property_name + ''' ?label .

        }
        group by ?label
        order by desc(?countLabel)
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    if (class_name == 'Game' or class_name == 'Seller' or class_name == 'Enterprise') and (property_name == 'ratingValue'):
        cont_val = []
        sparql.setQuery('''
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX mgns: <http://inf558.org/games#>
                PREFIX schema: <http://schema.org/>
                SELECT ?label 
                WHERE{
                  ?game a mgns:'''+class_name+''' .
                  ?game mgns:ratingValue ?label .
                  FILTER(?label != -1)

                }
                ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            store_result.append(result['label']['value'])
        return store_result

    if (class_name == 'Game') and (property_name == 'datePublished'):
        sparql.setQuery('''
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX mgns: <http://inf558.org/games#>
                PREFIX schema: <http://schema.org/>
                SELECT ?label (count(?label) as ?countLabel)
                WHERE{
                ?game a mgns:Game .
                ?game schema:datePublished ?label .
                }
                group by ?label
                order by desc(?countLabel)
                LIMIT 20
                ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    #type_of_key = results['results']['bindings'][0]['label']
    '''if ('xml:lang' in type_of_key) or ('datatype' in type_of_key and 'integer' in type_of_key['datatype']):
        return store_result, "discrete"
    if ('datatype' in type_of_key and 'decimal' in type_of_key['datatype']):
        return store_result, "continuous"'''
    # print(results)
    for result in results['results']['bindings']:
        store_result.append((result['label']['value'], result['countLabel']['value']))

    return store_result

def getGameInformation(game_id):
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    game_info_dict = defaultdict(lambda: set())
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    
    #SELECT ?game_summary ?name ?released_year ?platform_name ?developer_name ?publisher_name ?game_mode_label ?genre_label ?theme_label ?#rating ?seller_name ?price ?discount ?url
    SELECT ?game_summary ?name ?released_year ?platform_name ?developer_name ?publisher_name ?game_mode_label ?genre_label ?theme_label ?rating ?seller_name ?price ?discount ?url
    WHERE{
      mgns:'''+game_id+''' a mgns:Game ;
                 schema:name ?name ;
                 schema:description ?game_summary ;
      OPTIONAL {mgns:'''+game_id+''' schema:datePublished ?released_year}.
      OPTIONAL{mgns:'''+game_id+''' mgns:supportedPlatform ?platform .
               ?platform mgns:platformName ?platform_name } .
      OPTIONAL{mgns:'''+game_id+''' mgns:developedBy ?developer .
               ?developer schema:name ?developer_name } .
      OPTIONAL{mgns:'''+game_id+''' mgns:publishedBy ?publisher .
               ?publisher schema:name ?publisher_name} .
      OPTIONAL{mgns:'''+game_id+''' mgns:hasGameMode ?game_mode .
               ?game_mode rdfs:label ?game_mode_label }.
      OPTIONAL{mgns:'''+game_id+''' mgns:hasGenre ?genre .
               ?genre rdfs:label ?genre_label }.
      OPTIONAL{mgns:'''+game_id+''' mgns:hasTheme ?theme . 
               ?theme rdfs:label ?theme_label}.
     OPTIONAL{mgns:'''+game_id+''' mgns:ratingValue ?rating} .
     OPTIONAL{mgns:'''+game_id+''' mgns:soldBy ?seller .
              ?seller schema:name ?seller_name} .
     OPTIONAL{mgns:'''+game_id+''' mgns:price_USD ?price} .
     OPTIONAL{mgns:'''+game_id+''' mgns:discount_percent ?discount} .
     OPTIONAL{mgns:'''+game_id+''' mgns:sellerURL ?url} .
      
  
}
''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results['results']['bindings']:
        for key in result.keys():
            game_info_dict[key].add(result[key]['value'])
    for key in game_info_dict.keys():
        game_info_dict[key] = list(game_info_dict[key])


    if 'game_summary' in game_info_dict:
        game_info_dict['game_summary'] = ', '.join(x for x in game_info_dict['game_summary'])
    else:
        game_info_dict['game_summary'] = 'Not Available'

    if 'name' in game_info_dict:
        game_info_dict['name'] = ', '.join(x for x in game_info_dict['name'])
    else:
        game_info_dict['name'] = 'Not Available'

    if 'released_year' in game_info_dict:
        game_info_dict['released_year'] = ', '.join(x for x in game_info_dict['released_year'])
    else:
        game_info_dict['released_year'] = 'Not Available'

    if 'platform_name' in game_info_dict:
        game_info_dict['platform_name'] = ', '.join(x for x in game_info_dict['platform_name'])
    else:
        game_info_dict['platform_name'] = 'Not Available'

    if 'developer_name' in game_info_dict:
        game_info_dict['developer_name'] = ', '.join(x for x in game_info_dict['developer_name'])
    else:
        game_info_dict['developer_name'] = 'Not Available'

    if 'publisher_name' in game_info_dict:
        game_info_dict['publisher_name'] = ', '.join(x for x in game_info_dict['publisher_name'])
    else:
        game_info_dict['publisher_name'] = 'Not Available'

    if 'game_mode_label' in game_info_dict:
        game_info_dict['game_mode_label'] = ', '.join(x for x in game_info_dict['game_mode_label'])
    else:
        game_info_dict['game_mode_label'] = 'Not Available'

    if 'genre_label' in game_info_dict:
        game_info_dict['genre_label'] = ', '.join(x for x in game_info_dict['genre_label'])
    else:
        game_info_dict['genre_label'] = 'Not Available'

    if 'theme_label' in game_info_dict:
        game_info_dict['theme_label'] = ', '.join(x for x in game_info_dict['theme_label'])
    else:
        game_info_dict['theme_label'] = 'Not Available'

    if 'rating' in game_info_dict:
        game_info_dict['rating'] = ', '.join(x for x in game_info_dict['rating'])
    else:
        game_info_dict['rating'] = 'Not Available'

    if 'seller_name' in game_info_dict:
        game_info_dict['seller_name'] = ', '.join(x for x in game_info_dict['seller_name'])
    else:
        game_info_dict['seller_name'] = 'Not Available'

    if 'price' in game_info_dict:
        game_info_dict['price'] = ', '.join(x for x in game_info_dict['price'])
    else:
        game_info_dict['price'] = 'Not Available'

    if 'discount' in game_info_dict:
        game_info_dict['discount'] = ', '.join(x for x in game_info_dict['discount'])
    else:
        game_info_dict['discount'] = 'Not Available'

    if 'url' in game_info_dict:
        game_info_dict['url'] = ', '.join(x for x in game_info_dict['url'])
    else:
        game_info_dict['url'] = 'Not Available'


    return game_info_dict


def getRecommendedGameInformation(game_id, device_config, embeddings_model):
    rating_threshold = 80
    p_score_device = device_config["processor_score"]
    g_score_device = device_config["graphics_card_score"]
    ram_size = device_config["ram_MB"]
    hdd_size = device_config["hdd_space_MB"]

    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    sparql.setQuery('''
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX mgns: <http://inf558.org/games#>
            PREFIX schema: <http://schema.org/>
            SELECT ?game_id ?game_name
            WHERE{
              ?game_id a mgns:Game .
              ?game_id schema:name ?game_name .
              
              ?game_id mgns:ratingValue ?rating_value .
              FILTER(?rating_value >= ''' + str(rating_threshold) + ''')
              
              ?game_id mgns:hasMSD ?msd_id .
              ?msd_id mgns:memory_MB ?memory_val .
              FILTER(?memory_val <= ''' + str(ram_size) + ''')
              
              ?msd_id mgns:diskSpace_MB ?disk_val .
              FILTER(?disk_val <= ''' + str(hdd_size) + ''')
              
              ?msd_id mgns:processor ?proc_id .
              ?proc_id mgns:hasCPUMark ?p_score .
              FILTER(?p_score <= ''' + str(p_score_device) + ''')
              
              ?msd_id mgns:graphics ?gr_id .
              ?gr_id mgns:g3dMark ?g_score .
              FILTER(?g_score <= ''' + str(g_score_device) + ''')
            }
            ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    game_dict = {}
    for result in results['results']['bindings']:
        gid = result['game_id']['value'].split("#")[-1]
        gname = result['game_name']['value']
        game_dict[gid] = gname

    short_game_id = game_id.split("#")[-1]
    cur_game_embed = embeddings_model[short_game_id].reshape(1, -1)

    game_urls = []
    game_embedding_matrix = []
    for gid in game_dict.keys():
        if gid == game_id:
            continue
        game_urls.append(gid)
        game_embedding_matrix.append(embeddings_model[gid])

    game_embedding_matrix = np.array(game_embedding_matrix)
    cosine_sim_vals = cosine_similarity(cur_game_embed, game_embedding_matrix)
    ranks = rankdata(-cosine_sim_vals, method="ordinal")
    top_5_idx = list(np.where(ranks <= 5)[0])

    recommended_games_info_dict = {}
    for idx, rank in zip(top_5_idx, ranks[top_5_idx]):
        cur_dict = {}
        cur_dict["game_id"] = game_urls[idx]
        cur_dict["game_name"] = game_dict[game_urls[idx]]
        recommended_games_info_dict[rank] = cur_dict

    return recommended_games_info_dict

def getGenres():
    genre_list = []
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>
        SELECT distinct ?genre_label
        WHERE{
          ?game a mgns:Game .
          ?game mgns:hasGenre ?genre .
          ?genre rdfs:label ?genre_label

        }
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results['results']['bindings']:
        genre_list.append(result['genre_label']['value'])

    return genre_list

def getClassProperties():
    class_properties_dict = {}
    class_properties_dict['Game'] = ['hasGenre','hasTheme','hasGameMode','soldBy','developedBy','publishedBy','memory_MB',
                                     'diskSpace_MB','ratingValue','datePublished']

    class_properties_dict['Enterprise'] = ['ratingValue']
    class_properties_dict['Seller'] = ['ratingValue']
    return class_properties_dict

def getPrefixQuery():
    prefix = '''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    '''
    return prefix

def getGameNameQuery():
    pattern = '''
    {
    ?game_id a mgns:Game .
    ?game_id schema:name ?game_name .
    }
    '''
    return pattern

def getReleasedYearQuery(released_year):
    pattern = '''
    {
    ?game_id schema:datePublished ?released_year .
    FILTER(?released_year = ''' + str(released_year) + ''')
    }
    '''
    return pattern

def getGenreQuery(genre):
    pattern = '''
    {
      ?game_id mgns:hasGenre ?genre .
      ?genre rdfs:label \"''' + str(genre) + '''\"@en .
      }
    '''
    return pattern

def getMinRatingQuery(min_rating):
    pattern = '''
    { 
      ?game_id mgns:ratingValue ?rating_value .
      FILTER(?rating_value > ''' + str(min_rating) + ''')
    }
    '''
    return pattern

def create_query(released_year = None, genre_label = None, min_rating = None):
    query = ''
    query += getGameNameQuery()
    if len(released_year) != 0:
        query += getReleasedYearQuery(int(released_year))
    if len(genre_label) != 0:
        query += getGenreQuery(genre_label)
    if len(min_rating) != 0:
        query += getMinRatingQuery(int(min_rating))
    return query

def final_query(param_dict):
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    prefix_query = getPrefixQuery()
    query_generated = create_query(released_year=param_dict["released_year"], genre_label=param_dict["genre"], min_rating=param_dict["min_rating"])
    query = prefix_query + 'select *' + '\n where {' + query_generated + '}'
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    res = dict()
    cols = []
    data = []
    for result in results['results']['bindings']:
        if len(cols) == 0:
            cols = list(result.keys())
        cur_dict = {}
        for key in result.keys():
            cur_dict[key] = result[key]['value']
        data.append(cur_dict)

    res["cols"] = cols
    res["data"] = data
    return res

def convertSizeToMB(cur_size):
    cur_size = cur_size.lower()
    cur_val = ""
    for cur_char in cur_size:
        if cur_char.isdigit():
            cur_val += cur_char
        else:
            break

    cur_val = int(cur_val)
    cur_unit = cur_size

    if "kb" in cur_unit:
        cur_val /= 1024
    elif "gb" in cur_unit:
        cur_val *= 1024
    elif "tb" in cur_unit:
        cur_val *= (1024 * 1024)

    return cur_val

def getCPUs():
    cpu_dict = {}
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>
        SELECT distinct ?cpu_id ?cpu_name ?cpu_score
        WHERE{
          ?cpu_id a mgns:Processor .
          ?cpu_id schema:name ?cpu_name .
          ?cpu_id mgns:hasCPUMark ?cpu_score .
        }
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results['results']['bindings']:
        cpu_id = result['cpu_id']['value']
        cpu_name = result['cpu_name']['value']
        cpu_score = result['cpu_score']['value']
        cpu_dict[cpu_id] = (cpu_name, cpu_score)

    return cpu_dict

def getGPUs():
    gpu_dict = {}
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#>
        PREFIX schema: <http://schema.org/>
        SELECT distinct ?gpu_id ?gpu_name ?gpu_score
        WHERE{
          ?gpu_id a mgns:Graphics .
          ?gpu_id schema:name ?gpu_name .
          ?gpu_id mgns:g3dMark ?gpu_score .
        }
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results['results']['bindings']:
        gpu_id = result['gpu_id']['value']
        gpu_name = result['gpu_name']['value']
        gpu_score = result['gpu_score']['value']
        gpu_dict[gpu_id] = (gpu_name, gpu_score)

    return gpu_dict

def getLinkedDeviceData(input_device_param_dict):
    device_config = {}
    valid_flag = 1

    hdd_space = input_device_param_dict["hdd_space"]
    if len(hdd_space) != 0:
        device_config["hdd_space_MB"] = convertSizeToMB(hdd_space)
    else:
        device_config["hdd_space_MB"] = -1
        valid_flag = 0

    ram = input_device_param_dict["ram"]
    if len(ram) != 0:
        device_config["ram_MB"] = convertSizeToMB(ram)
    else:
        device_config["ram_MB"] = -1
        valid_flag = 0

    # Mapping CPU
    processor = input_device_param_dict["processor"].lower()
    cpu_dict = getCPUs()
    if len(processor) != 0:
        max_match_id = None
        max_match_val = None
        max_match_score = -1
        for key, val in cpu_dict.items():
            cur_score = levenshtein_similarity(processor, val[0].lower())
            if cur_score > max_match_score:
                max_match_score = cur_score
                max_match_id = key
                max_match_val = val[0]

        device_config["processor_id"] = max_match_id
        device_config["processor_val"] = max_match_val
        device_config["processor_score"] = cpu_dict[max_match_id][1]
    else:
        device_config["processor_id"] = None
        device_config["processor_val"] = None
        device_config["processor_score"] = -1
        valid_flag = 0

    # Mapping GPU
    graphics_card = input_device_param_dict["graphics_card"].lower()
    gpu_dict = getGPUs()

    if len(graphics_card) != 0:
        max_match_id = None
        max_match_val = None
        max_match_score = -1
        for key, val in gpu_dict.items():
            cur_score = levenshtein_similarity(graphics_card, val[0].lower())
            if cur_score > max_match_score:
                max_match_score = cur_score
                max_match_id = key
                max_match_val = val[0]

        device_config["graphics_card_id"] = max_match_id
        device_config["graphics_card_val"] = max_match_val
        device_config["graphics_card_score"] = gpu_dict[max_match_id][1]
    else:
        device_config["graphics_card_id"] = None
        device_config["graphics_card_val"] = None
        device_config["graphics_card_score"] = -1
        valid_flag = 0

    return device_config, valid_flag



