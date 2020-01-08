import os
from typing import List
from os.path import join

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

extra_link_args: List[str] = []
if "LIKNORM_EXTRA_LINK_ARGS" in os.environ:
    extra_link_args += os.environ["LIKNORM_EXTRA_LINK_ARGS"].split(os.pathsep)


ffibuilder.set_source(
    "liknorm._ffi",
    _get_interface_c(),
    extra_link_args=extra_link_args,
    language="c",
    libraries=libs,
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
