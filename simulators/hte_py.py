#versao em python do hte. precisa ser otimizada (ex.: usar np.array em vez de lista built-in do python)

import math
import sys

CONT_FRAC_STEPS=20

def lbeta(a, b):
    return(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


def IB(x, a, b):
    multiplier=0
    fraction = x/4.0
    d=0
    m=0
    i=0

    if (x >= (a + 1) / (a + b + 1)):
        return(1 - IB(1 - x, b, a))

    multiplier = a * math.log(x) + b * math.log(1-x) - math.log(a) - lbeta(a, b)

    for i in range (CONT_FRAC_STEPS, 0, -1):
        m = i >> 1
        if (i & 1):
            d = -(a + m)*(a + b + m)*x / ((a + 2*m) * (a + 2*m + 1))
        else:
            d = m * (b - m) * x / ((a + 2*m) * (a + 2*m - 1))
        fraction = d / fraction + 1

    fraction = 1 / fraction
    return(math.exp(multiplier + math.log(fraction)))


def Fbin(k, n, p):
    
    return(1 - IB(p, k + 1, n - k))

def Pbin(k, n, p):
    return(math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1 - p)))



def invFbin(n, probab, q):

    k=0
    lowerK = -1
    lowerBound=0
    upperBound=0
    FbinAtK=0.0
    FbinAtLowerK=0.0

    p = probab

    if (q <= 0.0): 
        return(0)
    if (q >= 1.0): 
        return(n)


    if (p == 0):
        return 0

    if (p == 1): 
        return n


    lowerBound = 0
    upperBound = n

    if (q < 0.5):
        upperBound = int(n * p)

    else: 
        lowerBound = int(n * p)
    k = (upperBound + lowerBound) >> 1

    while(lowerBound < upperBound):

        if (k == lowerK):
            FbinAtK = FbinAtLowerK
        else:
            FbinAtK = Fbin(k, n, p)
        if (FbinAtK > q):
            if (k == 0): 
                return(0)
            lowerK = k - 1
            FbinAtLowerK = Fbin(lowerK, n, p)
            if (FbinAtLowerK < q): 
                return(k)
            upperBound = k - 1
        else:
            lowerBound = k + 1

        k = (lowerBound + upperBound) >> 1
    return(k)


#nao precisa
# t_window = {probes: [], first: 0, last: 0, length: 0, maxLength: 0, totalOn: 0, totalOff: 0}



def window_init(maxLength):
    t_window = {'probes': [0]*maxLength, 'first': 0, 'last': 0, 'length': 0, 'maxLength': maxLength, 'totalOn': 0, 'totalOff': 0}
    return t_window


def window_newprobe(w, value):

    if (w['length'] < w['maxLength']):
        w['probes'][w['last']] = value
        w['length'] = w['length']+1
    else:
        if (w['probes'][w['first']] == 0): 
            w['totalOff'] = w['totalOff']-1
        else: 
            w['totalOn'] = w['totalOn']-1

        w['probes'][w['last']] = value
        w['first'] = (w['first'] + 1) % w['maxLength']

    if (value == 0):
        w['totalOff'] = w['totalOff']+1
    else:
        w['totalOn'] = w['totalOn']+1

    w['last']=(w['last']+1) % w['maxLength']


def window_empty(w):
    w['length'] = 0
    w['first'] = 0
    w['last'] = 0



def window_getOn(w):
    return w['totalOn']

def window_getLength(w):
    return w['length']

# def probes_next()
#     unsigned int input;
#     unsigned char probe;

#     if (feof(stdin)) return(0xFF);
#     fscanf(stdin, "%d\n", & input);
#     probe = 0xFF & input;

#     return(probe);


n=0
k=0
p=0.0
q=0.0
alpha=0.0
probe=0
lowerBoundK = -1
upperBoundK = -1
n = int(sys.argv[1])
alpha = float(sys.argv[2])

probes = sys.stdin.read().splitlines()
probes = [int(x) for x in probes]
# trace_file = sys.argv[3]
# with open (trace_file, 'r') as trace:
#     probes = trace.read().splitlines()
#     probes = [int(x) for x in probes]

window = window_init(n)

for i in range(len(probes)):

    probe = probes[i]
    window_newprobe(window, probe)
    k = window_getOn(window)

    if (window_getLength(window) < n):
        p = k / n
    elif (lowerBoundK == -1):
        p = k / n
        lowerBoundK = invFbin(n, p, alpha / 2.0)
        upperBoundK = invFbin(n, p, 1 - alpha / 2.0)
    else:
        if (k < lowerBoundK or k > upperBoundK):
            p = k / n
            lowerBoundK = invFbin(n, p, alpha / 2.0)
            upperBoundK = invFbin(n, p, 1 - alpha / 2.0)
    print(p)

