# -*- coding: utf-8 -*-
"""
Created on Thu May 28 20:48:22 2015

@author: delfi
"""

def get_ids(date_number):
    from lxml import html
    import requests
    date_number=str(date_number)
    page = requests.get('http://www.espnfc.com/scores?date='+date_number)
    tree = html.fromstring(page.text)
    return tree.xpath('//div[@class="score full"]/@data-gameid')
ids= get_ids(20150503)
print ids[3]