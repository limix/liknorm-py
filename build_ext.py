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

extra_link_args: List[str] = []
if "LIKNORM_EXTRA_LINK_ARGS" in os.environ:
    extra_link_args += os.environ["LIKNORM_EXTRA_LINK_ARGS"].split(os.pathsep)

ffibuilder.set_source(
    "liknorm._ffi",
    _get_interface_c(),
    extra_link_args=extra_link_args,
    language="c",
    libraries=["liknorm"],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
