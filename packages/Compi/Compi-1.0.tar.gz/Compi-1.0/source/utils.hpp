#ifndef COMPI_UTILS_GUARD
#define COMPI_UTILS_GUARD
#include "compi.hpp"
#include <complex>
#include <vector>

namespace compi_internal {

inline std::complex<Real> complex_from_c_complex(const Py_complex& c) noexcept{
    return std::complex<Real>(c.real,c.imag);
}

inline Py_complex c_complex_from_complex(const std::complex<Real> c) noexcept{
    return Py_complex{c.real(),c.imag()};
}

inline bool has_callable_method(PyObject* obj, const char* name){
    return PyObject_HasAttrString(obj, name) && PyCallable_Check(PyObject_GetAttrString(obj,name));
}

inline bool convertable_to_py_complex(PyObject* obj) noexcept{
    return PyComplex_Check(obj) || has_callable_method(obj,"__complex__") 
            || has_callable_method(obj,"__float__") || has_callable_method(obj,"__index__");
}

inline PyObject* copy_py_tuple(PyObject* tup) noexcept{
    if(!PyTuple_Check(tup)){
        PyErr_SetString(PyExc_ValueError, "Object passed to copy_py_tuple was not a tuple");
        return NULL;
    }

    const Py_ssize_t size = PyTuple_Size(tup);

    PyObject* new_tup = PyTuple_New(size);
    if(new_tup == NULL){
        return NULL;
    }

    for(Py_ssize_t i = 0; i < size; ++i){
        PyObject* elm = PyTuple_GET_ITEM(tup, i);
        PyTuple_SET_ITEM(new_tup,i,elm);
        Py_INCREF(elm);
    }

    return new_tup;
}

template<typename RandomAccessContainer> 
PyObject* py_list_from_real_container(const RandomAccessContainer& arr) noexcept{
    using obj_vector = std::vector<PyObject*>;
    using ov_size_t = obj_vector::size_type;

    // Generate python list elements in advance, so that any errors can be dealt with
    // before the list is constructed
    obj_vector py_elements{};
    py_elements.reserve(arr.size());
    for(auto it = arr.cbegin(); it != arr.cend(); ++it){
        py_elements.emplace_back(PyFloat_FromDouble(*it));
        if(py_elements.back() == NULL){
            for(ov_size_t i = 0; i < static_cast<ov_size_t>(it - arr.cbegin()); ++i){
                Py_DECREF(py_elements[i]);
            }
            return NULL;
        }
    }

    const Py_ssize_t arr_ssize = static_cast<Py_ssize_t>(arr.size());

    PyObject* result_list = PyList_New(arr_ssize);
    if( result_list == NULL){
        return NULL;
    }

    for(Py_ssize_t i = 0; i < arr_ssize; ++i){
        PyList_SET_ITEM(result_list,i,py_elements[i]);
    }
    
    return result_list;
}

}
#endif
