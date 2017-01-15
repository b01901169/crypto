from Crypto.Util.number import getPrime
from math import log

n_bits = 512
p_bits = n_bits/2

p = getPrime(p_bits)
q = getPrime(p_bits)

N = p*q

print "N =",N
print p,q
print log(N,2)
