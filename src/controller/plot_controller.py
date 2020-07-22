import pandas as pd
from bokeh.palettes import Category10
import itertools
from flask import json
from src.controller.database import Database
from src.controller.forecasting_controller import predict, scale
import random
import json

pd.set_option('display.float_format', lambda x: '%.3f' % x)


# function to get colors
def color_gen(pallete=Category10):
    """
    Generates color from specified pallete.

    :param pallete: pallete to be used
    :return: single color value from specified pallete
    """
    yield from itertools.cycle(pallete[10])


colors = color_gen()


def get_line_data(df_name, columns, collection_name, reverse=False):
    """
    Gets the data, needed for the scatter plot, from mongodb and converts them to json format
    :param df_name: the table-df name
    :param columns: the columns to display. If there have been added any columns to the table (multi-line scatter),
     it displays them.
    :param collection_name: the mongodb collection name to get the df data
    :param reverse: Boolean. If true, reverse the df in descending order
    :return: the json data, with the values of the df columns,  a list with generated colors to be used in the
    different lines of the scatter, and a list with the columns names to be displayed
    """
    data = []
    color_list = []
    cols = [x for x in columns if x != 'date']
    for col, color in zip(cols, colors):
        data.append(json.dumps(Database.from_mongodb_json(collection_name, df_name, col, reverse=reverse)))
        color_list.append(color)

    return data, color_list, columns


def table_to_google(df, columns, years):
    """
    Converts the df to a dictionary, in the form needed for the google visualization table API

    :param df: the df to be converted
    :param columns: the list with the df columns
    :param years: a list with the years, which are going to be displayed as index in the table, and as x axis
     in the scatter
    :return: the dictionary with the df in the google visualization format
    """
    if 'date' not in columns:
        temp_cols = ['date']
        for col in columns:
            temp_cols.append(col)
        columns = temp_cols

    df['date'] = [x for x in years]

    colns = [{"id": col.replace('_', ' '),
             "label": col.replace('_', ' '),
              "type": "string" # if df[col].dtype == 'O' else "number"
              } for col in columns]

    jsdata = json.loads(df.to_json(orient="split"))["data"]
    rows = []
    for row in jsdata:
        row = [{"v": val} for val in row]
        rows.append({"c": row})
    to_google = json.dumps({"cols": colns, "rows": rows})

    return to_google


def update_df_chart(self, cols, selected_table, last_year, predict_flag=False, update_type=None, col_sel=None):
    """
    Updates the scatter and the table, by adding or removing columns and rows, or conducting prediction.

    :param self: the df object which calls the function, like being inside the class
    :param cols: the existing columns of the table/scatter
    :param selected_table: the df/table name
    :param last_year: the last element of the 'date' column inside the df, referring to the last date
    :param predict_flag: Boolean. If yes, then it was called by the getPredicted js function
    :param update_type: String: referring to the kind of update to be implemented, and provided by ajax call.
    It can take the folloing values: ('addCol', 'remCol', 'remYear', 'addYear', 'update', 'switch'), for adding
    a column/line, removing column/line, removing a row/date, adding a row/date, and pressing the
    update or switch btns in js.
    :return: data to be used in scatter and table updating
    """
    remaining_cols = None
    # initialize the columns list with the date
    columns = ['date']
    # if there are more columns than one
    cols = cols.split(',')
    for x in cols:
        columns.append(x)
    # get the df from the mongoDB
    countries = Database.find_one('project_data', {'index': 'countries'})['data']
    # if the df is a country and the columns are indicators, it is required merging and scaling
    df = self.df
    df_total_col_length = len(df.columns)
    df_index_length = len(df['date'])
    raw_dates = [x for x in df['date'].sort_values(ascending=False) if int(x.split('-')[0]) <= int(last_year)]
    if update_type == 'addCol':
        remaining_columns = [x for x in df.columns if x.replace(' ', '_') not in columns]

        if len(remaining_columns) > 0:
            # columns.append(random.choice(remaining_columns))
            columns.append(col_sel)
            remaining_cols = [x for x in remaining_columns if x.replace(' ', '_') != col_sel]
        # get the current dates in YYYY-mm-dd format
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) <= int(last_year)]
    elif update_type == 'remCol':
        remaining_cols = [x for x in df.columns if x.replace(' ', '_') not in columns]
        remaining_cols.append(columns[-1])
        columns = columns[:-1]
        # get the current dates in YYYY-mm-dd format
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) <= int(last_year)]
    elif update_type == 'addYear':
        if predict_flag == 'True':
            # TODO if there has been conducted already a forecasting just get the next year, avoiding the prediction
            df = predict(df)
            Database.df_to_mogodb('dataframes', self.name, df, scaling=False, alias=False)
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) <= int(last_year) + 1]
    elif update_type == 'remYear':
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) < int(last_year)]
    elif update_type == 'switch':
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) <= int(last_year)]
    elif update_type == 'update':
        raw_dates = [x for x in df['date'].sort_values(ascending=False) if
                     int(x.split('-')[0]) <= int(last_year)]
    # convert the dates in YYYY format, in which it will be plotted
    dates = [x.split('-')[0] for x in raw_dates]
    # replace whitespaces in indicators
    df.columns = [x.replace(' ', '_') for x in df.columns]
    columns = [x.replace(' ', '_') for x in columns]
    # map the df in the desired columns list
    df = df.loc[:][columns]
    # map the df in the rows of the new dates
    df = df.reset_index(drop=True)
    df = df[df['date'].isin(raw_dates)].sort_values(by=['date'], ascending=False)
    # scale the df in the mapped columns, not to it's all columns
    if selected_table in countries:
        if update_type == 'addCol' or update_type == 'remCol' or update_type == 'remYear' or update_type == 'addYear':
            df, min_max_scaler = scale(df)
    # exclude the date column from the df, so that the var to_google, to contain only data values
    columns = [x.replace('_', ' ') for x in df.columns if x != 'date']
    to_google = table_to_google(df, columns, dates)
    # convert the lists to json
    columns = json.dumps(columns)
    dates = json.dumps(dates)
    #  convert df columns to json
    my_dict = {}
    for col in df.columns:
        my_dict[col] = json.loads(df.iloc[:-1, :][col].to_json(orient='records'))
    return my_dict, dates, columns, to_google, df_total_col_length, df_index_length, last_year, remaining_cols
