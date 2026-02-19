cmake_minimum_required(VERSION 3.16)
project(LoadFileGenerator VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt5
find_package(Qt5 REQUIRED COMPONENTS Core Gui Widgets)

# Find PoDoFo (PDF library) - vcpkg uses CONFIG mode
find_package(podofo CONFIG REQUIRED)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/include
)

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/PDFProcessor.cpp
    src/CSVParser.cpp
    src/DATGenerator.cpp
    src/OPTGenerator.cpp
    src/VolumeManager.cpp
)

# Header files
set(HEADERS
    include/MainWindow.h
    include/PDFProcessor.h
    include/CSVParser.h
    include/DATGenerator.h
    include/OPTGenerator.h
    include/VolumeManager.h
    include/Document.h
)

# Create executable
add_executable(${PROJECT_NAME} WIN32 ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(${PROJECT_NAME}
    Qt5::Core
    Qt5::Gui
    Qt5::Widgets
    podofo::podofo
)

# Set output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# Install target
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)
