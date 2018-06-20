import os
import platform
from os.path import join
from sysconfig import get_config_var

from cffi import FFI


def windows_dirs(prefix, lib):
    dirs = []
    if 'PROGRAMW6432' in os.environ:
        fld = join(os.environ['PROGRAMW6432'], lib, prefix)
        if os.path.exists(fld):
            dirs += [fld]
    if 'PROGRAMFILES' in os.environ:
        fld = join(os.environ['PROGRAMFILES'], lib, prefix)
        if os.path.exists(fld):
            dirs += [fld]
    return dirs


def windows_include_dirs():
    include_dirs = []
    if 'INCLUDE' in os.environ:
        include_dirs += [os.environ['INCLUDE']]
    if 'LIBRARY_INC' in os.environ:
        include_dirs += [os.environ['LIBRARY_INC']]
    include_dirs += windows_dirs('include', 'liknorm')
    return include_dirs


def windows_library_dirs():
    library_dirs = []
    if 'LIBRARY_LIB' in os.environ:
        library_dirs += [os.environ['LIBRARY_LIB']]
    library_dirs += windows_dirs('lib', 'liknorm')
    return library_dirs


def windows_find_libname(lib, library_dirs):
    names = [
        "{}.lib".format(lib), "lib{}.lib".format(lib), "{}lib.lib".format(lib)
    ]
    folders = [f for ldir in library_dirs for f in ldir.split(';')]
    for f in folders:
        for n in names:
            if os.path.exists(join(f, n)):
                return n[:-4]

    raise RuntimeError("{} library not found.")


def prefix_liknorm_include(dirs):
    if platform.system() == 'Windows':
        sep = ';'
    else:
        sep = ':'

    for d in dirs:
        for folder in d.split(sep):
            if os.path.exists(join(folder, 'liknorm', 'liknorm.h')):
                return True

    return False


ffibuilder = FFI()

folder = os.path.dirname(os.path.abspath(__file__))

with open(join(folder, 'liknorm', 'interface.h'), 'r') as f:
    ffibuilder.cdef(f.read())

with open(join(folder, 'liknorm', 'interface.c'), 'r') as f:
    interface_content = f.read()

include_dirs = [join(get_config_var('prefix'), 'include')]
library_dirs = [join(get_config_var('prefix'), 'lib')]

if platform.system() == 'Windows':
    include_dirs += windows_include_dirs()
    library_dirs += windows_library_dirs()
    libraries = [
        windows_find_libname('liknorm', library_dirs)
    ]

else:
    libraries = ['liknorm']
    include_dirs += ['/usr/include', '/usr/local/include']
    library_dirs += ['/usr/lib', '/usr/local/lib']

if prefix_liknorm_include(include_dirs):
    interface_content = interface_content.replace(
        "include \"liknorm.h\"", "include \"liknorm/liknorm.h\"")

ffibuilder.set_source(
    "liknorm.machine_ffi",
    interface_content,
    libraries=libraries,
    library_dirs=library_dirs,
    include_dirs=include_dirs,
    language='c')

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
