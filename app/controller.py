from app import app
from flask import render_template, request, redirect, jsonify
from datetime import datetime, date
from random import randint

@app.route('/', methods=['GET', 'POST'])
def home():
    choices = [x*randint(1, 100) for x in range(randint(1, 100))]
    return render_template('index.html', current_year=datetime.now().year, categories=choices)

@app.route('/submit_data', methods=['POST'])
def submit_data():
    today = date.today()
    return jsonify(entries=request.form, date_today=str("%s/%s/%s" % (today.month, today.day, today.year)))