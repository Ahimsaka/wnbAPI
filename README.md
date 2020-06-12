# wnbAPI

This project utilized the same backend API that powers searches on stats.wnba.com to scrape and process data for WNBA games, players, and teams. It included pandas integration, and some basic tools for automating generation of interactive shot chart svgs. It was intended to make wnba data analytics easier for independent bloggers & analysts to help grow the WNBA data analytics community.

Unfortunately, the WNBA (and NBA) stats API was revised after the project's most recent commit, so it is no longer expected to work. There are no current plans to refactor.

The base Search class contains logic for setting search parameters, submitting HTTP requests, storing and navigating session history (to review old results or return to previous parameters), converting json results to pandas dataframes, and accessing a few specific endpoints which could apply to any subclass. 

Subclasses for Game, League, Player, and Team contain specific endpoint methods for searches related to the class type. Each instance of any subtype holds its own result and parameter history, making it easy to query multiple endpoints with the same set of parameters and hold all results for comparison. 
