
if __name__ == '__main__':
  n = 64213
  b = 1
  while 1:
    m = n+pow(b,2)
    a = int(pow(m,0.5))
    if pow(a,2) == m:
      print a+b,a-b
      print 'b:',b,'a:',a
      break
    b += 1
  print 'check:',(a+b)*(a-b),'=',n
