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
####                   league module tests                      ####
####                                                            ####
####################################################################
class TestLeagueObjectCreation(unittest.TestCase):
    '''
    This TestCase should include tests to create a League object. 
       - League object should initialize with:
           
           self.requiredParams =         {
                'DateFrom': '',    # Required but empty string accepted
                'DateTo':'',       # Required but empty string accepted
                'GameSegment': '', # Required but empty string accepted
                'LastNGames':'0',  # 0 stands for all games
                'LeagueID':'10',   # 10 is WNBA. 00 is NBA and 30 is G-League 
                'Location':'',     # Required but empty string accepted
                'MeasureType': 'Base',#Required and needs string. 
                'Month':'0',       # 0 stands for all months 
                'Outcome':'',      # Required but empty string accepted
                'OpponentTeamID': '0',# 0 stands for all opponents
                'PaceAdjust':'N',  # Requires Y or N 
                'PerMode': 'PerGame',# Requires string input
                'Period': '0',     # 0 stands for all periods
                'PlusMinus':'N',   # Requires Y or N
                'Rank': 'N',       # Requires Y or N
                'SeasonSegment':'',# Required but empty string accepted
                'SeasonType':'Regular Season', # Requires string input
                'VsConference': '',# Required but empty string accepted 
                'VsDivision':'',   # Required but empty string accepted
                'Season': currentSeason, # Requires string or integer year.
                'GameScope': '',   # Required but empty string accepted
                'PlayerExperience': '',# Required but empty string accepted
                'PlayerPosition': '',# Required but empty string accepted
                'StarterBench':''  # Required but empty string accepted
                }   
           
           self.endpoints =  {
                'players': 
                    'https://stats.wnba.com/stats/leaguedashplayerstats',
                'standings':
                    'https://stats.wnba.com/stats/leaguestandingsv3',
                'teams':
                    'https://stats.wnba.com/stats/leaguedashteamstats',
                'shotLocations':
                    'https://stats.wnba.com/stats/leaguedashteamshotlocations',
                'statLeaders':
                    'https://stats.wnba.com/stats/leagueLeaders',
                'alltimeLeaders':
                    'https://stats.wnba.com/stats/alltimeleadersgrids',
                'lineups':
                    'https://stats.wnba.com/stats/leaguedashlineups'
                }
    '''
    def setUp(self):
        '''
        create Test object and set to self.session
    
        '''
        self.session = wnbAPI.League()
        
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
        
    def test_initial_values(self):
        self.assertEqual(self.session.requiredParams, {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '10', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'Outcome': '', 'OpponentTeamID': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': '', 'Season': '2019', 'GameScope': '', 'PlayerExperience': '', 'PlayerPosition': '', 'StarterBench': ''})
        self.assertEqual(self.session.endpoints,{'players': 'https://stats.wnba.com/stats/leaguedashplayerstats', 'standings': 'https://stats.wnba.com/stats/leaguestandingsv3', 'teams': 'https://stats.wnba.com/stats/leaguedashteamstats', 'shotLocations': 'https://stats.wnba.com/stats/leaguedashteamshotlocations', 'statLeaders': 'https://stats.wnba.com/stats/leagueLeaders', 'alltimeLeaders': 'https://stats.wnba.com/stats/alltimeleadersgrids', 'lineups': 'https://stats.wnba.com/stats/leaguedashlineups'})
            

class TestLeagueObjectMethods(unittest.TestCase):
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
        self.session = wnbAPI.League() 
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session

        def test_alltimeleaders_method(self):
            '''
            test alltimeLeaders() method
            '''
            self.assertEqual(self.session.alltimeLeaders()['resource'], 'alltimeleadersgrids')

        def test_lineups_method(self):
            '''
            test lineups() method
            '''
            self.assertEqual(self.session.lineups()['resource'], 'leaguedashlineups')
        def test_players_method(self):
            '''
            test players() method
            '''
            self.assertEqual(self.session.players()['resource'], 'leaguedashplayerstats')
        def test_shotlocations_method(self):
            '''
            test shotLocations() method
            '''
            self.assertEqual(self.session.shotLocations()['resource'], 'leaguedashteamshotlocations')

        def test_shotchartdetail_method(self):
            '''
            test shotchartDetail() method
            '''
            self.assertEqual(self.session.shotchartDetail()['resource'], 'shotchartdetail')
        def test_standings_method(self):
            '''
            test standings() method
            '''
            self.assertEqual(self.session.shotchartDetail()['resource'], 'shotchartdetail')

        def test_statleaders_method(self):
            '''
            test statLeaders() method
            '''
            self.assertEqual(self.session.statLeaders()['resource'], 'leagueleaders')
        def test_teams_method(self):
            '''
            test teams() method
            '''    
            self.assertEqual(self.session.teams()['resource'], 'leaguedashteamstats')
            