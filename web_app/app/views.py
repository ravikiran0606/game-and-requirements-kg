from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for

@app.route('/')
def main():
    return render_template('index.html')