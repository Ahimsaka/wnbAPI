#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:46:47 2019

####################################################################
####                                                            ####
####                        player module                       ####
####                                                            ####
####################################################################
    
This module houses the Search subclass Player.

Like Search, a Player object can be created with or without parameters:
    
    p = Player()

    or

    p = Player(PlayerID='203399', Season='2019'...etc...)

    or
    
    params = {'PlayerID'='203399', 'Season'='2019'...etc...}
    p = Player(**params)
    
Perform a search by calling any Player class method, with or without params. 

Player's methods may also be used without creating a Player object:
    
    Player().method(**params)
    
If no parameters are passed, default parameters are used and data is returned
relevant to the current 2019 WNBA Most Valuable Player, Elena Delle Donne. 

For information on the search history capabilities inherited from the Search 
method, please see the search module documentation. 
"""
import search

             
class Player(search.Search):
    '''
    Extends Search class with methods to access endpoints for player data.
    
    Player Methods:
        awards():
            https://stats.wnba.com/stats/playerawards?
        career():
            https://stats.wnba.com/stats/playercareerstats?
        gamelogs():
            https://stats.wnba.com/stats/playergamelogs
        shooting():
            https://stats.wnba.com/stats/playerdashboardbyshootingsplits?
        clutch():
            https://stats.wnba.com/stats/playerdashboardbyclutch?
        splits():
            https://stats.wnba.com/stats/playerdashboardbygeneralsplits?
        lastNGames():
            https://stats.wnba.com/stats/playerdashboardbylastngames?
        opponentSplits():
            https://stats.wnba.com/stats/playerdashboardbyopponent?
        teamPerformance():
            https://stats.wnba.com/stats/playerdashboardbyteamperformance?
        yearOverYear():
            https://stats.wnba.com/stats/playerdashboardbyyearoveryear?
        shotChartDetail() * inherited from Search superclass * 
            'https://stats.wnba.com/stats/shotchartdetail'
            
        Player Default Required Params:            
            {
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
            'PlayerID': '203399', # 2019 WNBA MVP Elena Delle Donne
             }
    '''
    def __init__(self, **params):
        search.Search.__init__(self, **params)
        # create dictionary of the endpoints assigned to each method. 
        # these could also have been stored inside each method. 
        # and that might have been a better choice, but I like
        # having a list of the accessible endpoints built into the
        # object. 
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
            'PlayerID': '203399', # 2019 WNBA MVP Elena Delle Donne
                }
               
    def awards(self, **params):
        '''
        function to get player awards. 

        uses: awards: 
            'https://stats.wnba.com/stats/playerawards
        
        ACCEPTS ONLY PlayerID & TeamID (TeamID filters the players
        records to only show records earned while playing for
        the listed team)
    
        IGNORES ALL OTHER INPUT
        
        
        SAMPLE TABLES AND HEADERS: 
            
        'PlayerAwards'
            'PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 
            'TEAM', 'DESCRIPTION', 'ALL_NBA_TEAM_NUMBER', 
            'SEASON', 'MONTH', 'WEEK', 
            'CONFERENCE', 'TYPE', 'SUBTYPE1', 
            'SUBTYPE2', 'SUBTYPE3', 

        '''
        return self.search(self.endpoints['awards'], self.requiredParams, params)
    
    def career(self, **params):
        '''
        function to get player career stats

        uses: career: 
            'https://stats.wnba.com/stats/playercareerstats
        
        ACCEPTS 
            PlayerID, TeamID, PerMode (PerGame, Totals)
                                                
        REJECTS PerMode - MinutesPer, Per48, Per40, 
                      Per36, PerMinute, PerPossession, 
                      PerPlay, Per100Possessions, Per100Plays
                      
        SAMPLE TABLES AND HEADERS:
            'SeasonTotalsRegularSeason'
            'SeasonTotalsPostSeason'
            'SeasonTotalsAllStarSeason'
                'PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 
                'GP', 'GS', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS', 


            'CareerTotalsRegularSeason'
            'CareerTotalsPostSeason'
            'CareerTotalsAllStarSeason'
                'PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 
                'GP', 'GS', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS', 


            'SeasonTotalsCollegeSeason'
                'PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 
                'ORGANIZATION_ID', 'SCHOOL_NAME', 'PLAYER_AGE', 
                'GP', 'GS', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS', 


            'CareerTotalsCollegeSeason'
                'PLAYER_ID', 'LEAGUE_ID', 'ORGANIZATION_ID', 
                'GP', 'GS', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS', 


            'SeasonRankingsRegularSeason'            
            'SeasonRankingsPostSeason'
                'PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 
                'GP', 'GS', 'RANK_PG_MIN', 
                'RANK_PG_FGM', 'RANK_PG_FGA', 'RANK_FG_PCT', 
                'RANK_PG_FG3M', 'RANK_PG_FG3A', 'RANK_FG3_PCT', 
                'RANK_PG_FTM', 'RANK_PG_FTA', 'RANK_FT_PCT', 
                'RANK_PG_OREB', 'RANK_PG_DREB', 'RANK_PG_REB', 
                'RANK_PG_AST', 'RANK_PG_STL', 'RANK_PG_BLK', 
                'RANK_PG_TOV', 'RANK_PG_PTS', 'RANK_PG_EFF', 
 
        '''
        return self.search(self.endpoints['career'], self.requiredParams, params)

    def gamelogs(self, **params):
        '''
        function to get player gamelogs
 
        uses: gamelogs: 
            'https://stats.wnba.com/stats/playergamelogs       
        
        UNTESTED: Height, Weight, Country, 

        does not play well with DateTo or DateFrom. 

        REJECTS: MeasureType: Usage, Defense

        IGNORES: 
            LastNGames, PaceAdjust, PerMode,
            PlusMinus, Rank, GameScope, 
            PlayerExperience, PlayerPosition, StarterBench, 
            TopX, Conference, Division, 
            GroupQuantity, StatCategory, TwoWay, 
            Scope, PORound, PointDiff,
            ActiveFlag, AheadBehind, ClutchTime,
            DraftPick, DraftYear, DistanceRange
                          
        AFFECTED by:
            'DateFrom', 'DateTo', 'GameSegment', 
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID', 
            'PerMode','Period', 'SeasonSegment',
            'SeasonType','VsConference, 'VsDivision', 
            'Season', 'ShotClockRange'
    
        SAMPLE TABLES AND HEADERS: 
            'PlayerGameLogs'
                'SEASON_YEAR', 'PLAYER_ID', 'PLAYER_NAME', 
                'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 
                'GAME_ID', 'GAME_DATE', 'MATCHUP', 
                'WL', 'MIN', 'FGM', 
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
                'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 
                'TD3_RANK', 

        '''
        return self.search(self.endpoints['gamelogs'], self.requiredParams, params)
        
    def shooting(self, **params):
        '''
        function to get player shooting dashboard
        
        uses: shooting: 
            'https://stats.wnba.com/stats/playerdashboardbyshootingsplits

        PARAMS UNTESTED
        
        SAMPLE TABLES AND HEADERS: 
            'OverallPlayerDashboard'
            'Shot5FTPlayerDashboard'
            'Shot8FTPlayerDashboard'
            'ShotAreaPlayerDashboard'
            'AssitedShotPlayerDashboard'
            'ShotTypePlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'FGM', 
                'FGA', 'FG_PCT', 'FG3M', 
                'FG3A', 'FG3_PCT', 'EFG_PCT', 
                'BLKA', 'PCT_AST_2PM', 'PCT_UAST_2PM', 
                'PCT_AST_3PM', 'PCT_UAST_3PM', 'PCT_AST_FGM', 
                'PCT_UAST_FGM', 'FGM_RANK', 'FGA_RANK', 
                'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
                'FG3_PCT_RANK', 'EFG_PCT_RANK', 'BLKA_RANK', 
                'PCT_AST_2PM_RANK', 'PCT_UAST_2PM_RANK', 'PCT_AST_3PM_RANK', 
                'PCT_UAST_3PM_RANK', 'PCT_AST_FGM_RANK', 'PCT_UAST_FGM_RANK', 
                'CFID', 'CFPARAMS', 

            'ShotTypeSummaryPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'FGM', 
                'FGA', 'FG_PCT', 'FG3M', 
                'FG3A', 'FG3_PCT', 'EFG_PCT', 
                'BLKA', 'PCT_AST_2PM', 'PCT_UAST_2PM', 
                'PCT_AST_3PM', 'PCT_UAST_3PM', 'PCT_AST_FGM', 
                'PCT_UAST_FGM', 'CFID', 'CFPARAMS', 

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
            
        '''
        return self.search(self.endpoints['shooting'], self.requiredParams, params)
    
    def clutch(self, **params):
        '''
        function to get player dashboard by clutch    
        
        uses: clutch: 
            'https://stats.wnba.com/stats/playerdashboardbyclutch
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX, 
            Conference, Division, GroupQuantity, 
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, Country, 
            ActiveFlag, AheadBehind, ClutchTime, 
            DraftPick, DraftYear, GameID, 
            DistanceRange
              
        ACCEPTS: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID',
            'PaceAdjust', 'PerMode', 'Period',
            'PlusMinus','SeasonSegment','SeasonType',
            'VsConference','VsDivision','Season',
            'ShotClockRange'
    
        MeasureType does not accept Four Factors, Opponent, or Defense. 
    
        SAMPLE TABLES AND HEADERS:
            'OverallPlayerDashboard'            
            'Last5Min5PointPlayerDashboard'
            'Last3Min5PointPlayerDashboard'
            'Last1Min5PointPlayerDashboard'
            'Last30Sec3PointPlayerDashboard'
            'Last10Sec3PointPlayerDashboard'
            'Last5MinPlusMinus5PointPlayerDashboard'
            'Last3MinPlusMinus5PointPlayerDashboard'
            'Last1MinPlusMinus5PointPlayerDashboard'
            'Last30Sec3Point2PlayerDashboard'
            'Last10Sec3Point2PlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'GP', 
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
        return self.search(self.endpoints['clutch'], self.requiredParams, params)
    
    def splits(self, **params):
        '''
        function to get player dashboard by general splits
        
        uses: splits: 
            'https://stats.wnba.com/stats/playerdashboardbygeneralsplits        
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX, 
            Conference, Division, GroupQuantity,
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, Country, 
            ActiveFlag, AheadBehind, ClutchTime, 
            DraftPick, DraftYear, GameID, 
            DistanceRange
              
        AFFECTED BY: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames','Location', 'MeasureType',
             'Month', 'Outcome', 'OpponentTeamID', 
             'PaceAdjust', 'PerMode', 'Period',
             'PlusMinus', 'SeasonSegment',' SeasonType',
             'VsConference', 'VsDivision', 'Season',
             'ShotClockRange'
        
        MeasureType does not accept Four Factors, Opponent, or Defense. 
        
        TABLES AND HEADERS:
            'OverallPlayerDashboard'
            'LocationPlayerDashboard'
            'WinsLossesPlayerDashboard'
            'MonthPlayerDashboard'
            'PrePostAllStarPlayerDashboard'
            'StartingPosition'
            'DaysRestPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'GP', 
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
        return self.search(self.endpoints['splits'], self.requiredParams, params)

    def lastNGames(self, **params):
        '''
        function to get player dashboard by last N games

        uses: lastNGames: 
            'https://stats.wnba.com/stats/playerdashboardbylastngames
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench,
            TopX, Conference, Division, 
            GroupQuantity, StatCategory, TwoWay,
            Scope, PORound, PointDiff, 
            Country, ActiveFlag, AheadBehind,
            ClutchTime, DraftPick, DraftYear, 
            GameID, DistanceRange
              
        AFFECTED BY: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID',
            'PaceAdjust', 'PerMode', 'Period',
            'PlusMinus', 'SeasonSegment', 'SeasonType',
            'VsConference', 'VsDivision', 'Season',
            'ShotClockRange'
    
        MeasureType does not accept Four Factors, Opponent, or Defense. 
    
                                    ***note*** 
        Despite the name, LastNGames parameter does not affect this 
        endpoint's return. Rather, this dashboard returns stats that 
        fit other params, grouped by Last 5, 10, 15, 20 games 
        as well as in batches of Games 1-10, 11-20, 21-30, 31-40     
        
        SAMPLE TABLES AND HEADERS: 
            'OverallPlayerDashboard'
            'Last5PlayerDashboard'
            'Last10PlayerDashboard'
            'Last15PlayerDashboard'
            'Last20PlayerDashboard'
            'GameNumberPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'GP', 
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
        return self.search(self.endpoints['lastNGames'], self.requiredParams, params)
    
    def opponentSplits(self, **params):
        '''
        function to get player dashboard by opponent splits

        uses: opponentSplits: 
            'https://stats.wnba.com/stats/playerdashboardbyopponent
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX, 
            Conference, Division, GroupQuantity, 
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, Country, 
            ActiveFlag, AheadBehind, ClutchTime, 
            DraftPick, DraftYear, GameID, DistanceRange
              
        AFFECTED BY:
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames','Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID',
            'PaceAdjust', 'PerMode', 'Period',
            'PlusMinus', 'SeasonSegment', 'SeasonType',
            'VsConference', 'VsDivision', 'Season',
            'ShotClockRange'
        
        MeasureType does not accept Four Factors, Opponent, or Defense. 
        
        SAMPLE TABLES AND HEADERS:
            'OverallPlayerDashboard'     
            'ConferencePlayerDashboard'
            'DivisionPlayerDashboard'
            'OpponentPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'GP', 
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
        return self.search(self.endpoints['opponentSplits'], self.requiredParams, params)
    
    def teamPerformance(self, **params):
        '''
        function to get player dashboard by team performance

        uses: teamPerformance: 
            'https://stats.wnba.com/stats/playerdashboardbyteamperformance
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX, 
            Conference, Division, GroupQuantity, 
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, Country, 
            ActiveFlag, AheadBehind, ClutchTime, 
            DraftPick, DraftYear, GameID, 
            DistanceRange
              
        AFFECTED BY: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID',
            'PaceAdjust', 'PerMode', 'Period',
            'PlusMinus', 'SeasonSegment', 'SeasonType',
            'VsConference', 'VsDivision', 'Season',
            'ShotClockRange'
    
        MeasureType does not accept Four Factors, Opponent, or Defense. 

        SAMPLE TABLES AND HEADERS:
            'OverallPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'GP', 
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
                
            'ScoreDifferentialPlayerDashboard'     
            'PointsScoredPlayerDashboard'
            'PontsAgainstPlayerDashboard' 
                'GROUP_SET', 'GROUP_VALUE_ORDER', 'GROUP_VALUE', 
                'GROUP_VALUE_2', 'GP', 'W', 
                'L', 'W_PCT', 'MIN', 
                'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 
                'FTM', 'FTA', 'FT_PCT', 
                'OREB', 'DREB', 'REB', 
                'AST', 'TOV', 'STL', 
                'BLK', 'BLKA', 'PF', 
                'PFD', 'PTS', 'PLUS_MINUS', 
                'NBA_FANTASY_PTS', 'DD2', 'TD3', 
                'GP_RANK', 'W_RANK', 'L_RANK', 
                'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 
                'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 
                'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 
                'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 
                'DREB_RANK', 'REB_RANK', 'AST_RANK', 
                'TOV_RANK', 'STL_RANK', 'BLK_RANK', 
                'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 
                'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 
                'DD2_RANK', 'TD3_RANK', 'CFID', 
                'CFPARAMS',          
        '''
        return self.search(self.endpoints['teamPerformance'], self.requiredParams, params)
    
    def yearOverYear(self, **params):
        '''
        function to get player dashboard by year over year

        uses: yearOverYear: 
            'https://stats.wnba.com/stats/playerdashboardbyyearoveryear
        
        IGNORES:
            Rank, GameScope, PlayerExperience, 
            PlayerPosition, StarterBench, TopX, 
            Conference, Division, GroupQuantity, 
            StatCategory, TwoWay, Scope, 
            PORound, PointDiff, Country, 
            ActiveFlag, AheadBehind, ClutchTime, 
            DraftPick, DraftYear, GameID, 
            DistanceRange          
    
        ACCEPTS: 
            'DateTo', 'DateFrom', 'GameSegment',
            'LastNGames', 'Location', 'MeasureType',
            'Month', 'Outcome', 'OpponentTeamID',
            'PaceAdjust', 'PerMode', 'Period',
            'PlusMinus', 'SeasonSegment', 'SeasonType',
            'VsConference', 'VsDivision', 'Season',
            'ShotClockRange' 
    
        MeasureType does not accept Four Factors, Opponent, or Defense. 

        SAMPLE TABLES AND HEADERS:    
            'OverallPlayerDashboard'
            'ByYearPlayerDashboard'
                'GROUP_SET', 'GROUP_VALUE', 'TEAM_ID', 
                'TEAM_ABBREVIATION', 'MAX_GAME_DATE', 'GP', 
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
        return self.search(self.endpoints['yearOverYear'], self.requiredParams, params)
    
    
def __main__():
    pass
