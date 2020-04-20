# Libraries Included:
from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS
import json
import datetime
import jsonlines

class GameKG:
    def __init__(self):
        self.my_kg = Graph()

    def define_namespaces(self):
        # Namespaces:
        self.FOAF = Namespace('http://xmlns.com/foaf/0.1/')
        self.MGNS = Namespace('http://inf558.org/games#')
        self.SCHEMA = Namespace('http://schema.org/')

        self.my_kg.bind('mgns', self.MGNS)
        self.my_kg.bind('foaf', self.FOAF)
        self.my_kg.bind('schema', self.SCHEMA)

    def define_classes(self):
        ## Enterpise Class ##
        self.enterprise_global = URIRef(self.MGNS['Enterprise'])
        self.my_kg.add((self.enterprise_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.enterprise_global, RDFS.subClassOf, self.SCHEMA["Organisation"]))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.enterprise_global, self.MGNS['ratingValue'], XSD.decimal))
        self.my_kg.add((self.enterprise_global, self.MGNS['ratingCount'], XSD.integer))
        self.my_kg.add((self.enterprise_global, self.MGNS['bestRating'], XSD.decimal))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['logo'], self.SCHEMA['URL']))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['url'], self.SCHEMA['URL']))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['foundingDate'], XSD.date))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['foundingLocation'], self.SCHEMA['Place']))

        ## Seller Class ##
        self.seller_global = URIRef(self.MGNS['Seller'])
        self.my_kg.add((self.seller_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.seller_global, RDFS.subClassOf, self.SCHEMA["seller"]))
        self.my_kg.add((self.seller_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.seller_global, self.MGNS['ratingValue'], XSD.decimal))
        self.my_kg.add((self.enterprise_global, self.MGNS['bestRating'], XSD.decimal))

        ## Platform Class ##
        self.platform_global = URIRef(self.MGNS['Platform'])
        self.my_kg.add((self.platform_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.platform_global, self.MGNS['platformName'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['platformType'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['operatingSystem'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['memory'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['cpu'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['storage'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['supportedResolution'], self.SCHEMA['Text']))

        ## Processor Class ##
        self.processor_global = URIRef(self.MGNS["Processor"])
        self.my_kg.add((self.processor_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.processor_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['numCores'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['processorClockSpeed'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['l3Cache'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['socket'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['process'], self.SCHEMA['Text']))

        ## Graphics Class ##
        self.graphics_global = URIRef(self.MGNS["Graphics"])
        self.my_kg.add((self.graphics_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.graphics_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuChip'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.SCHEMA['datePublished'], self.SCHEMA['date']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemory'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuClockSpeed'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['memoryClockSpeed'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_1'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_2'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['TMUs'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['ROPs'], XSD.integer))

        ## Minimum Supporting Device Class ##
        self.msd_global = URIRef(self.MGNS["MSD"])
        self.my_kg.add((self.msd_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.msd_global, self.MGNS['processor'], self.processor_global))
        self.my_kg.add((self.msd_global, self.MGNS['graphics'], self.graphics_global))
        self.my_kg.add((self.msd_global, self.MGNS['memory'], self.SCHEMA['Text']))
        self.my_kg.add((self.msd_global, self.MGNS['diskSpace'], self.SCHEMA['Text']))

        ### Additional Classes ###
        self.game_mode_global = URIRef(self.MGNS['GameMode'])
        self.my_kg.add((self.game_mode_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.game_mode_global, RDFS.label, Literal("Game Mode")))

        self.genre_global = URIRef(self.MGNS["Genre"])
        self.my_kg.add((self.genre_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.genre_global, RDFS.label, Literal("Genre")))

        self.theme_global = URIRef(self.MGNS["Theme"])
        self.my_kg.add((self.theme_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.theme_global, RDFS.label, Literal("Theme")))

        ## Game Class ##
        self.game_global = URIRef(self.MGNS["Game"])
        self.my_kg.add((self.game_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.game_global, RDFS.subClassOf, self.SCHEMA["Game"]))
        self.my_kg.add((self.game_global, self.SCHEMA["name"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.SCHEMA["description"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.SCHEMA["url"], self.SCHEMA["URL"]))
        self.my_kg.add((self.game_global, self.SCHEMA["datePublished"], self.SCHEMA["date"]))
        self.my_kg.add((self.game_global, self.MGNS["supportedPlatform"], self.platform_global))
        self.my_kg.add((self.game_global, self.MGNS["hasMSD"], self.msd_global))
        self.my_kg.add((self.game_global, self.MGNS["developedBy"], self.enterprise_global))
        self.my_kg.add((self.game_global, self.MGNS["publishedBy"], self.enterprise_global))
        self.my_kg.add((self.game_global, self.MGNS["hasGameMode"], self.game_mode_global))
        self.my_kg.add((self.game_global, self.MGNS["hasGenre"], self.genre_global))
        self.my_kg.add((self.game_global, self.MGNS["hasTheme"], self.theme_global))
        self.my_kg.add((self.game_global, self.MGNS["ratingValue"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["ratingCount"], XSD.integer))
        self.my_kg.add((self.game_global, self.MGNS["bestRating"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["soldBy"], self.seller_global))
        self.my_kg.add((self.game_global, self.MGNS["price"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.MGNS["oldPrice"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.MGNS["discount"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.MGNS["sellerFeedback"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.MGNS["sellerUrl"], self.SCHEMA["Text"]))

    def define_properties(self):
        ## Properties ##
        self.supported_platform_global = URIRef(self.MGNS["supportedPlatform"])
        self.my_kg.add((self.supported_platform_global, RDF.type, RDF.Property))
        self.my_kg.add((self.supported_platform_global, RDFS.label, Literal("Supported Platform", lang="en")))
        self.my_kg.add((self.supported_platform_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.supported_platform_global, RDFS.range, self.MGNS['Platform']))

        self.msd_global = URIRef(self.MGNS["hasMSD"])
        self.my_kg.add((self.msd_global, RDF.type, RDF.Property))
        self.my_kg.add((self.msd_global, RDFS.label, Literal("Minimum Supporting Device", lang="en")))
        self.my_kg.add((self.msd_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.msd_global, RDFS.range, self.MGNS['MSD']))

        self.developed_by_global = URIRef(self.MGNS["developedBy"])
        self.my_kg.add((self.developed_by_global, RDF.type, RDF.Property))
        self.my_kg.add((self.developed_by_global, RDFS.label, Literal("Developed By", lang="en")))
        self.my_kg.add((self.developed_by_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.developed_by_global, RDFS.range, self.MGNS['Enterprise']))

        self.published_by_global = URIRef(self.MGNS["publishedBy"])
        self.my_kg.add((self.published_by_global, RDF.type, RDF.Property))
        self.my_kg.add((self.published_by_global, RDFS.label, Literal("Published By", lang="en")))
        self.my_kg.add((self.published_by_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.published_by_global, RDFS.range, self.MGNS['Enterprise']))

        self.has_game_mode_global = URIRef(self.MGNS["hasGameMode"])
        self.my_kg.add((self.has_game_mode_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_game_mode_global, RDFS.label, Literal("Has Game", lang="en")))
        self.my_kg.add((self.has_game_mode_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.has_game_mode_global, RDFS.range, self.MGNS['GameMode']))

        self.has_genre_global = URIRef(self.MGNS["hasGenre"])
        self.my_kg.add((self.has_genre_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_genre_global, RDFS.label, Literal("Has Genre", lang="en")))
        self.my_kg.add((self.has_genre_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.has_genre_global, RDFS.range, self.MGNS['Genre']))

        self.has_theme_global = URIRef(self.MGNS["hasTheme"])
        self.my_kg.add((self.has_theme_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_theme_global, RDFS.label, Literal("Has Theme", lang="en")))
        self.my_kg.add((self.has_theme_global, RDFS.domain, self.MGNS['Theme']))
        self.my_kg.add((self.has_theme_global, RDFS.range, self.MGNS['Genre']))





    def define_ontology(self):
        self.define_classes()
        self.define_properties()

    def storeKG(self, kg_file_name):
        self.my_kg.serialize(kg_file_name, format="turtle")

    def addEnterpriseInstance(self, enterprise_instance):
        cur_uri = URIRef(self.MGNS[list(enterprise_instance.keys())[0]])
        cur_val = list(enterprise_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.enterprise_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["company_name"], lang="en")))

        try:
            self.my_kg.add((cur_uri, self.MGNS['ratingValue'], Literal(float(cur_val["rating_value"]))))
        except:
            pass

        try:
            self.my_kg.add((cur_uri, self.MGNS['ratingCount'], Literal(int(cur_val["num_ratings"]))))
        except:
            pass

        try:
            self.my_kg.add((cur_uri, self.MGNS['bestRating'], Literal(float(cur_val["best_rating"]))))
        except:
            pass

        if len(cur_val["logo_url"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['logo'], Literal(cur_val["logo_url"], lang="en")))

        if len(cur_val["url"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['url'], Literal(cur_val["url"], lang="en")))

        if len(cur_val["founding_date"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['foundingDate'], Literal(cur_val["founding_date"], lang="en")))

        if len(cur_val["founding_country"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['foundingLocation'], Literal(cur_val["founding_country"], lang="en")))

    def addSellerInstance(self):
        pass

    def addPlatformInstance(self, platform_instance):
        cur_uri = URIRef(self.MGNS[list(platform_instance.keys())[0]])
        cur_val = list(platform_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.platform_global))
        self.my_kg.add((cur_uri,self.MGNS['platformName'],Literal(cur_val['platform_name'],lang = "en")))

        try:
            if len(cur_val['PLATFORM TYPE']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['platformType'],Literal(cur_val['PLATFORM TYPE'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['PLATFORM TYPE']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['platformType'],Literal(cur_val['PLATFORM TYPE'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Operating System']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['operatingSystem'],Literal(cur_val['Operating System'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Memory']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['memory'],Literal(cur_val['Operating System'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['CPU']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['CPU'],Literal(cur_val['CPU'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Storage']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['storage'],Literal(cur_val['Storage'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Supported Resolutions']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['supportedResolution'],Literal(cur_val['Supported Resolutions'],lang = "en")))
        except:
            pass




    def addProcessorInstance(self, processor_instance):
        pass

    def addGraphicsInstance(self, graphics_instance):
        pass

    def addMSDInstance(self, msd_instance):
        pass

    def addGameModeInstance(self, game_mode_instance):
        pass

    def addGenreInstance(self, genre_instance):
        pass

    def addThemeInstance(self, theme_instance):
        pass

    def addGameInstance(self, game_instance):
        pass

if __name__ == "__main__":
    my_game_kg = GameKG()
    my_game_kg.define_namespaces()
    my_game_kg.define_ontology()

    igdb_companies_file = "../../data_with_ids/igdb_companies.jl"
    with open(igdb_companies_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addEnterpriseInstance(cur_dict)
            break

    my_game_kg.storeKG("sample_game_kg.ttl")
