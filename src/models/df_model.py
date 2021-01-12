from src.controller.plot_controller import get_line_data, table_to_google, update_df_chart
from src.controller.df_controller import get_df, save_df_to_mongo
from src.controller.country_df_controller import get_country_df, get_partial_df, save_partial_df_to_mongo
from src.controller.database import Database
import numpy as np


class DfModel:
    def __init__(self, name, dates_updated=False):
        self.name: str = name
        self.dates_updated = dates_updated
        self.df = self.get_df_type()

    @staticmethod
    def get_google_data(df, columns, years):
        return table_to_google(df, columns, years)

    def add_year(self):
        # predict
        pass

    @staticmethod
    def remove_year(self):
        pass

    def construct_table(self):
        pass

    def get_line(self, collection_name, columns, reverse=False):
        """
        Gets the data for the line plot

        :param reverse: boolean value to reverse the df in descending order
        :param collection_name: the collection name
        :param columns: a list of  columns
        :return: None
        """
        if columns == 'all':
            return get_line_data(self.name, self.df.columns, collection_name, reverse=reverse)
        # if only one column
        elif isinstance(columns, str):
            return get_line_data(self.name, [columns], collection_name, reverse=reverse)
        # if more than one column
        else:
            return get_line_data(self.name, columns, collection_name, reverse=reverse)

    def get_df_type(self):
        countries = Database.find_one('project_data', {'index': 'countries'})['data']
        if self.name in countries:
            df = get_country_df(self.name, self.dates_updated, last_default_year=2018)
        else:
            df = get_df(self.name, self.dates_updated)
        # drop the columns that have more than 60% nan values
        df = df.loc[:, df.isin([' ', np.nan, 0]).mean() < .6].rename(columns={'Slovakia': 'Slovak_Republic',
                                                                     'Czechia': 'Czech_Republic'})
        return df

    def save_df_full(self):
        save_df_to_mongo(self.name, self.df)

    def update_chart(self, cols, selected_table, last_year, predict_flag=False, update_type=None, col_sel=None):
        return update_df_chart(self, cols, selected_table, last_year, predict_flag=predict_flag, update_type=update_type, col_sel=col_sel)

    def save_df_partial(self, columns):
        df = get_partial_df(self.df, columns)
        save_partial_df_to_mongo(self.name, df)

        return df
