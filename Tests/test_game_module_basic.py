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
####                     game module tests                      ####
####                                                            ####
####################################################################
class TestGameObjectCreation(unittest.TestCase):
    '''
    This TestCase should include tests to create a Game object. 
       - Game object should initialize with:
           
           self.requiredParams = {'GameID': '1041900405', 'LeagueID': '10'}
           
           self.endpoints = {'scoreboard': 'https://stats.wnba.com/stats/scoreboard', 'scoreboardv2': 'https://stats.wnba.com/stats/scoreboardv2', 'playbyplay': 'https://stats.wnba.com/stats/playbyplay', 'playbyplayv2': 'https://stats.wnba.com/stats/playbyplayv2'}

    '''
    def setUp(self):
        '''
        create Test object and set to self.session
    
        '''
        self.session = wnbAPI.Game()
        
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
        
    def test_initial_values(self):
        self.assertEqual(self.session.requiredParams, {'GameID': '1041900405', 'LeagueID': '10'})
        self.assertEqual(self.session.endpoints, {'scoreboard': 'https://stats.wnba.com/stats/scoreboard', 'scoreboardv2': 'https://stats.wnba.com/stats/scoreboardv2', 'playbyplay': 'https://stats.wnba.com/stats/playbyplay', 'playbyplayv2': 'https://stats.wnba.com/stats/playbyplayv2'})
            

class TestGameObjectMethods(unittest.TestCase):
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
        self.session = wnbAPI.Game() 
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session

        def test_pbp_method(self):
            '''
            test pbp method
            this method uses a different url & does not have
            the resource endpoint. We'll use the gameID
            of the default game to validate the return
            
            '''
            self.assertEqual(self.session.pbp()['g']['gid'], '1041900405')
        
        def test_playbyplay_method(self):
            '''
            test playByPlay method
            '''         
            self.assertEqual(self.session.playByPlay()['resource'], 'playbyplay')
        
        def test_playbyplayv2_method(self):
            '''
            test playByPlayv2 method
            '''
            self.assertEqual(self.session.playByPlayv2()['resource'], 'playbyplay')
        def test_scoreboard_method(self):
            '''
            test scoreboard method
            '''
            self.assertEqual(self.session.scoreboard()['resource'], 'scoreboard')
        def test_scoreboardv2_method(self):
            '''
            test scoreboardv2 method
            '''
            self.assertEqual(self.session.scoreboardv2()['resource'], 'scoreboardV2')
 
    def test_shotchartdetail_method(self):
            '''
            test shotchartDetail method
            '''
            self.assertEqual(self.session.shotchartDetail()['resource'], 'shotchartdetail')