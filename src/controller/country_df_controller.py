from src.controller.database import Database
from src.controller.forecasting_controller import scale
from src.controller.df_controller import pre_predict, get_df
import pandas as pd
import numpy as np


def transpose_df(indicators, dates, country_name):
    """
    Gets all the indicator dfs and from them keeps the columns of the country_name provided, merging them in a new df,
    and keeping those which don't have more than 60% of nan values.

    :param indicators: the list with the indicators, got from mongodb
    :param dates: the dates list, with the dates/rows to keep
    :param country_name: the name of the country/df which will be constructed
    :return: the country df
    """
    country_name = country_name.replace('_', ' ')
    # check if the country_name provided exists in indicator_df columns and get its index
    idx = 0
    for i in range(len(indicators)):
        if country_name in Database.from_mongodb_df('dataframes', {'index': indicators[i]}):
            idx = i

    master_df = pd.DataFrame(Database.from_mongodb_df('dataframes', {'index': indicators[idx]})
                             # .sort_values(by=['date'], ascending=False)
                             .reset_index(drop=True).set_index('date', drop=True).reindex(dates)[country_name]
                             .rename(indicators[idx])).astype(float)
    for indicator in indicators:
        if indicator != indicators[idx]:
            # get from mongodb, set index the dates & keep only the ones between (2005,2018) or until the year predicted
            indicator_df = Database.from_mongodb_df('dataframes', {'index': indicator})
            indicator_df = indicator_df.reset_index(drop=True)
            indicator_df = indicator_df.set_index('date', drop=True)
            indicator_df = indicator_df.reindex(dates)

            if country_name in indicator_df.columns:
                indicator_df = indicator_df[country_name]
                # rename the series whith the indicator's name, so that it will be it's column name
                indicator_df = pd.DataFrame(indicator_df.rename(indicator)).astype(float)

                # merge columns to a single dataframe
                master_df = master_df.merge(indicator_df, on='date')
    # drop the columns with more than 60% nan values
    master_df = master_df.loc[:, master_df.isin([' ', np.nan, 0]).mean() < .6]

    return master_df


def get_country_df(country_name, dates_updated, last_default_year):
    """
    Gets the country df if it has already been transposed and gaps-filled, or calls the transpose function
    to conduct mergins, interpolation and pre-prediction

    :param country_name: the country name of the df to be delivered
    :param dates_updated: Boolean. If true, then the current function is called for chart updating
    , instead of chart initializing
    :param last_default_year: the last year to be mapped the df
    :return: the country df
    """
    if Database.find('dataframes', {'index': country_name}).count() > 0:
        country_df = get_df(country_name, dates_updated)
    else:
        indicators = Database.find_one('project_data', {'index': 'indicators'})['data']
        dates = [f'{x}-01-01' for x in range(2005, last_default_year+1)]

        # get the provided country's df with it's indicators for columns and interpolate the gaps in the middle & start
        country_df = transpose_df(indicators=indicators, dates=dates, country_name=country_name)\
            .interpolate(method='linear', axis=0, limit_direction='backward')

        for col in country_df:
            nans = country_df[col].isna().sum()
            if nans >= 1:
                country_df = pre_predict(country_df, nans, col)

    if 'date' not in country_df.columns:
        country_df['date'] = country_df.index

    return country_df


def get_partial_df(country_df, indicator_columns):
    """
    Get the country df, mapped in the specific columns provided.

    :param country_df: the df, to be mapped
    :param indicator_columns: the columns to be kept
    :return: the country df mapped to the columns
    """
    date_column = country_df['date']
    if not isinstance(indicator_columns, list):
        indicator_columns = [indicator_columns]
        # map the df in the columns provided
        country_df_partial = country_df.loc[:][[x for x in indicator_columns if x in country_df.columns]]
    else:
        # map the df in the columns provided
        country_df_partial = country_df.loc[:][[x for x in indicator_columns if x in country_df.columns]]
        country_df_partial, min_max_scaler = scale(country_df_partial)
    temp_list = ['date']
    for x in indicator_columns:
        temp_list.append(x)
    df = pd.DataFrame(date_column, columns=['date'])

    country_df_partial = pd.concat([df, country_df_partial], axis=1)

    return country_df_partial


def save_partial_df_to_mongo(country_name, country_df_partial):
    """
    Saves the mapped df to the mongodb, in the 'partial_dfs' collection.

    :param country_name: the name of the country/df
    :param country_df_partial: the mapped df
    :return: None
    """
    # save to mongoDB
    Database.df_to_mogodb(collection='partial_dfs', df_name=country_name, df=country_df_partial, scaling=True)
