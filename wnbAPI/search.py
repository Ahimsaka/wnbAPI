#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:32:31 2019

########################################################################
####                                                                ####
####                        search module                           ####
####                                                                ####
########################################################################

This module holds the base Search class on which the search subclasses
are built, and also contains a handful of convenience methods. 

    The Search object is the core of this package. It is essentially
    an extended wrapper for a standard API request using the Python 
    builtin requests.Session() object. Parameter permutations are the 
    largest obstacle to accessing the stats.wnba.com/ api, so the Search
    object is primarily a parameter handler. 
    
    Features include:
        - Parameter memory, including stored results to prevent multiple 
        API requests to the same endpoint with identicle headers. 
        - Memory navigation to quickly see results from previous searches
        - Set parameters and view current parameters
        - Set the returned data to a pandas Dataframe 
        
    While the search class is not intended for independent usage, it is 
    technically possible to do so, and could be used to handle parameters
    for queries to any API that is willing to accept the headers 
    (which are stored in the resources module and can't be changed inside 
    the search object). In any case, all methods of the Search object are 
    available to instances of all subclass objects and have identical 
    function for each. 
    
    A Search object (or any subclass) can be intialized with or without 
    parameters, passed in as either keyword arguments or a **dict
    
          s = Search()
          
          or
          
          s = Search(TeamID=111111, Season=2018)
          
          or
          
          params = {'TeamID': 11111, 'Season': 2018}
          
          s = Search(**params)
          
    In all cases, the Search object intializes successfully, but the pointer
    initializes to an empty dictionary. To perform a search requires using the 
    Search object's search method, which we'll come to later. 
    
    s.__call__(), s(), and s.getPointer() all return the data currently in
    the 'pointer', stored as s.pointer, which holds the return of the most
    recent search (and initializes as an empty dict).
    
    s.setParams(**params) sets new param values for the object. 
    
    s.getParams() shows the current param values
    
    s.getRequiredParams() returns the default required params for the object.
       - For the Search() class, this is an empty dictionary. 
       - Each of the subclasses have their own set of generic required 
       parameters representing sensible defaults for all parameter keys that 
       are required for the endpoint to return data. 
    
    s.search(endpoint, requiredParams, params) is the core search function. 
        - the endpoint argument is required, and consists of the full URL 
        for the desired endpoint, in string form. The subclasses each 
        store those urls in dictionaries accessed by the methods. 
        - requiredParams is an optional dictionary argument describing 
        default values for the parameters that are required to 
        make the endpoint work. 
        - params is an optional dictionary argument describing requested 
        parameters for the search. If no params argument is supplied, the 
        search will use a combination of the Search object instance's params
        and the requiredParams argument (with s.params recieving priority for
        any key that appears in both dictionaries).
        - s.search returns the data object created by calling the .json() 
        method of the response object sent by the server. 
        
    s.back() and s.forw() are used to move the pointer through the search
    history. 
    
    s.pointerParams() retrieves the parameters which were used to generate
    the data currently showing in the pointer. 
        - Call s.setParams(s.pointerParams()) to easily reset the 
        parameters to the values used in any previous search. 
    
    s.dataFrame() returns a pandas dataFrame describing the object currently
    in the pointer. 
        - This dataFrame is not stored and should always be set to a
        variable for further processing. 
    
    s.shotChartDetail() is a special method. It is currently the only
    endpoint method that is used by all subclasses, so it lives here
    on the superclass. 
      
Outside of the Search object, this holds the following methods. These methods
are separated from the core Search object because they do not require
parameters: 
    logo() - to retrieve an svg of the wnba logo.
    logo2() - to retrieve an svg of the secondary wnba logo. 
    teamLogo() - to retrieve an svg of a wnba team's logo (which requires 
                 the team's TeamID as an argument)
    schedule() - to retrieve a team's season schedule (which requires 
                 the team's TeamID as an argument)
    
Additonally, 3 items of interest which are imported to this module from the 
Resources module can be called directly: 
    - headers - which shows the default headers for the package
    - teams - which shows a dict of wnba teams keyed by their unique TeamIDs
              with basic information for each team
    - param_list - which is a dictionary containing a working list of ALL known 
    wnba stats parameters and known acceptable values or types of values for 
    each. If you're not sure what values a parameter accepts, you can call 
    print(param_list['Parameter']) to quickly see a list of known options. 
    This is important, because, although unknown parameters do not break these
    endpoints in any of the cases tested so far, unknown values submitted for
    acceptable parameters break the overwhelming majority of them. 
    
"""
DEBUG = False # set Debug to true and searches will return response objects
              # instead of json. 

import numpy as np         # import numpy as pandas pre-req
import pandas as pd        # import pandas to look at data 
from datetime import date  # import date to access current year in schedule()
import requests            # import requests to make requests

# Import default headers, basic team info, currentSeason value, 
# and list of all possible parameters. 
from .resources import *
     

class Search(object):
    '''
    While the search class is not intended for independent usage, it is 
    technically possible to do so, and could be used to handle parameters
    for queries to any API that is willing to accept the headers 
    (which are stored in the resources module and can't be changed inside 
    the search object). In any case, all methods of the Search object are 
    available to instances of all subclass objects and have identical 
    function for each. 
    
    
    
    '''
    def __init__(self, **params):
        '''
        A Search object (or any subclass) can be intialized with or without 
        parameters, passed in as either keyword arguments or a **dict
    
          s = Search()
          
          or
          
          s = Search(TeamID=111111, Season=2018)
          
          or
          
          params = {'TeamID': 11111, 'Season': 2018}
          
          s = Search(**params)
          
        In each case, the Search object intializes successfully, but the pointer
        initializes to an empty dictionary. To perform a search requires using the 
        Search object's search method, which we'll come to later. 
        '''
        # Set up history functionality: 
        self.history = [] # store endpoint/param in history to reduce API calls
        self.index = 0    # track index of history for back and forward funcs
        self.data = {}    # store search data 
        self.pointer = {} # hold the "current" data set
    
        self.params = {}  # intialize params to empty dictionary to explicitly
                          # declare type
                          
        self.required_params = {} # initialize requiredParams to empty dictionary
                                  # to explicitly declare type. 
       # Though 3 of the subclasses have large numbers of common required 
       # params,  the current implementation is to explicitly declare all 
       # required params at the class level rather than inheriting
       # common values. I believe this will make it easier to add
       # possible future subclasses, and makes it easier to determine
       # what parameter values will be passed to search from each method. 
        
        # if object was initialized with params argument, set the params. 
        if params:
            self.setParams(params)
            
    def __call__(self):
        '''
        Calling the Search object returns the current data pointer, and is
        convenient for use in the console. 
        '''
        return self.pointer
    
    def getPointer(self):
        '''
        s.getPointer() is redundant with s(), but I believe it's a prudent 
        redundancy. While s() is convenient for use in the console,
        s.getPointer() is more explicit and better practice for use in any
        extending code
        '''
        return self.pointer
        
    def setParams(self, params):
        '''
        simple method to change the parameters. accepts dictionary
        
        s.setParams() *only* changes the values of the keys in the argument
        dictionary. Params from a prior search which are not included in the 
        new dictionary will remain set their existing values. 
        '''
        self.prevParams = self.params
        self.params.update(params)
        
    def getRequiredParams(self):
        '''
        returns required_params for class
        '''
        return self.required_params
    
    def getParams(self):
        '''
        returns list of all known parameter keys and accepted values for
        stats.wnba.com
        '''
        return param_list
        
    def search(self, endpoint, required_params, params):
        '''
        univeral method attempts to GET the selected URL with the params
        currently stored in self.params as the parameter values.
        
        If a params argument is included, self.params is updated before the
        request is sent.
        
        raises error if unable to connect after 5 tries. 
        
        For all endpoints tested so far, the data returned by this
        method is a dictionary with the keys {'resource', 'parameters',
        and 'resultSet' or 'resultSets' depending on number of datasets}
        
            - 'resultSet' is a dictionary with keys {'name','headers', 'rowSet'} 
                - 'name' is a string labeling the resultSet
                - 'headers' is a list of strings: the column headers for the 
                   data
                - 'rowSets' is a list of lists, where each sublist is a row
                   of data (strings, floats, int) with indices that correspond 
                   to columns and to the indices of the appropriate labels 
                   in 'headers' 
            - 'resultSets' is a list of dictionaries each composed in the same 
               manner as 'resultSet'. 

           - in all endpoints tested so far the key 'rowSet' has not varied 
            
        '''
        # if parameter argument is submitted, updated the params
        if params:
            self.setParams(params)
        
        # initialize an empty dictionary to collect parameters for this search
        params = {}
        
        # first fill the empty dictionary with all required parameter values. 
        if required_params:
            params.update(required_params)
            
        # update the dictionary with all values from self.params and
        # overide any required_params if the same key exists in both sources
        params.update(self.params)
        
        # assign endpoint/parameter combination to history array
        self.history.append((endpoint, str(params)))
        # this may result in the same endpoint/parameter combination being
        # included in the array multiple times. This is intentional. If a
        # search is repeated, the user should see that search at both positions
        # in their history scroll. The data is separated to avoid storing
        # that more than once, the end endpoint/params tuple is used as the 
        # key of that storage dict. 
        
        # store the current index -- this doesn't use self.index += 1 because
        # the user may have navigated through their search history. The new
        # search should still sit at the end of the list, and the current index
        # should reflect that. 
        self.index = len(self.history)-1
        
        # check if endpooint/parameter combination has been requested during this session
        if (endpoint, str(params)) in self.history[:-1]:                        
            # if the search has already been used, return the result of the
            # previous search. 
            return self.data[endpoint][str(params)][1]
        
    
        s = requests.Session()  # initialize requests.Session
        s.headers = headers     # set headers
        s.params = params       # set params
        
        # Set up error handling for the upcoming API request. 
        # These features only became necessary when I was testing the object
        # and repeated searches started to cause failures that weren't 
        # related to the program itself. 
        errors = []       # Initialize list to collect request errors 
                          # if multiple tries are needed. 
        retry_flag = 0    # set flag to count number of retries

        
        while True:                                      # open loop
            try:                                         # handle exceptions
                data = s.get(endpoint, timeout=(4,100))  # attempt request 
            except (requests.exceptions.Timeout,         
                    requests.exceptions.TooManyRedirects, # for all exceptions
                    requests.exceptions.RequestException) as e: 
                retry_flag += 1                           # increment flag
                errors.append({endpoint: e})              # store the error
                
                if retry_flag == 5:                      # if we hit 5, give up
                    print(errors)
                    raise e
                
            else: # if we get through the try statement without an error 
                  # store the data in history
                if not self.data.get(endpoint,False):
                    self.data[endpoint] = {}
                
                if not DEBUG:
                    self.data[endpoint][str(params)] = (params, data.json())
                    # set the new pointer
                    self.pointer = data.json()
                    # and return the data
                    return data.json()
                if DEBUG:
                     self.data[endpoint][str(params)] = (params, data)
                     self.pointer = data
                     return data
            
    def back(self):
        '''
        moves pointer back one search in history. if the current search was
        first in the session, moves to the most recent search. 
        '''
        self.index -= 1
        if self.index < 0:
            self.index = len(self.history)-1
            
        newPointer = self.history[self.index]
        self.pointer = self.data[newPointer[0]][newPointer[1]][1]        
        return self.pointer
    
    def forw(self):
        '''
        moves pointer to the next search in history. if current search
        is the most recent, moves to the first search of session. 
        '''
        self.index += 1
        if self.index > len(self.history) -1:
            self.index = 0
            
        newPointer = self.history[self.index]
        self.pointer = self.data[newPointer[0]][newPointer[1]][1]
        return self.pointer
    
    def pointerParams(self):
        '''
        Restores the paramaters that were set for the search that is 
        currently displayed in self.pointer
        '''
        self.params = self.data[self.history[self.index][0]][self.history[self.index][1]][0]
        
    def dataFrame(self):
        '''
        sets the dataset in the pointer to a pandas dataframe
        
        So far all endpoints investigated have the same basic structure
        and so this function works universally. This may not 
        always be the case if endpoints are changed or added. 
        
        This is purely a convenience method and does not constitute a 
        suggestions that a pandas dataframe will be the best way to process
        or review the data returned by a search. 
        '''
        # check if there is data in the pointer
        if not self.pointer:
            return 'No search recorded.'
        
        if self.pointer.get('resultSet', False): # check for singular variation
            data = self.pointer['resultSet']     # get the data from the pointer
                                                 # then make the data frame.  
            df = {data['name']: pd.DataFrame(data['rowSet'], columns=data['headers'])}
        elif self.pointer.get('resultSets', False): # else look for plural
            data = self.pointer['resultSets']       # retrieve data
            tables = {}                             # intialize empty dictionary
            for table in data:                      # loop through the data
                tables[table['name']] = pd.DataFrame(table['rowSet'],\
                      columns=table['headers'])  # fill the dictionary, use 
                                                 # resultSet's as key, df as value 
           # after the loop, return the full dictionary. 
            df = tables 
        else: # if we don't find resultSets or resultSet, but the pointer 
              # wasn't empty, we don't want to raise an error. just inform
              # the user that the method couldn't find the search results. 
            return 'Unable to find search results.'
        return df
    
    def shotChartDetail(self, **params):
        '''
        Method added 11/1 for shotChartDetail endpoint
        
        ** This is the only endpoint hosted on the
        team superclass. Because it accepts PlayerID,
        TeamID, and GameID parameters, but also accepts
        '0' or '' as values to indicate 'all' for each of these 
        parameters, it can be accessed in a manner 
        relevant to any of the subclasses and so
        is housed on the superclass. 
        
        uses 'shotchartDetail':
                'https://stats.wnba.com/stats/shotchartdetail',
            
        PARAMS UNTESTED
        
        TABLES AND HEADERS: 
            'Shot_Chart_Detail'
                'GRID_TYPE', 'GAME_ID', 'GAME_EVENT_ID', 
                'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 
                'TEAM_NAME', 'PERIOD', 'MINUTES_REMAINING', 
                'SECONDS_REMAINING', 'EVENT_TYPE', 'ACTION_TYPE',
                'SHOT_TYPE', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 
                'SHOT_ZONE_RANGE', 'SHOT_DISTANCE', 'LOC_X', 
                'LOC_Y', 'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG', 
                'GAME_DATE', 'HTM', 'VTM', 
            
            'LeagueAverages'
                'GRID_TYPE', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 
                'SHOT_ZONE_RANGE', 'FGA', 'FGM', 
                'FG_PCT', 
        '''
        
        # initialize empty dictionary
        requiredParams = {}
        # fill it with object's default required params
        requiredParams.update(self.requiredParams)
        # insert additional defaults
        requiredParams.update({'PlayerID': 0,
                               'RookieYear': '',
                               'ContextMeasure': 'PTS',
                               'GameID': '',
                               'PlayerPosition': '',
                               'TeamID': '0'
                               })
        # run the search    
        return self.search('https://stats.wnba.com/stats/shotchartdetail', requiredParams, params)


########################################################################
####                                                                ####
####               SCHEDULES AND LOGO SVG IMAGES                    ####
####                                                                ####
########################################################################


def logo():
    '''
    method to get main wnba loga as svg
    
    sends a normal get request to a static url. 
    
    url: 'https://stats.wnba.com/media/img/league/wnba-logo.svg'
    
    included because the author of this package may use it for the 
    sport-stats blog project that inspired the package. 
    '''
    
    s = requests.Session()
    
    s.headers = headers
        
    return s.get('https://stats.wnba.com/media/img/league/wnba-logo.svg')
        
def logo2():
    '''
    method to get secondary wnba loga as svg
    
    sends a normal get request to a static url:
    
    url 'https://stats.wnba.com/media/img/league/wnba-secondary-logo.svg'
    
    included because the author of this package may use it for the 
    sport-stats blog project that inspired the package. 

    '''
   
    s = requests.Session()
    
    s.headers = headers

    return s.get('https://stats.wnba.com/media/img/league/wnba-secondary-logo.svg')
    
def nbaLogo():
    '''
    method to get nba loga as svg
    
    sends a normal get request to a static url:
    
    url'https://stats.wnba.com/media/img/league/nba-logoman.svg'
            
    
    included for possible NBA extension in which cause author may use it 
    for sports blog related etc. etc. etc. 
    '''
 
    s = requests.Session()
    
    s.headers = headers
   
    return s.get('https://stats.wnba.com/media/img/league/nba-logoman.svg')  

    
def teamLogo(TeamID='1611661321'):
        '''
        method to pull team logo as .svg
        
        sends normal get request to static url format
        
       
        url format: 'https://stats.wnba.com/media/img/teams/logos/' +\
                    shortCode + '.svg'
                    
        shortcode is the three letter abbreviation for a team's name. 
        these are stored in the subdictionary of the dictionary teams 
        from the resources module, accessible as: 
            teams[TeamID]['ta']
            
        '''
    
        s = requests.Session()
        
        s.headers = headers
            
        shortCode = teams[TeamID]['ta']
       
        return s.get('https://stats.wnba.com/media/img/teams/logos/' + shortCode + '.svg')


def schedule(TeamID='1611661324', Season=currentSeason):
    '''
    method to get team schedule
    
    sends normal get request to url to retrieve a data object containing a 
    team's season schedule. 
    
    accepts "Season" kwarg, which defaults to the currentSeason variable set
    at the top of this file. 
    
    url: 'https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/' + 
              str(Season) + '/teams/' + teamName + '_schedule.json')
    '''
    s = requests.Session()
    
    s.headers = headers
    
    teamName = teams[TeamID]['tn'].lower() #retrieve team shortCode 
        
    return s.get('https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/' + 
              str(Season) + '/teams/' + teamName + '_schedule.json')
                 

        
def __main__():
    print('Search superclass locked and loaded, ma\'am.') # Thank'ya doll. 
    