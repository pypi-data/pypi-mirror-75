from setuptools import setup,Extension
import os, sys, re

try:
    import readline # makes terminal input nice
except ModuleNotFoundError:
    pass

#############################################################################################
#
# The file locations in this tuple are searched in order to find the boost library. The first
# valid location is used. The location of the boost library used can be modified by changing 
# this tuple
#

boost_library_search_locations = (
                                    "/usr/include/boost",
                                    "local_boost"
                                 )
#############################################################################################

def check_valid_boost_path(path):
      '''
      Returns True if the path entered gives the location of the boost library, including,
      at a minimum, all files required by Compi
      '''

      include_regex = re.compile(r'#include <(boost/\S*)>') # matches a c++ include for a boost header file

      quad = "boost/math/quadrature/"
      files_required = {quad+"gauss_kronrod.hpp",
                        quad+"tanh_sinh.hpp",
                        quad+"sinh_sinh.hpp",
                        quad+"trapezoidal.hpp",
                        quad+"exp_sinh.hpp",
                        "boost/math/tools/precision.hpp"}


      # Recusively checks that a file exists, searches it for boost includes
      # and then checks those files

      files_checked = set()
      while files_required:
            f = files_required.pop()
            try:
                  for line in open(path+'/'+f,'r'):
                        include = include_regex.match(line)
                        if include is not None and include.group(1) not in files_checked:
                              files_required.add(include.group(1))
                        

            except FileNotFoundError:
                  return False
            files_checked.add(f)


      return True

def set_boost_path():
    while(True):
        default_search = input("search for c++ boost in default locations? [y/n]")
        if default_search.lower().strip() == 'y':
            for path in boost_library_search_locations:
                if check_valid_boost_path(path):
                    return path
            print("Unable to locate C++ Boost library headers", end="\n\n")
            break
        if default_search.lower().strip() == 'n':
            break
        print("Invalid input")
      
    print("C++ Boost can be downloaded from www.boost.org", end="\n\n")
    while True:
        path = input("Please enter file path to Boost library location. Press Enter to exit\n").strip('/')
        if not path:
            raise FileNotFoundError("Unable to locate C++ Boost library headers")

        if check_valid_boost_path(path):
            return path
            
        print("The directory path you entered is not a valid path to the Boost library")
            

boost_path = set_boost_path()
print("Using " + boost_path + " as Boost location\n")

src = 'source/'

setup(name='Compi',
      version='0.3',
      author='Conor Jackson',
      author_email='conorgjackson@gmail.com',
      url='https://github.com/CGJackson/Compi',
      ext_modules=[Extension('compi',[src+f for f in ('compi.c',
                                            'GaussKronrod.cpp',
                                            'tanh_sinh.cpp',
                                            'sinh_sinh.cpp',
                                            'exp_sinh.cpp',
                                            'trapezoid.cpp',
                                            'IntegrandFunctionWrapper.cpp')],

                                       include_dirs=[boost_path],extra_compile_args=["-std=c++17"]
                            )],
     )
