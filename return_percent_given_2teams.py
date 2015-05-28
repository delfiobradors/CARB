# -*- coding: utf-8 -*-
"""
Created on Mon May 18 22:42:15 2015

@author: delfi
"""
import pandas as pd
import numpy as np
import time
import datetime

def convert_dates(analysis_df):
    analysis_df.date=analysis_df.date.apply(convert_to_datetime)
    
    #this will return dates converted to ordinal in order to be able to filter easier
    #analysis_df.date=analysis_df.date.apply(convert_toordinal)

def convert_to_datetime(date):
    string2=(date[4:15])
    #if there is a problem will return date 1999-01-01
    try:
        conv_time=time.strptime(string2,'%d %b %Y')
        d=datetime.date(conv_time.tm_year, conv_time.tm_mon, conv_time.tm_mday)
    except:
        d=datetime.date(1999, 1, 1)
    return d

def filter_two_teams(df,team_list):
    #select all the rows where one of the teams is involved
    x = df[(df['team_home'].isin(team_list)) | (df['team_away'].isin(team_list))]
    #sort with the newest matches on top
    x=x.sort_index(by=['date'], ascending=[False])
    return x

def return_pct_last_matches(df,num_matches,team_list):
    #given a row of the dataframe, filter the dataframe only with the involved teams
    df2=filter_two_teams(df,team_list)
    #select how many matches should we look back, and select only those
    df2=df2.head(num_matches)
    try:
        #calculate percentage of trues
        num_true=float(len(df2[df2.corner9==True]))
        num_tot=float(len(df2))
        percent=float(num_true/num_tot)*float(100)
    except:
        percent=np.nan
    return percent

df=pd.read_csv('corners_append.csv')
#PREPARE THE FILE TO RUN FUNCTIONS TO ADD COLUMNS OF LAST MATCHES PCT

#filter chosen competitions
competition_list=['SPANISH PRIMERA DIVISIÓN','BARCLAYS PREMIER LEAGUE','ITALIAN SERIE A']
df = df[(df['competition'].isin(competition_list))]
#remove any duplicate matches (id)
df=df.drop_duplicates(subset='id',take_last=True)
#drop matches without minc1
df=df.dropna(subset = ['minc1'])
#add column for corner before 9 true or false
df['corner9']=df.minc1<10
#convert dates to be able to sort and compare
convert_dates(df)
#reset indexes to be able to run the for loop
df = df.reset_index(drop=True)
'''
[AC Milan]	[Fiorentina]
[Atalanta]	[Siena]
[Cagliari]	[Internazionale]
[Cesena]	[Bologna]
[Chievo Verona]	[Catania]
[Lazio]	[Napoli]
[Lecce]	[AS Roma]
[Novara]	[Genoa]
[Palermo]	[Juventus]
[Udinese]	[Parma]
[Bologna]	[Palermo]
[Cagliari]	[Atalanta]
[Catania]	[AC Milan]
[Fiorentina]	[Chievo Verona]
[Internazionale]	[Genoa]
[Juventus]	[Napoli]
[Lecce]	[Cesena]
[Parma]	[Lazio]
[AS Roma]	[Novara]
[Siena]	[Udinese]
[AC Milan]	[AS Roma]
[Atalanta]	[Bologna]
[Cesena]	[Parma]
[Chievo Verona]	[Siena]
[Genoa]	[Fiorentina]
[Juventus]	[Internazionale]


'''
JV='[Juventus]'
NP='[Napoli]'
ASRM='[AS Roma]'
LZ='[Lazio]'
#perform the calculation at once for several matches
match1=[ASRM,LZ]
match2=[JV,NP]
match3=[JV,NP]
match4=[JV,NP]
match5=[JV,NP]
#print return_pct_last_matches(df,30,team_list)

matches_list=[match1,match2,match3,match4,match5]
for match in matches_list:
    print match
    print return_pct_last_matches(df,4000,match)
print filter_two_teams(df,match1)
#con el len() de esto podria mirar si tengo o no los 30 partidos
