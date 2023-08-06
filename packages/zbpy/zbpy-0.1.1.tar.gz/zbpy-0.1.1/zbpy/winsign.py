from ellipticcurve.signature import Signature
from ellipticcurve.math import Math 
from ellipticcurve.utils.integer import RandomInteger
from ellipticcurve.utils.binary import BinaryAscii


def sign(signing_bytes, pk, hashfunc):
    """
    Returns r, s.
    """
    hashed = hashfunc(signing_bytes).digest()
    num_bytes = BinaryAscii.numberFromString(hashed)
    curve = pk.curve 
    rand_num = RandomInteger.between(1, curve.N - 1)
    rand_sign_point = Math.multiply(curve.G, n=rand_num, A=curve.A, P=curve.P, N=curve.N)
    r = rand_sign_point.x % curve.N 
    s = ((num_bytes + r * pk.secret) * (Math.inv(rand_num, curve.N))) % curve.N
    
    return r, s
