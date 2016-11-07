from fractions import gcd

if __name__ == '__main__':
  n = 2510839
  k = 21
  b_init = 90
  b = b_init
  kn = k*n
  while 1:
    m = kn+pow(b,2)
    a = int(pow(m,0.5))
    if pow(a,2) == m:
      print a+b,a-b
      break
    b += 1
  print 'check kn:',(a+b)*(a-b),'=',kn
  d = gcd(a+b,n)
  print n,'has prime:',d,n/d
