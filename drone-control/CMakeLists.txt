cmake_minimum_required(VERSION 2.6)
project(demo)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

set(${PROJECT_NAME}_VERSION_MAJOR_0)
set(${PROJECT_NAME}_VERSION_MINOR_1)
set(${PROJECT_NAME}_VERSION_PATCH_0)

# include_directories("${PROJECT_SOURCE_DIR}/include")

# SET(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ~/code/libcflie/lib)
# SET(CMAKE_LIBRARY_PATH ~/code/libcflie/lib)

find_library(USB_LIB usb-1.0)
if(${USB_LIB} STREQUAL "USB_LIB-NOTFOUND")
  message(STATUS "It appears the USB libs are not installed.")
endif()

find_library(CFLIE_LIB cflie) # installed without version!?
if(${CFLIE_LIB} STREQUAL "CFLIE_LIB-NOTFOUND")
  message(STATUS "It appears the cflie libs are not installed.")
endif()

add_executable(demo src/demo/demo.cpp)

target_link_libraries(${PROJECT_NAME} ${USB_LIB})
target_link_libraries(${PROJECT_NAME} ${CFLIE_LIB})

install(
  TARGETS ${PROJECT_NAME}
  RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
  ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
  COMPONENT library
)
