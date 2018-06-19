#include "liknorm.h"

enum Lik {
    BERNOULLI,
    BINOMIAL,
    POISSON,
    EXPONENTIAL,
    GAMMA,
    GEOMETRIC,
    PROBIT
};

struct LikNormMachine *create_machine(int n) {
    return liknorm_create_machine(n);
}
void destroy_machine(struct LikNormMachine *machine) {
    liknorm_destroy_machine(machine);
}

typedef void lik1d(struct LikNormMachine *, double);
typedef void lik2d(struct LikNormMachine *, double, double);

void *set_lik[] = {liknorm_set_bernoulli, liknorm_set_binomial,
                   liknorm_set_poisson,   liknorm_set_exponential,
                   liknorm_set_gamma,     liknorm_set_geometric,
                   liknorm_set_probit};

void apply1d(struct LikNormMachine *machine, enum Lik lik, int size, double *x,
             double *tau, double *eta, double *log_zeroth, double *mean,
             double *variance) {
    int i;
    for (i = 0; i < size; ++i) {
        ((lik1d *)set_lik[lik])(machine, x[i]);
        liknorm_set_prior(machine, tau[i], eta[i]);
        liknorm_integrate(machine, log_zeroth + i, mean + i, variance + i);
    }
}

void apply2d(struct LikNormMachine *machine, enum Lik lik, int size, double *x0,
             double *x1, double *tau, double *eta, double *log_zeroth,
             double *mean, double *variance) {
    int i;
    for (i = 0; i < size; ++i) {
        ((lik2d *)set_lik[lik])(machine, x0[i], x1[i]);
        liknorm_set_prior(machine, tau[i], eta[i]);
        liknorm_integrate(machine, log_zeroth + i, mean + i, variance + i);
    }
}
