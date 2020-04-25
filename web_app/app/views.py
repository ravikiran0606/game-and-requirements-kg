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
    '''
    pass game_id as 'mig_0'. do not pass the namespace -> mgns
    :return: game_info ---> dictionary (key, value pair with values being list)
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
             Note: There would be no key of the above name present in the dictionary if there isn't a relation present.
    '''
    game_id = request.args.get("game_id")
    game_info, recommended_games_info = getGameInformation(game_id)
    return render_template('game.html', game_info=game_info, rec_games_info=recommended_games_info)

@app.route('/visualize')
def visualizationPage():
    return render_template('visualization.html')