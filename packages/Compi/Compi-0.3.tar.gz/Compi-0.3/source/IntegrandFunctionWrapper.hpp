#ifndef COMPI_INTEGRAND_FUNCTION_WRAPPER_GUARD
#define COMPI_INTEGRAND_FUNCTION_WRAPPER_GUARD

#include "compi.hpp"

#include <vector>

namespace compi_internal {

// Exceptions to be used in IntegrandFunctionWrapper
class unable_to_construct_wrapper: public std::runtime_error{
    using std::runtime_error::runtime_error;
};
class unable_to_construct_py_object: public std::runtime_error{
    using std::runtime_error::runtime_error;
};
class function_not_callable: public std::invalid_argument{
    using std::invalid_argument::invalid_argument;
    public:
        function_not_callable(const char* c_message, const char* python_message):invalid_argument(c_message){
        PyErr_SetString(PyExc_ValueError,python_message);
    }
};
class PythonError: public std::runtime_error{
    using std::runtime_error::runtime_error;
};
class arg_list_not_tuple: public std::invalid_argument{
    using std::invalid_argument::invalid_argument;
    public:
        arg_list_not_tuple(const char * c_message, const char* python_message): std::invalid_argument(c_message){
        PyErr_SetString(PyExc_ValueError,python_message);
    }
};
class kwargs_given_not_dict: public std::invalid_argument{
    using std::invalid_argument::invalid_argument;
    public:
        kwargs_given_not_dict(const char * c_message, const char* python_message): std::invalid_argument(c_message){
        PyErr_SetString(PyExc_ValueError,python_message);
    }
};
class function_did_not_return_complex: public std::invalid_argument{
    using std::invalid_argument::invalid_argument;
    public:
        function_did_not_return_complex(const char * c_message, const char* python_message): std::invalid_argument(c_message){
        PyErr_SetString(PyExc_ValueError,python_message);
    }
};
class unable_to_form_arg_tuple: public std::runtime_error{
    using std::runtime_error::runtime_error;
};

class IntegrandFunctionWrapper {
    private:
        PyObject* callback;
        std::vector<PyObject*> args;
        PyObject* kwargs = NULL;
        
        // Forms a python tuple with a Py_Float of x in the first element, followed by the elements of args
        PyObject* buildArgTuple(Real x) const;

    public:
        IntegrandFunctionWrapper() = delete;
        IntegrandFunctionWrapper(PyObject* func, PyObject* new_args = Py_None, PyObject* new_kw = Py_None);
        IntegrandFunctionWrapper(const IntegrandFunctionWrapper& other);
        IntegrandFunctionWrapper(IntegrandFunctionWrapper&& other);

        friend inline void swap(IntegrandFunctionWrapper& first, IntegrandFunctionWrapper& second) noexcept;

        IntegrandFunctionWrapper& operator=(IntegrandFunctionWrapper other){
            swap(*this, other);
            return *this;
        }

        // similar to move constructor, the most efficent thing to do here
        // simply seems to be to swap elements
        IntegrandFunctionWrapper& operator=(IntegrandFunctionWrapper&& other){
            swap(*this,other);
            return *this;
        }

        ~IntegrandFunctionWrapper(){
            Py_DECREF(callback);
            if(kwargs != NULL){
                Py_DECREF(kwargs);
            }
            for(auto a: args){
                Py_DECREF(a);
            }
        }

        std::complex<Real> operator()(Real x) const;
};

inline void swap(IntegrandFunctionWrapper& first, IntegrandFunctionWrapper& second) noexcept{
            using std::swap;
            swap(first.callback,second.callback);
            swap(first.args,second.args);
}
}

#endif
