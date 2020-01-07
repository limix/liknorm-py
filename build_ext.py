import os
from os.path import join

import platform
from cffi import FFI


def _get_interface_h():
    folder = os.path.dirname(os.path.abspath(__file__))

    with open(join(folder, "liknorm", "interface.h"), "r") as f:
        return f.read()


def _get_interface_c():
    folder = os.path.dirname(os.path.abspath(__file__))

    with open(join(folder, "liknorm", "interface.c"), "r") as f:
        return f.read()


ffibuilder = FFI()
ffibuilder.cdef(_get_interface_h())
libs = ["liknorm"]

# if platform.system() == "Windows":
#     win = Windows()
#     progfiles = win.get_programfiles()
#     for lib in libs:
#         win.add_library_dir(join(progfiles, lib, "lib"))
#         win.add_include_dir(join(progfiles, lib, "include"))

#     libs = [win.find_libname(lib) for lib in libs]
#     system: System = win
# else:
#     system = Unix()

# library_dirs = system.get_library_dirs()
# extra_link_args: List[str] = []
# if platform.system() != "Windows":
#     if len(library_dirs) > 0:
#         extra_link_args += ["-Wl,-rpath,/usr/local/lib"]

if platform.system() == "Windows":
    sep = ";"
else:
    sep = ":"

extra_link_args = os.environ.get("LIKNORM_EXTRA_LINK_ARGS", "").split(sep)
include_dirs = os.environ.get("LIKNORM_INCLUDE_DIRS", "").split(sep)
library_dirs = os.environ.get("LIKNORM_LIBRARY_DIRS", "").split(sep)


ffibuilder.set_source(
    "liknorm._ffi",
    _get_interface_c(),
    extra_link_args=extra_link_args,
    include_dirs=include_dirs,
    language="c",
    libraries=libs,
    library_dirs=library_dirs,
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
