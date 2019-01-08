from app import app
from flask import render_template, request
from datetime import date
from app.utils import send_data_to_sheet, get_categories


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', current_year=date.today().year,
                           categories=get_categories())


@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = [value for value in request.form.values()]
    today = str("%s/%s/%s" % (date.today().month, date.today().day, date.today().year))
    data.append(today)
    send_data_to_sheet(data, send_data=False)
    return render_template('index.html', current_year=date.today().year, categories=get_categories())