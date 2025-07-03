#!/usr/bin/env python3
"""
Test script para verificar que gen_context funciona correctamente.
"""

import os
import subprocess
import tempfile
import sys

def test_gen_context_execution():
    """Test que el ejecutable gen_context se puede ejecutar y genera salida válida."""
    print("Testing gen_context execution...")
    
    # Crear directorio temporal para el test
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Intentar encontrar el ejecutable
            gen_context_paths = [
                "gen_context",
                "./gen_context", 
                "build/Release/gen_context",
                "build/gen_context"
            ]
            
            gen_context = None
            for path in gen_context_paths:
                if os.path.exists(path) and os.access(path, os.X_OK):
                    gen_context = path
                    break
            
            if not gen_context:
                print("❌ gen_context executable not found in expected locations")
                return False
            
            # Crear directorio src como espera el programa
            os.makedirs("src", exist_ok=True)
            
            # Ejecutar gen_context
            result = subprocess.run([gen_context], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            if result.returncode != 0:
                print(f"❌ gen_context failed with return code {result.returncode}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
            
            # Verificar que se generó el archivo
            output_file = "src/ecmult_static_context.h"
            if not os.path.exists(output_file):
                print(f"❌ Expected output file {output_file} was not created")
                return False
            
            # Verificar contenido básico del archivo
            with open(output_file, 'r') as f:
                content = f.read()
                
            required_content = [
                "#ifndef _SECP256K1_ECMULT_STATIC_CONTEXT_",
                "#define _SECP256K1_ECMULT_STATIC_CONTEXT_",
                "secp256k1_ecmult_gen_prec_table"
            ]
            
            for required in required_content:
                if required not in content:
                    print(f"❌ Required content '{required}' not found in output")
                    return False
            
            print(f"✅ gen_context executed successfully")
            print(f"✅ Generated {output_file} with {len(content)} characters")
            return True
            
        finally:
            os.chdir(old_cwd)

def test_build_with_cmake():
    """Test que el proyecto se puede compilar con CMake."""
    print("Testing CMake build...")
    
    with tempfile.TemporaryDirectory() as build_dir:
        try:
            # Configurar CMake
            result = subprocess.run([
                "cmake", 
                "-B", build_dir,
                "-S", ".",
                "-DCMAKE_BUILD_TYPE=Release"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ CMake configuration failed: {result.stderr}")
                return False
            
            # Compilar
            result = subprocess.run([
                "cmake", 
                "--build", build_dir,
                "--config", "Release"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"❌ CMake build failed: {result.stderr}")
                return False
            
            # Verificar que el ejecutable se creó
            exe_paths = [
                os.path.join(build_dir, "gen_context"),
                os.path.join(build_dir, "Release", "gen_context"),
                os.path.join(build_dir, "gen_context.exe"),
                os.path.join(build_dir, "Release", "gen_context.exe")
            ]
            
            exe_found = any(os.path.exists(path) for path in exe_paths)
            if not exe_found:
                print("❌ gen_context executable not found after build")
                return False
            
            print("✅ CMake build successful")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ CMake build timed out")
            return False

def main():
    """Ejecutar todos los tests."""
    print("Running secp256k1-precompute tests...")
    print("=" * 50)
    
    tests = [
        test_build_with_cmake,
        test_gen_context_execution
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
