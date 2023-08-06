cmake_minimum_required(VERSION 2.8.12)
project(omp_wrapper)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

# Set source directory
set(SOURCE_DIR "src/omp_wrapper")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})

set(SOURCES src/omp_wrapper/omp_wrapper.cpp src/omp_wrapper/CardRange.cpp src/omp_wrapper/CardRange.h src/omp_wrapper/CombinedRange.cpp src/omp_wrapper/CombinedRange.h src/omp_wrapper/Constants.h src/omp_wrapper/EquityCalculator.cpp src/omp_wrapper/EquityCalculator.h src/omp_wrapper/Hand.h src/omp_wrapper/HandEvaluator.cpp src/omp_wrapper/HandEvaluator.h src/omp_wrapper/Random.h src/omp_wrapper/Util.h src/omp_wrapper/libdivide.h)


add_subdirectory(lib/pybind11)
pybind11_add_module(omp_wrapper ${SOURCES} "${SOURCE_DIR}/bindings.cpp")