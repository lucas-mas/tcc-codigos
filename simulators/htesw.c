
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

#define CONT_FRAC_STEPS     20

double lbeta(double a, double b) {

    return(lgamma(a) + lgamma(b) - lgamma(a + b));
}

double IB(double x, double a, double b) {

    double multiplier;
    double fraction = x/4.0;
    double d;
    int m, i;

    //if (x==0) fraction = 0;

    if (x >= (a + 1) / (a + b + 1)) return(1 - IB(1 - x, b, a));

    multiplier = a * log(x) + b * log(1-x) - log(a) - lbeta(a, b);
//printf("multiplier = %.4f, lbeta(%1.0f,%1.0f) = %e\n", multiplier, a, b, lbeta(a, b));
    for (i = CONT_FRAC_STEPS; i > 0; i--) {

        m = i >> 1;
        if (i & 1) {

            d = -(a + m)*(a + b + m)*x / ((a + 2*m) * (a + 2*m + 1));
        }
        else {

            d = m * (b - m) * x / ((a + 2*m) * (a + 2*m - 1));
        }

        fraction = d / fraction + 1;
    }

    fraction = 1 / fraction;
//printf("fraction = %.4f (%e)\n", fraction, fraction);
    return(exp(multiplier + log(fraction)));
}

double Fbin(int k, int n, double p) {

    return(1 - IB(p, (double) k + 1, (double) n - k));
}

double Pbin(int k, int n, double p) {

    return(exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * log(p) + (n - k) * log(1 - p)));
}


/*
 * Find lowest value of k s.t. Fbin(k, n, p) >= q.
 * Binary search.
 */

//n eh o w(janela), probab eh a probabilidade estimada,
//e q eh o alfa/2 (ou, no caso do calculo do limite superior, eh 1-alfa/2)
int invFbin(int n, double probab, double q) {

    int k;
    int lowerK = -1;
    int lowerBound, upperBound;
    double FbinAtK;
    double FbinAtLowerK;

    double p = probab;

    if (q <= 0.0) return(0);
    if (q >= 1.0) return(n);


    if (p == 0) return 0;


    if (p == 1) return n;


    lowerBound = 0;
    upperBound = n;


    if (q < 0.5) upperBound = (int) (n * p);

    else lowerBound = (int) (n * p);



    k = (upperBound + lowerBound) >> 1;


    while(lowerBound < upperBound) {

        if (k == lowerK) {

            FbinAtK = FbinAtLowerK;
        }
        else {

            FbinAtK = Fbin(k, n, p);





        }


        if (FbinAtK > q) {

            if (k == 0) return(0);

            lowerK = k - 1;
            FbinAtLowerK = Fbin(lowerK, n, p);
            if (FbinAtLowerK < q) return(k);

            upperBound = k - 1;
        }
        else {

            lowerBound = k + 1;
        }



        k = (lowerBound + upperBound) >> 1;
    }

    return(k);

}

typedef struct {

    unsigned char * probes;
    int first;
    int last;
    int length;
    int maxLength;
    int totalOn;
    int totalOff;
} t_window;

t_window * window_init(int maxLength) {

    t_window * w;

    w = (t_window *) malloc(sizeof(t_window));
    w->probes = (unsigned char *) malloc(maxLength);
    w->length = 0;
    w->first = 0;
    w->last = 0;
    w->maxLength = maxLength;

    return(w);
}

void window_newprobe(t_window * w, unsigned char value) {

    if (w->length < w->maxLength) {

        w->probes[w->last] = value;
        w->length++;
    }
    else {

        if (w->probes[w->first] == 0) w->totalOff--;
        else w->totalOn--;

        w->probes[w->last] = value;
        w->first = (w->first + 1) % w->maxLength;
    }

    if (value == 0) w->totalOff++;
    else w->totalOn++;

    w->last = (w->last + 1) % w->maxLength;
}

void window_empty(t_window * w) {

    w->length = 0;
    w->first = 0;
    w->last = 0;
}

int window_getOn(t_window * w) {

    return(w->totalOn);
}

int window_getLength(t_window * w) {

    return(w->length);
}

unsigned char probes_next() {

    unsigned int input;
    unsigned char probe;

    if (feof(stdin)) return(0xFF);
    fscanf(stdin, "%d\n", & input);
    probe = 0xFF & input;

    return(probe);
}


void half_window_fill (t_window * half_window, t_window * full_window) {

    int full_window_middle_probe_index= (full_window->first+ full_window->length/2) % full_window->length;


    for (int i=0;  i < full_window->maxLength/2; i++) {
        window_newprobe(half_window, full_window->probes[full_window_middle_probe_index]);
        full_window_middle_probe_index=(full_window_middle_probe_index+1) % full_window->length;
    }
}

t_window * new_full_window(t_window * half_window, int fullWindowMaxLength) {

    t_window * full_window = window_init(fullWindowMaxLength);
    int half_window_index;

    for (int i=0; i < full_window->maxLength; i++) {
        half_window_index = i % half_window->maxLength;
        window_newprobe(full_window, half_window->probes[half_window_index]);
    }
    return full_window;
}


int main(int argc, char ** argv) {

    int n, k;
    double p, q, alpha;
    t_window * window;
    unsigned char probe;
    int lowerBoundK = -1, upperBoundK = -1;
    t_window * half_window;

    
    int halfOpenModeOn=0;
    int halfOpenModeCount=0;

    n = atoi(argv[1]);
    alpha = (double) atof(argv[2]);

    window = window_init(n);

    half_window = window_init(n/2);

    while((probe = probes_next()) != 0xFF) {

        window_newprobe(window, probe);

        k = window_getOn(window);

        if (window_getLength(window) < window->maxLength) {
            p = (double) k / (double) window->maxLength;
        }
        else if (lowerBoundK == -1) {
         
            p = (double) k / (double) window->maxLength;
            lowerBoundK = invFbin(window->maxLength, p, alpha / 2.0);
            upperBoundK = invFbin(window->maxLength, p, 1 - alpha / 2.0);
        }
        else {

            if (k < lowerBoundK || k > upperBoundK) {

                p = (double) k / (double) window->maxLength;
                lowerBoundK = invFbin(window->maxLength, p, alpha / 2.0);
                upperBoundK = invFbin(window->maxLength, p, 1 - alpha / 2.0);

                if (halfOpenModeOn) halfOpenModeCount=0;

                else {
                    halfOpenModeOn=1;
                    half_window_fill(half_window, window);
                    window = half_window;
                    lowerBoundK = invFbin(window->maxLength, p, alpha / 2.0);
                    upperBoundK = invFbin(window->maxLength, p, 1 - alpha / 2.0);
                }
            }

            else if (halfOpenModeOn) {

            	halfOpenModeCount++;

            	if (halfOpenModeCount == n) {
            		halfOpenModeOn=0;
                    halfOpenModeCount=0;
                    window = new_full_window(window, n);


                    lowerBoundK = invFbin(window->maxLength, p, alpha / 2.0);
                    upperBoundK = invFbin(window->maxLength, p, 1 - alpha / 2.0);

            	}
            }
        }


        printf("%.8f\n", p);
    }

    return(0);
}

