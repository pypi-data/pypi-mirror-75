import unittest
import cmath,math
import compi

import known_interval_tests

class TestGaussKronrod(known_interval_tests.TestFiniteIntevalIntegration):
    
    def routine_to_test(self,f,*args,**kwargs):
        return compi.gauss_kronrod(f,*args,**kwargs)

    def test_accept_ponts_parameter(self):
        self._accept_ketword_test('points',15)

    def test_invalid_number_of_points_raises_ValueError(self):
        def func(x):
            return 1j

        self.assertRaises(ValueError, self.routine_to_test,func,*self.default_range,points=17)

    def test_points_changes_result(self):
        def difficult_function(x):
            return (0.501+0.00000001j -x)**(-1.5)

        bad_result,*_= self.routine_to_test(difficult_function,*self.default_range,max_levels=1, points=15)
        good_result,*_ = self.routine_to_test(difficult_function,*self.default_range,max_levels=1, points=61)

        self.assertNotAlmostEqual(bad_result,good_result,places=self.tolerance)

    def test_full_output_contains_L1_norm_abscissa_and_weights(self):
        def func(x):
            return 1j

        _,_,diagnostics = self.routine_to_test(func,*self.default_range,full_output=True)

        self.assertSetEqual({"L1 norm", "abscissa", "weights"}, set(diagnostics.keys()))
        self.assertIsInstance(diagnostics["L1 norm"], float)
        self.assertIsInstance(diagnostics["abscissa"][0], float)
        self.assertIsInstance(diagnostics["weights"][0], float)

if __name__ == '__main__':
    unittest.main()