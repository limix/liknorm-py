import os
import shutil
import sysconfig
from pathlib import Path
from subprocess import check_call

from cffi import FFI
from git import Repo


def envlist(name: str) -> list[str]:
    value = os.environ.get(name, None)
    if value is None:
        return []
    return value.split(":")


def uname():
    if os.name == "nt":
        return "Windows"
    return os.uname().sysname


def build_and_install(
    root: Path, prefix: str, git_url: str, prj_dir: str, dst_dir: str, force: bool
):
    os.makedirs(root / ".gitdir", exist_ok=True)
    if force or not (root / dst_dir).exists():
        shutil.rmtree(root / ".gitdir" / dst_dir, ignore_errors=True)
        Repo.clone_from(git_url, root / ".gitdir" / dst_dir, depth=1)
        shutil.rmtree(root / dst_dir, ignore_errors=True)
        shutil.move(root / ".gitdir" / dst_dir / prj_dir, root / dst_dir)

    env = os.environ.copy()
    env["C_INCLUDE_PATH"] = ":".join(envlist("C_INCLUDE_PATH") + [f"{prefix}/include"])
    env["LIBRARY_PATH"] = ":".join(envlist("LIBRARY_PATH") + [f"{prefix}/lib"])
    env["CFLAGS"] = "-std=c11 -O3 -fPIC"
    env["PREFIX"] = prefix

    if uname() == "Darwin" and "MACOSX_DEPLOYMENT_TARGET" not in env:
        target = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")
        env["MACOSX_DEPLOYMENT_TARGET"] = target

    check_call(["make"], cwd=root / dst_dir, env=env)
    check_call(["make", "install"], cwd=root / dst_dir, env=env)


if __name__ == "__main__":
    CWD = Path(".").resolve()
    TMP = CWD / ".build_ext"
    PKG = CWD / "liknorm"

    url = "https://github.com/limix/liknorm.git"
    build_and_install(TMP, str(PKG), url, ".", "liknorm", True)

    ffibuilder = FFI()

    interface_c = open(PKG / "interface.c", "r").read()
    ffibuilder.cdef(open(PKG / "interface.h", "r").read())
    ffibuilder.set_source(
        "liknorm._cffi",
        interface_c,
        language="c",
        libraries=["liknorm"],
        library_dirs=[str(PKG / "lib")],
        include_dirs=[str(PKG / "include")],
    )

    ffibuilder.compile(verbose=True)
