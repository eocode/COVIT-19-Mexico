import urllib
import pandas as pd

def extract():
    # Mundial Data
    outfilename = f'COVIT-19.xls'
    url_of_file = f'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
    print(f'Extrayendo: {url_of_file}')
    urllib.request.urlretrieve(url_of_file, outfilename)
    print(f'Descarga correcta')

def process():
    # Read Data
    file = f'COVIT-19.xls'
    df = pd.read_excel(file)

    # Prepare Dataset
    data = pd.DataFrame(df, columns= ['dateRep', 'day','month', 'year', 'cases', 'deaths', 'countriesAndTerritories'])
    data = data.rename(columns={"dateRep": "Date", "countriesAndTerritories": "Country", "cases":"Cases", "deaths": "Deaths", "month": "Month", "day": "Day"})

    # Filter Dataset
    data = data[data['Cases'] > 0]
    data['Period'] = data['Month']*100+data['Day']
    data = data.sort_values(['Country', 'Date'], ascending=[True, True])

    # Index DataSet
    data['Id'] = data.groupby(['Country']).cumcount()

    # Prepare data
    ant = data.iloc[0]['Cases']
    antd = data.iloc[0]['Deaths']
    ants = 0
    country = data.iloc[0]['Country']
    i = 0
    c = [] # cases
    d = [] # deaths
    s = [] # start deaths
    p = [] # impact

    death = False
    for i in range(i, len(data)):

        # Validate start first death
        if country == data.iloc[i]['Country']:
            if death == False and data.iloc[i]['Deaths'] > 0:
                death = True
        else:
            death = False

        # Sumarize
        Cases = (data.iloc[i]['Cases'] + (ant if i > 0 else 0)) if country == data.iloc[i]['Country'] else data.iloc[i]['Cases']
        Deaths = (data.iloc[i]['Deaths'] + (antd if i > 0 else 0)) if country == data.iloc[i]['Country'] else data.iloc[i]['Deaths']
        StartDeaths = 1 if country == data.iloc[i]['Country'] and death else 0
        Impact = Deaths / (0 if Cases == 0 else Cases) * 100
        
        
        # Append cases
        c.append(Cases)
        d.append(Deaths)
        s.append(StartDeaths)
        p.append(Impact)
        ant = Cases
        antd = Deaths
        ants = StartDeaths
        country = data.iloc[i]['Country']

    data["Total_Cases"] = c
    data["Total_Deaths"] = d
    data['StartDeaths'] = s
    data['Impact'] = p


    # Index DataSet start by deaths
    data = data[data['StartDeaths'] == 1]
    data['Id'] = data.groupby(['Country']).cumcount()

    return data

def flow():
    extract()
    return process()