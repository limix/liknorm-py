import os
import platform
from os.path import join
from sysconfig import get_config_var

from cffi import FFI

__all__ = ["ffibuilder"]


def _windows_dirs(prefix, lib):
    dirs = []
    if "PROGRAMW6432" in os.environ:
        fld = join(os.environ["PROGRAMW6432"], lib, prefix)
        if os.path.exists(fld):
            dirs += [fld]
    if "PROGRAMFILES" in os.environ:
        fld = join(os.environ["PROGRAMFILES"], lib, prefix)
        if os.path.exists(fld):
            dirs += [fld]
    return dirs


def _windows_include_dirs():
    include_dirs = []
    if "INCLUDE" in os.environ:
        include_dirs += [os.environ["INCLUDE"]]
    if "LIBRARY_INC" in os.environ:
        include_dirs += [os.environ["LIBRARY_INC"]]
    include_dirs += _windows_dirs("include", "liknorm")
    return include_dirs


def _windows_library_dirs():
    library_dirs = []
    if "LIBRARY_LIB" in os.environ:
        library_dirs += [os.environ["LIBRARY_LIB"]]
    library_dirs += _windows_dirs("lib", "liknorm")
    return library_dirs


def _windows_find_libname(lib, library_dirs):
    names = ["{}.lib".format(lib), "lib{}.lib".format(lib), "{}lib.lib".format(lib)]
    folders = [f for ldir in library_dirs for f in ldir.split(";")]
    for f in folders:
        for n in names:
            if os.path.exists(join(f, n)):
                return n[:-4]

    raise RuntimeError("{} library not found.".format(lib))


def _get_interface_h():
    folder = os.path.dirname(os.path.abspath(__file__))

    with open(join(folder, "liknorm", "interface.h"), "r") as f:
        return f.read()


def _get_interface_c():
    folder = os.path.dirname(os.path.abspath(__file__))

    with open(join(folder, "liknorm", "interface.c"), "r") as f:
        return f.read()


def _get_include_dirs():
    include_dirs = [join(get_config_var("prefix"), "include")]

    if platform.system() == "Windows":
        include_dirs += _windows_include_dirs()
    else:
        include_dirs += ["/usr/include", "/usr/local/include"]

    return include_dirs


def _get_library_dirs():
    library_dirs = [join(get_config_var("prefix"), "lib")]

    if platform.system() == "Windows":
        library_dirs += _windows_library_dirs()
    else:
        library_dirs += ["/usr/lib", "/usr/local/lib"]

    return library_dirs


def _get_libraries():
    if platform.system() == "Windows":
        libraries = [_windows_find_libname("liknorm", _get_library_dirs())]
    else:
        libraries = ["liknorm"]
    return libraries


def _get_extra_link_args():
    lib_dirs = _get_library_dirs()
    if platform.system() == "Darwin":
        if len(lib_dirs) > 0:
            return ["-Wl,-rpath," + ",-rpath,".join(lib_dirs)]
    return []


ffibuilder = FFI()
ffibuilder.cdef(_get_interface_h())

ffibuilder.set_source(
    "liknorm.machine_ffi",
    _get_interface_c(),
    libraries=_get_libraries(),
    library_dirs=_get_library_dirs(),
    include_dirs=_get_include_dirs(),
    extra_link_args=_get_extra_link_args(),
    language="c",
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
