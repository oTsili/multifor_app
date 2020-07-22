from flask import Blueprint, render_template, request, jsonify
from flask import json
from src.controller.database import Database
from src.models.df_model import DfModel
from src.models.indicator_df import IndicatorDf
from src.models.country_df import CountryDf
countries = Database.find_one('project_data', {'index': 'countries'})['data']

plots_blueprint = Blueprint("plots", __name__)


@plots_blueprint.route("/line", defaults={'table': None}, methods=["GET"])
@plots_blueprint.route("/line/<string:table>", methods=["GET"])
def plot_line_chart(table):
    cols = request.args.get('col')
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    return render_template("plots.html", table=table, countries=countries, indicators=indicators, cols=cols)


@plots_blueprint.route("/chart_update/<string:type>", methods=["POST"])
def chart_update(type):
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    # get the ajax variables, in json form and convert to dictionary
    data = request.form.to_dict()
    # get the vars
    cols = data['cols'].replace('[', '').replace(']', '').replace('"', '')
    table = data['selTbl'].replace(' ', '_')
    col_sel = data['col_sel'].replace(' ', '_')
    last_year = data['lastYear']
    predict_flag = data['flag']
    df_obj = DfModel(table, dates_updated=True)

    my_dict, dates, columns, to_google, df_total_col_length, df_index_length, last_year, remaining_cols \
        = df_obj.update_chart(cols, table, last_year, predict_flag=predict_flag, update_type=type, col_sel=col_sel)

    # return in json format
    return {"data": my_dict, "dates": dates, "columns": columns, "to_google": to_google, "last_year": last_year,
            "df_length": df_total_col_length, 'df_index_length': df_index_length, 'table': table,
            'indicators': indicators, 'remaining_cols': remaining_cols}


# returns the columns of the df name (table), in order to fill the 2nd droplist (columns) in the plot.htm
@plots_blueprint.route("/select", methods=["POST"])
def get_columns():
    data = request.form.to_dict()
    table = data['table'].replace(' ', '_')
    df_obj = DfModel(table)
    df_obj.save_df_full()
    cols = [x for x in df_obj.df.columns if x != 'date']

    return jsonify(cols)


@plots_blueprint.route("/initial", methods=["GET"])
def get_initial():
    indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
    col = request.args.get('col')
    table = request.args.get('tbl')
    table = table.replace(' ', '_').replace("'", '')
    if table in countries:
        # get the full df
        df_obj = CountryDf(table)
        # save to mongodb, in collection dataframes
        df_obj.save_df_full()
        df_columns = df_obj.df.columns.tolist()
        # get and save to mongodb (in collection partial dfs), the partial dfs
        df = df_obj.save_df_partial(col)
        df = df.reset_index(drop=True)
        df = df.sort_values(by=['date'], ascending=False)
        collection_name = 'partial_dfs'
        data, color_list, columns = df_obj.get_line(collection_name, col, reverse=True)
    else:
        # get the df object
        df_obj = IndicatorDf(table)
        # get the df of the df object
        df = df_obj.df
        df_obj.df = df.reset_index(drop=True)
        df_obj.df = df_obj.df.sort_values(by=['date'], ascending=False).set_index('date', drop=False)
        df = df_obj.df
        # save to mongodb
        df_obj.save_df_full()
        df_columns = [x.replace('_', ' ') for x in df.columns]
        collection_name = 'dataframes'
        data, color_list, columns = df_obj.get_line(collection_name, col)

    # get the data for the line plot
    years = [str(x).replace('-01-01', '') for x in df['date']]
    # get the data for the table plot
    to_google = df_obj.get_google_data(df, columns, years)
    years = json.dumps(years)

    return {'data': data, "columns": columns, 'years': years, "header": table, 'to_google': to_google,
            'df_columns': df_columns, "indicators": indicators}
