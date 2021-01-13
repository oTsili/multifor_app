import pandas as pd
import json
from src.controller.database import Database
from helping_data import indicators, pestel_categories, country_codes, eurostat_country_codes

Northern = ['Iceland', 'Norway', 'Sweden', 'Denmark', 'Finland']
Eastern = ['Estonia', 'Latvia', 'Lithuania', 'Poland', 'Czech_Republic', 'Slovak_Republic',
           'Hungary', 'Romania', 'Bulgaria', 'Croatia', 'Slovenia']
Western = ['Germany', 'Netherlands', 'Belgium', 'Austria', 'Switzerland', 'France', 'Ireland', 'United_Kingdom',
           'Luxembourg', 'Liechtenstein']
Southern = ['Portugal', 'Spain', 'Italy', 'Greece', 'Cyprus', "Malta"]

regions_list = [Northern, Eastern, Western, Southern]

countries_list = []
for i in regions_list:
    for j in i:
        countries_list.append(j)

countries_list.sort()

# lambda function to parse strings to datetime
dateparse_dby = lambda dates: pd.datetime.strptime(dates, "%d %b %Y")
dateparse_ymd = lambda dates: pd.datetime.strptime(dates, "%Y-%m-%d")
dateparse_y = lambda dates: pd.datetime.strptime(dates, "%Y")


my_dict = {'index': 'countries',
           'data': countries_list}
Database.insert("project_data", my_dict)

my_dict = {'index': 'indicator_aliases',
           'data': indicators}
Database.insert("project_data", my_dict)


my_dict = {'index': 'pestel_categories',
           'data': pestel_categories}
Database.insert("project_data", my_dict)


my_dict = {'index': 'eurostat_country_codes',
           'data': eurostat_country_codes}
Database.insert("project_data", my_dict)


my_dict = {'index': 'country_codes',
           'data': country_codes}
Database.insert("project_data", my_dict)

my_dict = {'index': 'indicators',
           'data': [x for x in indicators.values()]}
Database.insert("project_data", my_dict)

csv_path='script_files/dataframes'
for country in countries_list:
    my_col = Database.DATABASE['dataframes']
    df = pd.read_csv(csv_path + '/' + country + '.csv', encoding='utf-8', index_col=0)
    my_dict = {}
    for col in df.columns:
        my_dict[col] = json.loads(df[col].to_json(orient='records'))

    my_col.insert_one({"index": country, "data": my_dict})

for indicator in indicators.values():
    my_col = Database.DATABASE['dataframes']
    df = pd.read_csv(csv_path + '/' + indicator + '.csv', encoding='utf-8', index_col=0)
    my_dict = {}
    for col in df.columns:
        my_dict[col] = json.loads(df[col].to_json(orient='records'))

    my_col.insert_one({"index": indicator, "data": my_dict})

csv_path = 'script_files/partial_dfs'

for country in ['Ireland', 'Spain', 'Greece', 'United_Kingdom', 'Sweden']:
    my_col = Database.DATABASE['partial_dfs']
    df = pd.read_csv(csv_path + '/' + country + '.csv', encoding='utf-8', index_col=0)
    my_dict = {}
    for col in df.columns:
        my_dict[col] = json.loads(df[col].to_json(orient='records'))

    my_col.insert_one({"index": country, "data": my_dict})


path_file = 'src/indicators/'

for indicator, alias in indicators.items():
    Database.csv_to_mogodb(alias, f'{path_file}/{alias}.csv')

