import abc
import unittest

class IntegrationRoutineTestsBase(abc.ABC, unittest.TestCase):
    @abc.abstractclassmethod
    def routine_to_test(self,f,*args,**kwargs):
        pass

    @abc.abstractclassmethod
    def func(self,x):
        pass

    def setUp(self):
        self.default_range = ()
        self.positional_args = 0
        self.tolerance = 7 #number of dp