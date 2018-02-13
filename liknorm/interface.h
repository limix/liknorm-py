typedef struct LikNormMachine LikNormMachine;
enum Lik { BERNOULLI, BINOMIAL, POISSON, EXPONENTIAL, GAMMA, GEOMETRIC };

LikNormMachine *create_machine(int);
void apply1d(LikNormMachine *, enum Lik, size_t, double *, double *, double *,
             double *, double *, double *);
void apply2d(LikNormMachine *, enum Lik, size_t, double *, double *, double *,
             double *, double *, double *, double *);
void destroy_machine(LikNormMachine *);
