import math

e = math.e
year_computations = 365.25 * 24 * 60 * 60 * pow(10,9)

ln_n = 2000
ln_ln_n = math.log(ln_n)

exp = math.sqrt(ln_n*ln_ln_n)

LN = pow(e,exp)

time = LN / year_computations

print 'require:',time,'years'
