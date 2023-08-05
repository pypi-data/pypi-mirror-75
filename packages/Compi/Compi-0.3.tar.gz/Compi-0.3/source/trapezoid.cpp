#include "compi.hpp"

#include <limits>

#include <boost/math/quadrature/trapezoidal.hpp>

extern "C" {
    #include "integration_routines.h"
}
#include "integration_routines_template.hpp"
#include "IntegrandFunctionWrapper.hpp"

struct TrapezoidParamerters: public RoutineParametersBase {
    Real x_min, x_max;

    TrapezoidParamerters(PyObject* routine_args, PyObject* routine_kwargs):RoutineParametersBase{std::numeric_limits<Real>::epsilon(),12}{
        constexpr auto keywords = generate_keyword_list<IntegralRange::finite>();


        if(!PyArg_ParseTupleAndKeywords(routine_args,routine_kwargs,"Odd|OO$pId",const_cast<char**>(keywords.data()),
                &integrand,&x_min,&x_max,
                &args,&kw,
                &full_output, &max_levels,&tolerance)){
            throw could_not_parse_arguments("Unable to parse python arguments to C variables");
        }
    }
};

TrapezoidParamerters::result_type run_integration_routine(const compi_internal::IntegrandFunctionWrapper& f, const TrapezoidParamerters& params){
    TrapezoidParamerters::result_type result;

    result.result = boost::math::quadrature::trapezoidal(f,params.x_min, params.x_max,params.tolerance,params.max_levels, &(result.err),&(result.l1));

    return result;
}

template<>
PyObject* generate_full_output_dict(const TrapezoidParamerters::result_type& result,const TrapezoidParamerters& params)noexcept{
    return Py_BuildValue("{sd}", "L1 norm", result.l1);
}

extern "C" PyObject* trapezoidal(PyObject* self, PyObject* args, PyObject* kwargs){
    return integration_routine<TrapezoidParamerters>(args,kwargs);
}