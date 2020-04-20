# Libraries Included:
from rdflib import Graph, URIRef, BNode, Literal, XSD, Namespace, RDF, RDFS
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
        self.my_kg.add((self.seller_global, self.MGNS['bestRating'], XSD.decimal))

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
        self.my_kg.add((self.platform_global, self.SCHEMA['url'], self.SCHEMA['URL']))

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
        self.my_kg.add((self.graphics_global, self.MGNS['bus'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.SCHEMA['datePublished'], self.SCHEMA['date']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemorySize_MB'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemoryType'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemoryBits'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuClockSpeed_MHz'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['memoryClockSpeed_MHz'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_1'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_2'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['TMUs'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['ROPs'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.SCHEMA['url'], self.SCHEMA['URL']))

        ## Minimum Supporting Device Class ##
        self.msd_global = URIRef(self.MGNS["MSD"])
        self.my_kg.add((self.msd_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.msd_global, self.MGNS['processor'], self.processor_global))
        self.my_kg.add((self.msd_global, self.MGNS['graphics'], self.graphics_global))
        self.my_kg.add((self.msd_global, self.MGNS['memory_MB'], self.SCHEMA['Text']))
        self.my_kg.add((self.msd_global, self.MGNS['diskSpace_MB'], self.SCHEMA['Text']))

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
        self.my_kg.add((cur_uri, self.MGNS['platformName'], Literal(cur_val['platform_name'],lang = "en")))

        try:
            if len(cur_val['PLATFORM TYPE:']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['platformType'], Literal(cur_val['PLATFORM TYPE:'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Operating System']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['operatingSystem'], Literal(cur_val['Operating System'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Memory']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['memory'], Literal(cur_val['Memory'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['CPU']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['CPU'], Literal(cur_val['CPU'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Storage']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['storage'], Literal(cur_val['Storage'],lang = "en")))
        except:
            pass

        try:
            if len(cur_val['Supported Resolutions']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['supportedResolution'], Literal(cur_val['Supported Resolutions'],lang = "en")))
        except:
            pass


    def addProcessorInstance(self, processor_instance):
        cur_uri = URIRef(self.MGNS[list(processor_instance.keys())[0]])
        cur_val = list(processor_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.processor_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["name"], lang="en")))

        try:
            if len(cur_val['Cores']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['numCores'], Literal(cur_val['Cores'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Clock']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['processorClockSpeed'], Literal(cur_val['Clock'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['L3 Cache']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['l3Cache'], Literal(cur_val['L3 Cache'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Socket']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['socket'], Literal(cur_val['Socket'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Process']) != 0:
                self.my_kg.add((cur_uri,self.MGNS['process'], Literal(cur_val['Process'], lang="en")))
        except:
            pass

    def addGraphicsInstance(self, graphics_instance):
        cur_uri = URIRef(self.MGNS[list(graphics_instance.keys())[0]])
        cur_val = list(graphics_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.graphics_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["product_name"], lang="en")))
        self.my_kg.add((cur_uri, self.SCHEMA['url'], Literal(cur_val["product_url"], lang="en")))

        try:
            if len(cur_val['gpu_chip']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['gpuChip'], Literal(cur_val['gpu_chip'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['bus_info']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['bus'], Literal(cur_val['bus_info'], lang="en")))
        except:
            pass

        try:
            if cur_val['released_year'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['datePublished'], Literal(cur_val['released_year'])))
        except:
            pass

        try:
            if cur_val['memory_val_mb'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemorySize_MB'], Literal(cur_val['memory_val_mb'])))

            if len(cur_val["memory_type"]) != 0:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemoryType'], Literal(cur_val["memory_type"], lang="en")))

            if cur_val['memory_bits'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemoryBits'], Literal(cur_val['memory_bits'])))
        except:
            pass

        try:
            if cur_val['gpu_clock_mhz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuClockSpeed_MHz'], Literal(cur_val['gpu_clock_mhz'])))
        except:
            pass

        try:
            if cur_val['memory_clock_mhz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['memoryClockSpeed_MHz'], Literal(cur_val['memory_clock_mhz'])))
        except:
            pass

        try:
            if cur_val['shader_1'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['shader_1'], Literal(cur_val['shader_1'])))
        except:
            pass

        try:
            if cur_val['shader_2'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['shader_2'], Literal(cur_val['shader_2'])))
        except:
            pass

        try:
            if cur_val['tmus'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['TMUs'], Literal(cur_val['tmus'])))
        except:
            pass

        try:
            if cur_val['rops'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['ROPs'], Literal(cur_val['rops'])))
        except:
            pass

    def addMSDInstance(self, cur_cpu_uri, cur_gpu_uri, memory_val, disk_space_val):
        cur_msd_node = BNode()
        self.my_kg.add((cur_msd_node, RDF.type, self.msd_global))
        self.my_kg.add((cur_msd_node, self.MGNS['processor'], URIRef(cur_cpu_uri)))
        self.my_kg.add((cur_msd_node, self.MGNS['graphics'], URIRef(cur_gpu_uri)))
        self.my_kg.add((cur_msd_node, self.MGNS['memory_MB'], Literal(memory_val)))
        self.my_kg.add((cur_msd_node, self.MGNS['diskSpace_MB'], Literal(disk_space_val)))
        return cur_msd_node

    def addGameModeInstance(self, game_mode_instance):
        pass

    def addGenreInstance(self, genre_instance):
        pass

    def addThemeInstance(self, theme_instance):
        pass

    def __convertSizeToMB(self, cur_size):
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

    def addGameInstance(self, igdb_game_id, igdb_game, g2a_game, gpu_list, cpu_list):
        cur_uri = URIRef(igdb_game_id)
        self.my_kg.add((cur_uri, RDF.type, self.game_global))

        try:
            disk_space = g2a_game["min_requirements"]["Disk space"]
            disk_space_val = self.__convertSizeToMB(disk_space)
            memory = g2a_game["min_requirements"]["Memory"]
            memory_val = self.__convertSizeToMB(memory)

            for cur_cpu_uri in cpu_list:
                for cur_gpu_uri in gpu_list:
                    cur_msd_node = self.addMSDInstance(cur_cpu_uri, cur_gpu_uri, memory_val, disk_space_val)
                    self.my_kg.add((cur_uri, self.MGNS["hasMSD"], cur_msd_node))
        except:
            pass

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def createMAPforGPU(json_lines_file):
    score_threshold = 0.75
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = cur_dict["g2a_games_id"]
            val = []

            gpu1 = cur_dict["tpowerup_gpu1"]
            gpu2 = cur_dict["tpowerup_gpu2"]
            if bool(gpu1):
                if gpu1["max_score"] >= score_threshold:
                    val.append(gpu1["max_match_id"])

            if bool(gpu2):
                if gpu2["max_score"] >= score_threshold:
                    val.append(gpu2["max_match_id"])

            result_dict[key] = val
    return result_dict

def createMAPforCPU(json_lines_file):
    score_threshold = 1.2
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = cur_dict["g2_games_id"]
            val = []

            cpu1 = cur_dict["tpowerup_cpu1"]
            cpu2 = cur_dict["tpowerup_cpu2"]
            if bool(cpu1):
                if cpu1["max_match_score"] >= score_threshold:
                    val.append(cpu1["max_match_id"])

            if bool(cpu2):
                if cpu2["max_match_score"] >= score_threshold:
                    val.append(cpu2["max_match_id"])

            result_dict[key] = val
    return result_dict

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

    igdb_platforms_file = "../../data_with_ids/igdb_platforms.jl"
    with open(igdb_platforms_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addPlatformInstance(cur_dict)
            break

    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs_cleaned.jl"
    with open(techpowerup_gpu_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addGraphicsInstance(cur_dict)
            break

    techpowerup_cpu_file = "../../data_with_ids/techpowerup_cpu.jl"
    with open(techpowerup_cpu_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addProcessorInstance(cur_dict)
            break


    # Adding Games:
    g2a_games_file = "../../data_with_ids/g2a_games_with_requirements.jl"
    igdb_games_file = "../../data_with_ids/igdb_games.jl"
    er_g2a_igdb_file = "../../data_er/er_g2a_igdb_levenshtein_jaro_rijul_v4_short.jl"
    er_g2a_gpu_file = "../../data_er/ER_g2a_games_gpus_and_techpowerup_gpus_short.jl"
    er_g2a_cpu_file = "../../data_er/g2a_game_techpowerup_cpu_er_v3.jl"

    g2a_games = constructDictfromJL(g2a_games_file)
    igdb_games = constructDictfromJL(igdb_games_file)
    er_g2a_gpu = createMAPforGPU(er_g2a_gpu_file)
    er_g2a_cpu = createMAPforCPU(er_g2a_cpu_file)

    with open(er_g2a_igdb_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)

            # igdb_game_id = cur_dict["igdb_key"]
            igdb_game_id = "mgns_igdb_games_10"
            igdb_game = igdb_games[igdb_game_id]

            # g2a_game_id = cur_dict["similar_g2a_key"]
            g2a_game_id = "mgns_g2a_games_with_requirements_10"
            g2a_game = g2a_games[g2a_game_id]

            gpu_list = er_g2a_gpu[g2a_game_id]
            cpu_list = er_g2a_cpu[g2a_game_id]

            my_game_kg.addGameInstance(igdb_game_id, igdb_game, g2a_game, gpu_list, cpu_list)
            break

    my_game_kg.storeKG("sample_game_kg.ttl")
