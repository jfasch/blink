# quick hack to get started
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/../install/include)
LINK_DIRECTORIES(${CMAKE_SOURCE_DIR}/../install/lib)

ADD_EXECUTABLE(blink-get-single blink-get-single.cpp)
TARGET_LINK_LIBRARIES(blink-get-single gpiod)

ADD_EXECUTABLE(blink-watch-single blink-watch-single.cpp)
TARGET_LINK_LIBRARIES(blink-watch-single gpiod)

ADD_EXECUTABLE(blink-set-single blink-set-single.cpp)
TARGET_LINK_LIBRARIES(blink-set-single gpiod)

ADD_EXECUTABLE(blink-kitt blink-kitt.cpp)
TARGET_LINK_LIBRARIES(blink-kitt gpiod)
