# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:19:49 2015

@author: delfi
"""
import pandas as pd
import numpy as np
import scipy
from scipy import stats

def chisquare_on_csv(expected_freq,file):
    analysis_df=pd.read_csv(file)
    #we drop every match where minc1=NaN
    analysis_df=analysis_df.dropna(subset = ['minc1'])
    total_matches=len(analysis_df)-1
    corner_true=len(analysis_df[analysis_df.minc1<10])
    expected_true=total_matches*expected_freq
    observed = np.array([corner_true,total_matches-corner_true])
    expected = np.array([expected_true,total_matches-expected_true])
    chsq,pval= scipy.stats.chisquare(observed,f_exp=expected)
    proportion_true=float((corner_true*100)/total_matches)
    return str(chsq),str(pval),str(total_matches),str(corner_true),str(proportion_true)
    
def chisquare_primera_on_csv(expected_freq,file):
    analysis_df=pd.read_csv(file)
    #we drop every match where minc1=NaN
    analysis_df=analysis_df.dropna(subset = ['minc1'])
    analysis_df=analysis_df[analysis_df.competition.str.startswith('SPANISH PRIMERA')==True]
    total_matches=len(analysis_df)-1
    corner_true=len(analysis_df[analysis_df.minc1<10])
    expected_true=total_matches*expected_freq
    observed = np.array([corner_true,total_matches-corner_true])
    expected = np.array([expected_true,total_matches-expected_true])
    chsq,pval= scipy.stats.chisquare(observed,f_exp=expected)
    proportion_true=float((corner_true*100)/total_matches)
    return str(chsq),str(pval),str(total_matches),str(corner_true),str(proportion_true)
    
def chisquare_3ligas_on_csv(expected_freq,file):
    analysis_df=pd.read_csv(file)
    #we drop every match where minc1=NaN
    analysis_df=analysis_df.dropna(subset = ['minc1'])
    #remove any duplicate matches (id)
    analysis_df=analysis_df.drop_duplicates(cols='id',take_last=True)
    analysis_df=analysis_df[analysis_df.competition.str.startswith(('SPANISH PRIMERA','BARCLAYS','ITALIAN SERIE'))==True]
    total_matches=len(analysis_df)-1
    corner_true=len(analysis_df[analysis_df.minc1<10])
    expected_true=total_matches*expected_freq
    observed = np.array([corner_true,total_matches-corner_true])
    expected = np.array([expected_true,total_matches-expected_true])
    chsq,pval= scipy.stats.chisquare(observed,f_exp=expected)
    proportion_true=float((corner_true*100)/total_matches)
    return str(chsq),str(pval),str(total_matches),str(corner_true),str(proportion_true)
    
expected_freq=1/1.83
 #expected 54%
chsq,pval,total_matches,corner_true,proportion_true=chisquare_on_csv(expected_freq,'corners_append.csv')
expected_freq=expected_freq*100
print "TODOS LOS PARTIDOS:"
print "Expected: "+str("%.2f" % expected_freq)+"%, Observed: "+proportion_true+"% on "+total_matches+" matches"
print "Your p-value is "+pval

expected_freq=1/1.83
chsq,pval,total_matches,corner_true,proportion_true=chisquare_primera_on_csv(expected_freq,'corners_append.csv')
expected_freq=expected_freq*100
print "PRIMERA"
print "Expected: "+str("%.2f" % expected_freq)+"%, Observed: "+proportion_true+"% on "+total_matches+" matches"
print "Your p-value is "+pval

expected_freq=1/1.83
chsq,pval,total_matches,corner_true,proportion_true=chisquare_3ligas_on_csv(expected_freq,'corners_append.csv')
expected_freq=expected_freq*100
print "PRIMERA,PREMIER,SERIE A"
print "Expected: "+str("%.2f" % expected_freq)+"%, Observed: "+proportion_true+"% on "+total_matches+" matches"
print "Your p-value is "+pval