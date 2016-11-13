# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 09:29:06 2016

@author: delfi
"""

import timeit
from lxml import html
import requests
import pandas as pd
import numpy as np
import time

id=450904
id=str(id)
#try para evitar que pete el programa si no puede cargar bien la url
#page = requests.get('http://www.espnfc.com/commentary/'+id+'/commentary.html')
page = requests.get('http://www.espnfc.com/commentary?gameId='+id+'')
tree = html.fromstring(page.text)
#ANTES        
#times = tree.xpath('//td[@class="timestamp"]/text()')
times = tree.xpath('//tr[@data-type="corner-kick"]/td[1]/text()')
#times = tree.xpath('//*[starts-with(@data-id, "comment")]/div[1]/p/text()')        
#ANTES        
#comments = tree.xpath('//td[@class="game-details"]/text()')
comments=tree.xpath('//tr[@data-type="corner-kick"]/td[3]/text()')
#comments = tree.xpath('//*[starts-with(@data-id, "game-details")]/text()')        
df = pd.DataFrame({'times':times, 'comments':comments})
print df

id=str(id)
page = requests.get('http://www.espnfc.us/match?gameId='+id+'')
tree = html.fromstring(page.text)
team_away = tree.xpath('//*[@id="custom-nav"]/header/div[2]/div[3]/div/div[2]/div/a/span[1]/text()')#visitante
#team_home=tree.xpath('//div[@class="team home"]/p/a/text()')#local
team_home=tree.xpath('//*[@id="custom-nav"]/header/div[2]/div[1]/div/div[1]/div/a/span[1]/text()')#local
fecha=tree.xpath('//*[@id="gamepackage-game-information"]/article/div/ul[2]/li/div[1]/span/@data-date')
fecha=str(fecha[0])
fecha = fecha[0:10]
print fecha
fecha=time.strptime(fecha, "%Y-%m-%d")  
print fecha
fecha=time.strftime("%a %d %b %Y %00:%00:%00 GMT", fecha)
print fecha
#fecha = tree.xpath('//*[@id="gamepackage-game-information"]/article/div/ul[2]/li/div[1]/span/span[2]/text()')
competicion = tree.xpath('//*[@id="custom-nav"]/header/div[1]/text()')
home_corners = tree.xpath('//*[@id="gamepackage-soccer-match-stats"]/div/div/div[2]/table/tbody/tr[5]/td[1]/text()')
away_corners = tree.xpath('//*[@id="gamepackage-soccer-match-stats"]/div/div/div[2]/table/tbody/tr[5]/td[3]/text()')
df2= pd.Series([id,team_away,team_home,competicion,home_corners,away_corners,fecha],index=['id','team_home','team_away','competition','corners_home','corners_away','fecha'])
print df2

def delete_after_sep(a):
    sep = "'"
    return(a.split(sep, 1)[0])

#calculate minute of first corner

#remove the last two characters of "times" column
#canvinov16    
#df.times=df.times.apply(delete_last)
df.times=df.times.apply(delete_after_sep)    
#convert times to number, since they are a string
df.times=df.times.convert_objects(convert_numeric=True)
#filtering rows where comment string starts with 'Corner' and returning minimum time
print np.amin(df.times)

    
