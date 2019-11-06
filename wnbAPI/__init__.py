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

It was created because reading about statistical analysis was my own avenue
to becoming a passionate basketball fan. I feel that the WNBA is putting out
an extraordinary basketball product, and that lowering the bar for those
who are interested in performing statistical analysis on the W can be a 
wonderful way to bring new readers and viewers to the sport and the league. 

Though there were a handful of existing packages to access WNBA stats
when I began work on wnbAPI, I found that, as a rule, these were NBA
tools that were converted to WNBA tools after-the-fact, when the authors
realized that the two leagues share a backend system for statistics. As 
a result, the default parameters for these packages very rarely successfully
pulled any data. Additionally, some of these packages seemed to mandate that 
all parameters be input as arguments for every search. With around 30 params
available at each endpoint, this is a lot of work, and seems barely more
useful than typing out the URL string manually. These inadequacies led me
to develop my own tool from scratch with the following goals:
    
    - wnbAPI should be a tailored solution that prioritizes the W. 
    - wnbAPI should allow users to quickly create a search.
    - wnbAPI should include sensible parameter defaults so that only.
      the specifically desired parameters need be entererd by the user.
    - wnbAPI should allow searches with no parameter input, and should.
      return a valid data set for these searches. 
    - wnbAPI should be sufficiently simple to allow a user with no prior.
      coding experience to obtain the information they are looking for
      in less than 10 minutes.
    
I hope that eventual collaboration with the authors of the existing tools
will be possible, as we build a community around the complex numbers
involved in this incredible sport. In particular, I would like to 
thank the authors of py_ball, whose documentation was invaluable in the 
creation of wnbAPI. 

Planned future development of wnbAPI focuses on the addition of several
additional features aimed at not only ease of access, but also allowing
users to easily process, interpret, and visualize the data gathered. Intended
improvements include:
    - Data vizualization macros to create vizualizations that can
      quickly and easily be inserted into HTML.
    - Methods to calculate derivative advanced stats.
    - Methods to compare groups of players against one another (separate 
      from the existing parameters that allow queries for multiple players).
    - Methods to search large datasets for statistical anomalies based on
      standard deviation. 
    - Most likely we will eventually add methods to generate CSVs with the
      collected data. However, this is a very low priority, because
      the package already integrates pandas DataFrames, which have
      a built in method to generate csv files. That isn't my ideal
      solution, but since the functionality exists I'd rather focus 
      on new tools before refactoring the csv option. 

The package currently consists of four main objects, all subclasses of a Search class. 
These are:
    
    Player()
    Team()
    League()
    Game()
    
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

