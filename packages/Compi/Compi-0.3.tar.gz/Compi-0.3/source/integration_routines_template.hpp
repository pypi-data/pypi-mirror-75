#ifndef COMPI_INTEGRATION_ROUTINES_TEMPLATE_GUARD
#define COMPI_INTEGRATION_ROUTINES_TEMPLATE_GUARD

#include "compi.hpp"

#include <array>
#include <complex>
#include <utility>
#include <stdexcept>
#include <regex>

#include <boost/math/tools/precision.hpp>

#include "IntegrandFunctionWrapper.hpp"
#include "utils.hpp"

enum class IntegralRange: short unsigned {infinite, semi_infinite, finite};

// Generates an array of the standard keywords, appropriate bounds depending
// on the integration bounds, and any extra required, optional and keyword
// only arguments, in the correct order to be used in Py_ParseTupleAndKeywords
// for an integration routine.
template<IntegralRange bounds,size_t L=0, size_t M=0, size_t N=0>
constexpr auto generate_keyword_list(const std::array<const char*, L>& required = {}, const std::array<const char*,M> optional = {}, const std::array<const char*,N> keyword_only = {}) noexcept {

    std::array<const char *, L+M+N+7+static_cast<size_t>(bounds)> keywords{"f"};

    size_t k_idx = 1;

    switch(bounds){
        case IntegralRange::finite:
            keywords[k_idx++] = "a";
        case IntegralRange::semi_infinite:
            keywords[k_idx++] = "b";
        case IntegralRange::infinite:;
    }

    for(auto kw: required){
        keywords[k_idx++] = kw;
    }

    keywords[k_idx++] = "args";
    keywords[k_idx++] = "kwargs";

    for(auto kw: optional){
        keywords[k_idx++] = kw;
    }

    keywords[k_idx++] = "full_output";
    keywords[k_idx++] = "max_levels";
    keywords[k_idx++] = "tolerance";

    for(auto kw: keyword_only){
        keywords[k_idx++] = kw;
    }

    keywords[k_idx++] = nullptr;

    return keywords;
}

struct RoutineParametersBase{
    PyObject* integrand;
    PyObject* args = Py_None;
    PyObject* kw = Py_None;

    bool full_output = false;
    Real tolerance = boost::math::tools::root_epsilon<Real>();
    unsigned max_levels = 15;

    struct result_type{
        std::complex<Real> result;
        Real err;
        Real l1;
    };

    RoutineParametersBase() = default;
    explicit RoutineParametersBase(Real tol, unsigned levels):tolerance{tol},max_levels{levels}{}

};
class could_not_parse_arguments: std::runtime_error{
    using std::runtime_error::runtime_error;
};

class unable_to_call_integration_routine: std::runtime_error{
    using std::runtime_error::runtime_error;
};

// general template for running integration routines. handles the overall flow of control and exception handelling. Specialized based on 
// RoutineParameters class, which stores the various parameters which the routine needs to run. Expects 3 funtions to exist.
//      a construtor for RoutineParameters, which accepts the python arg tuple and keyword dict and handles parsing those into c type, stored
//      in the constructed RoutineParameters instance. Throws could_not_parse_arguments exception on failure.
//      run_integration_routine, which takes an IntegrandFunctionWrapper and a RoutineParameters instance and handles the actual calling of the integration routine
//      generate_full_output_dict, which takes an object of the type returned by run_integration_routine and an instance od RoutineParameters and 
//      returns a a python dict, containing the extra information provided if full_output is true
// The RoutineParametersBase class has all the functionality expected of RoutineParameters, except the constructor mentioned above
template<typename RoutineParameters>
PyObject* integration_routine(PyObject* args, PyObject* kwargs){
    using namespace::compi_internal;
    std::unique_ptr<const RoutineParameters> parameters;

    // The input Python Objects are parsed into c variables
    try{
        parameters = std::make_unique<const RoutineParameters>(args,kwargs);
    }catch(const could_not_parse_arguments& e){
        return NULL;
    }

    // C++ wrapper for Python integrand funciton is constructed
    
    std::unique_ptr<IntegrandFunctionWrapper> f;
    try{
        f = std::make_unique<IntegrandFunctionWrapper>(parameters->integrand,parameters->args,parameters->kw);
    } catch( const unable_to_construct_wrapper& e ){
        return NULL;
    } catch( const function_not_callable& e ){
        return NULL;
    } catch( const arg_list_not_tuple& e ){
        return NULL;
    } catch( const kwargs_given_not_dict& e){
        return NULL;
    } 

    // The actual integration routine is run

    decltype(run_integration_routine(*f,*parameters)) result;
    try{
        result = run_integration_routine(*f,*parameters);
    } catch (const unable_to_call_integration_routine& e){
        return NULL;
    } catch( const unable_to_construct_py_object& e ){
        return NULL;
    } catch( const unable_to_form_arg_tuple& e ){
        return NULL;
    } catch( const PythonError& e ){
        return NULL;
    } catch( const function_did_not_return_complex& e ){
        return NULL;
    } catch( const boost::wrapexcept<std::domain_error>& e){
        //TODO improve error messages
        if(std::regex_search(e.what(),std::basic_regex<char>("The function you are trying to integrate does not go to zero at infinity")) ){
            PyErr_SetString(PyExc_ValueError, "Function to be integrated does not go to 0 at infinity");
        }
        else{
            PyErr_SetString(PyExc_RuntimeError,e.what());
        }
        return NULL;
    } catch( const boost::wrapexcept<std::exception>& e){
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }catch(const std::exception& e){
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    } catch(...){
        PyErr_SetString(PyExc_RuntimeError, "An unknown error has occured");
        return NULL;
    }

    // The results are parsed back to Python Objects 

    auto c_complex_result = c_complex_from_complex(result.result);

    if(parameters->full_output){
        PyObject* full_output_dict = generate_full_output_dict(result,*parameters);
        if(!full_output_dict){
            return NULL;
        }
        return Py_BuildValue("(DdO)", &c_complex_result, result.err,full_output_dict);
    }
    else{
        return Py_BuildValue("(Dd)", &c_complex_result,result.err);
    }

}

// generate_full_output_dict template for classes that expect the full_output dict to contain only the l1 norm and the number of
// levels of adaptive quadrature
template<typename ExpIntegratorParameterType,typename ExpIntegratorResultType>
PyObject* generate_full_output_dict(const ExpIntegratorResultType& result,const ExpIntegratorParameterType& parameters) noexcept{
    return Py_BuildValue("{sdsI}","L1 norm",result.l1,"levels",result.levels);
}
#endif
