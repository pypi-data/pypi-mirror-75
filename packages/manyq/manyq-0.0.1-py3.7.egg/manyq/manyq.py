try: import cupy
except: pass
try: import numexpr as ne
except: pass
import numpy

np = numpy

class Qreg:
    nbqubits = 2
    n = 1  # batch size
    gpu = False
    multicore = False
    inQ = np.zeros((2**nbqubits, n), dtype=np.complex)  # quantum state, input buffer 
    outQ = np.empty_like(inQ)                           # quantum state, output buffer 


def initQreg(nbqubits, n=1, gpu =False, multicore=False):
    """ all qubits at ket0"""
    Qreg.multicore = multicore
    if Qreg.nbqubits == nbqubits and\
            Qreg.n == n and\
            Qreg.inQ.shape == (2**nbqubits, n) and\
            Qreg.gpu == gpu and\
            Qreg.outQ.shape == (2**nbqubits, n):
        # * No need to allocate memory if already done
        Qreg.inQ.fill(0)
        Qreg.inQ[0].fill(1)
        return
    Qreg.gpu = gpu
    global np
    if gpu: np = cupy
    Qreg.nbqubits = nbqubits
    Qreg.n = n
    Qreg.inQ = np.zeros((2**nbqubits, n), dtype=np.complex)
    Qreg.outQ = np.empty_like(Qreg.inQ)
    Qreg.inQ[0] = np.ones(n)

# initQreg(2,3)
# print(Qreg.inQ)

def oneQubitGate(gate, qbit):
    if Qreg.multicore: 
        oneQubitGate_multicore(gate,qbit)
        return
    shape = (2**qbit, 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape
    Qreg.outQ[:, 0, :] = (gate[0, 0] * Qreg.inQ[:, 0, :] +
                          gate[0, 1] * Qreg.inQ[:, 1, :])
    Qreg.outQ[:, 1, :] = (gate[1, 0] * Qreg.inQ[:, 0, :] +
                          gate[1, 1] * Qreg.inQ[:, 1, :])

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ

def oneQubitGate_multicore(gate, qbit):
    shape = (2**qbit, 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape
    
    g00, g01, g10, g11 = gate[0, 0], gate[0, 1], gate[1, 0], gate[1, 1]
    q0,q1 = Qreg.inQ[:, 0, :], Qreg.inQ[:, 1, :]
    
    Qreg.outQ[:, 0, :] = ne.evaluate('g00 * q0 + g01 * q1')
    Qreg.outQ[:, 1, :] = ne.evaluate('g10* q0 + g11 * q1')

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ



def twoQubitGate(gate, qbit0, qbit1):
    """ qbit1 > qbit0 """
    shape = (2**qbit0, 2, 2**(qbit1 - qbit0 - 1), 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape

    Qreg.outQ[:, 0, :, 0, :] = (Qreg.inQ[:, 0, :, 0, :]*gate[0, 0] + Qreg.inQ[:, 0, :, 1, :]*gate[0, 1] +
                                gate[0, 2]*Qreg.inQ[:, 1, :, 0, :] + gate[0, 3]*Qreg.inQ[:, 1, :, 1, :])

    Qreg.outQ[:, 0, :, 1, :] = (Qreg.inQ[:, 0, :, 0, :]*gate[1, 0] + Qreg.inQ[:, 0, :, 1, :]*gate[1, 1] +
                                Qreg.inQ[:, 1, :, 0, :]*gate[1, 2] + Qreg.inQ[:, 1, :, 1, :]*gate[1, 3])

    Qreg.outQ[:, 1, :, 0, :] = (Qreg.inQ[:, 0, :, 0, :]*gate[2, 0] + Qreg.inQ[:, 0, :, 1, :]*gate[2, 1] +
                                Qreg.inQ[:, 1, :, 0, :]*gate[2, 2] + Qreg.inQ[:, 1, :, 1, :]*gate[1, 3])

    Qreg.outQ[:, 1, :, 1, :] = (Qreg.inQ[:, 0, :, 0, :]*gate[3, 0] + Qreg.inQ[:, 0, :, 1, :]*gate[3, 1] +
                                Qreg.inQ[:, 1, :, 0, :]*gate[3, 2] + Qreg.inQ[:, 1, :, 1, :]*gate[3, 3])

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ

def RZ(qbit, t):
    """ 
    optimized ( not using oneQubitGate(RZgate(t), qbit) )
    """
    if Qreg.multicore: 
        RZ_multicore(qbit,t)
        return
    t2 = t/2
    cost = np.cos(t2)
    isint = 1j*np.sin(t2)
    gate00 = cost - isint
    gate11 = cost + isint
    shape = (2**qbit, 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape

    Qreg.outQ[:, 0, :] = gate00 * Qreg.inQ[:, 0, :]
    Qreg.outQ[:, 1, :] = gate11 * Qreg.inQ[:, 1, :]

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ

def RZ_multicore(qbit, t):
    """ 
    optimized ( not using oneQubitGate(RZgate(t), qbit) )
    """
    t2 = t/2
    cost = ne.evaluate('cos(t2)')
    isint = ne.evaluate('1j*sin(t2)')
    gate00 = ne.evaluate('cost - isint')
    gate11 = ne.evaluate('cost + isint')
    shape = (2**qbit, 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape
    q0 = Qreg.inQ[:, 0, :]
    q1 = Qreg.inQ[:, 1, :]
    Qreg.outQ[:, 0, :] = ne.evaluate('gate00 * q0')
    Qreg.outQ[:, 1, :] = ne.evaluate('gate11 * q1')

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ



c0 = (1 + 1j)/np.sqrt(2)
c1 = (1 - 1j)/np.sqrt(2)
def ZZ(q0, q1):
    """ 
    Honeywell native entangling gate
    diag(1 + 1j, 1 - 1j, 1 - 1j, 1 + 1j)/sqrt(2)
    diag(c0,c1,c1,c0)
    """
    qbit0 = min(q0, q1)
    qbit1 = max(q0, q1)
    shape = (2**qbit0, 2, 2**(qbit1 - qbit0 - 1), 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape

    Qreg.outQ[:, 0, :, 0, :] = c0 * Qreg.inQ[:, 0, :, 0, :]
    Qreg.outQ[:, 0, :, 1, :] = c1 * Qreg.inQ[:, 0, :, 1, :]
    Qreg.outQ[:, 1, :, 0, :] = c1 * Qreg.inQ[:, 1, :, 0, :]
    Qreg.outQ[:, 1, :, 1, :] = c0 * Qreg.inQ[:, 1, :, 1, :]

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ


def CZ(c, t):
    """ 
    diag(1,1,1,-1)
    """
    qbit0 = min(c, t)
    qbit1 = max(c, t)
    shape = (2**qbit0, 2, 2**(qbit1 - qbit0 - 1), 2, -1, Qreg.n)
    Qreg.inQ.shape = shape
    Qreg.outQ.shape = shape

    a0 = a1 = a2 = 1
    a3 = -1

    # q00, q01, q10, q11 = Qreg.inQ[:, 0, :, 0, :], Qreg.inQ[:, 0, :, 1, :], Qreg.inQ[:, 1, :, 0, :], Qreg.inQ[:, 1, :, 1, :]

    Qreg.outQ[:, 0, :, 0, :] = Qreg.inQ[:, 0, :, 0, :]
    Qreg.outQ[:, 0, :, 1, :] = Qreg.inQ[:, 0, :, 1, :]
    Qreg.outQ[:, 1, :, 0, :] = Qreg.inQ[:, 1, :, 0, :]
    Qreg.outQ[:, 1, :, 1, :] = - Qreg.inQ[:, 1, :, 1, :]

    Qreg.inQ.shape = (-1, Qreg.n)
    Qreg.outQ.shape = (-1, Qreg.n)
    Qreg.inQ, Qreg.outQ = Qreg.outQ, Qreg.inQ



Hgate = numpy.array([[1, 1], [1, -1]], dtype=numpy.complex)/numpy.sqrt(2)
Xgate = numpy.array([[0, 1], [1, 0]], dtype=numpy.complex)
SXgate = numpy.array([[1+1j, 1-1j], [1-1j, 1+1j]], dtype=numpy.complex)/2
Zgate = numpy.array([[1, 0], [0, -1]], dtype=numpy.complex)


def SX(qbit): oneQubitGate(SXgate, qbit)
def H(qbit): oneQubitGate(Hgate, qbit)
def X(qbit): oneQubitGate(Xgate, qbit)
def Z(qbit): oneQubitGate(Zgate, qbit)


CX01 = numpy.array([[1, 0, 0, 0], 
                 [0, 1, 0, 0], 
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]], dtype=numpy.complex)
CX10 = numpy.array([[1, 0, 0, 0], 
                 [0, 0, 0, 1], 
                 [0, 0, 1, 0],
                 [0, 1, 0, 0]], dtype=numpy.complex)


def CX(c, t):
    if c < t:
        twoQubitGate(CX01, c, t)
    else:
        twoQubitGate(CX10, t, c)



def measureAll():
    Qreg.mQ = np.abs(Qreg.inQ)**2
    return Qreg.mQ


def makeShots(nbshots):
    """ 
    has to be called after measureAll
    """
    if Qreg.gpu: Qreg.mQ = cupy.asnumpy(Qreg.mQ)
    def fun(v): return np.random.multinomial(nbshots, v)
    return numpy.apply_along_axis(fun, 0, Qreg.mQ)

