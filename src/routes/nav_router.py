from flask import Blueprint


from src.controller.database import Database

nav_blueprint = Blueprint("nav", __name__)


@nav_blueprint.route("/indicators", methods=["POST"])
def get_countries_indicators():
        ind = Database.find_one("project_data", {"index": "indicators"})
        cn = Database.find_one("project_data", {"index": "countries"})
        ind['_id'] = str(ind['_id'])
        cn['_id'] = str(cn['_id'])

        return {"indicators": ind, "countries": cn}