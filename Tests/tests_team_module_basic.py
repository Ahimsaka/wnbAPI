#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:19:45 2019

File spun off from original test_basic file because the basic unit tests
had gotten long enough to lag my IDE a bit, so it seemed best to split them
up. 
"""
from .context import wnbAPI
#from context import wnbAPI
import unittest # import unittest module
                #    - see docs.python.org/3/library/unittest.html


####################################################################
####                                                            ####
####                     team module tests                      ####
####                                                            ####
####################################################################
class TestTeamObjectCreation(unittest.TestCase):
    '''
    This TestCase should include tests to create a Team object. 
       - Team object should initialize with:
           
           self.requiredParams = {
            'DateFrom': '',   # Required but empty string accepted
            'DateTo':'',      # Required but empty string accepted
            'GameSegment': '',# Required but empty string accepted
            'LastNGames':'0', # 0 stands for all games
            'LeagueID':'10',  # 10 is WNBA. 00 is NBA and 30 is G-League 
            'Location':'',    # Required but empty string accepted
            'MeasureType': 'Base',#Required and needs string. 
            'Month':'0',      # 0 stands for all months 
            'Outcome':'',     # Required but empty string accepted
            'OpponentTeamID': '0',# 0 stands for all opponents
            'PaceAdjust':'N', # Requires Y or N 
            'PerMode': 'PerGame',# Requires string input
            'Period': '0',    # 0 stands for all periods
            'PlusMinus':'N',  # Requires Y or N
            'Rank': 'N',      # Requires Y or N
            'SeasonSegment':'',# Required but empty string accepted
            'SeasonType':'Regular Season', # Requires string input
            'VsConference': '',# Required but empty string accepted 
            'VsDivision':'',  # Required but empty string accepted
            'Season': search.currentSeason, # Requires string or integer year.
            'TeamID':'1611661322', # 2019 World Champion Washington Mystics
            }    
           
           self.endpoints = {
            'details':
                'https://stats.wnba.com/stats/teamdetails',
           'roster':
                'https://stats.wnba.com/stats/commonteamroster',
            'gamelogs':
                'https://stats.wnba.com/stats/teamgamelogs',
            'shooting': 
                'https://stats.wnba.com/stats/teamdashboardbyshootingsplits',
            'clutch':
                'https://stats.wnba.com/stats/leaguedashteamclutch',
            'lineups':
                'https://stats.wnba.com/stats/teamdashlineups',
            'playerDashboard':
                'https://stats.wnba.com/stats/teamplayerdashboard',
            'dashboardBySplits':
                'https://stats.wnba.com/stats/teamdashboardbygeneralsplits', 
            'onOff':
                'https://stats.wnba.com/stats/teamplayeronoffdetails',
            'onOffSummary':
                'https://stats.wnba.com/stats/teamplayeronoffsummary',
            'yearByYearStats':
                'https://stats.wnba.com/stats/teamyearbyyearstats'
             }
    '''
    def setUp(self):
        '''
        create Test object and set to self.session
    
        '''
        self.session = wnbAPI.Team()
        
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
        
    def test_initial_values(self):
        self.assertEqual(self.session.requiredParams, {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '10', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'Outcome': '', 'OpponentTeamID': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'TeamID': '1611661322', 'VsConference': '', 'VsDivision': '', 'Season': '2019'})

        self.assertEqual(self.session.endpoints, {
            'details':
                'https://stats.wnba.com/stats/teamdetails',
           'roster':
                'https://stats.wnba.com/stats/commonteamroster',
            'gamelogs':
                'https://stats.wnba.com/stats/teamgamelogs',
            'shooting': 
                'https://stats.wnba.com/stats/teamdashboardbyshootingsplits',
            'clutch':
                'https://stats.wnba.com/stats/leaguedashteamclutch',
            'lineups':
                'https://stats.wnba.com/stats/teamdashlineups',
            'playerDashboard':
                'https://stats.wnba.com/stats/teamplayerdashboard',
            'dashboardBySplits':
                'https://stats.wnba.com/stats/teamdashboardbygeneralsplits', 
            'onOff':
                'https://stats.wnba.com/stats/teamplayeronoffdetails',
            'onOffSummary':
                'https://stats.wnba.com/stats/teamplayeronoffsummary',
            'yearByYearStats':
                'https://stats.wnba.com/stats/teamyearbyyearstats'
             })
            

class TestTeamObjectMethods(unittest.TestCase):
    '''
    This test set should include tests for each individual Team
    object method. 

    The API server's response object includes a key called
    'resource' which corresponds to the url extension of the
    endpoint called. We'll use this to test that the 
    correct resource was returned. 
    '''
    def setUp(self):
        '''
        set up test environment for all Team object tests
        
        create Team object and set to self.session
        
        For the subclass objects, all methods perform searches, 
        so there is no need to prepopulate the history variables.
        If the history variables aren't working, the Search object 
        tests will fail. 
        '''
        self.session = wnbAPI.Team() 
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
        
    def test_clutch_method(self):
        '''
        test clutch() method
        '''
        self.assertEqual(self.session.clutch()['resource'], 'leaguedashteamclutch') 

    def test_details_method(self):
        '''
        test details() method
        '''
        self.assertEqual(self.session.details()['resource'], 'teamdetails') 

    def test_gamelogs_method(self):
        '''
        test gamelogs() method
        '''
        self.assertEqual(self.session.gamelogs()['resource'], 'gamelogs') 

    def test_lineups_method(self):
        '''
        test lineups method()
        '''
        self.assertEqual(self.session.lineups()['resource'], 'teamdashlineups' ) 

    def test_onoff_method(self):
        '''
        test onOff() method
        '''
        self.assertEqual(self.session.onOff()['resource'], 'teamplayeronoffdetails') 
    
    def test_onoffsummary_method(self):
        '''
        test onOffSummary() method
        '''
        self.assertEqual(self.session.onOffSummary()['resource'], 'teamplayeronoffsummary') 

    def test_players_method(self):
        '''
        test players() method
        '''
        self.assertEqual(self.session.players()['resource'], 'teamplayerdashboard') 

    def test_roster_method(self):
        '''
        test roster() method
        '''
        self.assertEqual(self.session.roster()['resource'], 'commonteamroster') 

    def test_shooting_method(self):
        '''
        test shooting() method
        '''
        self.assertEqual(self.session.shooting()['resource'], 'teamdashboardbyshootingsplits') 

    def test_shotchartdetail_method(self):
        '''
        test shotchartDetail() method
        '''
        self.assertEqual(self.session.shotchartDetail()['resource'], 'shotchartdetail') 

    def test_splits_method(self):
        '''
        test splits() method
        '''
        self.assertEqual(self.session.splits()['resource'], 'teamdashboardbygeneralsplits') 

    def test_yearbyyear_method(self):
        '''
        test yearByYear() method
        '''
        self.assertEqual(self.session.yearByYear()['resource'], 'teamyearbyyearstats') 
