import numpy
from fractions import gcd

def factor(n):
  base = 2
  a = base
  for i in range(1,n+1):
    a = pow(a,i,n)
    d = gcd(a-1,n)
    if d == 1 or d == n:
      continue
    print 'prime:',d,n/d
    print 'iteration:',i
    return True
  return False

if __name__ == '__main__':
  n1 = 1739
  n2 = 220459
  n3 = 48356747
  factor(n1)
  factor(n2)
  factor(n3)
  
