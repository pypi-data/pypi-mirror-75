#include <pybind11/pybind11.h>
#include "omp_wrapper.h"

namespace py = pybind11;

PYBIND11_PLUGIN(omp_wrapper){

	py::module m("Wrapper functions for ompeval");
	m.def("evaluator", &evaluator);
	m.def("hand_potential", &hand_potential);
	m.def("is_best_hand", &is_best_hand);
	m.def("win_percentage", &win_percentage);
	m.def("win_percentages", &win_percentages);
	return m.ptr();

}