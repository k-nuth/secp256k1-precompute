# test_package/conanfile.py
from conan import ConanFile
from conan.tools.build import can_run
import os

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    
    def requirements(self):
        self.tool_requires(self.tested_reference_str)
    
    def test(self):
        if can_run(self):
            gen_context = os.environ.get("SECP256K1_GEN_CONTEXT")
            if gen_context:
                self.run(f"{gen_context}")
                # Verificar que se generó el archivo
                if os.path.exists("src/ecmult_static_context.h"):
                    self.output.info("✅ Tabla generada correctamente")
                else:
                    raise Exception("❌ No se generó la tabla")