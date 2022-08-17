import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path
from typing import List

from cffi import FFI
from cmake import CMAKE_BIN_DIR

pwd = Path(os.path.dirname(os.path.abspath(__file__)))


def rm(folder: Path, pattern: str):
    for filename in folder.glob(pattern):
        filename.unlink()


def build_deps(pwd: Path, user: str, project: str, version: str):
    ext_dir = pwd / ".ext_deps"
    shutil.rmtree(ext_dir, ignore_errors=True)

    prj_dir = ext_dir / f"{project}-{version}"
    build_dir = prj_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    url = f"https://github.com/{user}/{project}/archive/refs/tags/v{version}.tar.gz"

    with urllib.request.urlopen(url) as rf:
        data = rf.read()

    tar_filename = f"{project}-{version}.tar.gz"

    with open(ext_dir / tar_filename, "wb") as lf:
        lf.write(data)

    with tarfile.open(ext_dir / tar_filename) as tf:
        tf.extractall(ext_dir)

    cmake_bin = str(next(Path(CMAKE_BIN_DIR).glob("cmake*")))
    subprocess.check_call(
        [
            cmake_bin,
            "-S",
            str(prj_dir),
            "-B",
            str(build_dir),
            "-DCMAKE_BUILD_TYPE=Release",
            "-DENABLE_ALL_WARNINGS=ON",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
        ],
    )
    subprocess.check_call([cmake_bin, "--build", str(build_dir), "--config", "Release"])
    subprocess.check_call(
        [cmake_bin, "--install", str(build_dir), "--prefix", str(ext_dir)]
    )
    rm(ext_dir / "lib", "*.dylib")
    rm(ext_dir / "lib", "*.so*")
    rm(ext_dir / "lib64", "*.dylib")
    rm(ext_dir / "lib64", "*.so*")


if not os.getenv("LIKNORM_SKIP_BUILD_DEPS", False):
    build_deps(pwd, "limix", "liknorm", "1.5.7")

with open(pwd / "liknorm" / "interface.h", "r") as f:
    interface_h = f.read()

with open(pwd / "liknorm" / "interface.c", "r") as f:
    interface_c = f.read()

extra_link_args: List[str] = []
if "LIKNORM_EXTRA_LINK_ARGS" in os.environ:
    extra_link_args += os.environ["LIKNORM_EXTRA_LINK_ARGS"].split(os.pathsep)

ffibuilder = FFI()
ffibuilder.cdef(interface_h)
ffibuilder.set_source(
    "liknorm._ffi",
    interface_c,
    libraries=["liknorm"],
    extra_link_args=extra_link_args,
    language="c",
    library_dirs=[str(pwd / ".ext_deps" / "lib"), str(pwd / ".ext_deps" / "lib64")],
    include_dirs=[str(pwd / ".ext_deps" / "include")],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
