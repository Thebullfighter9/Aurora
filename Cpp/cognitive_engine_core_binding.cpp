#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include "cognitive_engine_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(cognitive_engine_core, m) {
    m.doc() = "Cognitive Engine Core module";

    py::class_<CognitiveEngineCore>(m, "CognitiveEngineCore")
        .def(py::init<>())
        .def("load", &CognitiveEngineCore::load)
        .def("process_query", &CognitiveEngineCore::processQuery)
        .def("process_query_async", &CognitiveEngineCore::processQueryAsync)
        .def("introspect", &CognitiveEngineCore::introspect)
        .def("reload", &CognitiveEngineCore::reload)
        .def("status", &CognitiveEngineCore::status);
}
