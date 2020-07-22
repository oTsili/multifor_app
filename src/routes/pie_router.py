from flask import Blueprint, render_template
from src.models.pestel_model import Pestel_category_model
from src.controller.database import Database

pie_blueprint = Blueprint("pie", __name__)


@pie_blueprint.route('/', methods=["GET"])
def pestel_pie():
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template("pie_chart.html", countries=countries, indicators=indicators)


@pie_blueprint.route("/indicators", methods=["POST"])
def get_pestel():
    pestel_headers = ['POLITICAL', 'ECONOMICAL', 'SOCIAL', 'TECHNOLOGICAL', 'ECOLOGICAL', 'LEGISLATIVE']
    pestel_values = []

    for category in pestel_headers:
        google_data = Pestel_category_model(category).construct_google_data()
        pestel_values.append(google_data)
    return {"pestel": pestel_values}