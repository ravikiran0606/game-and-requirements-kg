from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict



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

def sayHello():
    result = "Hello world"
    return result

def getGameInformation(game_id):
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    game_info_dict = defaultdict(lambda: set())
    recommended_games_info_dict = {}
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
        game_info_dict['game_summary'] = ','.join(x for x in game_info_dict['game_summary'])
    else:
        game_info_dict['game_summary'] = 'Not Available'

    if 'name' in game_info_dict:
        game_info_dict['name'] = ','.join(x for x in game_info_dict['name'])
    else:
        game_info_dict['name'] = 'Not Available'

    if 'released_year' in game_info_dict:
        game_info_dict['released_year'] = ','.join(x for x in game_info_dict['released_year'])
    else:
        game_info_dict['released_year'] = 'Not Available'

    if 'platform_name' in game_info_dict:
        game_info_dict['platform_name'] = ','.join(x for x in game_info_dict['platform_name'])
    else:
        game_info_dict['platform_name'] = 'Not Available'

    if 'developer_name' in game_info_dict:
        game_info_dict['developer_name'] = ','.join(x for x in game_info_dict['developer_name'])
    else:
        game_info_dict['developer_name'] = 'Not Available'

    if 'publisher_name' in game_info_dict:
        game_info_dict['publisher_name'] = ','.join(x for x in game_info_dict['publisher_name'])
    else:
        game_info_dict['publisher_name'] = 'Not Available'

    if 'game_mode_label' in game_info_dict:
        game_info_dict['game_mode_label'] = ','.join(x for x in game_info_dict['game_mode_label'])
    else:
        game_info_dict['game_mode_label'] = 'Not Available'

    if 'genre_label' in game_info_dict:
        game_info_dict['genre_label'] = ','.join(x for x in game_info_dict['genre_label'])
    else:
        game_info_dict['genre_label'] = 'Not Available'

    if 'theme_label' in game_info_dict:
        game_info_dict['theme_label'] = ','.join(x for x in game_info_dict['theme_label'])
    else:
        game_info_dict['theme_label'] = 'Not Available'

    if 'rating' in game_info_dict:
        game_info_dict['rating'] = ','.join(x for x in game_info_dict['rating'])
    else:
        game_info_dict['rating'] = 'Not Available'

    if 'seller_name' in game_info_dict:
        game_info_dict['seller_name'] = ','.join(x for x in game_info_dict['seller_name'])
    else:
        game_info_dict['seller_name'] = 'Not Available'

    if 'price' in game_info_dict:
        game_info_dict['price'] = ','.join(x for x in game_info_dict['price'])
    else:
        game_info_dict['price'] = 'Not Available'

    if 'discount' in game_info_dict:
        game_info_dict['discount'] = ','.join(x for x in game_info_dict['discount'])
    else:
        game_info_dict['discount'] = 'Not Available'

    if 'url' in game_info_dict:
        game_info_dict['url'] = ','.join(x for x in game_info_dict['url'])
    else:
        game_info_dict['url'] = 'Not Available'


    return game_info_dict, recommended_games_info_dict

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



def getDevelopers():
    developer_list = []
    return developer_list

def getClassProperties():
    class_properties_dict = {}
    class_properties_dict['Game'] = ['hasGenre','hasTheme','hasGameMode','soldBy','developedBy','publishedBy','memory_MB',
                                     'diskSpace_MB','ratingValue','datePublished']

    class_properties_dict['Enterprise'] = ['ratingValue']
    class_properties_dict['Seller'] = ['ratingValue']
    return class_properties_dict

def prefix():
    prefix = '''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    '''
    return prefix

def game_name():
    pattern = '''
    {
    ?game a mgns:Game .
    ?game schema:name ?name .
    }
    '''
    return pattern
def released_year_query(released_year):
    pattern = '''
    {
    ?game schema:datePublished ?date .
    FILTER(?date = '''+str(released_year)+''')
    }
    '''
    return pattern

def genre(genre):
    pattern = '''
    {
      ?game mgns:hasGenre ?genre .
      ?genre rdfs:label ''' + str(genre) + '''@en .
      }
    '''
    return pattern

def rating(min_rating):
    pattern = '''
    { 
      ?game mgns:ratingValue ?label .
      FILTER(?label > '''+str(min_rating)+''')
    }
    '''
    return pattern

def create_query(released_year = None,genre_men = None,min_rating = None):
    query = ''
    query += game_name()
    if released_year != None:
        query += released_year_query(released_year)
    if genre != None:
        query += genre(genre_men)
    if min_rating != None:
        query += rating(min_rating)
    #print(query)
    return query

def final_query():
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    prefix_query = prefix()
    query_generated = create_query(released_year=2007, genre_men='"Adventure"', min_rating=60)
    query = prefix_query + 'select *' + '\n where {' + query_generated + '}'
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    res = defaultdict(lambda: list())
    for result in results['results']['bindings']:
        for key in result.keys():
            res[key].append(result[key]['value'])
    return res
