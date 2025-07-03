# secp256k1-precompute

[![Build and Test](https://github.com/k-nuth/secp256k1-precompute/actions/workflows/main.yml/badge.svg)](https://github.com/k-nuth/secp256k1-precompute/actions/workflows/main.yml)

Tool for generating secp256k1 static context. This utility generates precomputed tables that optimize secp256k1 cryptographic operations.

This package is designed to be used as a `tool_requires` in Conan profiles for cross-compilation scenarios, particularly when building for Emscripten/WebAssembly or other target platforms where you need to generate tables on the host system.

## Description

This project builds a `gen_context` executable that generates the `src/ecmult_static_context.h` file containing precomputed tables to accelerate scalar multiplication operations in secp256k1.

## Installation

### As a Conan tool_requires (Recommended)

This package is designed to be used as a `tool_requires` in Conan profiles, especially for cross-compilation:

```ini
# ~/.conan2/profiles/emscripten
[settings]
arch=wasm
build_type=Release
compiler=clang
compiler.cppstd=23
compiler.libcxx=libc++
compiler.version=14
os=Emscripten

[tool_requires]
emsdk/3.1.73
secp256k1-precompute/[>=1.0.0]

```

### Direct installation with Conan

```bash
# Install the package
conan install secp256k1-precompute/[>=1.0.0]

# Or build from source
git clone https://github.com/k-nuth/secp256k1-precompute.git
cd secp256k1-precompute
conan create . --build=missing
```

### With CMake directly

```bash
git clone --recursive https://github.com/k-nuth/secp256k1-precompute.git
cd secp256k1-precompute
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

## Usage

### As a tool_requires in Conan recipes

When used as a `tool_requires`, the `gen_context` executable will be available during the build process via the `SECP256K1_GEN_CONTEXT` environment variable:

```python
# In your conanfile.py
def tool_requires(self):
    self.tool_requires("secp256k1-precompute/[>=1.0.0]")

def build(self):
    gen_context = os.environ.get("SECP256K1_GEN_CONTEXT")
    if gen_context:
        self.run(f"{gen_context}")
```

### Direct execution

```bash
# Run the generator (must be executed from project root directory)
./gen_context

# This generates the src/ecmult_static_context.h file
```

## Configuration Options

The project supports the following options (when using Conan):

- `ecmult_window_size`: Window size for ecmult (2-15, default: 15)
  - Higher values = larger tables but faster calculations
- `ecmult_gen_precision`: Precision for ecmult_gen (2, 4, 8, default: 4)
  - Higher values = more precision but longer generation time

### Examples with tool_requires

```bash
# Create a Conan profile for Emscripten with secp256k1-precompute
cat > ~/.conan2/profiles/emscripten << EOF
[settings]
arch=wasm
build_type=Release
compiler=clang
compiler.cppstd=23
compiler.libcxx=libc++
compiler.version=14
os=Emscripten

[tool_requires]
emsdk/3.1.73
secp256k1-precompute/[>=1.0.0]

EOF

# Use the profile for cross-compilation
conan create your-secp256k1-project --profile:build=default --profile:host=emscripten
```

### Package configuration examples

```bash
# Generate with smaller window
conan create . -o ecmult_window_size=8

# Generate with higher precision
conan create . -o ecmult_gen_precision=8

# Combine options
conan create . -o ecmult_window_size=10 -o ecmult_gen_precision=2
```

## Tests

```bash
# Run tests locally
python test_gen_context.py

# Or with Conan
conan create . --build=missing
```

## Project Structure

```
├── CMakeLists.txt              # Build configuration
├── conanfile.py               # Conan package
├── src/
│   ├── gen_context.c          # Main source code
│   ├── libsecp256k1-config.h.cmake.in  # Config template
│   └── secp256k1/            # secp256k1 submodule
├── test_package/              # Conan tests
└── test_gen_context.py        # Test script
```

## License

MIT License - see the LICENSE file for details.