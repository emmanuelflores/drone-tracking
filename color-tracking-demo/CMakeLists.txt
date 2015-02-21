cmake_minimum_required( VERSION 2.8 )

project( color-tracking-demo )

# If you build opencv from source, provide the path here
# Otherwise comment this and it should work
SET(OpenCV_DIR ~/code/opencv/build)

find_package( OpenCV REQUIRED )

add_executable( color-tracking-demo color-tracking-demo.cpp )

target_link_libraries( color-tracking-demo ${OpenCV_LIBS} )
