import unittest
import cmath

import compi
import known_interval_tests

class TestExpSinh(known_interval_tests.TestSemiInfiniteIntegration):
    def routine_to_test(self,f,*args,**kwargs):
        return compi.exp_sinh(f,*args,**kwargs)

    def test_full_output_contains_L1_norm_levels(self):
        _,_,diagnostics = self.routine_to_test(self.func,*self.default_range,full_output=True)

        self.assertSetEqual({"L1 norm", "levels"}, set(diagnostics.keys()))
        self.assertIsInstance(diagnostics["L1 norm"], float)
        self.assertIsInstance(diagnostics["levels"], int)

    def test_accept_inteval_ininifty_by_position(self):
        self._accept_ketword_test("interval_infinity",+1)
        self.assertIsNotNone(self.routine_to_test(lambda x: 1j*cmath.exp(x),*self.default_range,None,None,-1))

    def test_accept_interval_infinity_keyword(self):
        self._accept_ketword_test("interval_infinity",+1)
        self.assertIsNotNone(self.routine_to_test(lambda x: 1j*cmath.exp(x),*self.default_range,**{"interval_infinity":-1}))

    def test_positional_interval_infinity_changes_result(self):
        def asymmetric_function(x):
            return (1.0/(x-5+1j))**2 + (1.0/(x-2j))**3

        result1,*_ = self.routine_to_test(asymmetric_function, *self.default_range)
        result2,*_ = self.routine_to_test(asymmetric_function, *self.default_range, None,None,-1)

        self.assertNotAlmostEqual(result1.real,result2.real,places=self.tolerance)
        self.assertNotAlmostEqual(result1.imag,result2.imag,places=self.tolerance)

    def test_interval_infinity_keyword_changes_result(self):
        def asymmetric_function(x):
            return (1.0/(x-5+1j))**2 + (1.0/(x-2j))**3

        result1,*_ = self.routine_to_test(asymmetric_function, *self.default_range)
        result2,*_ = self.routine_to_test(asymmetric_function, *self.default_range, interval_infinity=-1)

        self.assertNotAlmostEqual(result1.real,result2.real,places=self.tolerance)
        self.assertNotAlmostEqual(result1.imag,result2.imag,places=self.tolerance)

    def test_interval_infinity_changes_sign_of_odd_intergral(self):
        '''
        Check that changing interval infinity is probably doing what we expect by putting in an integral where 
        the result on the 2 semi-infinite ranges are simply related
        '''
        def odd_function(x):
            return 1j*x*cmath.exp(-abs(x))

        pos_result,*_ = self.routine_to_test(odd_function,0.0,interval_infinity=+1)
        neg_result,*_ = self.routine_to_test(odd_function,0.0,interval_infinity=-1)

        self.assertAlmostEqual(pos_result.real, -neg_result.real, places=self.tolerance)
        self.assertAlmostEqual(pos_result.imag, -neg_result.imag, places=self.tolerance)

    def test_ValueError_if_interval_infinity_0(self):
        self.assertRaises(ValueError,self.routine_to_test,self.func,*self.default_range,interval_infinity=0)

if __name__ == '__main__':
    unittest.main()