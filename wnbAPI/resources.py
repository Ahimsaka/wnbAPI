#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:42:47 2019

@author: devinarnold
"""
from datetime import date
''' from os.path import isfile, isdir
from os import makedirs'''

# set currentSeason variable for access from search module
if date.today().month <= 3:                   # the season starts in May, 
    currentSeason = str(date.today().year - 1)# so use last year until April
else:
    currentSeason = str(date.today().year)    # after April, use this year

# create a headers dictionary to use on all API requests. 
# this is necessary because the API system we're querying is
# designed for use in the browser, not via Python. 
# to get this list I accessed stats.wnba.com in a web browser
# and copied all request headers that were sent, except for Cookies.
# It may be that some of these headers are not required. Because 
# the set is working I haven't taken time to test each individually. 
headers = {'authority': 'a.data.nba.com',
           'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9',
           'cache-control': 'no-cache', 
           'dnt': '1',
           'pragma': 'no-cache',
           'referer': 'https://a.data.nba.com/wnba/player/203831',
           'sec-fetch-mrode': 'no-cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)' \
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'  \
                         '77.0.3865.90 Safari/537.36',
           }



# create a dictionary of basic team information.
# this is primarily a convenience object which can be printed
# to show the user all valid TeamID values and what team
# they refer to. 
#
# It is also used in the search module to retrieve the
# three letter abbreviations that must be inserted into the
# URL in the teamLogo and schedule functions.
#
# This dictionary will also eventually be used as the basis
# for the planned typed search functionality, allowing users to
# retrieve a TeamID based on the team's name or location 
teams = {'1611661330': {'ta': 'ATL',     # Atlanta and Chicago's data wasn't
                        'tn':'Dream',     # included in the original dict I pulled
                        'tc':'Atlanta'}, # I've added the minimum requirement
        '1611661329': {'ta':'CHI',       # and will finish filling out as needed
                       'tn': 'Sky',
                       'tc':'Chicago'},                        
        '1611661323': {'tid': '1611661323',
                       'tn': 'Sun',
                       'tc': 'Connecticut',
                       'ta': 'CON',
                       'co': 'Eastern Conference',
                       'sta': 'CT',
                       'tz': 'ET'},
        '1611661321': {'tid': '1611661321',
                       'tn': 'Wings',
                       'tc': 'Dallas',
                       'ta': 'DAL',
                       'co': 'Western Conference',
                       'sta': 'TX',
                       'tz': 'CT'},
        '1611661325': {'tid': '1611661325',
                       'tn': 'Fever',
                       'tc': 'Indiana',
                       'ta': 'IND',
                       'co': 'Eastern Conference',
                       'sta': 'IN',
                       'tz': 'ET'},
        '1611661319': {'tid': '1611661319',
                       'tn': 'Aces',
                       'tc': 'Las Vegas',
                       'ta': 'LVA',
                       'co': 'Western Conference',
                       'sta': 'NV',
                       'tz': 'PT'},
        '1611661320': {'tid': '1611661320', 
                       'tn': 'Sparks',
                       'tc': 'Los Angeles',
                       'ta': 'LAS',
                       'co': 'Western Conference',
                       'sta': 'CA',
                       'tz': 'PT'},
        '1611661324': {'tid': '1611661324',
                       'tn': 'Lynx',
                       'tc': 'Minnesota',
                       'ta': 'MIN',
                       'co': 'Western Conference',
                       'sta': 'MN',
                       'tz': 'CT'},
        '1611661313': {'tid': '1611661313',
                       'tn': 'Liberty',
                       'tc': 'New York',  
                       'ta': 'NYL',
                       'co': 'Eastern Conference',
                       'sta': 'NY',
                       'tz': 'ET'},
        '1611661317': {'tid': '1611661317',
                       'tn': 'Mercury',
                       'tc': 'Phoenix',
                       'ta': 'PHO',
                       'co': 'Western Conference',
                       'sta': 'AZ',
                       'tz': 'MT'},
        '1611661328': {'tid': '1611661328',
                       'tn': 'Storm',
                       'tc': 'Seattle',
                       'ta': 'SEA',
                       'co': 'Western Conference',
                       'sta': 'WA',
                       'tz': 'PT'},
        '1611661322': {'tid': '1611661322',  
                       'tn': 'Mystics',
                       'tc': 'Washington',
                       'ta': 'WAS',
                       'co': 'Eastern Conference',
                       'sta': 'DC',
                       'tz': 'ET'}
        } # It is vitally important to note here that Philadelphia, 
          # the greatest city in the country, the capitol of college 
          # basketball, birthplace of Wilt and Kobe, does not have
          # a WNBA team. This is a shameful omission and a critical error. 
          # The people of Philadelphia are very serious about basketball. 
          # Many of them actively follow EVERY Philly NCAA team because they
          # are fans of Philly basketball moreso than any individual school
          # or organization. A Philly WNBA team would have a dedicated fan
          # base from day 1, and the number of major D1 basketball arenas 
          # in the city would give the team amazing leverage in negotiating
          # a stadium deal and practice facilities. 


# creates dictionary of known parameters and accepted values. 
# at the moment this is purely a convenience object which the user
# can print (or access by key) to see the known acceptable values
# for a given parameter. 
#
# when this dictionary has been cleaned up and finalized, it should
# also be useful in building an input validation function to notify
# the user when they've requested an invalid value for a parameter. 
    # this will likely involve converting this dict to its own class
    # so that we can store printable strings displaying examples of the
    # acceptable values, but also store regex strings to validate input 
param_list = {
        'DateFrom':['2001-02-10','12/10/2002', '2014-02-14'], # 'MM(-/)DD(-/)YYYY' || 'YYYY(-/)MM(-/)DD,
        'DateTo': ['2018-02-10','02/10/2019','2017-06-30'], #'MM(-/)DD(-/)YYYY' || 'YYYY(-/)MM(-/)DD,
        'GameSegment': ['','First Half', 'Overtime', 'Second Half'], # The field GameSegment must match the regular expression '^((First Half)|(Overtime)|(Second Half))?$'.
        'LastNGames': '[x for x in range(33)]', #100 doesn't work, 30 and below do so far
        'LeagueID': ['10'],
        'Location': ['Home','Road',''], # The field Location must match the regular expression '^((Home)|(Road))?$'.; 
        'MeasureType': ['Base', 'Advanced','Misc',
                        'Four Factors','Scoring','Opponent',
                        'Usage','Defense'], # The field MeasureType must match the regular expression '^(Base)|(Advanced)|(Misc)|(Four Factors)|(Scoring)|(Opponent)|(Usage)|(Defense)$'.
        'Month': list(set(range(12))),
        'Outcome': ['','W','L'], # The field Outcome must match the regular expression '^((W)|(L))?$'.; 
        'OpponentTeamID': ['0','1611661323', '1611661321', '1611661325',
                               '1611661319','1611661320','1611661324',
                               '1611661313', '1611661317', '1611661328',
                               '1611661322'], # Must be valid Team Id or 0 
        'PaceAdjust': ['Y','N'],
        'PerMode': ['Totals','PerGame','MinutesPer',
                    'Per48','Per40','Per36',
                    'PerMinute','PerPossession','PerPlay',
                    'Per100Possessions','Per100Plays'], # The field PerMode must match the regular expression '^(Totals)|(PerGame)|(MinutesPer)|(Per48)|(Per40)|(Per36)|(PerMinute)|(PerPossession)|(PerPlay)|(Per100Possessions)|(Per100Plays)$'.
        'Period': ['0','1','2','3','4'], 
        'PlusMinus': ['Y','N'],
        'Rank': ['Y','N'],
        'SeasonSegment': ['','Post All-Star', 'Pre All-Star'], #The field SeasonSegment must match the regular expression '^((Post All-Star)|(Pre All-Star))?$'. 
        'SeasonType': ['Regular Season','Pre Season', 'Playoffs', 'All Star'], # The field SeasonType must match the regular expression '^(Regular Season)|(Pre Season)|(Playoffs)|(All Star)$'.
        'VsConference': ['East','West'], # The field VsConference must match the regular expression '^((East)|(West))?$'. 
        'VsDivision': ['Atlantic','Central','Northwest',
                     'Pacific','Southeast','Southwest'], # The field VsConference must match the regular expression '^((East)|(West))?$'.
        'Season': ['2000','2012','2019'],
        'GameScope': ['','Yesterday','Last 10'], # '((Yesterday)|(Last 10))?'.
        'PlayerExperience': ['Rookie','Sophomore','Veteran'], #((Rookie)|(Sophomore)|(Veteran))?'.
        'PlayerPosition': ['', 'F','C','G','C-F','F-C','F-G','G-F'], # The field PlayerPosition must match the regular expression '((F)|(C)|(G)|(C-F)|(F-C)|(F-G)|(G-F))?'.
        'StarterBench': ['', 'Starters','Bench'], # The field StarterBench must match the regular expression '((Starters)|(Bench))?'
        'PlayerID': ['203399'], # Valid player ID, 0 or '' where not required. 
        'TopX': ['','1','6','10'], #any number
        'Conference': ['East','West'], # The field Conference must match the regular expression '((East)|(West))?'.
        'Division': ['Atlantic','Central','Northwest',
                     'Pacific','Southeast','Southwest'], # The field Division must match the regular expression '((Atlantic)|(Central)|(Northwest)|(Pacific)|(Southeast)|(Southwest))?'.
        'GroupQuantity': ['1','2','5'],
        'StatCategory': ['MIN','FGM','FGA','FG_PCT',
                         'FG3M','FG3A','FG3_PCT','FTM','FTA',
                         'FT_PCT','OREB', 'DREB','AST',
                         'STL','BLK','TOV','PTS'],
        'ShotClockRange': ['24-22', '22-18 Very Early', '18-15 Early',
                           '15-7 Average','7-4 Late', '4-0 Very Late',
                           'ShotClock Off'], # The field ShotClockRange must match the regular expression '((24-22)|(22-18 Very Early)|(18-15 Early)|(15-7 Average)|(7-4 Late)|(4-0 Very Late)|(ShotClock Off))?'.
        'Scope': ['S','Rookies','','RS'], # The field Scope must match the regular expression '^(RS)|(S)|(Rookies)$'.; 
        'PORound': ['','1','2','3','4'], # '' or number
        'PointDiff': ['','1','2','5'], # Number or ''
        'Country': ['USA','CAN','AUS',''],# ?String?
        'ActiveFlag': ['','Y','N'], # Y/N
        'AheadBehind': ['Ahead or Behind', 'Ahead','Behind'],
        'ClutchTime': ['Last 5 Minutes', 'Last 4 Minutes','Last 3 Minutes',
                       'Last 2 Minutes','Last 1 Minute', 'Last 30 Seconds',
                       'Last 10 Seconds'], # The field ClutchTime must match the regular expression '^((Last 5 Minutes)|(Last 4 Minutes)|(Last 3 Minutes)|(Last 2 Minutes)|(Last 1 Minute)|(Last 30 Seconds)|(Last 10 Seconds))?$'.
        'DraftPick': ['','1','2','5'], # ?num
        'DraftYear': ['','2019'], # valid year
        'GameID': ['1021900201','','1021900177'], # The field GameID must match the regular expression '^(\d{10})?$'.; 
        'DistanceRange': ['5ft Range','8ft Range','By Zone'],
        'TwoWay': 'I don\'t know what values are valid for this.',
        'Weight': 'I don\'t know what values are valid for this.',
        'Height': 'I don\'t know what values are valid for this.',
        'Split': 'I don\'t know what values are valid for this.'

}


def __main__():
    pass