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
    #PARA MIRAR TODOS LOS PARTIDOS DD HAN ESTADO INVOLUCRADOS
    #x = df[(df['team_home'].isin(team_list)) | (df['team_away'].isin(team_list))]
    #select rows where home team played as homoe and away team played as away

    #MIRO CASA:
    #x = df[(df['team_home']==team_list[0])]
    #MIRO AMBOS:
    #x = df[(df['team_home']==team_list[0]) | (df['team_away']==team_list[1])]
    #MIRO FUERA:
    x = df[(df['team_away']==team_list[1])]
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
competition_list=['SPANISH PRIMERA DIVISIÓN','BARCLAYS PREMIER LEAGUE','ITALIAN SERIE A','GERMAN BUNDESLIGA','FRENCH LIGUE 1']
#competition_list=['ENGLISH LEAGUE CHAMPIONSHIP']
df = df[(df['competition'].isin(competition_list))]
#remove any duplicate matches (id)
df=df.drop_duplicates(subset='id',take_last=True)
#drop matches without minc1
df=df.dropna(subset = ['minc1'])
#add column for corner before 9 true or false
df['corner9']=df.minc1<11
#convert dates to be able to sort and compare
convert_dates(df)
#reset indexes to be able to run the for loop
df = df.reset_index(drop=True)
'''


'''
MAL='[Malaga]'
SEV='[Sevilla FC]'
ESP='[Espanyol]'
GET='[Getafe]'
DEP='[Deportivo La Coruña]'
RSO='[Real Sociedad]'
RAY='[Rayo Vallecano]'
VAL='[Valencia]'
ATB='[Athletic Bilbao]'
BAR='[Barcelona]'
CEL='[Celta Vigo]'
LEV='[Levante]'
GRA='[Granada]'
EIB='[Eibar]'
VIL='[Villarreal]'
ATM='[Atletico Madrid]'
SPO='[Sporting Gijon]'
RMA='[Real Madrid]'
RBE='[Real Betis]'
LPA='[Las Palmas]'

match1=[RMA,CEL]
match2=[VIL,LPA]
match3=[GET,SEV]
match4=[DEP,MAL]
match5=[RBE,GRA]
match6=[EIB,BAR]
match7=[RSO,LEV]
match8=[SPO,ATB]
match9=[VAL,ATM]
match10=[ESP,RAY]

JUV='[Juventus]'
NAP='[Napoli]'
ASR='[AS Roma]'
LAZ='[Lazio]'
BOL='[Bologna]'
UDI='[Udinese]'
FIO='[Fiorentina]'
MIL='[AC Milan]'
ATA='[Atalanta]'
INT='[Internazionale]'
PAL='[Palermo]'
GEN='[Genoa]'
SAU='[Sassuolo]'
EMP='[Empoli]'
TOR='[Torino]'
SAM='[Sampdoria]'
CES='[Cesena]'
FRO='[Frosinone]'
GEN='[Genoa]'
VER='[Hellas Verona]'
CHI='[Chievo Verona]'
CAR='[Carpi]'

match21=[ASR,FIO]
match22=[VER,SAM]
match23=[NAP,CHI]
match24=[TOR,LAZ]
match25=[SAU,MIL]
match26=[BOL,CAR]
match27=[ATA,JUV]
match28=[GEN,EMP]
match29=[FRO,UDI]
match30=[INT,PAL]

MAN='[Manchester United]'
NCS='[Newcastle United]'
CPL='[Crystal Palace]'
ASV='[Aston Villa]'
LEI='[Leicester City]'
TOT='[Tottenham Hotspur]'
NOR='[Norwich City]'
STO='[Stoke City]'
SUN='[Sunderland]'
SWA='[Swansea City]'
WHM='[West Ham United]'
BMT='[AFC Bournemouth]'
WBR='[West Bromwich Albion]'
CHE='[Chelsea]'
EVE='[Everton]'
MCT='[Manchester City]'
WFD='[Watford]'
SOU='[Southampton]'
ARS='[Arsenal]'
LIV='[Liverpool]'

match41=[TOT,ARS]
match42=[CHE,STO]
match43=[SWA,NOR]
match44=[SOU,SUN]
match45=[NCS,BMT]
match46=[MCT,ASV]
match47=[EVE,WHM]
match48=[WFD,LEI]
match49=[CPL,LIV]
match50=[WBR,MAN]

MAI='[Mainz]'
HOF='[TSG Hoffenheim]'
COL='[FC Cologne]'
BMO='[Borussia Monchengladbach]'
HAM='[Hamburg SV]'
FRA='[Eintracht Frankfurt]'
WOL='[VfL Wolfsburg]'
HBE='[Hertha Berlin]'
STU='[VfB Stuttgart]'
SCH='[Schalke 04]'
BDO='[Borussia Dortmund]'
BLE='[Bayer Leverkusen]'
WER='[Werder Bremen]'
ING='[FC Ingolstadt 04]'
DAR='[SV Darmstadt 98]'
BMU='[Bayern Munich]'
AUG='[FC Augsburg]'
HAN='[Hannover 96]'

match61=[WOL,BMO]
match62=[STU,HOF]
match63=[AUG,BLE]
match64=[WER,HAN]
match65=[FRA,ING]
match66=[COL,SCH]
match67=[BDO,BMU]
match68=[MAI,DAR]
match69=[HAM,HBE]

'''
SRN='[Stade Rennes]'
LIL='[Lille]'
SRI='[Stade de Reims]'
PSG='[Paris Saint-Germain ]'
ANG='[Angers]'
TRO='[Troyes]'
BAS='[Bastia]'
NIC='[Nice]'
CAE='[Caen]'
MTP='[Montpellier]'
GUI='[Guingamp]'
AJA='[AC Ajaccio]'
BOR='[Bordeaux]'
TOU='[Toulouse]'
ASM='[AS Monaco]'
LOR='[Lorient]'
STE='[St Etienne]'
NAN='[Nantes]'
MAR='[Marseille]'
LYO='[Lyon]'

match71=[SRN,LIL]
match72=[SRI,PSG]
match73=[ANG,TRO]
match74=[BAS,NIC]
match75=[CAE,MTP]
match76=[GUI,AJA]
match77=[BOR,TOU]
match78=[ASM,LOR]
match79=[STE,NAN]
match80=[MAR,LYO]
'''

BRI='[Brighton & Hove Albion]'
WOL='[Wolverhampton Wanderers]'
QPR='[Queens Park Rangers]'
HUL='[Hull City]'
BUR='[Burnley]'
IPS='[Ipswich Town]'
CHA='[Charlton Athletic]'
NOT='[Nottingham Forest]'
BIR='[Birmingham City]'
BRE='[Brentford]'
REA='[Reading]'
BRI='[Bristol City]'
BOL='[Bolton Wanderers]'
HUD='[Huddersfield Town]'
MID='[Middlesbrough]'
DER='[Derby County]'
FUL='[Fulham]'
SHE='[Sheffield Wednesday]'
CAR='[Cardiff City]'
BLA='[Blackburn Rovers]'
PRE='[Preston North End]'
ROT='[Rotherham United]'
LEE='[Leeds United]'
MKD='[Milton Keynes Dons]'

match91=[BRI,WOL]
match92=[QPR,HUL]
match93=[BUR,IPS]
match94=[CHA,NOT]
match95=[BIR,BRE]
match96=[REA,BRI]
match97=[BOL,HUD]
match98=[MID,DER]
match99=[FUL,SHE]
match100=[CAR,BLA]
match101=[PRE,ROT]
match102=[LEE,MKD]

#perform the calculation at once for several matches
#print return_pct_last_matches(df,30,team_list)

matches_list=[match1,match2,match3,match4,match5,match6,match7,match8,match9,match10,match21,match22,match23,match24,match25,match26,match27,match28,match29,match30,match41,match42,match43,match44,match45,match46,match47,match48,match49,match50,match61,match62,match63,match64,match65,match66,match67,match68,match69]

for match in matches_list:
    print match
    print return_pct_last_matches(df,30,match)
    print len(filter_two_teams(df,match))
#print filter_two_teams(df,match22)
#con el len() de esto podria mirar si tengo o no los 30 partidos
   
#para intentar hacer el filtro de df a partir de una fecha
#def filter_newer_dates(date)
#df = df[df.date < date]
