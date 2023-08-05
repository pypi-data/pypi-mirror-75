import unittest

import compi
import known_interval_tests

class TestTanhSinh(known_interval_tests.TestFiniteIntevalIntegration):
    def routine_to_test(self,f,*args,**kwargs):
        return compi.tanh_sinh(f,*args,**kwargs)

    def test_full_output_contains_L1_norm_levels(self):
        _,_,diagnostics = self.routine_to_test(self.func,*self.default_range,full_output=True)

        self.assertSetEqual({"L1 norm", "levels"}, set(diagnostics.keys()))
        self.assertIsInstance(diagnostics["L1 norm"], float)
        self.assertIsInstance(diagnostics["levels"], int)

if __name__ == '__main__':
    unittest.main()