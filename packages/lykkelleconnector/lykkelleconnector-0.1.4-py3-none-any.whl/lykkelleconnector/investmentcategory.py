#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#tested successfully. ready to be deployed in Prod
#deployed in Prod. This is the final version
"""
Created on Mon Jul 15 23:14:15 2019
This program identifies various investment categories
 based on rating and region
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import psycopg2 as pgs
grade = {'AAA': 'Prime', 'AA+': 'High Grade', 'AA': 'High Grade',
         'AA-': 'High Grade', 'A+': 'UM Grade', 'A': 'UM Grade',
         'A-': 'UM Grade', 'BBB+': 'LM Grade', 'BBB': 'LM Grade',
         'BBB-': 'LM Grade', 'BB+': 'Non-Inv Grade',
         'BB': 'Non-Inv Grade', 'BB-': 'Non-Inv Grade',
         'B+': 'High Yield', 'B': 'High Yield',
         'B-': 'High Yield', 'NR': 'Not Rated'}


class investmentcategory:
    def __init__(self):
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            sel = "select country, region, rating from benchmark_all"
            cursor.execute(sel)
            myselection = cursor.fetchall()
            length = len(myselection)
            c = 0
            brow = []
            for i in range(length):
                mysel = myselection[i]
                country = mysel[0]
                region = mysel[1]
                rating = mysel[2]
                # print(country,'-',region,'-',rating)
                if region == 'Europe':
                    inv_category = 'EU_'+grade.get(rating, 'Sub-Prime')
                elif region == 'Asia':
                    inv_category = 'AS_'+grade.get(rating, 'Sub-Prime')
                elif region == 'Africa':
                    inv_category = 'AF_'+grade.get(rating, 'Sub-Prime')
                elif region == 'NAmerica':
                    inv_category = 'NA_'+grade.get(rating, 'Sub-Prime')
                elif region == 'SAmerica':
                    inv_category = 'SA_'+grade.get(rating, 'Sub-Prime')
                elif region == 'Oceania':
                    inv_category = 'OC_'+grade.get(rating, 'Sub-Prime')
                else:
                    print("unknown region " + region + ". Adjust region in the benchmark_all table")
                    inv_category = None
                upd = "update benchmark_all set mkt_type=%s where country=%s and region =%s and rating =%s"
                try:
                    cursor.execute(upd, (inv_category, country, region, rating))
                    c = c+1
                except pgs.Error as e:
                       print(e.pgerror)
                       brow.append(country)
            print("updated investment category for ", c, "records successfully")
            if brow != []:
                print("could not update few records and they are ", brow)
            else:
                print("all records successfully loaded")
        print("postgres connection closed")
