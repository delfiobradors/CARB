# corners_arbitrage

This repository is my capstone project for the Data Science and Big Data course in Universitat de Barcelona.

The idea is to gain advantage on bets regarding minute of first corner of a given match.

The odds are usually the same regardless of the match and league, and I wanted to perform a study to check whether there were cases where it could be profitable to bet with a specific pattern.

First step was to extract the data. ESPN has a log of matches with the comments, where the corners are indicated, so the first target was to extract, for a given match, the minute of the first corner, the involved teams, the league, the date and the match ID.

This is coded in the file "ESPN_functions.py", with previous tests on "Notebook funcions ESPN.ipynb" and "ESPN Scraping.ipynb".

Scraped matches are saved into "corners_append.csv"

This file takes two numbers that will be the first and last match ID that we want to scrap, and a "chunk" size, in order to save the results from time to time to avoid losing data in case there is some problem.

Second step was to perform a statistical significance analysis.

Odds are always the same for any given match: You can bet 1 dollar to "there will be a corner before 09:00" and if you are right, you will get back 1,83 USD.
This bet is assuming that, on average, there is a 55% chance that there will be a corner before min 09:00 on a given match.

I studied the deviation from this value with certain conditions:

- On all matches
- On Spain's Primera División
- On Spain's Primera División + England Premier League + Italy Serie A.

The third selection was done taking into account the leagues where the percentage was highest.

The code and results are in "ESPN_chisquared.py". Significance was found.

Third step is going to be to apply Machine Learning to try to predict the likelihood of a corner on a given match.
