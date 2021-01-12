from flask import Blueprint, render_template, request, jsonify
from src.controller.database import Database

map_blueprint = Blueprint("map", __name__)


@map_blueprint.route('/', methods=["GET"])
def europe_map():
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template('index.html', countries=countries, indicators=indicators)


@map_blueprint.route("/codes", methods=["POST"])
def get_country_codes():
    country_codes = Database.find_one("project_data", {"index": "country_codes"})
    country_codes['_id'] = str(country_codes['_id'])
    return country_codes

