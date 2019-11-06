#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:42:02 2019

    ####################################################################
    ####                                                            ####
    ####   (married to the)     game module                         ####
    ####                                                            ####
    ####################################################################
    
This module houses the Search subclass Game.

Like Search, a Game object can be created with or without parameters:
    
    g = Game()

    or

    g = Game(GameID='1041900405', LeagueID=10...etc...)

    or
    
    params = {'GameID'='1041900405', LeagueID'='10'...etc...}
    g = Game(**params)
    
Perform a search by calling any Game class method, with or without params. 

Game's methods may also be used without creating a League object:
    
    Game().method(**params)
    
If no parameters are passed, default parameters are used and data 
is returned relevant to the series-clinching 5th Game of the 2019 
WNBA Finals.

For information on the search history capabilities inherited from the Search 
method, please see the search module documentation. 
"""

from wnbAPI.search import Search, currentSeason, requests, headers, DEBUG

class Game(Search):
    '''
    Extends Search class with methods to access endpoints for Game data. 
    
    Game Methods:
        pbp() *** Does not use core search method
            http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2019/scores/pbp/1041900405_1_pbp.json
        scoreboard()
            https://stats.wnba.com/stats/scoreboard
        scoreboardv2()
            https://stats.wnba.com/stats/scoreboardv2
        playbyplay()
            https://stats.wnba.com/stats/playbyplay
        uses: playbyplayv2()
            https://stats.wnba.com/stats/playbyplayv2
    
    Game default required params: 
        requiredParams = {
                'GameID': '1041900405',# requires int or string GameID
                'LeagueID': '10'    # 10 is WNBA. 00 is NBA and 30 is G-League 
                }
        
    '''
    def __init__(self, **params):
        Search.__init__(self, **params)
        # create dictionary of the endpoints assigned to each method. 
        # these could also have been stored inside each method. 
        # and that might have been a better choice, but I like
        # having a list of the accessible endpoints built into the
        # object. 
        self.endpoints = {
                'scoreboard': 
                    'https://stats.wnba.com/stats/scoreboard',
                'scoreboardv2':
                    'https://stats.wnba.com/stats/scoreboardv2',
                'playbyplay':'https://stats.wnba.com/stats/playbyplay',
                'playbyplayv2':'https://stats.wnba.com/stats/playbyplayv2',
                }
            
        # set default required Parameters. These parameters are required for the 
        # majority of the methods in the class. When not required, can 
        # be overridden at the method level. But most of these params
        # can be passed without affecting return for the methods where they
        # are not required.         

        self.requiredParams = {
                'GameID': '1041900405',
                'LeagueID': '10'
                }
        
    def pbp(self, **params):
        '''
        Does not use core search method but is the most detailed play by 
        play data, and is the only dataset currently known to me that 
        provides the locations of plays on the court. 
        
        uses:
            http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2019/scores/pbp/1041900405_1_pbp.json
       
        AFFECTED ONLY BY GameID, Period, and Season. 
        
        Unlike the other endpoints it affects, the Period parameter
        for this endpoint requires the string 'full' rather than an 
        empty string to query data for the entire game. 
                      
        **** THIS ENDPOINT RETURNS A COMPLETELY DIFFERENT FORMAT THAN    ****
        **** ANY OTHER ENDPOINT IN THE PACKAGE, BUT IS INDISPENSABLE     ****
        **** BECAUSE OF THE UNIQUE INFORMATION IT INCLUDES. NO CHANGE TO ****
        **** DATAFRAME HAS BEEN MADE TO ACCOMMODATE THE FORMATTING       ****
        **** OF THESE RESULTS. UNTIL THAT IS FIXED THIS METHOD SHOULD NOT****
        **** BE USED IN CONJUNCTION WITH THE DATAFRAME METHOD            ****
        
        SAMPLE DATA STRUCTURE:
            if 'full'
            {'g':
                { 'mid': integer. not sure of meaning.,
                  'gid': string of numbers representing unique GameID,
                  'gcode': string made of 8 digit date + / + away team abbrev. 
                           + home team abbrev. i.e. '20191010/CONWAS',
                  'next': in theory returns URL string for pbp endpoint of the 
                          next game (chronologically) of the WNBA season. 
                          Unfortunately, and HIGHLY disappointingly, this
                          uses an inherited system from the NBA's version 
                          of the same endpoint and does NOT return a functional
                          URL for WNBA games
                  'pd': a list of periods dictionaries, each representing
                        one period of the game. 
                        [{'p': period number as int,
                          'pla': a chronological list of dicts, each 
                                 representing a play or game event, for 
                                 all plays recorded during the period
                                 [{'evt': int representing # of events 
                                          in the game up to present, meaning 
                                          that evt 30 is the 30th event. 
                                          Does not always increment by one,
                                          which may be caused missing plays
                                          but as yet no other evidence of
                                          missing plays has been found. 
                                   'cl': MM:SS - string representing time 
                                                 remaining in period when 
                                                 the event occurred,
                                   'de': Short string description of event,
                                   'locX': Int between -250 and 250. This int 
                                           describes the x value of a coordinate
                                           on half-court grid, where -250 and
                                           250 represent the side-lines, 0 
                                           represents the center of the court
                                           and 10 units is equivalent to 1 foot
                                   'locY': Int between -40 and 860, OR -80. 
                                           locY describes the locations of the
                                           event between the two baselines, 
                                           where 0 represents the defense's
                                           basket, -40 represents the baseline
                                           below that basket, 860 represents 
                                           the opposite baseline, and 10 units
                                           is equivalent to 1 foot. -80 is a 
                                           standard value for events which 
                                           do not necessarily have a location
                                           on the court, such as timeout calls
                                           or player substitutions.
                                           All events with locY -80 have a locX
                                           of 0, and should be confidently omitted
                                           from any charts created using these
                                           coordinates.
                                           ********BIG NOTE**********
                                           locY is ALWAYS relative to the 
                                           defensive teams basket, meaning
                                           that mosts are plotted on
                                           the same half-court grid. The only
                                           events with locY values over 430
                                           (which represents the half-court
                                           line) are those that occur in the
                                           backcourt, such as backcourt
                                           fouls & turnovers, fullcourt heaves,
                                           etc. The data seems designed to 
                                           work mostcomfortably with half-court
                                           charts, like those made by tha legend
                                           Kirk Goldsberry (if you're 
                                           unfamiliar with Mr. Goldsberry's 
                                           work, you have no business trying
                                           to use this package. Shame. Shame).
                                   'opt1': int. unknown meaning. defaults to 0 
                                   'opt2': int. unknown meaning. defaults to 0
                                   'mtype':int. unknown meaning. defaults to 0,
                                   'etype': int code describing the type of
                                            event. Known values:
                                                1 is a made shot, 
                                                2 is a missed shot,
                                                3 is a free throw 
                                                       (made or missed),
                                                4 is a rebound,
                                                5 is a turnover,
                                                6 is a personal foul,
                                                7 is a team penalty,
                                                8 is a substition,
                                                9 is a team timeout,
                                                13 is the end of a period
                                            if an event fits two etypes, 
                                            such as a turnover caused by
                                            an offensive foul, it is listed
                                            twice, with a separate 'evt' value
                                            for each entry. 
                                   'opid': '' or int representing player id of 
                                           the opposing player (ie the defender
                                           on a jump shot). If no opposing 
                                           player was recorded, ''. 
                                   'tid': int representing the TeamID of the
                                          primary team in the event (the 
                                          offensive team on a shot, the 
                                          team calling timeout on a timeout). 
                                          Lists 0 if the event is not specific
                                          to either team
                                   'pid': int representing the PlayerID of the
                                          primary player in the event (shooter, 
                                          rebounder, player committing foul)
                                          Lists 0 if the event is not specific
                                          to any player,                                   
                                   'hs': int score of the home team at the time
                                         of the event,
                                   'vs': int score of the visiting team at the
                                         time of the event,
                                   'epid': int representing the PlayerID of 
                                           a secondary player involved in 
                                           the event (such as the player
                                           who assisted on a made shot)
                                           Lists '' if no secondary player
                                           was credited on the play,
                                   'oftid': int representing the TeamID of the 
                                            team that was on offense at the 
                                            time of the event. For all shots, 
                                            the 'oftid' value will match the 
                                            'tid' value,
                                   'ord': int with length between 5 and 7. 
                                          the leftmost 3 digits seem to 
                                          correspond with 'evt', but are 
                                          usually slightly lower. These may 
                                          represent # of possessions in the 
                                          game. The 4 rightmost digits are
                                          almost always 0000. Observed 
                                          exceptions so far have always 
                                          incremented the prior event's 'ord' 
                                          value by 1, leaving the leftmost 
                                          digits unchanged. This may represent
                                          possessions with multiple distinct
                                          actions, such as multiple offensive
                                          rebounds. 
                                   }
                                 ]

                            }
                        ]
                }
            }
                    
            if a specific period is selected:
            {'g':
                { 'mid': integer. not sure of meaning.,
                  'gid': string of numbers representing unique GameID,
                  'gcode': string made of 8 digit date + / + away team abbrev. 
                           + home team abbrev. i.e. '20191010/CONWAS',
                  'p' : period number as int                  
                  'next': in theory returns URL string for pbp endpoint of the 
                          next game (chronologically) of the WNBA season. 
                          Unfortunately, and HIGHLY disappointingly, this
                          uses an inherited system from the NBA's version 
                          of the same endpoint and does NOT return a functional
                          URL for WNBA games
                  'pla': [Array of events with identical format to the 'pla'
                          array described in the full-game dataset above]
                }
            }
        
        '''
        # Since this method doesn't use the core search method, 
        # set input parameters to self.params now
        # instead of passing them to 

        if params:
            self.setParams(params)
        
        # Set accepted params for this method to strings to use
        # in URL string. 
        gameID = self.params.get('GameID','1041900405')
        season = self.params.get('Season', currentSeason)
        period = self.params.get('Period', 'full')
                
        # For most endpoints, period accepts '' to mean fullgame
        # But this endpoint is different, so if self.params
        # shows Period: '', cchange it to 'full'. 
        if period == '':         
            period = 'full'
        
        # create requests Session object and set the default headers,
        # which are borrowed from the search module. 
        s = requests.Session() # use requests from search to save import
        s.headers = headers
                
        # check the DEBUG flag in the search module
        # if the flag is set to True, send get request and 
        # return the full response object
        if DEBUG == True:
            return s.get('http://data.wnba.com/data/5s/v2015/json/mobile_teams/' \
                         'wnba/' + season + '/scores/pbp/' + gameID + '_' 
                         + period + '_pbp.json')
        # otherwise, send Get request to the URL and return data object
        # generated by calling the json() method on the response object
        return s.get('http://data.wnba.com/data/5s/v2015/json/mobile_teams/' \
                     'wnba/' + season + '/scores/pbp/' + gameID + '_' 
                     + period + '_pbp.json').json()
        # For the get requests above, I debated using Python's String.format() 
        # method to form the URL string because it is the current standard
        # for string substitution. In this case, because the inserted 
        # strings are already set to descriptive variables, I feel that 
        # plus-sign concatenation is the most readable implementation.     
                
    def scoreboard(self, **params):
        '''
        method to access scoreboard
        
        uses: 'scoreboard':
            'https://stats.wnba.com/stats/scoreboard'
        
        AFFECTED BY:
            GameID, LeagueID, DayOffset, 
            GameDate 
            
        DayOffset and GameDate have not been added to param_list yet. 
        These two params are used to specify a date or range of dates
        from which to pull scoreboard data. 
            GameDate is a string in the format "MM/DD/YYYY"
            DayOffset requires an Int of days before or after 
                              GameDate from which to include data
                              
        FULL PARAMS LIST NOT TESTED FOR THIS METHOD
        
        SAMPLE TABLES AND HEADERS:
            'GameHeader'
                'GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 
                'GAME_STATUS_ID', 'GAME_STATUS_TEXT', 'GAMECODE', 
                'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON', 
                'LIVE_PERIOD', 'LIVE_PC_TIME', 'NATL_TV_BROADCASTER_ABBREVIATION', 
                'LIVE_PERIOD_TIME_BCAST', 'WH_STATUS', 

            'LineScore'
                'GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY_NAME', 
                'TEAM_WINS_LOSSES', 'PTS_QTR1', 'PTS_QTR2', 
                'PTS_QTR3', 'PTS_QTR4', 'PTS_OT1', 
                'PTS_OT2', 'PTS_OT3', 'PTS_OT4', 
                'PTS_OT5', 'PTS_OT6', 'PTS_OT7', 
                'PTS_OT8', 'PTS_OT9', 'PTS_OT10', 
                'PTS', 'FG_PCT', 'FT_PCT', 
                'FG3_PCT', 'AST', 'REB', 
                'TOV', 

            'SeriesStandings'
                'GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 
                'GAME_DATE_EST', 'HOME_TEAM_WINS', 'HOME_TEAM_LOSSES', 
                'SERIES_LEADER', 

            'LastMeeting'
                'GAME_ID', 'LAST_GAME_ID', 'LAST_GAME_DATE_EST', 
                'LAST_GAME_HOME_TEAM_ID', 'LAST_GAME_HOME_TEAM_CITY', 'LAST_GAME_HOME_TEAM_NAME', 
                'LAST_GAME_HOME_TEAM_ABBREVIATION', 'LAST_GAME_HOME_TEAM_POINTS', 'LAST_GAME_VISITOR_TEAM_ID', 
                'LAST_GAME_VISITOR_TEAM_CITY', 'LAST_GAME_VISITOR_TEAM_NAME', 'LAST_GAME_VISITOR_TEAM_CITY1', 
                'LAST_GAME_VISITOR_TEAM_POINTS', 

            'EastConfStandingsByDay'
                'TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 
                'STANDINGSDATE', 'CONFERENCE', 'TEAM', 
                'G', 'W', 'L', 
                'W_PCT', 'HOME_RECORD', 'ROAD_RECORD', 


            'WestConfStandingsByDay'
                'TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 
                'STANDINGSDATE', 'CONFERENCE', 'TEAM', 
                'G', 'W', 'L', 
                'W_PCT', 'HOME_RECORD', 'ROAD_RECORD', 


            'CenterConfStandingsByDay'
                'GAME_ID', 'PT_AVAILABLE', 

            'Available'
                 -- all scoreboard searches tested to date have
                    returned an empty headers array and empty 
                    rowSet array for the 'Available' table. 
        '''
        # create dictionary with methods unique params 
        requiredParams = {
                'GameDate': '10/10/2019',
                'DayOffset': '0'
                }
        # update dictionary with class required parameters
        requiredParams.update(self.requiredParams)
        # call self.search
        return self.search(self.endpoints['scoreboard'], requiredParams, params)
    
    def scoreboardv2(self, **params):
        '''
        method to access scoreboardv2 endpoint

        uses: 'scoreboardv2':
            'https://stats.wnba.com/stats/scoreboardv2' 
       
        ACCEPTS:
            GameID, LeagueID, DayOffset, 
            GameDate 
            
        DayOffset and GameDate have not been added to param_list yet. 
        These two params are used to specify a date or range of dates
        from which to pull scoreboard data. 
            GameDate is a string in the format "MM/DD/YYYY"
            DayOffset requires an Int of days before or after 
                              GameDate from which to include data

            'GameHeader'
                'GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 
                'GAME_STATUS_ID', 'GAME_STATUS_TEXT', 'GAMECODE', 
                'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON', 
                'LIVE_PERIOD', 'LIVE_PC_TIME', 'NATL_TV_BROADCASTER_ABBREVIATION', 
                'HOME_TV_BROADCASTER_ABBREVIATION', 'AWAY_TV_BROADCASTER_ABBREVIATION', 'LIVE_PERIOD_TIME_BCAST', 
                'ARENA_NAME', 'WH_STATUS', 

            'LineScore'
                'GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY_NAME', 
                'TEAM_NAME', 'TEAM_WINS_LOSSES', 'PTS_QTR1', 
                'PTS_QTR2', 'PTS_QTR3', 'PTS_QTR4', 
                'PTS_OT1', 'PTS_OT2', 'PTS_OT3', 
                'PTS_OT4', 'PTS_OT5', 'PTS_OT6', 
                'PTS_OT7', 'PTS_OT8', 'PTS_OT9', 
                'PTS_OT10', 'PTS', 'FG_PCT', 
                'FT_PCT', 'FG3_PCT', 'AST', 
                'REB', 'TOV', 

            'SeriesStandings'
                'GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 
                'GAME_DATE_EST', 'HOME_TEAM_WINS', 'HOME_TEAM_LOSSES', 
                'SERIES_LEADER', 

            'LastMeeting'
                'GAME_ID', 'LAST_GAME_ID', 'LAST_GAME_DATE_EST', 
                'LAST_GAME_HOME_TEAM_ID', 'LAST_GAME_HOME_TEAM_CITY', 'LAST_GAME_HOME_TEAM_NAME', 
                'LAST_GAME_HOME_TEAM_ABBREVIATION', 'LAST_GAME_HOME_TEAM_POINTS', 'LAST_GAME_VISITOR_TEAM_ID', 
                'LAST_GAME_VISITOR_TEAM_CITY', 'LAST_GAME_VISITOR_TEAM_NAME', 'LAST_GAME_VISITOR_TEAM_CITY1', 
                'LAST_GAME_VISITOR_TEAM_POINTS', 

            'EastConfStandingsByDay'
                'TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 
                'STANDINGSDATE', 'CONFERENCE', 'TEAM', 
                'G', 'W', 'L', 
                'W_PCT', 'HOME_RECORD', 'ROAD_RECORD', 


            'WestConfStandingsByDay'
                'TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 
                'STANDINGSDATE', 'CONFERENCE', 'TEAM', 
                'G', 'W', 'L', 
                'W_PCT', 'HOME_RECORD', 'ROAD_RECORD', 


            'Available'
                'GAME_ID', 'PT_AVAILABLE', 

            'TeamLeaders'
                'GAME_ID', 'TEAM_ID', 'TEAM_CITY', 
                'TEAM_NICKNAME', 'TEAM_ABBREVIATION', 'PTS_PLAYER_ID', 
                'PTS_PLAYER_NAME', 'PTS', 'REB_PLAYER_ID', 
                'REB_PLAYER_NAME', 'REB', 'AST_PLAYER_ID', 
                'AST_PLAYER_NAME', 'AST', 

            'TicketLinks'
                'GAME_ID', 'LEAG_TIX', 

            'WinProbability'
                 -- all scoreboard searches tested to date have
                    returned an empty headers array and empty 
                    rowSet array for the 'WinProbability' table.
                    Current theory is that this table is only 
                    active while the game is in progress. so 
                    we should find out in May. 
        '''
        # set method's unique required params
        requiredParams = {
                'GameDate': '10/10/2019',
                'DayOffset': '0'
                }
        # update requiredParams with class requiredParams
        requiredParams.update(self.requiredParams)
        #return search
        return self.search(self.endpoints['scoreboardv2'], requiredParams, params)
    
    def playByPlay(self, **params):
        '''
        method to access playbyplay endpoint. This method has significant
        overlap with the pbp method and offers less detail.
        I see NO valid case for using this method over the other. 
        It is included only because it uses the API system as the majority
        of methods in this package. 

        uses: 'playbyplay':
            'https://stats.wnba.com/stats/playbyplay'
        
        ACCEPTS:
            GameID, EndPeriod, StartPeriod 
            
        EndPeriod and StartPeriod have not been added to param_list yet. 
        These two params are used to specify which periods to pull playbyplay
        data from. 
            Both params accept values 0, 1, 2, 3, 4. 0 represents full game, 
            and should always be used with both params set to zero. 
        
        SAMPLE TABLES AND HEADERS
            'PlayByPlay'
                'GAME_ID', 'EVENTNUM', 'EVENTMSGTYPE', 
                'EVENTMSGACTIONTYPE', 'PERIOD', 'WCTIMESTRING', 
                'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION', 
                'VISITORDESCRIPTION', 'SCORE', 'SCOREMARGIN', 


            'AvailableVideo'
                'VIDEO_AVAILABLE_FLAG',
                -- contains 1 if video available, 0 if not. Does
                   not provide link to video
           
        '''
        # set unique required params to dict
        requiredParams = {
                'EndPeriod': '0',
                'StartPeriod': '0'
                }
        # update dict with class required params
        requiredParams.update(self.requiredParams)
        # return the search
        return self.search(self.endpoints['playbyplay'], requiredParams, params)
    
    def playByPlayv2(self, **params):
        '''
        method to access playbyplayv2 endpoint

        uses: 'playbyplayv2':
            'https://stats.wnba.com/stats/playbyplayv2'
        
        
        ACCEPTS:
            GameID, EndPeriod, StartPeriod 
            
        EndPeriod and StartPeriod have not been added to param_list yet. 
        These two params are used to specify which periods to pull playbyplay
        data from. 
            Both params accept values 0, 1, 2, 3, 4. 0 represents full game, 
            and should always be used with both params set to zero. 

            'PlayByPlay'
                'GAME_ID', 'EVENTNUM', 'EVENTMSGTYPE', 
                'EVENTMSGACTIONTYPE', 'PERIOD', 'WCTIMESTRING', 
                'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION', 
                'VISITORDESCRIPTION', 'SCORE', 'SCOREMARGIN', 
                'PERSON1TYPE', 'PLAYER1_ID', 'PLAYER1_NAME', 
                'PLAYER1_TEAM_ID', 'PLAYER1_TEAM_CITY', 'PLAYER1_TEAM_NICKNAME', 
                'PLAYER1_TEAM_ABBREVIATION', 'PERSON2TYPE', 'PLAYER2_ID', 
                'PLAYER2_NAME', 'PLAYER2_TEAM_ID', 'PLAYER2_TEAM_CITY', 
                'PLAYER2_TEAM_NICKNAME', 'PLAYER2_TEAM_ABBREVIATION', 'PERSON3TYPE', 
                'PLAYER3_ID', 'PLAYER3_NAME', 'PLAYER3_TEAM_ID', 
                'PLAYER3_TEAM_CITY', 'PLAYER3_TEAM_NICKNAME', 'PLAYER3_TEAM_ABBREVIATION', 
                'VIDEO_AVAILABLE_FLAG', 

            'AvailableVideo'
                'VIDEO_AVAILABLE_FLAG', 
                -- contains 1 if video available, 0 if not. Does
                   not provide link to video
        '''
        # set unique required params to dict
        requiredParams = {
                'EndPeriod': '0',
                'StartPeriod': '0'
                }
        # update dict with class required params
        requiredParams.update(self.rrequiredParams)
        # return the search
        return self.search(self.endpoints['playbyplayv2'], requiredParams, params)
    
        
    def shotChart(self, title='untitled'):
        '''
        method to generate game chart svgs
        
        generates  /Web Resources/title.js and /Web Resources/title.html
        '''
        templatePath = 'Web Resources/template'
        
        folderPath = 'Web Resources/Game Charts/' + title + '/'
                
        if not isdir(folderPath):
            makedirs(folderPath)
        
        temptitle = title[:]
        
        print(temptitle)
        print(folderPath + temptitle + '.js')
        i = 1
        while True:
            if isfile(folderPath + temptitle + '.html'):
                temptitle = title + ' - ' + str(i)
                i+= 1
            else:
                break
        
        title = temptitle
        print(title)
        
        data = '`' + json.dumps(self.pbp().json(), indent=0) + '`'
        template = ''
    
            
        with open(templatePath + '.html') as f:
            template = f.read().replace('PUT_DATA', str(data))
            
        with open(folderPath + title + '.html', 'w+') as f:
            f.write(template)
            
        
def __main__():
    pass

def tempGetHeaders(endpoint):
    sample = endpoint()
    if sample.get('resultSet', False):
        resSets = [sample['resultSet']]
    elif sample.get('resultSets', False):
        resSets = sample['resultSets']
        if type(resSets) == dict:
            resSets = [resSets]
    for table in resSets:
        print("            '" + table['name'] + "'")
        for i in range(len(table['headers'])):
            if i % 3 == 0:
                print('                ', end='')
            print("'" + table['headers'][i], end="', ")
            if (i+1) % 3 == 0:
                print('')
        print('\n')