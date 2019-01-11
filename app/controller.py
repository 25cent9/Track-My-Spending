"""Controls the interaction between the app and the backend"""
from app import app
from flask import render_template, request, jsonify
from datetime import date
from app.utils import send_data_to_sheet
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path='./.env')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', current_year=date.today().year)


@app.route('/debug', methods=['POST'])
def debugging():
    return jsonify(form=request.form,
                   sumission_key=getenv('SECRET-SUBMISSION-KEY'))


@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = [value for value in request.form.values()]
    today = str("%s/%s/%s" % (date.today().month, date.today().day, date.today().year))
    data.append(today)
    sent = send_data_to_sheet(data, sent_key=request.form['sub_key'],
                              send_data=True)
    if sent:
        return 'True'
    else:
        return 'False'
