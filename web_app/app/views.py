from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/query')
def queryPage():
    return render_template('query.html')

@app.route('/game')
def gamePage():
    return render_template('game.html')

@app.route('/visualize')
def visualizationPage():
    return render_template('visualization.html')