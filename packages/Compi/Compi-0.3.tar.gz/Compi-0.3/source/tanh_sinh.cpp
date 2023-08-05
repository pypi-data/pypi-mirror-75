#include "compi.hpp"

#include <complex>

#include <boost/math/quadrature/tanh_sinh.hpp>

#include "integration_routines_template.hpp"
#include "IntegrandFunctionWrapper.hpp"

extern "C" {
    #include "integration_routines.h"
}

struct TanhSinhParameters: public RoutineParametersBase {
    Real x_min;
    Real x_max;

    TanhSinhParameters(PyObject* routine_args, PyObject* routine_kwargs){
        constexpr auto keywords = generate_keyword_list<IntegralRange::finite>();

        if(!PyArg_ParseTupleAndKeywords(routine_args,routine_kwargs,"Odd|OO$pId",const_cast<char**>(keywords.data()),
                &integrand,&x_min,&x_max,
                &args,&kw,
                &full_output, &max_levels,&tolerance)){
            throw could_not_parse_arguments("Unable to parse python arguments to C variables");
        }
    }

    struct result_type:public RoutineParametersBase::result_type {
        size_t levels;
    };
};

TanhSinhParameters::result_type run_integration_routine(const compi_internal::IntegrandFunctionWrapper& f,const TanhSinhParameters& parameters){
    auto integrator = boost::math::quadrature::tanh_sinh<Real>(static_cast<size_t>(parameters.max_levels));
    TanhSinhParameters::result_type result;

    result.result =  integrator.integrate(f,parameters.x_min,parameters.x_max,parameters.tolerance,&(result.err),&(result.l1),&(result.levels));

    return result;
}


extern "C" PyObject* tanh_sinh(PyObject* self, PyObject* args, PyObject* kwargs){
    return integration_routine<TanhSinhParameters>(args,kwargs);
}
