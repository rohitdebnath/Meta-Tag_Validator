# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:45:34 2020

@author: debrup.dutta
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.exceptions import ConnectionError
import random
from concurrent.futures import ThreadPoolExecutor
import dash_table
from dash.dependencies import Input, Output
s = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=2)
s.mount("http://", a)


def tag_validator(url1):
        try:
            token=str(random.randint(0,1000))
            headers = {
                        'cache-control': "no-cache",
                        'postman-token': token
                        }
            if requests.get(url1,headers=headers).status_code==200:
            # global df
                try:
                    token=str(random.randint(0,1000))
                    headers = {
                        'cache-control': "no-cache",
                        'postman-token': token
                        }

                    #r1 = s("GET", url, headers=headers)
                    r1 = s.get(url1, headers=headers)
                    htmlcontent1 = r1.content
                    # print(htmlcontent)
                    soup1 = BeautifulSoup(htmlcontent1, "html.parser")
                    dict_metatag1 = my_dictionary()
                    for link in soup1.find_all("meta"):
                        if link.get("name") != None:
                            if link.get("name") in [
                                "bu",
                                "sub_bu",
                                "flag_all",
                                "web_section_id",
                                "page_content",
                                "segment",
                                "lifecycle",
                                "user_profile",
                                "simple_title",
                                "analytics_template_name",
                                "product_service_name",
                                "analytics_section",
                            ]:
                                dict_metatag1.add(link.get("name"), link.get("content"))
                    print(dict_metatag1, url1)

                    # print(link.get("content"),link.get("name"))

                    df1 = pd.DataFrame(
                        columns=(
                            "url",
                            "redirect",
                            "status",
                            "bu",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "simple_title",
                            "sub_bu",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                        )
                    )
                    for col in df1.columns:

                        if col == "url":
                            df1.loc[1, col] = url1

                        elif col == "status":
                            df1.loc[1, col] = requests.get(url1).status_code
                        elif col == "redirect":
                            if requests.get(url1).url != url1:
                                df1.loc[1, col] = 1
                            else:
                                df1.loc[1, col] = 0
                        elif col in [
                            "sub_bu",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                        ]:
                            try:
                                if dict_metatag1[col] == "":
                                    df1.loc[1, col] = 1
                                else:
                                    df1.loc[1, col] = 0

                            except:
                                df1.loc[1, col] = 1
                        else:
                            try:
                                if dict_metatag1[col] == dict_metatag[col]:
                                    df1.loc[1, col] = 1
                                else:
                                    df1.loc[1, col] = 0

                            except:
                                df1.loc[1, col] = "NP"

                    return df1

                    # df = df.append(df1)
                except:
                    df1 = pd.DataFrame(
                        columns=(
                            "url",
                            "redirect",
                            "status",
                            "bu",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "simple_title",
                            "sub_bu",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                        )
                    )
                    for col in df1.columns:

                        if col == "url":
                            df1.loc[1, col] = url1
                        else:
                            df1.loc[1, col] = "NR"
                    # return df1
                    print(url1)
            time.sleep(3)
        except:
            pass
class my_dictionary(dict): 
 
    def __init__(self): 
        self = dict() 
 
    def add(self, key, value): 
        self[key] = value 
        
def path_extrt(url):
    l1 = url.split("/")
    sc = ""
    for i in l1[5:]:
            fr = i
            sc = sc + "/" + fr
    return sc  
def static_list(path):
    print(path)
    url = "http://www8.hp.com/us/en" + path
    r = requests.get(url)
    htmlcontent = r.content
    ##print(htmlcontent)
    soup = BeautifulSoup(htmlcontent, "html.parser")

    for link in soup.find_all("meta"):
        if link.get("name") != None:
            if link.get("name") in [
                "bu",
                "sub_bu",
                "web_section_id",
                "page_content",
                "segment",
                "lifecycle",
                "user_profile",
                "simple_title",
                "analytics_template_name",
                "product_service_name",
                "analytics_section",
            ]:
                dict_metatag.add(link.get("name"), link.get("content"))
    #print(dict_metatag)
    global workstnlist1
    workstnlist1=set()
    for url in list_urls:
        vr = url.split("/")
        sc1 = ""
        for i in vr[:5]:
            fr = i
            sc1 = sc1 + "/" + fr
        workstnlist1.add(sc1[1:] + path)
list_urls=['https://www8.hp.com/ar/es/home.html',
 'https://www8.hp.com/bo/es/home.html',
 'https://www8.hp.com/br/pt/home.html',
 'https://www8.hp.com/ca/en/home.html',
 'https://www8.hp.com/ca/fr/home.html',
 'https://www8.hp.com/lamerica_nsc_carib/en/home.html',
 'https://www8.hp.com/cl/es/home.html',
 'https://www8.hp.com/co/es/home.html',
 'https://www8.hp.com/ec/es/home.html',
 'https://www8.hp.com/lamerica_nsc_cnt_amer/es/home.html',
 'https://www8.hp.com/mx/es/home.html',
 'https://www8.hp.com/py/es/home.html',
 'https://www8.hp.com/pe/es/home.html',
 'https://www8.hp.com/pr/es/home.html',
 'https://www8.hp.com/us/en/home.html',
 'https://www8.hp.com/uy/es/home.html',
 'https://www8.hp.com/ve/es/home.html',
 'https://www8.hp.com/au/en/home.html',
 'https://www8.hp.com/cn/zh/home.html',
 'https://www8.hp.com/hk/en/home.html',
 'https://www8.hp.com/hk/zh/home.html',
 'https://www8.hp.com/in/en/home.html',
 'https://www8.hp.com/id/en/home.html',
 'https://www8.hp.com/kr/ko/home.html',
 'https://www8.hp.com/my/en/home.html',
 'https://www8.hp.com/nz/en/home.html',
 'https://www8.hp.com/ph/en/home.html',
 'https://www8.hp.com/sg/en/home.html',
 'https://www8.hp.com/tw/zh/home.html',
 'https://www8.hp.com/th/en/home.html',
 'https://www8.hp.com/vn/en/home.html',
 'https://www8.hp.com/emea_africa/en/home.html',
 'https://www8.hp.com/emea_africa/fr/home.html',
 'https://www8.hp.com/at/de/home.html',
 'https://www8.hp.com/by/ru/home.html',
 'https://www8.hp.com/be/fr/home.html',
 'https://www8.hp.com/be/nl/home.html',
 'https://www8.hp.com/bg/bg/home.html',
 'https://www8.hp.com/hr/hr/home.html',
 'https://www8.hp.com/cz/cs/home.html',
 'https://www8.hp.com/dk/da/home.html',
 'https://www8.hp.com/ee/et/home.html',
 'https://www8.hp.com/fi/fi/home.html',
 'https://www8.hp.com/fr/fr/home.html',
 'https://www8.hp.com/de/de/home.html',
 'https://www8.hp.com/gr/el/home.html',
 'https://www8.hp.com/hu/hu/home.html',
 'https://www8.hp.com/ie/en/home.html',
 'https://www8.hp.com/il/he/home.html',
 'https://www8.hp.com/it/it/home.html',
 'https://www8.hp.com/kz/ru/home.html',
 'https://www8.hp.com/lv/lv/home.html',
 'https://www8.hp.com/lt/lt/home.html',
 'https://www8.hp.com/emea_middle_east/ar/home.html',
 'https://www8.hp.com/emea_middle_east/en/home.html',
 'https://www8.hp.com/nl/nl/home.html',
 'https://www8.hp.com/no/no/home.html',
 'https://www8.hp.com/pl/pl/home.html',
 'https://www8.hp.com/pt/pt/home.html',
 'https://www8.hp.com/ro/ro/home.html',
 'https://www8.hp.com/ru/ru/home.html',
 'https://www8.hp.com/sa/ar/home.html',
 'https://www8.hp.com/sa/en/home.html',
 'https://www8.hp.com/rs/sr/home.html',
 'https://www8.hp.com/sk/sk/home.html',
 'https://www8.hp.com/si/sl/home.html',
 'https://www8.hp.com/za/en/home.html',
 'https://www8.hp.com/es/es/home.html',
 'https://www8.hp.com/se/sv/home.html',
 'https://www8.hp.com/ch/de/home.html',
 'https://www8.hp.com/ch/fr/home.html',
 'https://www8.hp.com/tr/tr/home.html',
 'https://www8.hp.com/ua/ru/home.html',
 'https://www8.hp.com/ua/uk/home.html',
 'https://www8.hp.com/uk/en/home.html',
 'https://www8.hp.com/ve/en/home.html',
 'https://www8.hp.com/jp/ja/home.html',
 'https://www8.hp.com/si/si/home.html',
 'https://www8.hp.com/rs/rs/home.html']
df1 = pd.DataFrame(
    columns=(
        "url",
        "redirect",
        "status",
        "bu",
        "web_section_id",
        "page_content",
        "segment",
        "lifecycle",
        "user_profile",
        "simple_title",
        "sub_bu",
        "analytics_template_name",
        "product_service_name",
        "analytics_section",
    )
)
dict_metatag = my_dictionary()
workstnlist1=set()
def app_backend(url):
    
    path=path_extrt(url)

    static_list(path)
    

    res = []
    with ThreadPoolExecutor(max_workers=8) as T:
        res = list(T.map(tag_validator, list(workstnlist1)))
    global df
    df = pd.DataFrame(
        columns=(
            "url",
            "redirect",
            "status",
            "bu",
            "web_section_id",
            "page_content",
            "segment",
            "lifecycle",
            "user_profile",
            "simple_title",
            "sub_bu",
            "analytics_template_name",
            "product_service_name",
            "analytics_section",
            )
            )    
    for i in res:
        
        
        df = df.append(i)
    return df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
    
])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    df=app_backend(value)
    print(df.shape)
    return html.Div(dash_table.DataTable(
         
        id='my-output',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
         style_table={'overflowX': 'auto'}
    ))
    



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)    

