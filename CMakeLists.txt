CMAKE_MINIMUM_REQUIRED(VERSION 3.16)
PROJECT(blink)

#FIND_PACKAGE(GTest REQUIRED)
#FIND_PACKAGE(Threads REQUIRED)
set(CMAKE_CXX_STANDARD 20)

# compiler options. (we only check for gcc)
if (${CMAKE_COMPILER_IS_GNUCC})
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O0 -g3 -Wall -Werror")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g3 -Wall -Werror")
endif()

# quick hack to get started
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/../install/include)
LINK_DIRECTORIES(${CMAKE_SOURCE_DIR}/../install/lib)

ADD_EXECUTABLE(blink-get blink-get.cpp)
TARGET_LINK_LIBRARIES(blink-get gpiod)

ADD_EXECUTABLE(blink-watch blink-watch.cpp)
TARGET_LINK_LIBRARIES(blink-watch gpiod)

ADD_EXECUTABLE(blink-set blink-set.cpp)
TARGET_LINK_LIBRARIES(blink-set gpiod)
