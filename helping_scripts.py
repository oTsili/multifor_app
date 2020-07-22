import pandas as pd
from src.controller.database import Database
from helping_data import indicators, pestel_categories, country_codes, eurostat_country_codes
import json

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


#
# my_dict = {'index': 'countries',
#            'data': countries_list}
# Database.insert("project_data", my_dict)

# my_dict = {'index': 'indicator_aliases',
#            'data': indicators}
# Database.insert("project_data", my_dict)


# my_dict = {'index': 'pestel_categories',
#            'data': pestel_categories}
# Database.insert("project_data", my_dict)


# my_dict = {'index': 'eurostat_country_codes',
#            'data': eurostat_country_codes}
# Database.insert("project_data", my_dict)

#
# my_dict = {'index': 'country_codes',
#            'data': country_codes}
# Database.insert("project_data", my_dict)

# my_dict = {'index': 'indicators',
#            'data': [x for x in indicators.values()]}
# Database.insert("project_data", my_dict)
#

# #
# path_file = 'src/countries'
#
# for country in countries_list:
#     Database.csv_to_mogodb(country, f'{path_file}/{country}.csv', scaling=True, alias=True)


path_file = '../src/indicators'

for indicator, alias in indicators.items():
    print(alias)
    Database.csv_to_mogodb(alias, f'{path_file}/{alias}.csv')

# Database.insert('indicators', indicators)

# path = '/media/odysseas/Data2/Projects/PycharmProjects/pestel_app/src/indicators/'
# indicator_files = glob.glob(path + '*.csv')
# indicator_files.sort(key=lambda v: v.lower())
# print(indicator_files)
# print(indicators)
# for file, indicator in zip(indicator_files, indicators):
#     print(file)
#     print(indicator)
#     Database.csv_to_mogodb(indicator, file)
#
# for indicator in indicators:
#     print(indicator)
#     # my_year = Database.from_mongodb('year')
#     print(Database.from_mongodb('Austria', indicator))
#     # print( my_indicator)



# df = pd.DataFrame(Database.find_one('dataframes', {'index': 'paok'})['data'])
# # print(df)
# my_dict = {}
# for col in df.columns:
#     my_dict[col] = json.loads(df[col].to_json(orient='records'))
# print(my_dict)
# Database.DATABASE['dataframes'].insert_one({"index": "paok", "data": my_dict})