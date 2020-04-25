from SPARQLWrapper import SPARQLWrapper, JSON

def get_games_based_on_genre(genre,sparql):
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        SELECT ?game ?game_name
        WHERE{
        ?game a mgns:Game .
        ?game mgns:hasGenre ?genre . 
        ?genre a mgns:Genre .
        ?genre rdfs:label ''' +str(genre)+'''@en .
        ?game schema:name ?game_name .
        }
        LIMIT 20
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_games_having_rating_higher(rating,sparql):
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        SELECT ?game ?game_name ?rating
        WHERE{
        ?game a mgns:Game .
        ?game mgns:ratingValue ?rating .
        FILTER(?rating > ''' +str(rating)+''')
        ?game schema:name ?game_name .
        }
        LIMIT 20
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_game_based_on_price_and_seller_url(lower_price,higher_price,sparql):
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    SELECT ?game ?game_name ?price ?seller_url
    WHERE{
    ?game a mgns:Game .
    ?game mgns:price_USD ?price .
    FILTER(?price > '''+str(lower_price)+ ''' && ?price < ''' + str(higher_price) + ''')
    ?game schema:name ?game_name .
    ?game mgns:sellerURL ?seller_url
    }
    LIMIT 20
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


if __name__ == '__main__':
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    # Query games based on genre
    '''genre = '"Adventure"'
    results = get_games_based_on_genre(genre,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ",result['game']['value'],end = ' ')
        print("Game Name: ",result['game_name']['value'])'''

    # Query game names based on rating
    '''rating = 80
    results = get_games_having_rating_higher(rating,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ", result['game']['value'], end=' ')
        print("Game Name: ", result['game_name']['value'], end = ' ')
        print("Rating: ", result['rating']['value'])'''

    # Query game and seller url based on price range
    lower_price = 10
    higher_price = 20
    results = get_game_based_on_price_and_seller_url(lower_price,higher_price,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ", result['game']['value'], end=' ')
        print("Game Name: ", result['game_name']['value'], end = ' ')
        print("Game Price: ",result['price']['value'], end = ' ')
        print('Seller URL: ',result['seller_url']['value'])


