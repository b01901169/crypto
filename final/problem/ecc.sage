# set_random_seed(1234567)
bits = 100
P = random_prime(2^bits-1,True,2^(bits-1))

x = ZZ.random_element(P)
y = ZZ.random_element(P)
A = ZZ.random_element(P)

R = Integers(P)
B = R(y^2 - x^3 - A*x)

ECC = EllipticCurve(R,[A,B])
G = ECC(x,y)
G_order = G.order()
GR = Integers(G_order)

k = Integer(GR(ZZ.random_element(P)))
kG = k*G

print "P =", P
print "A =", A
print "B =", B
print "G = " + "(" + str(G[0]) + "," + str(G[1]) + ")"
print "kG = " + "(" + str(kG[0]) + "," + str(kG[1]) + ")"

print "order =", G_order
print "k =", k


