cmake_minimum_required(VERSION 3.16)

add_library(${PROJECT_NAME} SHARED)
mo2_configure_plugin(${PROJECT_NAME} WARNINGS OFF)
mo2_install_target(${PROJECT_NAME})
