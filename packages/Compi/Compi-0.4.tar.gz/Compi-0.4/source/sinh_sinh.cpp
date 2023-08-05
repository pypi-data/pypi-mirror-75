#include "compi.hpp"

#include <complex>
#include <iostream>

#include <boost/math/quadrature/sinh_sinh.hpp>

extern "C" {
    #include "integration_routines.h"
}
#include "integration_routines_template.hpp"
#include "IntegrandFunctionWrapper.hpp"

struct SinhSinhParameters: public RoutineParametersBase {

    SinhSinhParameters(PyObject* routine_args, PyObject* routine_kwargs){
        constexpr auto keywords = generate_keyword_list<IntegralRange::infinite>();

        if(!PyArg_ParseTupleAndKeywords(routine_args,routine_kwargs,"O|OO$pId", const_cast<char**>(keywords.data()),
            &integrand,
            &args,&kw,
            &full_output,&max_levels,&tolerance)){
                throw could_not_parse_arguments("Unable to parse Python args to C variables");
        }
    }

    struct result_type: public RoutineParametersBase::result_type {
        size_t levels;
    };
};

auto run_integration_routine(const compi_internal::IntegrandFunctionWrapper& f, const SinhSinhParameters& parameters){
    SinhSinhParameters::result_type result;
    
    boost::math::quadrature::sinh_sinh<Real> integrator{static_cast<size_t>(parameters.max_levels)};

    result.result = integrator.integrate(f,parameters.tolerance,&result.err,&result.l1,&result.levels);

    return result;
}

extern "C" PyObject* sinh_sinh(PyObject* self, PyObject* args, PyObject* kwargs){
    return integration_routine<SinhSinhParameters>(args,kwargs);
}