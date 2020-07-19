# Game-and-Requirements-KG
Building a Knowledge Graph about Games, Requirements and Purchase source! 

## Project Submissions

**Project Demo**: The youtube video about our project demo can be found here: [https://www.youtube.com/watch?v=wa_C4xqBmjo](https://www.youtube.com/watch?v=wa_C4xqBmjo) <br>
**Project Presentation Slides**: The project presentation slides can be found here: [Slides](submissions/rselvam_rvohra_INF558_final_project_presentation.pdf) <br>
**Project Report**: The project report can be found here: [Report](submissions/rselvam_rvohra_INF558_final_project_report.pdf) <br>

## Modules

### 1. Crawling

​		a) Games information was crawled from [IGDB.com](https://www.igdb.com/discover)	

​		b) Information about the system specifications required to play a particular game, the cheapest purchase source was crawled from [G2A.com](https://www.g2a.com)

​		c) The details about all the CPU's and GPU's was crawled from [Techpower.com](https://www.techpowerup.com)

​		d) The baseline information about the performance scores for the CPU and GPU was crawled from [Passmark.com](https://www.passmark.com)

The code for all these crawling tasks can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/tree/master/1_crawling/crawlers)

### 2. Entity Resolution

​		a) The first entity resolution task that we handled was mapping the games crawled from IGDB to the games crawled from G2A. This mapping was necessary to enrich the games with information like the device specifications, cheapest purchase source. Code can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/2_entity_resolution/ER_igdb_g2a_rijul.py)

​		b) The second entity linking task that we did was to map the CPU and GPU information from G2A to the CPU and GPU information crawled from techpowerup. The entity linking code for the CPU can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/2_entity_resolution/ER_g2a_cpu_techpowerup_cpu_v1.py). Code for GPU linking can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/2_entity_resolution/ER_g2a_games_gpus_and_techpowerup_gpus.py)

​		c) Code for linking the CPU information from techpowerup to get the benchmark score from Passmark can be [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/2_entity_resolution/ER_techpowerup_cpubenchmark.py). Similar code for the GPU can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/2_entity_resolution/ER_benchmark_gpus_and_techpowerup_gpus.py)	

### 3. Ontology Mapping

We designed our own ontology. Our ontology for this project has a total of 7 classes. We inherited some of the classes and properties from schema.org and customized others according to our needs. The entire ontology file can be found [here](https://github.com/ravikiran0606/Game-and-Requirements-KG/blob/master/3_ontology_mapping/Game%20Requirements%20Ontology.pdf)

### 4. CPU and GPU Comparison

### 5. Building the KG

### 6. Querying the KG

### 7. Evaluation

### 8. Node Embeddings


(readme yet to be completed)


