import unittest

import compi
import known_interval_tests


class TestTrapiziodal(known_interval_tests.TestFiniteIntevalIntegration):
    def setUp(self):
        super().setUp()
        self.tolerance = 6

    def routine_to_test(self,f,*args,**kwargs):
        return compi.trapezoidal(f,*args,**kwargs)

    def test_full_output_contains_l1_norm(self):
        _,_,diagnostics = self.routine_to_test(self.func,*self.default_range,full_output=True)        

        self.assertSetEqual({"L1 norm"}, set(diagnostics.keys()))
        self.assertIsInstance(diagnostics["L1 norm"], float)