from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import datetime
import pickle as pkl
import os
url = "https://www.worldometers.info/coronavirus/"
filename_suff = 'data/df_hist'

def corona_parser(save_file=True,use_today=True):
    now = datetime.datetime.now().strftime("%Y-%-m-%d")
    filename = filename_suff + '_' + now + '.pkl'
    if os.path.isfile(filename):
        print(filename)
        print('loading historical data')
        df_hist = pd.read_pickle(filename)
    else:
        print('Downloading historical data')
        data_hist = requests.get("https://pomber.github.io/covid19/timeseries.json").json()
        df_hist = []
        for key in data_hist:
            for mydict in data_hist[key]:
                mydict['Country,Other'] = key
                df_hist.append(mydict)
        df_hist = pd.DataFrame(df_hist)
        if save_file:
            df_hist.to_pickle(filename)
    df_hist = df_hist.drop(df_hist[(df_hist['date']==now) | (df_hist['confirmed']==0)].index)
    html_page = requests.get(url)
    bs = BeautifulSoup(html_page.content, 'html.parser')
    table = bs.find('table', id="main_table_countries_today")
    df_latest =  pd.read_html(str(table))[0]
    df_latest['date'] = now
    df_latest=df_latest.rename(columns = {'TotalCases':'confirmed', 'TotalRecovered':'recovered', 'TotalDeaths':'deaths', 'TotalRecovered':'recovered'})
    if use_today:
        df_concat = pd.concat((df_hist, df_latest))
    else:
        df_concat=df_hist
    df_concat['date'] =  pd.to_datetime(df_concat['date'])

    return df_concat

def resample_df(df):
    return df

def fix_duplicates(df):
    for group in df.groupby:
        df = resample_df(df)
    return df