cmake_minimum_required(VERSION 3.15)
project(secp256k1-precompute)

# Parameter configuration
if(NOT DEFINED SECP256K1_ECMULT_WINDOW_SIZE)
    set(SECP256K1_ECMULT_WINDOW_SIZE 15)
endif()

if(NOT DEFINED SECP256K1_ECMULT_GEN_PRECISION)
    set(SECP256K1_ECMULT_GEN_PRECISION 4)
endif()

# Configure configuration header
configure_file(
    "${CMAKE_SOURCE_DIR}/src/libsecp256k1-config.h.cmake.in"
    "${CMAKE_BINARY_DIR}/libsecp256k1-config.h"
)

# Include directories - order is important!
include_directories(
    # Generated files first
    "${CMAKE_BINARY_DIR}"
    # Then base directory so it can find "include/secp256k1.h"
    "${CMAKE_SOURCE_DIR}/src/secp256k1"
    # And subdirectories
    "${CMAKE_SOURCE_DIR}/src/secp256k1/src"
    "${CMAKE_SOURCE_DIR}/src/secp256k1/include"
    "${CMAKE_SOURCE_DIR}/src"
)

# Create the executable
add_executable(gen_context src/gen_context.c)

# Define necessary macros - DO NOT include USE_ECMULT_STATIC_PRECOMPUTATION
target_compile_definitions(gen_context PRIVATE
    USE_BASIC_CONFIG=1
    ECMULT_GEN_PREC_BITS=${SECP256K1_ECMULT_GEN_PRECISION}
    SECP256K1_ECMULT_WINDOW_SIZE=${SECP256K1_ECMULT_WINDOW_SIZE}
    SECP256K1_ECMULT_GEN_PRECISION=${SECP256K1_ECMULT_GEN_PRECISION}
    SECP256K1_USE_ASM=OFF
)

# Additional configurations for different platforms
if(WIN32)
    target_compile_definitions(gen_context PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

# Debug info
message(STATUS "SECP256K1_ECMULT_WINDOW_SIZE: ${SECP256K1_ECMULT_WINDOW_SIZE}")
message(STATUS "SECP256K1_ECMULT_GEN_PRECISION: ${SECP256K1_ECMULT_GEN_PRECISION}")