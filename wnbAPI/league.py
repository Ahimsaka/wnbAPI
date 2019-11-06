#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:46:47 2019

####################################################################
####                                                            ####
####                        league module                       ####
####                                                            ####
####################################################################
    
This module houses the Search subclass League.

Like Search, a League object can be created with or without parameters:
    
    l = League()

    or

    l = League(LeagueID='10', Season='2019'...etc...)

    or
    
    params = {'LeagueID'='10', 'Season'='2019'...etc...}
    l = League(**params)
    
Perform a search by calling any League class method, with or without params. 

League's methods may also be used without creating a League object:
    
    League().method(**params)
    
If no parameters are passed, default parameters are used and data is returned
relevant to the WNBA roster during the current year's season.  

For information on the search history capabilities inherited from the Search 
method, please see the search module documentation. 
"""

from wnbAPI.search import Search, currentSeason
    
class League(Search):
    '''
    Extends Search class with methods to access endpoints for league data.
    
    League Methods:
        players():
            'https://stats.wnba.com/stats/leaguedashplayerstats?'
        standings():
            'https://stats.wnba.com/stats/leaguestandingsv3?'
        teams():
            'https://stats.wnba.com/stats/leaguedashteamstats?'
        shotLocations():
            'https://stats.wnba.com/stats/leaguedashteamshotlocations?'
        statLeaders():
            'https://stats.wnba.com/stats/leagueLeaders'
        alltimeLeaders():
            ''https://stats.wnba.com/stats/alltimeleadersgrids?'
        lineups():
            'https://stats.wnba.com/stats/leaguedashlineups?'
        shotChartDetail() * inherited from Search superclass * 
            'https://stats.wnba.com/stats/shotchartdetail'
            
    League Default Required Params: 
        {
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
        
    '''
    def __init__(self, **params):
        Search.__init__(self, **params)
        # create dictionary of the endpoints assigned to each method. 
        # these could also have been stored inside each method. 
        # and that might have been a better choice, but I like
        # having a list of the accessible endpoints built into the
        # object. 
        self.endpoints = {
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
               
        # set default required Parameters. These parameters are required for the 
        # majority of the methods in the class. When not required, can 
        # be overridden at the method level. But most of these params
        # can be passed without affecting return for the methods where they
        # are not required.         
          
        self.requiredParams = {
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
                               
    def players(self, **params):
        '''
        method for getting stats for all players in league (historic or per year)
        
        uses: players:
            https://stats.wnba.com/stats/leaguedashplayerstats
            
        IGNORES: 
            Outcome, Rank, GameScope, 
            TopX, GroupQuantity, StatCategory, 
            Scope, PORound, PointDiff,
            ActiveFlag, AheadBehind, Height,
            ClutchTime, Draft Pick
    
        REJECTS ShotClockRange
        
        MeasureType rejects Four Factors and Opponent. 
        
        AFFECTED BY LIST UNTESTED
        
        SAMPLE TABLES AND HEADERS    
            'LeagueDashPlayerStats'
                'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 
                'TEAM_ABBREVIATION', 'AGE', 'GP', 
                'W', 'L', 'W_PCT', 
                'MIN', 'FGM', 'FGA', 
                'FG_PCT', 'FG3M', 'FG3A', 
                'FG3_PCT', 'FTM', 'FTA', 
                'FT_PCT', 'OREB', 'DREB', 
                'REB', 'AST', 'TOV', 
                'STL', 'BLK', 'BLKA', 
                'PF', 'PFD', 'PTS', 
                'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 
                'TD3', 'GP_RANK', 'W_RANK', 
                'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 
                'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 
                'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 
                'OREB_RANK', 'DREB_RANK', 'REB_RANK', 
                'AST_RANK', 'TOV_RANK', 'STL_RANK', 
                'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
                'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 
                'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK', 
                'CFID', 'CFPARAMS', 
        
        
        '''
        return self.search(self.endpoints['players'], self.requiredParams, params)
  
    def standings(self, **params):
        '''
        method for getting current league standings
        
        uses: standings:
            https://stats.wnba.com/stats/leaguestandingsv3
        
        ONLY AFFECTED BY: 
            'SeasonType','Season'
    
        SAMPLE TABLES AND HEADERS:
            'Standings'
                'LeagueID', 'SeasonID', 'TeamID', 
                'TeamCity', 'TeamName', 'Conference', 
                'ConferenceRecord', 'PlayoffRank', 'ClinchIndicator', 
                'Division', 'DivisionRecord', 'DivisionRank', 
                'WINS', 'LOSSES', 'WinPCT', 
                'LeagueRank', 'Record', 'HOME', 
                'ROAD', 'L10', 'Last10Home', 
                'Last10Road', 'OT', 'ThreePTSOrLess', 
                'TenPTSOrMore', 'LongHomeStreak', 'strLongHomeStreak', 
                'LongRoadStreak', 'strLongRoadStreak', 'LongWinStreak', 
                'LongLossStreak', 'CurrentHomeStreak', 'strCurrentHomeStreak', 
                'CurrentRoadStreak', 'strCurrentRoadStreak', 'CurrentStreak', 
                'strCurrentStreak', 'ConferenceGamesBack', 'DivisionGamesBack', 
                'ClinchedConferenceTitle', 'ClinchedDivisionTitle', 'ClinchedPlayoffBirth', 
                'EliminatedConference', 'EliminatedDivision', 'AheadAtHalf', 
                'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird', 
                'BehindAtThird', 'TiedAtThird', 'Score100PTS', 
                'OppScore100PTS', 'OppOver500', 'LeadInFGPCT', 
                'LeadInReb', 'FewerTurnovers', 'PointsPG', 
                'OppPointsPG', 'DiffPointsPG', 'vsEast', 
                'vsAtlantic', 'vsCentral', 'vsSoutheast', 
                'vsWest', 'vsNorthwest', 'vsPacific', 
                'vsSouthwest', 'Jan', 'Feb', 
                'Mar', 'Apr', 'May', 
                'Jun', 'Jul', 'Aug', 
                'Sep', 'Oct', 'Nov', 
                'Dec', 
        
        '''
        return self.search(self.endpoints['standings'], self.requiredParams, params)
    
    def teams(self, **params):
        '''
        method for getting team stats
        
        uses: teams:
            https://stats.wnba.com/stats/leaguedashteamstats
          
        IGNORES: 
            Outcome, Rank, TopX, 
            GroupQuantity, StatCategory, Scope, 
            PORound, PointDiff, Country,
            ActiveFlag, AheadBehind, ClutchTime,
            DraftPick, DraftYear
            
        REJECTS: 
            ShotClockRange, TwoWay
        
        AFFECTED BY: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'OpponentTeamID', 'PaceAdjust',
            'PerMode', 'Period', 'PlusMinus',
            'SeasonSegment', 'SeasonType', 'VsConference',
            'VsDivision', 'Season', 'GameScope',
            'PlayerExperience', 'PlayerPosition','StarterBench',
            'Conference', 'Division', 'TwoWay'
        
        MeasureType rejects Usage for this endpoint.
        
        SAMPLE TABLES AND HEADERS:
            'LeagueDashTeamStats'
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
        return self.search(self.endpoints['teams'], self.requiredParams, params)
    
    def shotLocations(self, **params):
        '''
        method for getting League shot location data.
        
        uses: shotLocations:
            https://stats.wnba.com/stats/leaguedashteamshotlocations
 
        
        **** THIS ENDPOINT RETURNS TWO ROWS OF HEADERS. IT IS CURRENTLY  ****
        **** THE ONLY ENDPOINT DOCUMENTED WHICH DOES THIS. AS SUCH,      ****
        **** THE SEARCH DATAFRAME METHOD HAS NOT BEEN ADJUSTE            ****
        **** TO ACCOMDATE THE FORMATTING OF THESE RESULTS. UNTIL         ****
        **** THAT IS FIXED THIS METHOD SHOULD NOT BE USED IN CONJUNCTION ****
        **** WITH THE DATAFRAME METHOD                                   ****
        
        
        IGNORES:
            Outcome, Rank, TopX, 
            GroupQuantity, StatCategory, TwoWay, 
            Scope, PORound, PointDiff, 
            Country, ActiveFlag, AheadBehind, 
            ClutchTime, DraftPick, DraftYear
    
        REJECTS: 
            ShotClockRange
    
        AFFECTED BY:
            'DateTo', 'DateFrom','GameSegment','LastNGames',
               'Location','MeasureType','Month','OpponentTeamID',
               'PaceAdjust','PerMode','Period','PlusMinus',
               'SeasonSegment','SeasonType','VsConference',
               'VsDivision','Season','GameScope','PlayerExperience',
               'PlayerPosition','StarterBench','Conference',
               'Division', 'DistanceRange'
        
        REQUIRES DistanceRange
    
        MeasureType rejects Usage, Scoring, Four Factors, Misc, Advanced 
        
        
        SAMPLE TABLES AND HEADERS:
            'resultSets': {'name': 'ShotLocations',
            'headers': [{'name': 'SHOT_CATEGORY',
                         'columnsToSkip': 2,
                         'columnSpan': 3, 
                         'columnNames': [
                                         'Restricted Area',
                                         'In The Paint (Non-RA)',
                                         'Mid-Range',
                                         'Left Corner 3',
                                         'Right Corner 3',
                                         'Above the Break 3',
                                         'Backcourt']},
                        {'name': 'columns',
                         'columnSpan': 1,    
                         'columnNames': [
                                         'TEAM_ID',
                                         'TEAM_NAME',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT',
                                         'FGM',
                                         'FGA',
                                         'FG_PCT']}],
        '''
        requiredParams = {}
        
        for key in self.requiredParams:
            requiredParams[key] = self.requiredParams[key]
            
        requiredParams.update({'DistanceRange':'By Zone'})
        
        return self.search(self.endpoints['shotLocations'], requiredParams, params)
    
    def statLeaders(self, **params):
        '''
        method for getting statistical leader data
        
        uses: statLeaders:
            https://stats.wnba.com/stats/leagueLeaders
        
        can use this with Active Flag=Yes and Year=All Time to get all time
        active player rankings (the all time leaders endpoint doesn't 
        appear to honor the active flag)
        
        IGNORES:
            DateFrom, DateTo, GameSegment, 
            LastNGames, Location, MeasureType,
            Month, Outcome, OpponentTeamID, 
            PaceAdjust, PerMode, Period,
            PlusMinus, Rank, SeasonSegment, 
            SeasonType, VsConference, VsDivision, 
            GameScope, PlayerExperience, PlayerPosition,
            StarterBench, PlayerID, TopX, 
            Conference, Division, GroupQuantity
            
        ACCEPTS:
            'SeasonType', 'Season', 'StatCategory',
            'Country', 'DraftPick', 'DraftYear',
            'AheadBehind', 'ActiveFlag', 'PointDiff',
            'PORound', 'Scope', 'ShotClockRange',
            'ClutchTime', 'DraftPick', 'DraftYear',
            'GameID'
        
        CONFUSINGLY: testing says data set returned is changed by
        the params in the affected by list, but I can't find the changes. 
        To best of my ability to discern, this endpoint only 
        accepts PerMode and StatCategory. 
    
        REQUIRES - Scope
        
        SAMPLE TABLES AND HEADERS:        
            'LeagueLeaders'
                'PLAYER_ID', 'RANK', 'PLAYER', 
                'TEAM', 'GP', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS', 
                'EFF', 'AST_TOV', 'STL_TOV', 

        '''
        requiredParams = {}
        
        if self.params.get('PerMode',0) != 'Totals':
            self.setParams({'PerMode':'Totals'})
        
        for key in self.requiredParams:
            requiredParams[key] = self.requiredParams[key]
            
        requiredParams.update({'StatCategory':'FT_PCT',
                               'Scope': 'RS',
                               'PerMode': 'Totals'})
            
        return self.search(self.endpoints['statLeaders'], requiredParams, params)
        
    def alltimeLeaders(self, **params):
        '''
        method for getting all time statistical leader data
    
        uses: alltimeLeaders:
            https://stats.wnba.com/stats/alltimeleadersgrids
        
        AFFECTED BY: 
            'TopX', 'PerMode','SeasonType',
            'LeagueID'
    
        IGNORES ALL OTHERS, EXCEPT IS BROKEN BY A GOOD MANY
        THESE ARE ACCEPTABLE/NONBREAKING: {
                               'LeagueID':'10',
                               'SeasonType':'Regular Season',
                               'Season': currentSeason,
                               'GameScope': '',
                               'PlayerExperience': '',
                               'PlayerPosition': '',
                               'StarterBench':'',
                               'MeasureType':'Base',
                               'PerMode':'PerGame',
                               'PlusMinus':'N',
                               'PaceAdjust':'N',
                               'Rank':'N',
                               'OutCome':'',
                               'Location':'',
                               'Month':'0',
                               'SeasonSegment':'',
                               'DateFrom':'',
                               'DateTo':'',
                               'OpponentTeamID':'0',
                               'VsConference':'',
                               'VsDivision':'',                               
                               'GameSegment':'',
                               'Period':'0',    
                               'LastNGames':'0'
                               }}
        
        SAMPLE TABLES AND HEADERS:
            'GPLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'GP', 
                'GP_RANK', 

            'PTSLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'PTS', 
                'PTS_RANK', 

            'ASTLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'AST', 
                'AST_RANK', 

            'STLLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'STL', 
                'STL_RANK', 

            'OREBLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'OREB', 
                'OREB_RANK', 

            'DREBLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'DREB', 
                'DREB_RANK', 

            'REBLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'REB', 
                'REB_RANK', 

            'BLKLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'BLK', 
                'BLK_RANK', 

            'FGMLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FGM', 
                'FGM_RANK', 

            'FGALeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FGA', 
                'FGA_RANK', 

            'FG_PCTLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FG_PCT', 
                'FG_PCT_RANK', 

            'TOVLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'TOV', 
                'TOV_RANK', 

            'FG3MLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FG3M', 
                'FG3M_RANK', 

            'FG3ALeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FG3A', 
                'FG3A_RANK', 

            'FG3_PCTLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FG3_PCT', 
                'FG3_PCT_RANK', 

            'PFLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'PF', 
                'PF_RANK', 

            'FTMLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FTM', 
                'FTM_RANK', 

            'FTALeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FTA', 
                'FTA_RANK', 

            'FT_PCTLeaders'
                'PLAYER_ID', 'PLAYER_NAME', 'FT_PCT', 
                'FT_PCT_RANK', 
        '''
        requiredParams = {}
        
        for key in self.requiredParams:
            requiredParams[key] = self.requiredParams[key]
            
        requiredParams.update({'TopX':'10'})
        
        return self.search(self.endpoints['alltimeLeaders'], requiredParams, params)
    
    def lineups(self, **params):
        '''
        method for getting league lineup data
        
        uses: lineups:
            https://stats.wnba.com/stats/leaguedashlineups
        
        IGNORES:
            GameScope, PlayerExperience, PlayerPosition,
             StarterBench, TopX, StatCategory, 
             TwoWay, PORound , PointDiff, 
             Country, ActiveFlag, AheadBehind, 
             ClutchTime, DraftPick,  GameID, 
             DraftYear, DistanceRange
        
        ACCEPTS:
            'DateTo', 'DateFrom', 'GroupQuantity', 
            'Season', 'Period', 'GameSegment', 
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'OpponentTeamID', 'PaceAdjust', 
            'PerMode', 'PlusMinus', 'SeasonSegment', 
            'SeasonType', 'VsConference', 'VsDivision', 
            'Conference', 'Division', 'ShotClockRange'
    
        Does not accept MeasureTypes: 'Usage','Defense'
        
        SAMPLE TABLES AND HEADERS:        
            'Lineups'
                'GROUP_SET', 'GROUP_ID', 'GROUP_NAME', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 
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

        '''
        requiredParams = {}
        
        for key in self.requiredParams:
            requiredParams[key] = self.requiredParams[key]
        
        requiredParams.update({'GroupQuantity': '5'})
        
        return self.search(self.endpoints['lineups'], requiredParams, params)            
           


