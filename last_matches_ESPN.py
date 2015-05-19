# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:36:45 2015

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
    
def convert_toordinal(date):
    try:
        d= date.toordinal()
    except:
        d=0
    return d
    

#print df.tail()
#initialize last50hom and last50awa and corner9
#df['last50hom']=np.nan
#df['last50awa']=np.nan

#eliminate data without minc1 info
#df=df.dropna(subset = ['minc1'])
def filter_involved_teams_older_matches(df,ind):
#select the name of the team
    team_home=df.iloc[ind].team_home
    team_away=df.iloc[ind].team_away
    date_of_row=df.iloc[ind].date
    #select all the rows where one of the teams is involved
    team_list=[team_home,team_away]
    x = df[(df['team_home'].isin(team_list)) | (df['team_away'].isin(team_list))]
    #eliminate the newer dates than the studied date
    x=x[x.date < date_of_row]
    #sort with the newest matches on top
    x=x.sort_index(by=['date'], ascending=[False])
    return x

def add_last_matches_any(df,num_matches):
    #add column for adding corners on last X matches when any of both teams were involved
    df['last_matches_any']=np.nan
    for index in range(0,len(df)-1):
        #given a row of the dataframe, filter the dataframe only with the involved teams
        df2=filter_involved_teams_older_matches(df,index)
        #select how many matches should we look back, and select only those
        df2=df2.head(num_matches)
        try:
            #calculate percentage of trues
            num_true=float(len(df2[df2.corner9==True]))
            num_tot=float(len(df2))
            percent=float(num_true/num_tot)*float(100)
        except:
            percent=np.nan
        #add this value to df
        df.loc[index,'last_matches_any'] = percent
    return df
    
def filter_team_home_older_matches(df,ind):
#select the name of the team
    team_home=df.iloc[ind].team_home
    date_of_row=df.iloc[ind].date
    #select all the rows where one of the teams is involved
    team_list=[team_home]
    x = df[(df['team_home'].isin(team_list)) | (df['team_away'].isin(team_list))]
    #eliminate the newer dates than the studied date
    x=x[x.date < date_of_row]
    #sort with the newest matches on top
    x=x.sort_index(by=['date'], ascending=[False])
    return x
    
def add_last_matches_team_home(df,num_matches):
    #add column for adding corners on last X matches when any of both teams were involved
    df['last_matches_team_home']=np.nan
    for index in range(0,len(df)-1):
        #given a row of the dataframe, filter the dataframe only with the involved teams
        df2=filter_team_home_older_matches(df,index)
        #select how many matches should we look back, and select only those
        df2=df2.head(num_matches)
        try:
            #calculate percentage of trues
            num_true=float(len(df2[df2.corner9==True]))
            num_tot=float(len(df2))
            percent=float(num_true/num_tot)*float(100)
        except:
            percent=np.nan
        #add this value to df
        df.loc[index,'last_matches_team_home'] = percent
    return df

def filter_team_away_older_matches(df,ind):
#select the name of the team
    team_away=df.iloc[ind].team_away
    date_of_row=df.iloc[ind].date
    #select all the rows where one of the teams is involved
    team_list=[team_away]
    x = df[(df['team_home'].isin(team_list)) | (df['team_away'].isin(team_list))]
    #eliminate the newer dates than the studied date
    x=x[x.date < date_of_row]
    #sort with the newest matches on top
    x=x.sort_index(by=['date'], ascending=[False])
    return x
    
def add_last_matches_team_away(df,num_matches):
    #add column for adding corners on last X matches when any of both teams were involved
    df['last_matches_team_away']=np.nan
    for index in range(0,len(df)-1):
        #given a row of the dataframe, filter the dataframe only with the involved teams
        df2=filter_team_away_older_matches(df,index)
        #select how many matches should we look back, and select only those
        df2=df2.head(num_matches)
        try:
            #calculate percentage of trues
            num_true=float(len(df2[df2.corner9==True]))
            num_tot=float(len(df2))
            percent=float(num_true/num_tot)*float(100)
        except:
            percent=np.nan
        #add this value to df
        df.loc[index,'last_matches_team_away'] = percent
    return df


#read file
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
print df
#calculate and add last matches
df=add_last_matches_any(df,30)
print df
df=add_last_matches_team_home(df,30)
df=add_last_matches_team_away(df,30)
df=df.sort_index(by=['date'], ascending=[False])
print df

#fer el mateix pero per els ultims x partits en els que ha estat involucrat team_home i team_away
#afegir filtre per lligues
#fer funcio on li passi arxiu de dataframe, llista de competis, llista dels equips implicats i em torni els last x
