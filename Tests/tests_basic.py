#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:19:45 2019

@author: devinarnold
"""
from .context import wnbAPI
#from context import wnbAPI
import unittest # import unittest module
                #    - see docs.python.org/3/library/unittest.html

########################################################################
####                                                                ####
####                       basic tests module                       ####
####                                                                ####
########################################################################

####################################################################
####                                                            ####
####                    search module tests                     ####
####                                                            ####
####################################################################
'''
Blackbox test all functions of the search module, creating Search object, 
and all Search object methods.
'''
################################################################
####                                                        ####
####                   search.logo function tests           ####
####                                                        ####
################################################################
'''
Test should call search.logo() with no arguments (accepts none).
       
Expected return value should be a response object. 
    - Response object should have status code 200
    - Response object should always include the same URL
    - Response object.content should be a bits encoded svg file.
'''
################################################################
####                                                        ####
####                   search.logo2 tests                   ####
####                                                        ####
################################################################
'''
Test should call search.logo2() with no arguments (accepts none).
        
Expected return value should be a response object. 
    - Response object should have status code 200
    - Response object should always include the same URL
    - Response object.content should be a bits encoded svg file.
'''
################################################################
####                                                        ####
####                  search.nbaLogo tests                  ####
####                                                        ####
################################################################
'''
Test should call search.nbnLogo() with no arguments (accepts none).
     
Expected return value should be a response object. 
    - Response object should have status code 200
    - Response object should always include the same URL
    - Response object.content should be a bits encoded svg file.
'''
################################################################
####                                                        ####
####                 search.teamLogo tests                  ####
####                                                        ####
################################################################
'''
Test should call search.teamLogo() with no arguments (accepts none).
        
Expected return value should be a response object. 
    - Response object should have status code 200
    - Response object should always return the same URL template, 
      with the appropriate team shortcode included. 
    - Response object.content should be a bits encoded svg file.
'''
################################################################
####                                                        ####
####              search.Search() object TestCase           ####
####                                                        ####
################################################################

class TestSearchObjectCreation(unittest.TestCase):
    '''
    This TestCase should include tests to create a Search object. 
       - Search object should initialize with:
           self.endpoints == {}
           self.params == {}
           self.requiredParams == {}
           self.pointer == {}
           self.data == {}
           self.history == []
           self.index == 0
    '''
    def setUp(self):
        '''
        set up test environment for all TestSearchObject test
        '''
        self.session = wnbAPI.Search()
    
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
    
    def test_initial_values(self):
        '''
        Test that Search object is created with expected default
        values:
        
        self.endpoints == {}
        self.params == {}
        self.required_params == {}
        self.pointer == {}
        self.data == {}
        self.history == []
        self.index == 0
        '''
        self.assertEqual(self.session.endpoints, {})
        self.assertEqual(self.session.params,{})
        self.assertEqual(self.session.required_params, {})
        self.assertEqual(self.session.pointer,{})
        self.assertEqual(self.session.data, {})
        self.assertEqual(self.session.history,[])
        self.assertEqual(self.session.index, 0)
     
class TestSearchObjectMethods(unittest.TestCase):
    '''
    This TestCase should include tests to create a Search object. 
       - Search object should initialize with:
           self.endpoints == {}
           self.params == {}
           self.requiredParams == {}
           self.pointer == {}
           self.data == {}
           self.history == []
           self.index == 0
        
    This test set should include tests for each individual Search
    object method. 
    '''
    def setUp(self):
        '''
        set up test environment for all TestSearchObjectMethod tests
        
        create Search object and set to self.session
        
        fill the search object's history with appropriate
        values (set explicitly rather than via object's methods,
        so that a bug in one of the setter methods doesn't 
        break tests that aren't for that method)
        '''
        self.session = wnbAPI.Search()
        # on the subclass tests we'll perform real searches to fill the 
        # history and objects and such. 
        self.session.history=[('Test', 1), ('Test', 2),('Test', 3)]
        self.session.data = {('Test', 1): ({'paramsdict1': ''}, {'datadict1': ''}), 
                             ('Test', 2): ({'paramsdict2': ''}, {'datadict2': ''}), 
                             ('Test', 3): ({'paramsdict3': ''}, {'datadict3': ''})}
        self.session.index = 2
        self.session.pointer = self.session.data[self.session.history[self.session.index]]
        self.session.params = {'paramsdict3': ''}
        
            
    def tearDown(self):
        '''
        tear down test environment for TestSearchObject test
        '''
        del self.session
    
    def test_back_method(self):
        '''
        test the .back() method of the Search object. 
        '''
        self.session.back() 
        self.assertEqual(self.session.index,  1) 
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[1]][1])
        self.session.back()
        self.assertEqual(self.session.index, 0)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[0]][1])
        self.session.back()
        self.assertEqual(self.session.index, 2)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[2]][1])
        
    def test_forw_method(self):
        '''
        test the .forw() method of the Search object.
        '''
        self.session.forw() 
        self.assertEqual(self.session.index,  0) 
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[0]][1])
        self.session.forw()
        self.assertEqual(self.session.index, 1)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[1]][1])
        self.session.forw()
        self.assertEqual(self.session.index, 2)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[2]][1])
        
    def test_back_and_forw_methods(self):
        '''
        test both back() and forw() in conjunction
        '''
        self.session.forw() 
        self.assertEqual(self.session.index,  0) 
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[0]][1])
        self.session.forw()
        self.assertEqual(self.session.index, 1)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[1]][1])
        self.session.back()
        self.assertEqual(self.session.index, 0)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[0]][1])  
        self.session.back()
        self.assertEqual(self.session.index, 2)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[2]][1]) 
        self.session.forw()
        self.assertEqual(self.session.index,  0) 
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[0]][1])
        self.session.back()
        self.assertEqual(self.session.index, 2)
        self.assertEqual(self.session.pointer, \
                         self.session.data[self.session.history[2]][1]) 
   
    def test_dataframe_method(self):
        '''
        test pandas dataframe integration
        '''
        # first summon a real data set so you can get headers. 
        self.session.search('https://stats.wnba.com/stats/teamdetails', {}, {'TeamID':'1611661322'})
        
        #import pandas to get generic dataframe for type testing
        import pandas
                
        # details returns multiple resultsets, so it is expected to return a
        # dictionary of data frames.
        # test that df is a dict
        self.assertEqual(type(self.session.dataFrame()), dict)
        
        # test that one of the expected key values contains
        # a pandas data frame 
        self.assertEqual(type(self.session.dataFrame()['TeamBackground']), type(pandas.DataFrame()))

    def test_getpointer_method(self): 
        '''
        test getPointer() method
        '''
        # call getPointer() and check that expected value is returned
        self.assertEqual(self.session.getPointer(), ({'paramsdict3': ''},
                                                     {'datadict3': ''}))
        
        # call getPointer() and check that it matches value stored in pointer
        self.assertEqual(self.session.getPointer(), self.session.pointer)
        
    def test_getparams_method(self):
        '''
        test getParams() method
        '''
        # call getParams() and check that expected value is returned
        self.assertEqual(self.session.getParams(), {'paramsdict3': ''})
        
        # also confirm that getParams returns the same value as 
        # is stored in self.session.params
        self.assertEqual(self.session.getParams(), self.session.params)
    
    def test_getparamlist_method(self):
        '''
        test getParamList() method
        
        this test is barely necessary. this method is a very 
        minor convenience function. 
        '''
        # test that the params list returned is a dict
        # 
        self.assertEqual(type(self.session.getParamList()), dict)
    
    def test_getpointerparams_method(self):
        '''
        test getPointerParams() method
        '''
        # call getPointerParams() and test that it matches expected value
        self.assertEqual(self.session.getPointerParams(),  {'paramsdict3': ''})
        
        # call back() and get the params again
        self.session.back()
        self.assertEqual(self.session.getPointerParams(), {'paramsdict2': ''})
    
    def test_setpointerparams_method(self):
        '''
        test setPointerParams() method
        '''
        self.session.index = 0
        self.session.setPointerParams()
        self.assertEqual(self.session.params, {'paramsdict1': ''})
        
    
    def test_setparams_method(self):
        '''
        test setParams() method
        '''
        # call setParams() to set new params
        self.session.setParams({'new':1, 'paramsdict3': 'horses'})
        # setParams() uses params.update - it shouldn't remove any
        # existing params. 
        self.assertEqual(self.session.params, {'paramsdict3': 'horses', 'new': 1})
    
    def test_clearparams_method(self):
        '''
        test clearParams() method. 
        '''
        self.session.clearParams()
        self.assertEqual(self.session.getParams(), {})
        self.assertEqual(self.session.params, {})        
        
    def test_shotchartdetail_method(self):
        '''
        Test shotchartDetail() method
        
        this method is a unique method because it is the only
        endpoint access method on the superclass, and the only one that
        calls the Search.search() method. 
        
        As a consequence, this method will always fail if Search.search()
        is not working correctly. If both methods are failing, always
        debug Search.search() before debugging shotchartdetail. 
        '''
        
        ############################################################
        ####                                                    ####
        ####       Search.getRequiredParams() method test       ####
        ####                                                    ####
        ############################################################
        ############################################################
        ####                                                    ####
        ####            Search.search() method test             ####
        ####                                                    ####
        ############################################################
        
        ############################################################
        ####                                                    ####
        ####        Search.shotChartDetail() method test        ####
        ####                                                    ####
        ############################################################


####################################################################
####                                                            ####
####                    player module tests                     ####
####                                                            ####
####################################################################

####################################################################
####                                                            ####
####                     team module tests                      ####
####                                                            ####
####################################################################

####################################################################
####                                                            ####
####                    league module tests                     ####
####                                                            ####
####################################################################
