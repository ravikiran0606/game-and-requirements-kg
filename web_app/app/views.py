from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import sayHello, getGameInformation, getClassProperties
from app.queries import generate_visualization_data

@app.route('/')
def main():
    # result = generate_visualization_data("Game",'ratingValue')
    result = ""
    print(result)
    return render_template('index.html')

@app.route('/query')
def queryPage():
    return render_template('query.html')

@app.route('/game', methods=['GET'])
def gamePage():
    game_id = request.args.get("game_id")
    game_info, recommended_games_info = getGameInformation(game_id)

    return render_template('game.html', game_info=game_info, rec_games_info=recommended_games_info)

@app.route('/visualize')
def visualizationPage():
    class_properties_dict = getClassProperties()
    return render_template('visualization.html', class_properties_dict=class_properties_dict)

@app.route('/getVisualizationData', methods=['GET', 'POST'])
def getVisualizationData():
    class_name = request.args.get("class_name")
    property_name = request.args.get("property_name")
    x_vals = ['giraffes', 'orangutans', 'monkeys', 'abc', 'ravi', 'kiran']
    y_vals = [20, 14, 23, 20, 15, 10]
    result_dict = {}
    for i,j in zip(x_vals, y_vals):
        result_dict[i] = j
    return result_dict