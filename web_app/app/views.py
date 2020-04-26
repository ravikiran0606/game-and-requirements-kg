from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import getGameInformation, getClassProperties, getGenres
from app.queries import generate_visualization_data, final_query

gl_hdd_space = None
gl_ram = None
gl_processor = None
gl_graphics_card = None

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/storeConfig', methods=['GET', 'POST'])
def storeConfig():
    global gl_hdd_space, gl_ram, gl_processor, gl_graphics_card

    hdd_space = request.form["hdd_space"]
    ram = request.form["ram"]
    processor = request.form["processor"]
    graphics_card = request.form["graphics_card"]

    gl_hdd_space = hdd_space
    gl_ram = ram
    gl_processor = processor
    gl_graphics_card = graphics_card
    print([gl_hdd_space, gl_ram, gl_processor, gl_graphics_card])

    valid_flag = 1

    if len(gl_hdd_space) == 0 or len(gl_ram) == 0 or len(gl_processor) == 0 or len(gl_graphics_card) == 0:
        valid_flag = 0

    if valid_flag == 1:
        return "<h3 class=\"w3-green\">Successfully stored the device configuration!</h3>"
    else:
        return "<h3 class=\"w3-red\">The given device configuration is invalid! Please submit again!</h3>"

@app.route('/query')
def queryPage():
    global gl_hdd_space, gl_ram, gl_processor, gl_graphics_card

    print(gl_hdd_space, gl_ram, gl_processor, gl_graphics_card)
    genre_list = [] #getGenres()
    return render_template('query.html', genre_list=genre_list)

@app.route('/queryData', methods=['GET', 'POST'])
def queryData():
    global gl_hdd_space, gl_ram, gl_processor, gl_graphics_card
    input_param_dict = dict(request.form)
    print(input_param_dict)
    result_dict = final_query(input_param_dict)
    return result_dict


@app.route('/game', methods=['GET'])
def gamePage():
    '''
    pass game_id as 'mig_0'. do not pass the namespace -> mgns
    :return: game_info ---> dictionary (key, value pair with values being string)
                    keys are:
                    1. game_summary
                    2. name
                    3. released_year
                    4. platform_name
                    5. developer_name
                    6. publisher_name
                    7. game_mode_label
                    8. genre_label
                    9. theme_label
                    10. rating
                    11. seller_name
                    12. price
                    13. discount
                    14. url
             Note:
    '''
    game_id = request.args.get("game_id")
    if game_id is None:
        game_id = "mig_0"
    game_info, recommended_games_info = getGameInformation(game_id)
    return render_template('game.html', game_info=game_info, rec_games_info=recommended_games_info)

@app.route('/getPropertiesForClass', methods=['GET', 'POST'])
def getPropertiesForClass():
    cur_class_name = request.args.get("class_name")
    class_properties_dict = getClassProperties()
    cur_prop_list = class_properties_dict[cur_class_name]
    result = {}
    result["vals"] = cur_prop_list
    return result

@app.route('/visualize')
def visualizationPage():
    class_properties_dict = getClassProperties()
    class_list = list(class_properties_dict.keys())
    return render_template('visualization.html', class_list=class_list)

@app.route('/getVisualizationData', methods=['GET', 'POST'])
def getVisualizationData():
    class_name = request.args.get("class_name")
    property_name = request.args.get("property_name")
    result = generate_visualization_data(class_name, property_name)
    result_dict = {}

    if not isinstance(result[0], tuple):
        result_dict["data_type"] = "continuous"
        result_dict["x_vals"] = result
    else:
        x_vals = []
        y_vals = []
        for key, val in result:
            x_vals.append(key)
            y_vals.append(val)

        result_dict = {}
        result_dict["data_type"] = "discrete"
        result_dict["x_vals"] = x_vals
        result_dict["y_vals"] = y_vals

    return result_dict
