from src.controller.database import Database
from helping_data import indicators


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

out_directory = 'script_files/'


def get_df_from_mongodb(name, collection):
    dates = [f'{x}-01-01' for x in range(2005, 2019)]
    df = Database.from_mongodb_df(collection, {'index': name}).reset_index(drop=True)\
                    .set_index('date', drop=True).reindex(dates)
    print(df)
    # df['date'] = df.index

    return df

#
# for indicator in indicators.values():
#     df = get_df_from_mongodb(indicator, 'dataframes')
#     df.to_csv(out_directory + 'dataframes/' + indicator + '.csv', encoding='utf-8')
#
#
# for country in countries_list:
#     df = get_df_from_mongodb(country, 'dataframes')
#     df.to_csv(out_directory + 'dataframes/' + country + '.csv', encoding='utf-8')


# for country in ['Ireland', 'Spain', 'Greece', 'United_Kingdom', 'Sweden']:
#     df = get_df_from_mongodb(country, 'partial_dfs')
#     df.to_csv(out_directory + 'partial_dfs/' + country + '.csv', encoding='utf-8')

for country in ['Ireland', 'Spain', 'Greece', 'United_Kingdom', 'Sweden']:
    df = get_df_from_mongodb(country, 'partial_dfs')
    df.to_csv(out_directory + 'partial_dfs/' + country + '.csv', encoding='utf-8')