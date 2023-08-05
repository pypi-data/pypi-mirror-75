#include "compi.hpp"

#include <complex>
#include <unordered_map>
#include <algorithm>
#include <utility>

#include <boost/math/quadrature/gauss_kronrod.hpp>
#include <boost/math/tools/precision.hpp>

extern "C" {
    #include "integration_routines.h"
}

#include "integration_routines_template.hpp"
#include "IntegrandFunctionWrapper.hpp"
#include "utils.hpp"




struct GaussKronrodParameters: public RoutineParametersBase{
    Real x_min;
    Real x_max;
    unsigned points = 31;

    GaussKronrodParameters(PyObject* routine_args, PyObject* routine_kwargs){
        constexpr std::array<const char*,0> dumby_arg = {};
        constexpr std::array<const char*,1> keyword_only_args = {"points"};
        constexpr auto keywords = generate_keyword_list<IntegralRange::finite>(dumby_arg,dumby_arg,keyword_only_args);

        if(!PyArg_ParseTupleAndKeywords(routine_args,routine_kwargs,"Odd|OO$pIdI",const_cast<char**>(keywords.data()),
                &integrand,&x_min,&x_max,
                &args,&kw,
                &full_output, &max_levels,&tolerance,&points)){
            throw could_not_parse_arguments("Unable to parse python arguments to C variables");
        }
    }

};

GaussKronrodParameters::result_type run_integration_routine(const compi_internal::IntegrandFunctionWrapper& f, const GaussKronrodParameters& parameters){
    using std::complex;
    using namespace compi_internal;
    using boost::math::quadrature::gauss_kronrod;
    using IntegrationRoutine = complex<Real>(*)(IntegrandFunctionWrapper, Real, Real, unsigned, Real, Real*, Real*);

    // The possible tempates for the different allowed numbers of divisions are instasiated, 
    // so that the Python runtime can select which one to use
    static const std::unordered_map<unsigned,IntegrationRoutine> integration_routines{{15,gauss_kronrod<Real,15>::integrate},
                                                                                      {31,gauss_kronrod<Real,31>::integrate},
                                                                                      {41,gauss_kronrod<Real,41>::integrate},
                                                                                      {51,gauss_kronrod<Real,51>::integrate},
                                                                                      {61,gauss_kronrod<Real,61>::integrate}
                                                                                     };

    GaussKronrodParameters::result_type result;

    try{
        result.result = integration_routines.at(parameters.points)(f,parameters.x_min,parameters.x_max,parameters.max_levels,parameters.tolerance,&(result.err),&(result.l1));
    } catch (const std::out_of_range& e){
        PyErr_SetString(PyExc_ValueError,"Invalid number of points for gauss_kronrod");
        throw unable_to_call_integration_routine("Invalid number of points for gauss_kronrod");
    }

    return result;
}

template<unsigned points>
std::pair<PyObject*, PyObject*> get_abscissa_and_weights() noexcept{
    auto abscissa = compi_internal::py_list_from_real_container(boost::math::quadrature::gauss_kronrod<Real,points>::abscissa());
    if(abscissa == NULL){
        return std::make_pair<PyObject*,PyObject*>(NULL,NULL);
    }
    auto weights = compi_internal::py_list_from_real_container(boost::math::quadrature::gauss_kronrod<Real,points>::weights());
    if(weights == NULL){
        Py_DECREF(abscissa);
        return std::make_pair<PyObject*,PyObject*>(NULL,NULL);
    }
    return std::make_pair(abscissa,weights);
}

template<>
PyObject* generate_full_output_dict(const GaussKronrodParameters::result_type& result, const GaussKronrodParameters& parameters) noexcept{

    // The boost API returning the abscissa and weights simply spesifies that
    // they are returned as a (reference to a) random access container. 
    // Since this could (reasonably) depend on points (e.g. array<Real,points>)
    // it is awkward to use the map based appraoch in run_integation_routine
    // and instead we use more verbose a template/switch based approach

    std::pair<PyObject*,PyObject*> abscissa_and_weights;
    switch(parameters.points){
        case 15:
            abscissa_and_weights = get_abscissa_and_weights<15>();
            break;
        case 31:
            abscissa_and_weights = get_abscissa_and_weights<31>();
            break;
        case 41:
            abscissa_and_weights = get_abscissa_and_weights<41>();
            break;
        case 51:
            abscissa_and_weights = get_abscissa_and_weights<51>();
            break;
        case 61:
            abscissa_and_weights = get_abscissa_and_weights<61>();
            break;
        default:
            // Should never get here as have already checked the value of points is valid 
            PyErr_SetString(PyExc_NotImplementedError,"Unable to generate abscissa and weights for the given number of points.\nPlease report this bug");
            return NULL;
        }
        
        if(abscissa_and_weights.first == NULL || abscissa_and_weights.second == NULL){
            return NULL;
        }

        return Py_BuildValue("{sfsOsO}","L1 norm",result.l1,"abscissa",abscissa_and_weights.first,"weights",abscissa_and_weights.second);
}

// Integrates a Python function returning a complex over a finite interval using
// Gauss-Kronrod adaptive quadrature
extern "C" PyObject* gauss_kronrod(PyObject* self, PyObject* args, PyObject* kwargs){
    return integration_routine<GaussKronrodParameters>(args,kwargs);
}
