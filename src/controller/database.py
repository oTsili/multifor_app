from typing import Dict
import pymongo
import pandas as pd
# from help import replace_indicator_names
import json
from src.controller.forecasting_controller import scale


def reverse_list(lst):
    return [ele for ele in reversed(lst)]


class Database:
    URI = "mongodb://127.0.0.1:27017/multifor"
    DATABASE = pymongo.MongoClient(URI).get_default_database()

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['multifor']

    @staticmethod
    def get_collections():
        my_filter = {"name": {"$regex": r"^(?!system\.)"}}
        return Database.DATABASE.list_collection_names(filter=my_filter)

    @staticmethod
    def insert(collection: str, data: Dict) -> None:
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def insert_one(collection: str, df_name, data: Dict) -> None:
        Database.DATABASE[collection].insert_one({"index": df_name, "data": data})

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def insert_temp_to_mongodb(collection_name, my_dict):
        mycol = Database.DATABASE[collection_name]
        mycol.insert_one({"index": collection_name, "data": my_dict})

    @staticmethod
    def update_to_mongodb(collection_name, df):
        """
        Updates a document (df in dictionary form) in the mongodb, for the specified collection name.

        :param collection_name: the mongodb collection having the document/df
        :param df: the df to be saved
        :return: None
        """
        mycol = Database.DATABASE[collection_name]
        my_dict = {}
        for col in df.columns:
            my_dict[col] = json.loads(df[col].to_json(orient='records'))
        mycol.update({"index": collection_name}, {"$set": {"data": my_dict}})

    @staticmethod
    def csv_to_mogodb(df_name, csv_path, scaling=False, alias=False):
        """
        Reads a .csv file referring to a df and saves it to the mongodb, in the 'dataframes' collection

        :param df_name: the name of the df to be saved, and used as index in the mongodb collection
        :param csv_path: the .csv path to read from the df
        :param scaling: Boolean. If yes, scale to (0.1)
        :param alias: Boolean. If yes rename the df columns to the aliases provided
        :return: None
        """
        mycol = Database.DATABASE['dataframes']
        df = pd.read_csv(csv_path, encoding='utf-8', index_col=0)
        # if alias:
        #     df = replace_indicator_names(df, columns=True)
        if scaling:
            df, min_max_scaler = scale(df)

        df['date'] = df.index
        column_names = ['date']
        for x in df.columns:
            if x != 'date':
                column_names.append(x)
        df = df.reindex(columns=column_names)
        my_dict = {}
        for col in df.columns:
            my_dict[col] = json.loads(df[col].to_json(orient='records'))

        mycol.insert_one({"index": df_name, "data": my_dict})

    @staticmethod
    def df_to_mogodb(collection, df_name, df, scaling=False, alias=False):
        """
        Saves the specified df to the mongodb, after converting it in a dictionary, with index of it's name

        :param collection: the collection to be saved inside the mongodb
        :param df_name: the df/document name
        :param df: the df to be saved
        :param scaling: Boolean. If true, conduct scaling to (0,1)
        :param alias: Boolean. If true, rename the columns to the aliases provided
        :return: None
        """
        mycol = Database.DATABASE[collection]
        # if alias:
        #     df = replace_indicator_names(df, columns=True)
        if scaling:
            cols = [x for x in df.columns if x != 'date']
            df, min_max_scaler = scale(df.loc[:][cols])

        df['date'] = df.index
        column_names = ['date']
        for x in df.columns:
            if x != 'date':
                column_names.append(x)
        df = df.reindex(columns=column_names)

        my_dict = {}
        for col in df.columns:
            my_dict[col] = json.loads(df[col].to_json(orient='records'))

        if Database.find(collection, {'index': df_name}).count() > 0:
            # update the document
            mycol.update({"index": df_name}, {"$set": {"data": my_dict}})
        else:
            # save to mongoDB
            mycol.insert_one({"index": df_name, "data": my_dict})

    @staticmethod
    def from_mongodb_json(collection_name, document_name, property_name, reverse=False):
        """
        Gets the values of a specific df column from mongodb and converts it to json.

        :param collection_name: the mongodb collection from which to retrieved the df column
        :param document_name: the df/document name
        :param property_name: the df-column/dictionary-property name to be retrieved
        :param reverse: Boolean. If true, reverse the values of the list/df-column
        :return: the df-column in json format
        """
        data = Database.find_one(collection_name, {"index": document_name})

        try:
            if reverse:
                my_list = data['data'][property_name]
                my_list = reverse_list(my_list)
                return my_list
            else:
                return data['data'][property_name]
        except Exception as e:
            print(f'err{e}')

    @staticmethod
    def from_mongodb_df(collection_name, query):
        """
        Gets a df from mongodb, and converts it from dictionary to pandas dataframe before returning it.

        :param collection_name: the mongodb collection from which the db will be retrieved
        :param query: the query, to be used for using by pymongo
        :return: the df
        """
        data = Database.find_one(collection_name, query)
        df = pd.DataFrame(data['data'])
        try:
            return df
        except Exception as e:
            print(f'error{e}')
