from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import sayHello, getGameInformation
from app.queries import generate_visualization_data


@app.route('/')
def main():
    result = generate_visualization_data("Game",'ratingValue')
    print(result)
    return render_template('index.html')

@app.route('/query')
def queryPage():
    return render_template('query.html')

@app.route('/game', methods=['GET'])
def gamePage():
    game_id = request.args.get("game_id")
    result_dict = getGameInformation(game_id)
    return render_template('game.html', result=result_dict)

@app.route('/visualize')
def visualizationPage():
    return render_template('visualization.html')