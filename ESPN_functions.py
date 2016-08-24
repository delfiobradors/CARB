# -*- coding: utf-8 -*-
import timeit
from lxml import html
import requests
import pandas as pd
import numpy as np
import time

processed_match=pd.Series()

def extract_commentary_ESPN(id):
    id=str(id)
    #try para evitar que pete el programa si no puede cargar bien la url
    try:
        page = requests.get('http://www.espnfc.com/commentary/'+id+'/commentary.html')
        tree = html.fromstring(page.text)
        #ANTES        
        #times = tree.xpath('//div[@class="timestamp"]/p/text()')
        times = tree.xpath('//*[starts-with(@id, "'+id+'-comment")]/div[1]/p/text()')        
        #ANTES        
        #comments = tree.xpath('//div[@class="comment"]/p/text()')
        comments = tree.xpath('//*[starts-with(@id, "'+id+'-comment")]/div[2]/p/text()')        
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
    
def delete_first_last(a):
    return (a[1:-1])

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
    destination_df=pd.read_csv(file, error_bad_lines=False) #read the file
    obtained_df.id=obtained_df.id.convert_objects(convert_numeric=True)
    criterion=obtained_df.id.isin(destination_df.id)
    append_to_csv(file,obtained_df[-criterion])#inverse, because we want to include what is NOT already in the file

#We will save time by not extracting info from already-scraped matches
def select_ids(id_arange,file):
    destination_df=pd.read_csv(file, error_bad_lines=False) #read the file
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

def get_ids(date_number):
    from lxml import html
    import requests
    date_number=str(date_number)
    page = requests.get('http://www.espnfc.com/scores?date='+date_number)
    tree = html.fromstring(page.text)
    return tree.xpath('//div[@class="score full"]/@data-gameid')

def study_date(date,corner_file):
    ids2=get_ids(date)
    ids=pd.Series(ids2)
    analysis_range=select_ids(ids,corner_file)
    chunk_df=analyze_chunk(analysis_range)
    #append results to file if there are any
    try:
        #select_matches_append(chunk_df,corner_file)
        append_to_csv(corner_file,chunk_df)
        print "STUDIED"
        print date
        print "Added"
        print len(chunk_df)
    except:
        print "NOTHING ADDED"


def several_dates(datelist,corner_file):
    for date in datelist:
        study_date(date,corner_file)

#para hacerlo a saco    
#process_match(433703)
#study_in_chunks(397351,419900,50,'corners_append.csv')
#study_in_chunks(426800,434300,50,'corners_append.csv')
#study_in_chunks(424200,424800,50,'corners_append.csv')
#study_in_chunks(393300,393800,50,'corners_append.csv')
#para buscar los ids en una fecha y extraer ESOS
#study_date(20150913,'corners_append.csv')
#study_date(20150829,'corners_append.csv')
#study_date(20150830,'corners_append.csv')
#study_date(20150831,'corners_append.csv')

#para hacerlo con muchas fechas
'''
#2014
#datelist=(20140101,20140102,20140103,20140104,20140105,20140106,20140107,20140108,20140109,20140110,20140111,20140112,20140113,20140114,20140115,20140116,20140117,20140118,20140119,20140120,20140121,20140122,20140123,20140124,20140125,20140126,20140127,20140128,20140129,20140130,20140131)
#several_dates(datelist,'corners_append.csv')
datelist=(20140201,20140202,20140203,20140204,20140205,20140206,20140207,20140208,20140209,20140210,20140211,20140212,20140213,20140214,20140215,20140216,20140217,20140218,20140219,20140220,20140221,20140222,20140223,20140224,20140225,20140226,20140227,20140228,20140229,20140230,20140231)
several_dates(datelist,'corners_append.csv')
datelist=(20140301,20140302,20140303,20140304,20140305,20140306,20140307,20140308,20140309,20140310,20140211,20140312,20140313,20140314,20140315,20140316,20140317,20140318,20140319,20140320,20140321,20140322,20140323,20140324,20140325,20140326,20140327,20140328,20140329,20140330,20140331)
several_dates(datelist,'corners_append.csv')
datelist=(20140401,20140402,20140403,20140404,20140405,20140406,20140407,20140408,20140409,20140410,20140211,20140412,20140413,20140414,20140415,20140416,20140417,20140418,20140419,20140420,20140421,20140422,20140423,20140424,20140425,20140426,20140427,20140428,20140429,20140430,20140431)
several_dates(datelist,'corners_append.csv')
datelist=(20140501,20140502,20140503,20140504,20140505,20140506,20140507,20140508,20140509,20140510,20140211,20140512,20140513,20140514,20140515,20140516,20140517,20140518,20140519,20140520,20140521,20140522,20140523,20140524,20140525,20140526,20140527,20140528,20140529,20140530,20140531)
several_dates(datelist,'corners_append.csv')
datelist=(20140601,20140602,20140603,20140604,20140605,20140606,20140607,20140608,20140609,20140610,20140211,20140612,20140613,20140614,20140615,20140616,20140617,20140618,20140619,20140620,20140621,20140622,20140623,20140624,20140625,20140626,20140627,20140628,20140629,20140630,20140631)
several_dates(datelist,'corners_append.csv')
datelist=(20140701,20140702,20140703,20140704,20140705,20140706,20140707,20140708,20140709,20140710,20140211,20140712,20140713,20140714,20140715,20140716,20140717,20140718,20140719,20140720,20140721,20140722,20140723,20140724,20140725,20140726,20140727,20140728,20140729,20140730,20140731)
several_dates(datelist,'corners_append.csv')
datelist=(20140801,20140802,20140803,20140804,20140805,20140806,20140807,20140808,20140809,20140810,20140211,20140812,20140813,20140814,20140815,20140816,20140817,20140818,20140819,20140820,20140821,20140822,20140823,20140824,20140825,20140826,20140827,20140828,20140829,20140830,20140831)
several_dates(datelist,'corners_append.csv')
datelist=(20140901,20140902,20140903,20140904,20140905,20140906,20140907,20140908,20140909,20140910,20140211,20140912,20140913,20140914,20140915,20140916,20140917,20140918,20140919,20140920,20140921,20140922,20140923,20140924,20140925,20140926,20140927,20140928,20140929,20140930,20140931)
several_dates(datelist,'corners_append.csv')
datelist=(20141001,20141002,20141003,20141004,20141005,20141006,20141007,20141008,20141009,20141010,20141011,20141012,20141013,20141014,20141015,20141016,20141017,20141018,20141019,20141020,20141021,20141022,20141023,20141024,20141025,20141026,20141027,20141028,20141029,20141030,20141031)
several_dates(datelist,'corners_append.csv')
datelist=(20141101,20141102,20141103,20141104,20141105,20141106,20141107,20141108,20141109,20141110,20141111,20141112,20141113,20141114,20141115,20141116,20141117,20141118,20141119,20141120,20141121,20141122,20141123,20141124,20141125,20141126,20141127,20141128,20141129,20141130,20141131)
several_dates(datelist,'corners_append.csv')
datelist=(20141201,20141202,20141203,20141204,20141205,20141206,20141207,20141208,20141209,20141210,20141211,20141212,20141213,20141214,20141215,20141216,20141217,20141218,20141219,20141220,20141221,20141222,20141223,20141224,20141225,20141226,20141227,20141228,20141229,20141230,20141231)
several_dates(datelist,'corners_append.csv')
'''
'''
#2015
datelist=(20150101,20150102,20150103,20150104,20150105,20150106,20150107,20150108,20150109,20150110,20150111,20150112,20150113,20150114,20150115,20150116,20150117,20150118,20150119,20150120,20150121,20150122,20150123,20150124,20150125,20150126,20150127,20150128,20150129,20150130,20150131)
several_dates(datelist,'corners_append.csv')
datelist=(20150201,20150202,20150203,20150204,20150205,20150206,20150207,20150208,20150209,20150210,20150211,20150212,20150213,20150214,20150215,20150216,20150217,20150218,20150219,20150220,20150221,20150222,20150223,20150224,20150225,20150226,20150227,20150228,20150229,20150230,20150231)
several_dates(datelist,'corners_append.csv')
datelist=(20150301,20150302,20150303,20150304,20150305,20150306,20150307,20150308,20150309,20150310,20150211,20150312,20150313,20150314,20150315,20150316,20150317,20150318,20150319,20150320,20150321,20150322,20150323,20150324,20150325,20150326,20150327,20150328,20150329,20150330,20150331)
several_dates(datelist,'corners_append.csv')
datelist=(20150401,20150402,20150403,20150404,20150405,20150406,20150407,20150408,20150409,20150410,20150211,20150412,20150413,20150414,20150415,20150416,20150417,20150418,20150419,20150420,20150421,20150422,20150423,20150424,20150425,20150426,20150427,20150428,20150429,20150430,20150431)
several_dates(datelist,'corners_append.csv')
datelist=(20150501,20150502,20150503,20150504,20150505,20150506,20150507,20150508,20150509,20150510,20150211,20150512,20150513,20150514,20150515,20150516,20150517,20150518,20150519,20150520,20150521,20150522,20150523,20150524,20150525,20150526,20150527,20150528,20150529,20150530,20150531)
several_dates(datelist,'corners_append.csv')
datelist=(20150601,20150602,20150603,20150604,20150605,20150606,20150607,20150608,20150609,20150610,20150211,20150612,20150613,20150614,20150615,20150616,20150617,20150618,20150619,20150620,20150621,20150622,20150623,20150624,20150625,20150626,20150627,20150628,20150629,20150630,20150631)
several_dates(datelist,'corners_append.csv')
datelist=(20150701,20150702,20150703,20150704,20150705,20150706,20150707,20150708,20150709,20150710,20150211,20150712,20150713,20150714,20150715,20150716,20150717,20150718,20150719,20150720,20150721,20150722,20150723,20150724,20150725,20150726,20150727,20150728,20150729,20150730,20150731)
several_dates(datelist,'corners_append.csv')
datelist=(20150801,20150802,20150803,20150804,20150805,20150806,20150807,20150808,20150809,20150810,20150211,20150812,20150813,20150814,20150815,20150816,20150817,20150818,20150819,20150820,20150821,20150822,20150823,20150824,20150825,20150826,20150827,20150828,20150829,20150830,20150831)
several_dates(datelist,'corners_append.csv')
datelist=(20150901,20150902,20150903,20150904,20150905,20150906,20150907,20150908,20150909,20150910,20150211,20150912,20150913,20150914,20150915,20150916,20150917,20150918,20150919,20150920,20150921,20150922,20150923,20150924,20150925,20150926,20150927,20150928,20150929,20150930,20150931)
several_dates(datelist,'corners_append.csv')
datelist=(20151001,20151002,20151003,20151004,20151005,20151006,20151007,20151008,20151009,20151010,20151011,20151012,20151013,20151014,20151015,20151016,20151017,20151018,20151019,20151020,20151021,20151022,20151023,201501024,20151025,20151026,20151027,20151028,20151029,20151030,20151031)
several_dates(datelist,'corners_append.csv')
datelist=(20151101,20151102,20151103,20151104,20151105,20151106,20151107,20151108,20151109,20151110,20151111,20151112,20151113,20151114,20151115,20151116,20151117,20151118,20151119,20151120,20151121,20151122,20151123,20151124,20151125,20151126,20151127,20151128,20151129,20151130,20151131)
several_dates(datelist,'corners_append.csv')
datelist=(20151201,20151202,20151203,20151204,20151205,20151206,20151207,20151208,20151209,20151210,20151211,20151212,20151213,20151214,20151215,20151216,20151217,20151218,20151219,20151220,20151221,20151222,20151223,20151224,20151225,20151226,20151227,20151228,20151229,20151230,20151231)
several_dates(datelist,'corners_append.csv')

#2016
#datelist=(20160101,20160102,20160103,20160104,20160105,20160106,20160107,20160108,20160109,20160110,20160111,20160112,20160113,20160114,20160115,20160116,20160117,20160118,20160119,20160120,20160121,20160122,20160123,20160124,20160125,20160126,20160127,20160128,20160129,20160130,20160131)
#several_dates(datelist,'corners_append.csv')
datelist=(20160127,20160128,20160129,20160130,20160131)
several_dates(datelist,'corners_append.csv')
datelist=(20160201,20160202,20160203,20160204,20160205,20160206,20160207,20160208,20160209,20160210,20160211,20160212,20160213,20160214,20160215,20160216,20160217,20160218,20160219,20160220,20160221,20160222,20160223,20160224,20160225,20160226,20160227,20160228,20160229,20160230,20160231)
several_dates(datelist,'corners_append.csv')
datelist=(20160301,20160302,20160303,20160304,20160305,20160306,20160307)
several_dates(datelist,'corners_append.csv')
'''


datelist=(20160813,20160814,20160815,20160816,20160817,20160818)
several_dates(datelist,'corners_append.csv')
datelist=(20160819,20160820,20160821,20160822)
several_dates(datelist,'corners_append.csv')
