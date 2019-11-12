#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:29:11 2019

@author: Trixie Midnight









Welcome to the jungle, fuckstick



                                              we're going to make you...




                                            ...speak in a considerate \n\
                                                        tone of voice.





This file houses/consolidates the components of this Python WNBA stats
handling convenience application.

It was created because the slim pickings of other WNBA Python Statistics tools 
that I found were all converted from NBA tools, and had insufficient documentation
for easy use. I thought it would be better to have a WNBA tool that was designed
specifically for WNBA. 

The module consists of three main objects, all subclasses of a Search class. 
These are:
    
    Player()
    Team()
    League()
    
Each of these objects has a suite of methods representing the API endpoints
of available data. 

Call paramList to see a list of all tested valid parameter keys and values. 
(call help(Subclass) for further explanation)
    I plan to add individual methods to each subclass to get more specific lists
    as not all params are available for each class.

Passing invalid parameter keys will not harm or affect a search. Passing invalid
values for valid parameters will in many cases prevent a search, 
but not in all cases.

There are two ways to use the search objects. 
   
  1.   Creating a search object. This allows you to track changes in values,
       and stores 'session' history. 
       
       This can be done with or without params. 
       
       Without params:
           
           P = Player()
           T = Team()
           L = League()
           G = Game()
           
      With with params, (conventionally notated as SubclassName(**params)):
          
          P = (Player(PlayerID='203399', Location='Home','PlusMinus'='Y'))
          etc. 
         
          
      Params can be changed or added at any time, either
      by calling P.setParams(**params) or by passing **params as arguments 
      to any of the objects methods. If required params are missing for a
      certain endpoint, they will be filled in with generic defaults. 
      
      To view the generic parameters for the subclass in general, call
      SubclassName.getRequiredParams(). The help(Subclass.method) or docstring 
      for the individual methods specify method-level required params. 
      
      When you call any method, the search parameters and endpoint are stored
      in the session history. If the same method is called with the same params,
      the API call is skipped and the original data is returned. 
      
      You can call P.back() or P.forw() to navigate through the session history.
      
      P.get_pointer() returns the most recent search result (in case you didn't
      save it to a variable). Calling P() also returns the pointer.
      
      P.pointerParams() resets the params to the params that were used for the
      search currently returned by get_pointer(). 
      
      View current params with viewParams. 
      
      Finally, P.dataFrame converts the data currently in the pointer to a 
      pandas DataFrame. Returns a dictionary, where the keys are the names of 
      each result set, and the alues are the pandas DataFrame 
      for the named result set). 
      
  2.   The second way to use these objects is by calling the individual methods. 
       Doing so simply returns the data object that comes in the API response.
       
       This can also be done with or without params, and looks like:
           
           PlayerStats = Player().careerStats(**params)
           or
           PlayerStats = Player().careerStats()
           or
           PlayerStats = Player(**params).careerStats()
            



"""
'''
from Resources import * 
from Team import Team
from League import League
from Player import Player
from Game import Game

########################################################################
####                                                                ####
####                              MAIN                              ####
####                                                                ####
########################################################################
        
def main(*args):

    #if there are arguments, run in test mode.
    if args:
        
        from testboard import teamTest, playerTest, leagueTest
   
        print('\n\n\n\n\n         TESTING BEGIN\n\n\n\n\n\
                                                     READY FOR DIE?????')
        tests = ''
        
        \'''
        endpointSet = endpointTest(endpoints)
        
        for grade in endpointSet:
            tests += str(grade[0]) + grade[1]
             
        print(tests + '\n')     
        print('Passed ' + str(len([x for x in endpointSet if x[0]])) + 
              ' general endpoint tests.' + '\n\n')
        \'''
        print('\n\n\n\n\
                          PLAYER CLASS TEST SET START\n\n\n\n\n\
            YOU CAN NEVER SURVIVE\n\n\n\n\n')
        
        
        playerSet = playerTest()        
        tests = ''
        
        for grade in playerSet:
            tests += grade[1]
        
        print(tests+ '\n')
        print('Passed ' + str(len([x for x in playerSet if x[0]])) + 
              ' Player class endpoint tests.\n\n')
        
        print('\n\n\n\n\
                          NOW DEADLY LEAGUE CLASS TEST SET ATTACK\n\n\n\n\n\
                                                          YOU SURELY ARE DEFEATED!')
        leagueSet = leagueTest()
        
        tests = ''
        
        for grade in leagueSet:
            tests += grade[1]
            
            
        print(tests+'\n')
        print('Passed ' + str(len([x for x in leagueSet if x[0]])) + 
              ' League class endpoint tests.' + '\n\n')        
 
        print('\n\n\n\
                      Hold your horse, coward. I have to watch over my Oven. \n\n\n\n\n\n\n\
                          SURPRISE TEAM CLASS TEST SET START\n\n\n\n\n\
            YOU HAVE MEET DEATH AT HAND')
        
        teamSet = teamTest()
        
        tests = ''
        
        for grade in teamSet:
            tests += grade[1]
            
            
        print(tests+'\n')
        print('Passed ' + str(len([x for x in teamSet if x[0]])) + 
              ' Team class endpoint tests.' + '\n\n')
        
    #if no arguments print this pithy lyric and take us to the house.    
    else:
        print('\n\n\n\nWelcome to the jungle, fuckstick\n\n\n\n  \
                                            we\'re going to make you...\n\n\n\n\n\
                                            ...speak in a considerate\n\
                                                        tone of voice.')
    

'''
from wnbAPI.search import *
from wnbAPI.team import Team
from wnbAPI.league import League
from wnbAPI.game import Game
from wnbAPI.player import Player
