project(hello_world_plugin)

add_library(${PROJECT_NAME} SHARED)
mo2_configure_plugin(${PROJECT_NAME}
  WARNINGS OFF)
  
  # PRIVATE_DEPENDS gamebryo)

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

target_sources(${PROJECT_NAME}
  PRIVATE
  hello_world_plugin.cpp
)

mo2_install_target(${PROJECT_NAME})

syntax error