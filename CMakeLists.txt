cmake_minimum_required(VERSION 3.16)

project(mo2_plugin_examples)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/mob/mob_build_output/build/modorganizer_super/cmake_common")
include(mo2)

# mo2_required_variable(NAME BOOST_ROOT TYPE PATH)
# mo2_required_variable(NAME QT_ROOT TYPE PATH)
# mo2_required_variable(NAME PYTHON_ROOT TYPE PATH)
# mo2_required_variable(NAME CMAKE_INSTALL_PREFIX TYPE PATH)

add_subdirectory(cpp_examples)

syntax error