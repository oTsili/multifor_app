from sklearn import preprocessing
import pandas as pd


def scale(df):
    """
    Scales the dataframe specifyied to range (0,1), after dropping columns with only NaN values

    :param df: datafrmame to be scaled
    :return: scaled dataframe, scaler used, list with df columns with only NaN values
    """
    # drop nan columns
    nanColumns = []
    nanValues = False
    for col in df:
        if df[col].isna().values.all():
            nanValues = True
            nanColumns.append(col)
    if nanValues:
        df.drop(nanColumns, axis=1, inplace=True)
    # returns a numpy array
    idx = [x for x in df.index]
    columns = [x for x in df.columns]
    x = df.values
    # ensure all data is float
    x = x.astype('float64')
    # scale the dataframe to range (0,1)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    df.index = idx
    df.columns = columns
    return df, min_max_scaler, nanColumns


indicators = {
    # ecological
    'clean_footprint': 'footprint',
    'Renewable_energy_consumption_perc_of_total_final_energy_consumption': 'Renewable_enrg_cons',
    'Renewable_internal_freshwater_resources_per_capita_in_cubic_meters': 'Renewable_int_freshwater',
    # economical
    'Current_account_balance_BoP_current_US_dol': 'CAB_BoP_current_US_dol',
    'Current_account_balance_perc_of_GDP': 'CAB_of_GDP',
    'Exports_of_goods_and_services_perc_of_GDP': 'Export_goods_and_srvces',
    'Foreign_direct_investment_net_inflows_perc_of_GDP': 'FDI_net_inflows',
    'GDP_growth_annual_perc': 'GDP_growth',
    'GDP_PPP_current_international_dol': 'GDP_PPP_cur_int',
    'GNI_per_capita_PPP_current_international_dol': 'GNI_pc_PPP_cur_int',
    'GNI_PPP_current_international_dol': 'GNI_PPP_cur_int',
    'Unemployment_total_perc_of_total_labor_force_national_estimate': 'Unmplmnt_of_labor_force',
    # legislative
    'Control_Of_Corruption_Estimate': 'Control_Of_Corruption',
    'Rule_Of_Law_Estimate': 'Rule_Of_Law',
    'corruption_perceptions_index': 'CPI',
    # lift related
    'building_permits_annual': 'building_permits',
    'existing_lifts': 'existing_lifts',
    'new_lifts': "new_lifts",
    'Population_ages_65_and_above_perc_of_total_population': 'Population_over_65',
    # political
    'civil_liberties': 'civil_liberties',
    'Government_Effectiveness_Estimate': 'Government_Effectness',
    'Political_Stability_And_Absence_Of_Violence_Terrorism_Estimate': 'Political_Stability',
    'political_rights': 'political_rights',
    'Regulatory_Quality_Estimate': 'Regulatory_Quality',
    'Voice_And_Accountability_Estimate': 'Voice_And_Accountability',
    # social
    'GINI_index_World_Bank_estimate': 'GINI_index_World_Bank',
    'Human_development_index': 'Human_development_index',
    'Primary_education_pupils': 'Primary_education_pupils',
    'School_enrollment_primary_perc_gross': 'School_enrollement_prm',
    'School_enrollment_secondary_perc_gross': 'School_enrollement_sec',
    'School_enrollment_tertiary_perc_gross': 'School_enrollement_tert',
    'Secondary_education_pupils': 'Secondary_education_pup',
    # technological
    'internet_users_for_authority_servicies': 'int_users_for_auth_srvs',
    'Research_and_development_expenditure_perc_of_GDP': 'R_and_D_expenditure'
}


def replace_indicator_names(df, columns=True):

    if columns:
        for indicator, alias in indicators.items():
            df.rename(columns={indicator: alias}, inplace=True)
    else:
        for indicator, alias in indicators.items():
            df.rename(index={indicator: alias}, inplace=True)
    return df


aliases = list(indicators.values())
aliases.sort(key=lambda v: v.lower())


pestel_categories = {
    "POLITICAL": [
     'civil_liberties',
    'Government_Effectness',
    'Political_Stability',
    'political_rights',
    'Regulatory_Quality',
    'Voice_And_Accountability'
    ],

    'ECONOMICAL': [
    'CAB_BoP_current_US_dol',
    'CAB_of_GDP',
    'Export_goods_and_srvces',
    'FDI_net_inflows',
    'GDP_growth',
    'GDP_PPP_cur_int',
    'GNI_pc_PPP_cur_int',
    'GNI_PPP_cur_int',
    'Unmplmnt_of_labor_force'
    ],

    'SOCIAL': [
    'GINI_index_World_Bank',
    'Human_development_index',
    'Primary_education_pupils',
    'School_enrollement_prm',
    'School_enrollement_sec',
    'School_enrollement_tert',
    'Secondary_education_pup'
     ],

    'TECHNOLOGICAL': [
    'int_users_for_auth_srvs',
    'R_and_D_expenditure'
    ],

    'ECOLOGICAL': [
    'footprint',
    'Renewable_enrg_cons',
    'Renewable_int_freshwater'
    ],

    'LEGISLATIVE': [
    'Control_Of_Corruption',
    'Rule_Of_Law',
    'CPI'
    ]
}

country_codes = {
    "IS": 'Iceland',
    "NO": 'Norway',
    "SE": 'Sweden',
    "DK": 'Denmark',
    "FI":'Finland',
    "EE": 'Estonia',
    "LV": 'Latvia',
    "LT": 'Lithuania',
    "PL": 'Poland',
    "CZ": 'Czech Republic',
    "SK": 'Slovak Republic',
    "HU": 'Hungary',
    "RO": 'Romania',
    "BG": 'Bulgaria',
    "HR": 'Croatia',
    "SI": 'Slovenia',
    "DE": 'Germany',
    "NL": 'Netherlands',
    "BE": 'Belgium',
    "AT": 'Austria',
    "CH": 'Switzerland',
    "FR":'France',
    "IE": 'Ireland',
    "GB": 'United Kingdom',
    "LU": 'Luxembourg',
    "LI": 'Liechtenstein',
    "PT": 'Portugal',
    "ES": 'Spain',
    "IT": 'Italy',
    "GR": 'Greece',
    "CY": 'Cyprus',
    "MT": 'Malta'
}


eurostat_country_codes = {
    "Belgium": "BE", "Bulgaria": "BG", 'Czechia': 'CZ', 'Denmark': 'DK',
    'Germany(until 1990 former territory of the FRG)': 'DE', 'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL',
    'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT',
    'Luxembourg': 'LU', 'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland':  'PL',
    'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE',
    'United Kingdom': 'UK', 'Norway': 'NO', 'Montenegro': 'ME', 'North Macedonia': 'MK', 'Albania': 'AL',
    'Serbia': 'RS', 'Turkey': 'TR', 'Bosnia and Herzegovina': 'BA'
}