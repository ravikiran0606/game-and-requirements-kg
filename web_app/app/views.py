from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import sayHello, getGameInformation

@app.route('/')
def main():
    result = sayHello()
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
    return render_template('visualization.html')