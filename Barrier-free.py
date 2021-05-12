# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:36:03 2021

@author: Liang
"""

import requests
import pandas as pd
import json
import folium

def download():
    API_Key = '30c0fc11-81bb-4296-8bad-72dc7fae5eaf'
    url1 = "https://data.epa.gov.tw/api/v1/fac_p_13?format=csv&offset=0&api_key=%s" %(API_Key)
    url1_1 = "https://data.epa.gov.tw/api/v1/fac_p_13?format=csv&offset=1001&api_key=%s" %(API_Key)
    url2 = "https://data.coa.gov.tw/Service/OpenData/ODwsv/ODwsvAccessibleFarm.aspx"
    

    Toilet = pd.concat([pd.read_csv(url1), pd.read_csv(url1_1)], axis = 0)
    

    Toilet_fn = 'Toilet.csv'
    Toilet.to_csv(Toilet_fn, encoding = 'utf-8',index = False)
    
    other = requests.get(url2)
    other_fn = "other.json"
    
    with open(other_fn, 'w') as f:
        json.dump(other.json(), f)

#檔案整理及合併
def fileMerge():
        
    getDatas_A = pd.read_csv('Toilet.csv')
    getDatas_O = pd.read_json('other.json')
    #處理廁所資料    
    temp_data = getDatas_A[getDatas_A['Type2'] == "無障礙廁所"]
    All_data = temp_data.loc[: ,['Type', 'Name', 'Type2', 'Address', 'Latitude', 'Longitude']]
    
    #處理休閒農業區資料
    temp_data = getDatas_O[getDatas_O['County'] == "南投縣"]
    data_O = temp_data.loc[1:, [ 'FarmNm_CH', 'AccessibleItem', 'Address_CH', 'Latitude', 'Longitude']]

    #合併資料
    for FarmNm_CH, AccessibleItem, Address_CH, Latitude, Longitude in data_O.values:
       kind_data = pd.Series(['休閒農業區', FarmNm_CH, AccessibleItem, Address_CH, Latitude, Longitude],
                               index = ['Type', 'Name', 'Type2', 'Address', 'Latitude', 'Longitude'])
       All_data = All_data.append(kind_data, ignore_index=True)
    
    #存成csv檔
    All_data.to_csv("All_data.csv", encoding = 'utf-8')



if __name__  == "__main__":
    download()
    fileMerge()
   
    m = folium.Map((23.973694,120.680687),zoom_start=12)
    data_fn = 'All_data.csv'
    getDatas = pd.read_csv(data_fn , encoding = 'utf-8')

    for data in getDatas.values:
        popuptext="類型：%s<br>名稱：%s<br>無障礙設施：<b>%s</b><br>地址：%s"%(data[1],data[2], data[3], data[4])
        iframe = folium.IFrame(popuptext, height = 150)
        
        folium.Marker(
            location=[data[5],data[6]],
            radius=20,
            popup = folium.Popup(iframe, max_width=300,min_width=300) ,
            color='#3186cc',

            ).add_to(m)
    m.save("map.html")

