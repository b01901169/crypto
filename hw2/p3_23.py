from p3_22 import *

if __name__ == '__main__':
  for i in range(2,23):
    n = pow(2,i) - 1
    if factor(n):
      print i,n
