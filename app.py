from flask import Flask, render_template
from src.controller.database import Database

from src.routes.plot_router import plots_blueprint
from src.routes.pie_router import pie_blueprint
from src.routes.nav_router import nav_blueprint
from src.routes.map_router import map_blueprint

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

app.register_blueprint(plots_blueprint, url_prefix="/plots")
app.register_blueprint(pie_blueprint, url_prefix="/pie")
app.register_blueprint(nav_blueprint, url_prefix="/nav")
app.register_blueprint(map_blueprint, url_prefix="/")


# fix the browser CORS request restrictions
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route("/error/<string:code>", methods=["GET"])
def error_page(code):
    if code == 404 or code == '404':
        return render_template("error_404.html")
    elif code == 500 or code == '500':
        return render_template("error_500.html")


@app.route("/about", methods=["GET"])
def about_page():
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template("About.html", countries=countries, indicators=indicators)


@app.route("/feedback", methods=["GET"])
def feedback_page():
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template("feedback.html", countries=countries, indicators=indicators)


@app.route("/references", methods=["GET"])
def references_page():
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template("references.html", countries=countries, indicators=indicators)


if __name__ == "__main__":
    app.run(debug=True)