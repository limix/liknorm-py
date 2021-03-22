from setuptools import setup

if __name__ == "__main__":
    setup(cffi_modules="liknorm/build_ext.py:ffibuilder")
