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
####                    player module tests                     ####
####                                                            ####
####################################################################
        
class TestPlayerObjectCreation(unittest.TestCase):
    '''
    This TestCase should include tests to create a Player object. 
       - Player object should initialize with:
           
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
            'Season': currentSeason, # Requires string or integer year.
            'PlayerID': '203399', # 2019 WNBA MVP Elena Delle Donne
                }
           
           self.endpoints = {
                'awards':
                    'https://stats.wnba.com/stats/playerawards',
                'career':
                    'https://stats.wnba.com/stats/playercareerstats', 
                'gamelogs':
                    'https://stats.wnba.com/stats/playergamelogs',
                'shooting':
                    'https://stats.wnba.com/stats/playerdashboardbyshootingsplits',
                'clutch':
                    'https://stats.wnba.com/stats/playerdashboardbyclutch',
                'splits':
                    'https://stats.wnba.com/stats/playerdashboardbygeneralsplits',
                'lastNGames': 
                    'https://stats.wnba.com/stats/playerdashboardbylastngames',
                'opponentSplits':
                    'https://stats.wnba.com/stats/playerdashboardbyopponent',
                'teamPerformance':
                    'https://stats.wnba.com/stats/playerdashboardbyteamperformance',
                'yearOverYear':
                    'https://stats.wnba.com/stats/playerdashboardbyyearoveryear'
                  }
        

    This test set should include tests for each individual Player
    object method. 
    '''
    def setUp(self):
        '''        
        create Player object and set to self.session
        
        '''
        self.session = wnbAPI.Player(Season=2019)
        
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
        
    def test_initial_values(self):
        self.assertEqual(self.session.requiredParams, {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '10', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'Outcome': '', 'OpponentTeamID': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': '', 'Season': '2019', 'PlayerID': '203399'})
        self.assertEqual(self.session.endpoints, {
                'awards':
                    'https://stats.wnba.com/stats/playerawards',
                'career':
                    'https://stats.wnba.com/stats/playercareerstats', 
                'gamelogs':
                    'https://stats.wnba.com/stats/playergamelogs',
                'shooting':
                    'https://stats.wnba.com/stats/playerdashboardbyshootingsplits',
                'clutch':
                    'https://stats.wnba.com/stats/playerdashboardbyclutch',
                'splits':
                    'https://stats.wnba.com/stats/playerdashboardbygeneralsplits',
                'lastNGames': 
                    'https://stats.wnba.com/stats/playerdashboardbylastngames',
                'opponentSplits':
                    'https://stats.wnba.com/stats/playerdashboardbyopponent',
                'teamPerformance':
                    'https://stats.wnba.com/stats/playerdashboardbyteamperformance',
                'yearOverYear':
                    'https://stats.wnba.com/stats/playerdashboardbyyearoveryear'
                  })
            

class TestPlayerObjectMethods(unittest.TestCase):
    '''
    This test set should include tests for each individual Player
    object method. 


    The API server sets a key called 'resource' on the 
    data returned by the majority of these methods. if the 
    url extension stored in the Player object matches the 
    resource string set by the API server, then the method 
    has successfully sent the API server the request
     and returned data. 

    We'll test this rather than the return data, 
    both because the return data is very large and slows 
    the tests, and because this implementation leads to searches
    that are less likely to be broken by updates to the API server
    that don't really break the method. 
    '''
    def setUp(self):
        '''
        set up test environment for all Player object tests
        
        create Player object and set to self.session
        
        For the subclass objects, all methods perform searches, 
        so there is no need to prepopulate the history variables.
        If the history variables aren't working, the Search object 
        tests will fail. 
        '''
        self.session = wnbAPI.Player() 
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
    
    def test_awards_method(self):
        '''
        test awards() method
        '''
        self.assertEqual(self.session.awards()['resource'], 'playerawards') 


    def test_career_method(self):
        '''
        test career() method
        '''
        self.assertEqual(self.session.career()['resource'], 'playercareerstats') 

    def test_clutch_method(self):
        '''
        test clutch() method
        '''
        self.assertEqual(self.session.clutch()['resource'], 'playerdashboardbyclutch') 

    def test_gamelogs_method(self):
        '''
        test gamelogs() method
        '''
        self.assertEqual(self.session.gamelogs()['resource'], 'gamelogs') 

    def test_lastngames_method(self):
        '''
        test lastNGames() method
        '''
        self.assertEqual(self.session.lastNGames()['resource'], 'playerdashboardbylastngames') 

    def test_opponentsplits_method(self):
        '''
        test opponentSplits() method
        '''
        self.assertEqual(self.session.opponentSplits()['resource'], 'playerdashboardbyopponent') 

    def test_shooting_method(self):
        '''
        test shooting() method (it helps to tuck your elbow in)
        '''
        self.assertEqual(self.session.shooting()['resource'], 'playerdashboardbyshootingsplits') 

    def test_shotchartdetail_method(self):
        '''
        test shotchartDetail() method
        '''
        self.assertEqual(self.session.shotchartDetail()['resource'], 'shotchartdetail') 

    def test_splits_method(self):
        '''
        test splits() method
        ''' 
        self.assertEqual(self.session.splits()['resource'], 'playerdashboardbygeneralsplits') 

    def test_teamperformance_method(self):
        '''
        test teamPerformance() method
        ''' 
        self.assertEqual(self.session.teamPerformance()['resource'], 'playerdashboardbyteamperformance') 

    def test_yearoveryear_method(self):
        '''
        test yearOverYear() method
        '''
        self.assertEqual(self.session.yearOverYear()['resource'], 'playerdashboardbyyearoveryear') 

