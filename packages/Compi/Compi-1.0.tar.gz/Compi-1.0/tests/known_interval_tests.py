
import unittest
import cmath,math
pi = math.pi

from integration_routine_tests import TestIntegrationRoutine

class TestFiniteIntevalIntegration(TestIntegrationRoutine):
    
    # Note the purpose of these tests is not to test the unerlying
    # Integration library, it is to test the python wrapper. Consequently
    # we have not tried to find particularly difficult functions
    # for the quadrature routine to compute. 

    def setUp(self):
        super().setUp()
        self.default_range = (-1.0,1.0)

    def func(self,x):
        return 1j

    def test_exp_integral(self):
        '''
        tests that the integral of exp(i x) ~ 0 over 1 period
        '''
        result, *_ = self.routine_to_test(lambda x: cmath.exp(1j*x), 0, 2*pi)
        self.assertAlmostEqual(result.real,0.0,places=self.tolerance)
        self.assertAlmostEqual(result.imag,0.0,places=self.tolerance)

    def test_quadratic_integral(self):
        '''
        checks that the integal of a simple quadratic function is correct
        '''
        result, *_ = self.routine_to_test(lambda x: 3*(x-1j)**2, 0.0,1.0)
        expected_result = ( (1-1j)**3 ) - ( (-1j)**3 )
        self.assertAlmostEqual(result.real,expected_result.real,places=self.tolerance)
        self.assertAlmostEqual(result.imag,expected_result.imag,places=self.tolerance)

    def test_positivity_of_complicated_integral(self):
        '''
        Integrates a function with positive real and imaginary parts.
        Checks that the result of the integral also has positive real and
        imaginary parts
        '''
        def complicated_func(x):
            return math.exp(x) + 1j* math.exp(x**2)

        result, *_ = self.routine_to_test(complicated_func, 0, 5)
        self.assertGreater(result.real,0.0)
        self.assertGreater(result.imag,0.0)

class TestInfiniteIntegration(TestIntegrationRoutine):

    def setUp(self):
        super().setUp()
        self.default_range = ()

    def func(self,x):
        return (x-5j)**(-2)

    def test_gaussian_integral(self):
        '''
        checks the gaussian itegral
        '''
        def gaussian(x):
            '''
            A gaussian function, written to avoid overflow errors at large arguments
            '''
            if x > 0:
                return cmath.exp(-(0.5+0.5j)*x)**x 
            else:
                return cmath.exp((0.5+0.5j)*x)**-x

        result, *_ = self.routine_to_test(gaussian)
        squared_result = result**2 # Squared result used to avoid ambiguity with multivaluedness of complex square root
        expected_squared_result = 2 * pi / (1+1j) 
        self.assertAlmostEqual(squared_result.real,expected_squared_result.real,places=self.tolerance)
        self.assertAlmostEqual(squared_result.imag,expected_squared_result.imag,places=self.tolerance)

    def test_lorenzian_integral(self):
        '''
        Checks the integral of a lorenzian with a complex pole vanishes
        '''
        result, *_ = self.routine_to_test(lambda x: (x-5j)**-2)
        self.assertAlmostEqual(result.real,0.0,places=self.tolerance)
        self.assertAlmostEqual(result.imag,0.0,places=self.tolerance)

    def test_positivity_of_complicated_integral(self):
        '''
        Integrates a function with positive real and imaginary parts.
        Checks that the result of the integral also has positive real and
        imaginary parts
        '''

        def complicated_func(x):
            return cmath.exp(-abs(x)) + 1j*cmath.exp(-5*abs(x))

        result, *_ = self.routine_to_test(complicated_func)
        self.assertGreater(result.real,0.0)
        self.assertGreater(result.imag,0.0)

    def test_VauleError_if_integrand_does_not_tend_to_zero(self):

        def does_not_tend_to_zero(x):
            return 1j

        self.assertRaises(ValueError,self.routine_to_test,does_not_tend_to_zero)
        self.assertRaises(ValueError,self.routine_to_test,lambda x: cmath.exp(1j*x))

class TestSemiInfiniteIntegration(TestIntegrationRoutine):

    def setUp(self):
        super().setUp()
        self.default_range = (0.0,)

    def func(self,x):
        return cmath.exp((-1+1j) * x)

    def test_power_law(self):
        def power_law(x):
            return 1j*(1.0/(x+1))**2

        result, *_ = self.routine_to_test(power_law,0.0)

        self.assertAlmostEqual(result.real,0.0, places=self.tolerance)
        self.assertAlmostEqual(result.imag,1.0, places=self.tolerance)


    def test_exp(self):
        result, *_ = self.routine_to_test(lambda x: 1j*cmath.exp(-x),0.0)
        self.assertAlmostEqual(result.real,0.0,places=self.tolerance)
        self.assertAlmostEqual(result.imag,1.0,places=self.tolerance)

    def test_positivity_of_complicated_integral(self):
        '''
        Integrates a function with positive real and imaginary parts.
        Checks that the result of the integral also has positive real and
        imaginary parts
        '''

        def complicated_func(x):
            return (x+1)**-2 + 1j*cmath.exp(-5*x)

        result, *_ = self.routine_to_test(complicated_func,*self.default_range)
        self.assertGreater(result.real,0.0)
        self.assertGreater(result.imag,0.0)