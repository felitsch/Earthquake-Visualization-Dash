import pandas as pd
import wbdata
import pycountry
import pandas as pd
import numpy as np
from plotly.graph_objs import *
import wbdata
import pycountry
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')


################################################################
# Create functions for use in in app, layouts and calllbacks
################################################################


def load_data():
    # Load the raw data
    tectonic_plates = pd.read_csv("Tectonic.csv")
    data = pd.read_csv("significant-earthquake-database.csv", delimiter=";")
    humanAct = pd.read_excel("The_Human_Induced_Earthquake_Database_v2023.03.27.xlsx")

    return tectonic_plates, data, humanAct




def preprocess_data(raw_data):
    tectonic_plates, data, humanAct = raw_data

    # preprocessing code
    # Dictionary mit Plattenkurznamen als Schlüssel und vollständigen Namen als Wert erstellen
    plate_names = {'am': 'American Plate', 'an': 'Antarctic Plate', 'AP': 'African Plate', 
                'ar': 'Arabian Plate', 'AS': 'Australian Plate', 'AT': 'Eurasian Plate',
                'au': 'North American Plate', 'BH': 'Nazca Plate', 'BR': 'South American Plate',
                'BS': 'Scotia Plate', 'BU': 'Burma Plate', 'ca': 'Caribbean Plate', 
                'CL': 'Cocos Plate', 'co': 'Colombia Plate', 'cp': 'Capricorn Plate', 
                'CR': 'Caroline Plate', 'EA': 'Juan de Fuca Plate', 'eu': 'Euro-Asian Plate', 
                'FT': 'Filipino Plate', 'GP': 'Galapagos Plate', 'in': 'India Plate', 
                'jf': 'JF Plate', 'JZ': 'Pacific Plate', 'KE': 'Kermadec Plate', 
                'lw': 'Lord Howe Plate', 'MA': 'Mariana Plate', 'MN': 'Minor Plate', 
                'MO': 'Molucca Sea Plate', 'mq': 'Macquarie Plate', 'MS': 'South Sandwich Plate', 
                'na': 'North Andes Plate', 'NB': 'New Hebrides Plate', 'ND': 'North America Plate',
                'NH': 'New Hebrides Plate', 'NI': 'Nazca Plate', 'nu': 'Eurasian Plate',
                'nz': 'New Zealand Plate', 'OK': 'Okhotsk Plate', 'ON': 'Okhotsk Plate', 
                'pa': 'Pacific Plate', 'PM': 'Phoenix Plate', 'ps': 'South Shetland Plate', 
                'ri': 'River Plate', 'sa': 'South American Plate', 'SB': 'Solomon Sea Plate',
                'sc': 'South China Plate', 'SL': 'Sunda Plate', 'sm': 'Somali Plate', 
                'sr': 'South Sandwich Plate', 'SS': 'Scotia Plate', 'su': 'Sunda Plate',
                'sw': 'South Sandwich Plate', 'TI': 'Bird''s Head Plate', 'TO': 'Tonga Plate',
                'WL': 'Willis Plate', 'yz': 'Yangtze Plate'}

    # Neue Spalte mit vollständigem Namen erstellen
    tectonic_plates['Plate Name'] = tectonic_plates['plate'].map(plate_names)

    data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(',', expand=True).apply(pd.to_numeric)
    data = data.drop('Coordinates', axis=1)
    data = data.dropna(subset= ['Latitude', 'Longitude'] )
    data = data[data['Focal Depth']<100]

    data = data.dropna(subset=['Mw Magnitude','Ms Magnitude'], how='all')
    data['Magnitude'] = data['Mw Magnitude']
    fill_value = 2/3 * data['Ms Magnitude'] + 0.75
    data['Magnitude'] = data['Magnitude'].fillna(fill_value)
    data = data[data['Year']>1900]

    data = data.drop(columns=['Mw Magnitude','Ms Magnitude', 'Mb Magnitude', 'Ml Magnitude', 'MFA Magnitude','Unknown Magnitude',
                            'Earthquake : Deaths', 'Earthquake : Deaths Description','Earthquake : Missing',
                            'Earthquake : Missing Description','Earthquake : Injuries', 'Earthquake : Injuries Description',
                            'Earthquake : Damage (in M$)','Earthquake : Damage Description', 'Earthquakes : Houses destroyed',
                            'Earthquakes : Houses destroyed Description','Earthquakes : Houses damaged',
                            'Earthquakes : Houses damaged Description'])


    country_codes = []
    for country in data['Country']:
        search_results = wbdata.search_countries(country)
        if search_results:
            country_code = search_results[0]['id']
        else:
            country_code = None
        country_codes.append(country_code)

    data['Country ISO Code'] = country_codes
    data.reset_index(inplace=True)
    data[data['Country ISO Code'].isna()]['Country'].unique()

    for i in range(len(data['Country ISO Code'])):
        if pd.isna(data['Country ISO Code'][i]):
            if data['Country'][i]=='TURKEY':
                data['Country ISO Code'][i]='TUR'
            elif data['Country'][i]=='USA' or data['Country'][i]=='USA TERRITORY':
                data['Country ISO Code'][i]='USA'
            elif data['Country'][i]=='LAOS':
                data['Country ISO Code'][i]='LAO'
            elif data['Country'][i]=='MYANMAR (BURMA)':
                data['Country ISO Code'][i]='MMR'
            elif data['Country'][i]=='KYRGYZSTAN':
                data['Country ISO Code'][i]='KGZ'  
            elif data['Country'][i]=='AZORES (PORTUGAL)':
                data['Country ISO Code'][i]='PRT'
            elif data['Country'][i]=='SOUTH KOREA':
                data['Country ISO Code'][i]='KOR'
            elif data['Country'][i]=='KERMADEC ISLANDS (NEW ZEALAND)':
                data['Country ISO Code'][i]='NZL'
            elif data['Country'][i]=='BOSNIA-HERZEGOVINA':
                data['Country ISO Code'][i]='BIH'
            elif data['Country'][i]=='SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS' or data['Country'][i]== 'UK TERRITORY':
                data['Country ISO Code'][i]='GBR'
            elif data['Country'][i]=='MICRONESIA, FED. STATES OF':
                data['Country ISO Code'][i]='FSM'
            elif data['Country'][i]=='WALLIS AND FUTUNA (FRENCH TERRITORY)':
                data['Country ISO Code'][i]='FRA'


    # Group the data by country and sum the total deaths, Houses Destroyed, Houses Damaged, Injuries
    grouped_data = data.groupby('Country ISO Code')[['Total Effects : Deaths', 'Total Effects : Houses Destroyed', 'Total Effects : Houses Damaged', 'Total Effects : Injuries']].sum().reset_index()


    # Set the parameters for the data query
    indicators = {'SP.POP.TOTL': 'Population, total'}

    countries_ = list(set(list(data['Country ISO Code'])))
    countries = list()
    for element in countries_:
        if str(element) != "None":
            countries.append(element)

    # Retrieve the data from the World Bank API
    #print(wbdata.get_dataframe(indicators, country=countries))


    # Set the parameters for the data query
    indicators = {'SP.POP.TOTL': 'Population, total'}

    countries_ = list(set(list(data['Country ISO Code'])))
    countries = list()
    for element in countries_:
        if str(element) != "None":
            countries.append(element)

    # Retrieve the data from the World Bank API
    pop_data = wbdata.get_dataframe(indicators, country=countries)

    # Reset the index so that 'Country Name' is a column
    pop_data.reset_index(inplace=True)

    pop_data = pop_data.groupby('country')['Population, total'].mean()
    pop_data = pd.DataFrame(pop_data).reset_index()


    pop_data['country'] = pop_data['country'].str.extract('([^,]+)')
    pop_data['country'] = pop_data['country'].replace(['Turkiye', 'Lao PDR'], ['Turkey','Lao'])
    pop_data['Code'] = pd.Series(dtype='int')
    for i in range(len(pop_data['country'])):
        try:
            iso_code = pycountry.countries.search_fuzzy(pop_data['country'][i])[0].alpha_3
            pop_data['Code'][i] = iso_code
        except LookupError:
            pop_data['Code'][i] = None


    # Merge the population data with the existing data on total deaths by country
    merged_data = pd.merge(grouped_data, pop_data, left_on='Country ISO Code', right_on='Code')

    merged_data = merged_data.drop(columns='Code')
    merged_data.rename(columns={'country': 'Country'}, inplace=True)


    # Calculate the mortality rate per 1,000 individuals
    merged_data['Deaths per Capita'] = merged_data['Total Effects : Deaths'] / merged_data['Population, total']


    # prepare humanAct for sunburst
    humanAct_sb = humanAct.groupby(['Country', 'Earthquake cause (main class)']).agg({'Number of recorded earthquakes': 'count'})
    humanAct_sb = humanAct_sb[(humanAct_sb['Number of recorded earthquakes'] != 0) & (humanAct_sb['Number of recorded earthquakes'] > 1)].reset_index()
    humanAct_sb['Rank'] = humanAct_sb['Number of recorded earthquakes'].rank(method='dense', ascending=False).astype(int)


    # Return the processed data
    return tectonic_plates, data, merged_data, humanAct_sb


if __name__ == '__main__':
    raw_data = load_data()
    tectonic_plates, data, merged_data, humanAct_sb = preprocess_data(raw_data)


