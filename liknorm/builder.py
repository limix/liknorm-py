from os.path import join
from sysconfig import get_config_var

from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_unicode(False)

ffibuilder.cdef(r"""
    typedef struct LikNormMachine LikNormMachine;
    enum Lik {
        BERNOULLI,
        BINOMIAL,
        POISSON,
        EXPONENTIAL,
        GAMMA,
        GEOMETRIC
    };

    LikNormMachine* create_machine(int);
    void apply1d(LikNormMachine *, enum Lik, size_t, double *, double *,
                 double *, double *, double *, double *);
    void apply2d(LikNormMachine *, enum Lik, size_t, double *, double *,
                 double *, double *, double *, double *, double *);
    void destroy_machine(LikNormMachine *);
""")

ffibuilder.set_source(
    "liknorm.machine_ffi",
    r"#include \"liknorm/liknorm.h\"",
    sources=[join('liknorm', '_machine_ffi.c')],
    libraries=['liknorm'],
    library_dirs=[join(get_config_var('prefix'), 'lib')],
    include_dirs=[join(get_config_var('prefix'), 'include')])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
