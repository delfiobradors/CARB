# -*- coding: utf-8 -*-
import timeit
from lxml import html
import requests
import pandas as pd
import numpy as np
import time
import scipy
from scipy import stats

processed_match=pd.Series()

def extract_commentary_ESPN(id):
    id=str(id)
    #try para evitar que pete el programa si no puede cargar bien la url
    try:
        page = requests.get('http://www.espnfc.com/commentary/'+id+'/commentary.html')
        tree = html.fromstring(page.text)
        times = tree.xpath('//div[@class="timestamp"]/p/text()')
        comments = tree.xpath('//div[@class="comment"]/p/text()')
        try:
            df = pd.DataFrame({'times':times, 'comments':comments})
        except:
            df=pd.DataFrame()
        return df
    #si hay problemas para cargar la página, devolverá un dataframe vacío
    except:
        df=pd.DataFrame()
        return df

#remove the last two characters of "times" column
def delete_last(a):
    return (a[:-1])

#calculate minute of first corner
def calculate_minc1(df):
    #remove the last two characters of "times" column
    df.times=df.times.apply(delete_last)
    #convert times to number, since they are a string
    df.times=df.times.convert_objects(convert_numeric=True)
    #filtering rows where comment string starts with 'Corner' and returning minimum time
    return np.amin(df[df.comments.str.startswith('Corner')]).times

#Extract Match Statistics: teams, total corners
def extract_statistics_ESPN(id):
    id=str(id)
    page = requests.get('http://www.espnfc.com/gamecast/statistics/id/'+id+'/statistics.html')
    tree = html.fromstring(page.text)
    team_away = tree.xpath('//div[@class="team away"]/p/a/text()')#visitante
    team_home=tree.xpath('//div[@class="team home"]/p/a/text()')#local
    script=tree.xpath('//*[@id="matchcenter-'+id+'"]/div[1]/p[1]/span/script/text()')
    try:
        timestamp = float(script[0][52:65])
        fecha=time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(timestamp / 1000.0))
    except:
        fecha="UNKNOWN"
    competicion = tree.xpath('//div[@class="match-details"]/p[@class="floatleft"]/text()')
    try:
        competicion= competicion[0].strip()
    except:
        competicion="ERR COMPETICION"
    home_corners = tree.xpath('//td[@id="home-corner-kicks"]/text()')
    away_corners = tree.xpath('//td[@id="away-corner-kicks"]/text()')
    return pd.Series([id,team_away,team_home,competicion,home_corners,away_corners,fecha],index=['id','team_home','team_away','competition','corners_home','corners_away','date'])

#Put together the extracted info
def process_match(id):
    global processed_match
    global bad_match
    my_match=extract_commentary_ESPN(id)
    if len(my_match)>1:
        #en caso de que haya problemas de cargar url, que no pete
        try:
            processed_match=extract_statistics_ESPN(id)
            minc1=pd.Series([calculate_minc1(my_match)],index=['minc1'])
            processed_match=processed_match.append(minc1)
            bad_match=False
        except:
            #si no ha podido cargar la url, lo indica como partido inválido
            bad_match=True
    else:
        bad_match=True
    return processed_match,bad_match

#We need to extract chunks of matches and present them in a dataframe
def analyze_chunk(ids):
    partidos_df=pd.DataFrame()
    for id in ids:
        match_stats,partido_incorrecto=process_match(id)
        if partido_incorrecto==False:
            partidos_df=partidos_df.append(match_stats,ignore_index=True)
    return partidos_df

#Append results to a csv file
def append_to_csv(file,df):
    f = open(file, 'a') # Añadir los resultados al archivo de corners
    df.to_csv(f,header=False,encoding="utf-8")
    f.close()

#append only new matches
def select_matches_append(obtained_df,file):
    destination_df=pd.read_csv(file) #read the file
    obtained_df.id=obtained_df.id.convert_objects(convert_numeric=True)
    criterion=obtained_df.id.isin(destination_df.id)
    append_to_csv(file,obtained_df[-criterion])#inverse, because we want to include what is NOT already in the file

#We will save time by not extracting info from already-scraped matches
def select_ids(id_arange,file):
    destination_df=pd.read_csv(file) #read the file
    criterion=id_arange.isin(destination_df.id)
    return id_arange[-criterion].values

#study and save a range
def study_range (id_ini,id_fin,corner_file):
    #check what id_matches from the range have already been scraped
    raw_range=pd.Series(np.arange(id_ini,id_fin+1))
    analysis_range=select_ids(raw_range,corner_file)
    #perform scraping of missing id_matches
    chunk_df=analyze_chunk(analysis_range)
    #append results to file if there are any
    try:
        #select_matches_append(chunk_df,corner_file)
        append_to_csv(corner_file,chunk_df)
    except:
        print "NOTHING ADDED"
        
#study in chunks and calculate time    
def study_in_chunks(ini,last,step,file):
    for i in range(ini,last+1,step):
        start = timeit.default_timer()
        study_range(i,i+step,file)
        print i
        stop = timeit.default_timer()
        print (stop - start)/60
        print "MINUTOS"
    
study_in_chunks(293100,407000,50,'corners_append.csv')

#350000-401850 fets
