import json
from src.controller.database import Database


def get_indicators(header):
    """
    Gets the indicators names, from mongodb, for a specific PESTEL header.

    :param header: PESTEL header
    :return: a list with the specific's PESTEL header indicators
    """
    pestel_categories = Database.find_one("project_data", {"index": "pestel_categories"});

    return pestel_categories['data'][header]


def table_to_google(header):
    """
    Creates a dictionary, to be used from Google visualization table API, in order to construct
    the PESTEL indicators tables, for a specific header/category

    :param header: the PESTEL header/category
    :return: the dictionary, to be used from GOOGLE API
    """
    pestel_categories = Database.find_one("project_data", {"index": "pestel_categories"});

    colns = [{"id": header,
             "label": header,
              "type": "string" # if df[col].dtype == 'O' else "number"
              }]

    rows = []
    for row in pestel_categories['data'][header]:
        row = [{"v": f"<a class='indicator-link'>{row}</a>"}]
        rows.append({"c": row})
    to_google = json.dumps({"cols": colns, "rows": rows})

    return to_google