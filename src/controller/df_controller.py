import pandas as pd
from src.controller.database import Database
from src.controller.forecasting_controller import pre_predict


def save_df_to_mongo(df_name, df):
    """
    Saves a specific df to the mongodb, in the collection dataframes

    :param df_name: the table/df name
    :param df: the df to be saved
    :return: None
    """
    Database.df_to_mogodb(collection='dataframes', df_name=df_name, df=df)


# get the provided country's df with it's indicators for columns and interpolate the gaps in the middle & start
def get_df(name, dates_updated):
    """
    Gets the dataframe from the mongodb, and conducts a pre-prediction if needed (if there are any nan values in the
    last rows of the df), after conducting interpolation to the rows in the middle and in the beggining.

    :param name: the df name
    :param dates_updated: Boolean. If true, then the function is called for chart update, and not initial load. This is
    useful in order to use the existing dates in the table, or map the df to years (2005, 2018).
    :return: the df
    """

    if not dates_updated:
        dates = [f'{x}-01-01' for x in range(2005, 2019)]
        df = Database.from_mongodb_df('dataframes', {'index': name}).reset_index(drop=True)\
            .set_index('date', drop=False).reindex(dates)
    else:
        df = Database.from_mongodb_df('dataframes', {'index': name})
    flag = False
    temp_col = None

    if 'date' in df.columns:
        flag = True
        temp_col = df['date']
        df = df.loc[:][[x for x in df.columns if x != 'date']]

    # if there are any nans
    nans = len(df) - df.count()
    if any(nans) >= 1:
        # fill the gaps in the start & in the middle
        df = df.interpolate(method='linear', axis=0, limit_direction='backward')
        # drop the colums with all their values equal to NaN
        df = df.dropna(how='all', axis=1)
        # fills the gaps in the last rows of df, until year 2018
        for col in df.columns:
            if col != 'date':
                predictable_nans = df[col].isna().sum()
                if predictable_nans >= 1:
                    df = pre_predict(df, predictable_nans, col)
    if flag:
        df_date = pd.DataFrame(temp_col)
        df = pd.concat([df_date, df], axis=1)

    return df

