#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:46:47 2019

####################################################################
####                                                            ####
####                         team module                        ####
####                                                            ####
####################################################################

This module houses the Search subclass Team.

Like Search, a Team object can be created with or without parameters:
    
    t = Team()

    or

    t = Team(TeamID='1611661328', Season='2019'...etc...)

    or
    
    params = {'TeamID='1611661328', 'Season'='2019'...etc...}
    t = Team(**params)
    
Perform a search by calling any Team class method, with or without params. 

Team's methods may also be used without creating a Team object:
    
    Team().method(**params)
    
If no parameters are passed, default parameters are used and data is returned
relevant to the current 2019 WNBA Champion Washington Mystics. 

For information on the search history capabilities inherited from the Search 
method, please see the search module documentation. 
    
"""

from wnbAPI.search import Search, currentSeason, teamLogo
    
class Team(Search):
    '''
        Extends Search class with methods to access endpoints for team data.
        
        
        Team Methods:
            logo():
                'https://stats.wnba.com/media/img/teams/logos/IND.svg'
                *Left as convenience, simply returns 
                Main.teamLogo(self.params[TeamID])
            details():
                'https://stats.wnba.com/stats/teamdetails'
            roster():
                'https://stats.wnba.com/stats/commonteamroster'
            schedule():
                'https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/2019/teams/mystics_schedule.json'
                ^Left as convenience, simply returns 
                    Main.scheduleMain.teamLogo(self.params[TeamID])
            gamelogs() 
                https://stats.wnba.com/stats/teamgamelogs
            shooting()
                'https://stats.wnba.com/stats/teamdashboardbyshootingsplits'
            clutch()
                'https://stats.wnba.com/stats/leaguedashteamclutch'
            lineups():
                'https://stats.wnba.com/stats/teamdashlineups'
            players()
                'https://stats.wnba.com/stats/teamplayerdashboard'
            splits()
                https://stats.wnba.com/stats/teamdashboardbygeneralsplits
            onOff()
                https://stats.wnba.com/stats/teamplayeronoffdetails
            onOffSummary()
                https://stats.wnba.com/stats/teamplayeronoffsummary
            yearByYear()
                https://stats.wnba.com/stats/teamyearbyyearstats
            shotChartDetail() * inherited from Search superclass * 
                'https://stats.wnba.com/stats/shotchartdetail'
               
                       
         Team Default Required params: 
             self. requiredParams = {
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
        
    Except for teamLogo and schedule, all methods return data object with this
    format: 
                
        default parameter search returns data object with format:
            {'resource': endpoint's url extension as unbroken lowercase string
            'parameters': {Array of Parameters Used in Query},
            'resultSets': 
                [Array of tables formatted as:{'name': table name as 
                                                       unspaced string,
                                               'headers': [array of 
                                                           header strings],
                                               'rowSet': [array of 
                                                          data subarrays 
                                                          matching headers],
                               }
                           ]       
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
        
        # set default required Parameters. These parameters are required for the 
        # majority of the methods in the class. When not required, can 
        # be overridden at the method level. But most of these params
        # can be passed without affecting return for the methods where they
        # are not required. 
        
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
            'PaceAdjust':'N',
            'PerMode': 'PerGame',# Requires string input
            'Period': '0',    # 0 stands for all periods
            'PlusMinus':'N',  # Requires Y or N
            'Rank': 'N',      # Requires Y or N
            'SeasonSegment':'',# Required but empty string accepted
            'SeasonType':'Regular Season', # Requires string input
            'TeamID':'1611661322', # 2019 World Champion Washington Mystics
            'VsConference': '',# Required but empty string accepted 
            'VsDivision':'',  # Required but empty string accepted
            'Season': str(currentSeason) # Requires string or integer year. 
            }
        

    def details(self, **params):
        '''
        method to get 'team details'
        
        uses 'https://stats.wnba.com/stats/teamdetails',
        
        Affected ONLY by TeamID param

        TABLES AND HEADERS:
             'TeamBackground'
                'TEAM_ID', 'ABBREVIATION', 'NICKNAME', 
                'YEARFOUNDED', 'CITY', 'ARENA', 'ARENACAPACITY',
                'OWNER', 'GENERALMANAGER', 'HEADCOACH', 
                'DLEAGUEAFFILIATION', 

            'TeamHistory'*
               'TEAM_ID', 'CITY', 'NICKNAME', 
               'YEARFOUNDED', 'YEARACTIVETILL', 

            'TeamSocialSites'*
               'ACCOUNTTYPE', 'WEBSITE_LINK', 
                
            'TeamAwardsChampionships'*
               'YEARAWARDED', 'OPPOSITETEAM', 
            
            'TeamAwardsConf'*
               'YEARAWARDED', 'OPPOSITETEAM', 
            
            'TeamAwardsDiv'*
                'YEARAWARDED', 'OPPOSITETEAM', 
            
            'TeamHof'*
                'PLAYERID', 'PLAYER', 'POSITION', 
                'JERSEY', 'SEASONSWITHTEAM', 'YEAR', 
            
            'TeamRetird'*
                'PLAYERID', 'PLAYER', 'POSITION', 
                'JERSEY', 'SEASONSWITHTEAM', 'YEAR',   
                
                                
        * So far these tables always come up with empty data sets. This may
        be a deprecated endpoint, but it is included because the WNBA stat
        page uses it somehow. 
        
        
        '''        
        return self.search(self.endpoints['details'], self.requiredParams, params)
    
    def roster(self, **params):
        '''
        method to get team roster
        
        uses: 'roster':
                'https://stats.wnba.com/stats/commonteamroster',
               
        Affected ONLY by TeamID param. 
        
        SAMPLE TABLES AND HEADERS:
        
        'CommonTeamRoster'
            'TeamID', 'SEASON', 'LeagueID', 
            'PLAYER', 'NUM', 'POSITION', 'HEIGHT', 
            'WEIGHT', 'BIRTH_DATE', 'AGE', 'EXP', 
            'SCHOOL', 'PLAYER_ID', 
        
        'Coaches'
            'COACH_ID', 'TEAM_ID', 'SEASON', 
            'FIRST_NAME', 'LAST_NAME', 'COACH_NAME', 
            'COACH_CODE', 'IS_ASSISTANT', 'COACH_TYPE', 
            'SORT_SEQUENCE',
        
               
        '''
        return self.search(self.endpoints['roster'], self.requiredParams, params)
    
    def logo(self, **params):
        '''
        method to pull team logo as .svg
                
        Affected ONLY by TeamID param. 
        
        Returns response object. To access: 
            
           res = Team().logo()
           
           res.content
           
           
        '''
        if params: 
            self.setParams(params)
            
        return teamLogo(TeamID =self.params.get('TeamID','1611661328'))
        
    def schedule(self, **params):
        '''
        method to get team schedule
        
        Affected ONLY by TeamID. 
        
        Schedule returns a response object. 
        The content is JSON encoded. 
        
        To access in python, set the return to a variable and call .json():
            
            res = Team().schedule()
            
            schedule = res.json() 
            
        The object encoded is a dictionary with only one key, 'gscd', 
        which contains an subdictionary. The format looks like this:
            {'gscd': {'tid': TeamID of relevant team as int,
                      'g': an array of game dictionaries described below,
                      'ta': 3 letter uppercase team abbreviatioin as string,
                      'tn': Full team nickname (no city) as titlecased string,
                      'tc': Team's City name as titlecased String.}
            }
            
            The format for each game dictionary in the g array is as follows:
                {'gid': unique game ID as string of numbers ,
                'gcode': string - YYYYMMDD/VVVHHH, (YDM are 8 digit date, 
                                                    A is 3 letter uppercase 
                                                    visiting team abbreviation, 
                                                    home is same for home team)
                'seri': '' in regular season or string description of series if
                         game is part of playoff series (ie 'WAS leads series\
                                                             3-2',),
                'is': Usually a 1. I don't know what it means yet,
                'gdte': Date string formatted 'YYYY-MM-DD'
                'htm': Home timezone starttime string formatted 
                       'YYYY-MM-DDTHH:MM:SS' (T is an literal T),
                'vtm': Visitor timezone startime in same format,
                'etm': I think eastern time in same format,
                'an': Name of Arena as Titlecaps string (proper title caps, 
                                                         so no articles)
                'ac': City arena is in as String. ,
                'as': String two-letter caps abbreviation of state 
                      (or DC for Was),
                'st': All currently show '3' as string. I think this is a 
                       status, and 3 means the game is complete,
                'stt': 'Final' - may be word representation of 'st',
                'bd': dictionary describing tv coverage outlined below,
                'v': dict: {'tid': TeamID as int,
                            're': 'Record string formatted 'W-L' (Wins-Losses),
                            'ta': 3 letter caps visiting team abbreviation string,
                            'tn': title cap's visiting team name,
                            's': String teams score if game is current or ended
                        
                      },
                'h': dict for home team with same format as 'v' dict,
                'gdtutc': gamedate UTC,
                'utctm': UTC start time,
                'ppdst': 'I', in all samples seen so far. I don't know yet. 
                }
                
                
                'bd' dict describing television coverage formatted:
                    {'b':
                        [ List of broadcast partners as dicts 
                          formatted: {'seq': int, corresponds to 
                                             index in 'b' list,
                                      'disp': String name of channel 
                                            (ie. 'CBS Sports Network'),
                                      'scope': 'home','away', or 'natl',
                                      'type':'tv' - no others seen yet,
                                      'lan': language as titlecase string
                                      }
                          ]}
                    
                
        '''
        # this method doesn't use the core Search.search method, so
        # if params are entered as an argument we need to
        # set those here instead of passing them to search. 
        if params: 
            self.setParams(params)
        #call the schedule method that was imported earlier.     
        return self.search.schedule(TeamID=self.params.get('TeamID','1611661322'), Season=self.params.get('Season', '2019'))
        
        
    def gamelogs(self, **params):
        '''
        method to get team gamelogs
        
        uses  'gamelogs':
                'https://stats.wnba.com/stats/teamgamelogs',
                    
        SAMPLE TABLES AND HEADERS
        'TeamGameLogs'
            'SEASON_YEAR', 'TEAM_ID', 'TEAM_ABBREVIATION',
            'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 
            ' MATCHUP', 'WL', 'MIN', 
            'FGM', 'FGA', 'FG_PCT', 
            'FG3M', 'FG3A', 'FG3_PCT', 
            'FTM', 'FTA', 'FT_PCT', 
            'OREB', 'DREB', 'REB', 
            'AST', 'TOV', 'STL', 
            'BLK', 'BLKA', 'PF', 
            'PFD', 'PTS', 'PLUS_MINUS', 
            'GP_RANK', 'W_RANK', 'L_RANK', 
            'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK',
            'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 
            'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 
            'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 
            'DREB_RANK', 'REB_RANK', 'AST_RANK', 
            'TOV_RANK', 'STL_RANK', 'BLK_RANK', 
            'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 
            
            
            PARAM NOTES: (NOT GUARUNTEED - NOTES REFLECT
                          TEST RESULTS SO FAR BUT NOT COMPREHENSIVE
                          TESTING BY ANY MEANS)
            
            REJECTS: MeasureType: Usage, Defense
            
            IGNORES: [LastNGames, PaceAdjust,PerMode,PlusMinus,Rank,
                          GameScope, PlayerExperience,PlayerPosition,
                          StarterBench,TopX, Conference, Division, 
                          GroupQuantity, StatCategory, TwoWay, 
                          Scope, PORound, PointDiff, ActiveFlag, AheadBehind,
                          ClutchTime,DraftPick, DraftYear, DistanceRange
                          ]
            
            AFFECTED BY MAY MEAN ACCEPTS, BUT MAY ALSO MEAN THAT SETTING ANY
            VALUE BREAKS SEARCH
            
            AFFECTED BY: ['DateFrom', 'DateTo', 'GameSegment', 
                      'LastNGames', 'Location', 'MeasureType',
                      'Month', 'Outcome', 'OpponentTeamID', 
                      'PerMode','Period', 'SeasonSegment','SeasonType',
                      'VsConference, 'VsDivision', 'Season', 
                      'ShotClockRange']
        '''
        return self.search(self.endpoints['gamelogs'], self.requiredParams, params)
  
    def shooting(self, **params):
        '''
        Method added 10/29 for team shooting splits endpoint. 
        
        uses 'shooting': 
                'https://stats.wnba.com/stats/teamdashboardbyshootingsplits',
           
        SAMPLE TABLES AND HEADERS: 
            'OverallTeamDashboard'     shares below        
            'Shot5FTTeamDashboard'     shares below
            'Shot8FTTeamDashboard'     shares below
            'ShotAreaTeamDashboard'    shares below
            'AssitedShotTeamDashboard' shares below
            'ShotTypeTeamDashboard' 
                'GROUP_SET', 'GROUP_VALUE', 'FGM', 
                'FGA', 'FG_PCT', 'FG3M', 
                'FG3A', 'FG3_PCT','EFG_PCT', 
                'BLKA', 'PCT_AST_2PM','PCT_UAST_2PM',
                'PCT_AST_3PM', 'PCT_UAST_3PM', 'PCT_AST_FGM', 
                'PCT_UAST_FGM', 'FGM_RANK', 'FGA_RANK', 
                'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
                'FG3_PCT_RANK', 'EFG_PCT_RANK', 'BLKA_RANK', 
                'PCT_AST_2PM_RANK', 'PCT_UAST_2PM_RANK', 'PCT_AST_3PM_RANK', 
                'PCT_UAST_3PM_RANK', 'PCT_AST_FGM_RANK', 'PCT_UAST_FGM_RANK', 
                'CFID', 'CFPARAMS'
            
            'AssistedBy'
                'GROUP_SET', 'PLAYER_ID', 'PLAYER_NAME', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'EFG_PCT', 'BLKA', 'PCT_AST_2PM', 
                'PCT_UAST_2PM', 'PCT_AST_3PM', 'PCT_UAST_3PM', 
                'PCT_AST_FGM', 'PCT_UAST_FGM', 'FGM_RANK', 
                'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 
                'FG3A_RANK', 'FG3_PCT_RANK', 'EFG_PCT_RANK', 
                'BLKA_RANK', 'PCT_AST_2PM_RANK', 'PCT_UAST_2PM_RANK', 
                'PCT_AST_3PM_RANK', 'PCT_UAST_3PM_RANK', 'PCT_AST_FGM_RANK',
                'PCT_UAST_FGM_RANK', 'CFID', 'CFPARAMS', 
        
        
        PARAMS UNTESTED. 
        
        '''
        
        return self.search(self.endpoints['shooting'], self.requiredParams, params)
    

    def clutch(self, **params):
        '''
        method to get team clutch stats
        
        uses 'clutch':
                'https://stats.wnba.com/stats/leaguedashteamclutch',
                
        IGNORES Rank, TopX, Split,
                Weight, GroupQuantity, StatsCategory, 
                TwoWay, Scope, PORound, 
                Country, ActiveFlag, Height,
                DraftPick,DraftYear
                            
        REJECTS MeasureType: 'Defense','Usage'
    
        Doesnt seem to play well with Period
    
        AFFECTED BY: 
        'DateTo', 'DateFrom', 'GameSegment',
        'LastNGames','Location','MeasureType',
        'Month','Outcome','OpponentTeamID',
        'PaceAdjust','PerMode','Period',
        'PlusMinus','SeasonSegment','SeasonType',
        'VsConference','VsDivision','Season',
        'GameScope','PlayerExperience','PlayerPosition',
        'StarterBench','Conference','Division',
        'ShotClockRange','PointDiff','AheadBehind',
        'ClutchTime'
        
        If 'PointDiff' used, requires value (not empty string). 
        
        SAMPLE TABLES AND HEADERS:
            'LeagueDashTeamClutch'
                'TEAM_ID', 'TEAM_NAME', 'GP', 
                'W', 'L', 'W_PCT', 
                'MIN', 'FGM', 'FGA', 
                'FG_PCT', 'FG3M', 'FG3A', 
                'FG3_PCT', 'FTM', 'FTA', 
                'FT_PCT', 'OREB', 'DREB', 
                'REB', 'AST', 'TOV', 
                'STL', 'BLK', 'BLKA', 
                'PF', 'PFD', 'PTS', 
                'PLUS_MINUS', 'GP_RANK', 'W_RANK', 
                'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 
                'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 
                'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 
                'OREB_RANK', 'DREB_RANK', 'REB_RANK', 
                'AST_RANK', 'TOV_RANK', 'STL_RANK', 
                'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
                'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 
                'CFID', 'CFPARAMS', 
        '''            
        requiredParams = {}
        
        requiredParams.update(self.requiredParams)
        
        requiredParams.update({'ClutchTime': 'Last 5 Minutes',
                               'AheadBehind':'Ahead or Behind',
                               'PointDiff':'5',
                               'GameScope': '',
                               'PlayerExperience':'',
                               'PlayerPosition':'',
                               'StarterBench':''
                               })
        
        return self.search(self.endpoints['clutch'], requiredParams, params)
  
    def lineups(self, **params):
        '''
        method to get team dashboard by lineups
        
        uses 'lineups':
                'https://stats.wnba.com/stats/teamdashlineups',
                    
        IGNORES: Rank, GameScope, PlayerExperience, 
                 PlayerPosition, StarterBench, TopX, 
                 Conference, Division, Split, 
                 StatCategory, TwoWay, Scope,
                 PORound, PointDiff, Country, 
                 ActiveFlag, AheadBehind, ClutchTime, 
                 DraftPick, DraftYear, DistanceRange
            
        ACCEPTS:
            'DateTo','GameSegment','LastNGames',
            'Location','MeasureType','Month',
            'Outcome','OpponentTeamID','PaceAdjust',
            'PerMode','Period','SeasonSegment',
            'SeasonType','VsConference','VsDivision',
            'Season','GroupQuantity','ShotClockRange',
            'GameID'

        MeasureType does not accept values Usage, Defense
        
        SAMPLE TABLES AND HEADERS:
            
            'Overall'
                'GROUP_SET', 'GROUP_VALUE', 'TEAM_ID', 
                'TEAM_ABBREVIATION', 'TEAM_NAME', 'GP', 
                'W', 'L', 'W_PCT', 
                'MIN', 'FGM', 'FGA', 
                'FG_PCT', 'FG3M', 'FG3A', 
                'FG3_PCT', 'FTM', 'FTA', 
                'FT_PCT', 'OREB', 'DREB', 
                'REB', 'AST', 'TOV', 
                'STL', 'BLK', 'BLKA', 
                'PF', 'PFD', 'PTS', 
                'PLUS_MINUS', 'GP_RANK', 'W_RANK', 
                'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 
                'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 
                'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK',
                'OREB_RANK', 'DREB_RANK', 'REB_RANK', 
                'AST_RANK', 'TOV_RANK', 'STL_RANK',
                'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
                'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 
            
            'Lineups'
                'GROUP_SET', 'GROUP_ID', 'GROUP_NAME', 
                'GP', 'W', 'L', 
                'W_PCT', 'MIN', 'FGM', 
                'FGA', 'FG_PCT', 'FG3M', 
                'FG3A', 'FG3_PCT', 'FTM',
                'FTA', 'FT_PCT', 'OREB', 
                'DREB', 'REB', 'AST', 
                'TOV', 'STL', 'BLK', 
                'BLKA', 'PF', 'PFD', 
                'PTS', 'PLUS_MINUS', 'GP_RANK', 
                'W_RANK', 'L_RANK', 'W_PCT_RANK', 
                'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 
                'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
                'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 
                'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 
                'REB_RANK', 'AST_RANK', 'TOV_RANK', 
                'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 
                'PF_RANK', 'PFD_RANK', 'PTS_RANK', 
                'PLUS_MINUS_RANK', 
        
        '''
        requiredParams = {}
        
        requiredParams.update(self.requiredParams)
            
        requiredParams.update({'GroupQuantity':'5',
                               'GameID':''
                               })
        
        return self.search(self.endpoints['lineups'], requiredParams, params)

    def players(self, **params):
        '''
        method to get team player dashboard
        
        'playerDashboard':
                'https://stats.wnba.com/stats/teamplayerdashboard',
                
        
        IGNORES 
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, Starterbench, TopX, 
            Conference, Division, GroupQuantity, 
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, ActiveFlag, 
            AheadBehind, ClutchTime, DraftPick
        
        UNTESTED: GameID (only ''). 
        
        AFFECTED by: 
            'DateFrom', 'DateTo', 'GameSegment', 
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID', 
            'PaceAdjust', 'PerMode','Period',
            'PlusMinus','SeasonSegment','VsConference,
            'Season', 'ShotClockRange', 'VsDivision'
    
         Does not accept MeasureTypes 'Four Factors', 'Opponent', 'Defense'
         
         
         SAMPLE TABLES AND HEADERS:
             'TeamOverall'
                 'GROUP_SET', 'TEAM_ID', 'TEAM_NAME', 
                 'GROUP_VALUE', 'GP', 'W', 
                 'L', 'W_PCT', 'MIN', 'FGM', 
                 'FGA', 'FG_PCT', 'FG3M', 
                 'FG3A', 'FG3_PCT', 'FTM', 
                 'FTA', 'FT_PCT', 'OREB', 
                 'DREB', 'REB', 'AST', 
                 'TOV', 'STL', 'BLK', 
                 'BLKA', 'PF', 'PFD', 
                 'PTS', 'PLUS_MINUS', 'GP_RANK', 
                 'W_RANK', 'L_RANK', 'W_PCT_RANK', 
                 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 
                 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
                 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 
                 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 
                 'REB_RANK', 'AST_RANK', 'TOV_RANK', 
                 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 
                 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 
                 'PLUS_MINUS_RANK', 
             'PlayersSeasonTotals'
                 'GROUP_SET', 'PLAYER_ID', 'PLAYER_NAME',
                 'GP', 'W', 'L', 
                 'W_PCT', 'MIN', 'FGM', 
                 'FGA', 'FG_PCT', 'FG3M',
                 'FG3A', 'FG3_PCT', 'FTM', 
                 'FTA', 'FT_PCT', 'OREB', 
                 'DREB', 'REB', 'AST', 
                 'TOV', 'STL', 'BLK', 
                 'BLKA', 'PF', 'PFD', 
                 'PTS', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 
                 'DD2', 'TD3', 'GP_RANK', 
                 'W_RANK', 'L_RANK', 'W_PCT_RANK', 
                 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 
                 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
                 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 
                 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 
                 'REB_RANK', 'AST_RANK', 'TOV_RANK', 
                 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 
                 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 
                 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 
                 'DD2_RANK', 'TD3_RANK', 
             
        '''
        return self.search(self.endpoints['playerDashboard'], self.requiredParams, params)
        
    def splits(self, **params):
        '''
        method to get team player dashboard by splits
        
        uses 'dashboardBySplits':
                'https://stats.wnba.com/stats/teamdashboardbygeneralsplits', 
            
        IGNORES - Rank, GameScope, PlayerExperience,
                  PlayerPosition, StarterBench, TopX, 
                  Conference, Division, Split, 
                  GroupQuantity, StatCategory, TwoWay, 
                  Scope, PORound, PointDiff, 
                  Country, ActiveFlag, AheadBehind, 
                  ClutchTime, DraftPick, GameID, 
                  DistanceRange
                  
        ACCEPTS- 
            'DateFrom','DateTo','GameSegment',
            'LastNGames','Location','MeasureType',
            'Month','Outcome','OpponentTeamID',
            'PaceAdjust','PerMode','Period',
            'SeasonSegment','SeasonType','VsConference',
            'VsDivison','Season','ShotClockRange'
    
    
         MeasureType Fails for Usage, Defense
         
         SAMPLE TABLES AND HEADERS:
             'OverallTeamDashboard'
             'LocationTeamDashboard'      
             'WinsLossesTeamDashboard'
             'MonthTeamDashboard'
             'PrePostAllStarTeamDashboard'
             'DaysRestTeamDashboard'
                 'GROUP_SET', 'GROUP_VALUE', 'SEASON_YEAR', 
                 'GP', 'W', 'L', 
                 'W_PCT', 'MIN', 'FGM', 
                 'FGA', 'FG_PCT', 'FG3M', 
                 'FG3A', 'FG3_PCT', 'FTM', 
                 'FTA', 'FT_PCT', 'OREB', 
                 'DREB', 'REB', 'AST', 
                 'TOV', 'STL', 'BLK', 
                 'BLKA', 'PF', 'PFD', 
                 'PTS', 'PLUS_MINUS', 'GP_RANK', 
                 'W_RANK', 'L_RANK', 'W_PCT_RANK', 
                 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 
                 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK',
                 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK',
                 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 
                 'REB_RANK', 'AST_RANK', 'TOV_RANK', 
                 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 
                 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 
                 'PLUS_MINUS_RANK', 'CFID', 'CFPARAMS', 

    

        '''           
        return self.search(self.endpoints['dashboardBySplits'], self.requiredParams, params)
    
    def onOff(self, **params):
        '''
        method to get team player on Off information
        
        uses 'onOff':
                'https://stats.wnba.com/stats/teamplayeronoffdetails',
        
        IGNORES - 
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX,  
            Conference, Division, Weight, 
            GroupQuantity, StatCategory, TwoWay, 
            ShotClockRange, Scope, PORound, 
            PointDiff, Country, ActiveFlag, 
            AheadBehind, ClutchTime, DraftPick, 
            GameID, DistanceRange
        
        ACCEPTS - 
            'DateTo','DateFrom', 'GameSegment', 
            'LastNGames','Location','MeasureType',
            'Month','Outcome','OpponentTeamID',
            'PaceAdjust','PerMode','Period',
            'PlusMinus','SeasonSegment','SeasonType',
            'VsConference','VsDivision','Season'
    
        MeasureType Fails for Usage, Defense
        
        SAMPLE TABLES AND HEADERS:
            'OverallTeamPlayerOnOffDetails'
                'GROUP_SET', 'GROUP_VALUE', 'TEAM_ID', 
                'TEAM_ABBREVIATION', 'TEAM_NAME', 'GP', 
                'W', 'L', 'W_PCT', 
                'MIN', 'FGM', 'FGA', 
                'FG_PCT', 'FG3M', 'FG3A', 
                'FG3_PCT', 'FTM', 'FTA', 
                'FT_PCT', 'OREB', 'DREB', 
                'REB', 'AST', 'TOV', 
                'STL', 'BLK', 'BLKA', 
                'PF', 'PFD', 'PTS', 
                'PLUS_MINUS', 'GP_RANK', 'W_RANK', 
                'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 
                'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK',
                'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 
                'OREB_RANK', 'DREB_RANK', 'REB_RANK',
                'AST_RANK', 'TOV_RANK', 'STL_RANK',
                'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
                'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 
                
            'PlayersOnCourtTeamPlayerOnOffDetails'
            'PlayersOffCourtTeamPlayerOnOffDetails'
                'GROUP_SET', 'TEAM_ID', 'TEAM_ABBREVIATION', 
                'TEAM_NAME', 'VS_PLAYER_ID', 'VS_PLAYER_NAME',
                'COURT_STATUS', 'GP', 'W',
                'L', 'W_PCT', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT',
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB',
                'AST', 'TOV', 'STL', 
                'BLK', 'BLKA', 'PF', 
                'PFD', 'PTS', 'PLUS_MINUS',
                'GP_RANK', 'W_RANK', 'L_RANK',
                'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK',
                'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 
                'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 
                'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 
                'DREB_RANK', 'REB_RANK', 'AST_RANK', 
                'TOV_RANK', 'STL_RANK', 'BLK_RANK',
                'BLKA_RANK', 'PF_RANK', 'PFD_RANK',
                'PTS_RANK', 'PLUS_MINUS_RANK', 
    
    '''
        return self.search(self.endpoints['onOff'], self.requiredParams, params)
    
    def onOffSummary(self, **params):
        '''
        method to get team player on/off summary
        uses 'onOffSummary':
                'https://stats.wnba.com/stats/teamplayeronoffsummary',
            
        IGNORES - 
            MeasureType, Rank, GameScope, 
            PlayerExperience, PlayerPosition, StarterBench, 
            TopX, Conference, Division, 
            GroupQuantity, StatCategory, TwoWay, 
            ShotClockRange, Scope, PORound, 
            PointDiff, Country, ActiveFlag, 
            AheadBehind, ClutchTime, DraftPick, 
            DraftYear, GameID, DistanceRange
              
       ACCEPTS - 
           'DateTo','DateFrom','GameSegment',
           'LastNGames','Location','Month',
           'Outcome','OpponentTeamID','PaceAdjust',
           'PerMode','Period','PlusMinus',
           'SeasonSegment','SeasonType','VsConference',
           'VsDivision','Season'
           
        SAMPLE TABLES AND HEADERS:
        
        'OverallTeamPlayerOnOffSummary'
            'GROUP_SET', 'GROUP_VALUE', 'TEAM_ID', 
            'TEAM_ABBREVIATION', 'TEAM_NAME', 'GP', 
            'W', 'L', 'W_PCT', 
            'MIN', 'FGM', 'FGA', 
            'FG_PCT', 'FG3M', 'FG3A', 
            'FG3_PCT', 'FTM', 'FTA', 
            'FT_PCT', 'OREB', 'DREB', 
            'REB', 'AST', 'TOV', 
            'STL', 'BLK', 'BLKA', 
            'PF', 'PFD', 'PTS', 
            'PLUS_MINUS', 'GP_RANK', 'W_RANK', 
            'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
            'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 
            'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 
            'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 
            'OREB_RANK', 'DREB_RANK', 'REB_RANK', 
            'AST_RANK', 'TOV_RANK', 'STL_RANK', 
            'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
            'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 
        
        'PlayersOnCourtTeamPlayerOnOffSummary'
            'GROUP_SET', 'TEAM_ID', 'TEAM_ABBREVIATION',
            'TEAM_NAME', 'VS_PLAYER_ID', 'VS_PLAYER_NAME', 
            'COURT_STATUS', 'GP', 'MIN', 
            'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING',
            'NET_RATING', 
        
        'PlayersOffCourtTeamPlayerOnOffSummary'
            'GROUP_SET', 'TEAM_ID', 'TEAM_ABBREVIATION', 
            'TEAM_NAME', 'VS_PLAYER_ID', 'VS_PLAYER_NAME', 
            'COURT_STATUS', 'GP', 'MIN', 
            'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 
            'NET_RATING', 
                  
        '''
        return self.search(self.endpoints['onOffSummary'], self.requiredParams, params)
    
    def yearByYear(self, **params):
        '''
        method to get team year by year stats
        
        uses 'yearByYearStats':
                'https://stats.wnba.com/stats/teamyearbyyearstats'
    
        
        ACCEPTS ONLY TEAMID (ANDE PERMODE BUT ONLY TOTALS IS KNOWN TO BE VALID 
        
        
        SAMPLE TABLES AND HEADERS:
            'TeamStats'
                'TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 
                'YEAR', 'GP', 'WINS', 
                'LOSSES', 'WIN_PCT', 'CONF_RANK', 
                'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 
                'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE',
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT',
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'PF', 'STL', 
                'TOV', 'BLK', 'PTS', 
                'PTS_RANK', 
        '''
        return self.search(self.endpoints['yearByYearStats'],self.requiredParams, params)

def __main__():
    pass