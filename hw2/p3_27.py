import primefac

def smooth(i,b):
  f = primefac.factorint(i)
  for j in f.keys():
    if j > b:
      return False
  return True

def phi(x,b):
  count = 0
  for i in range(2,x+1):
    if smooth(i,b):
      count += 1
  return count

if __name__ == '__main__':
  x = 100
  b = 7
  phi_value = phi(x,b)
  print 'phi(' + str(x) + ',' + str(b) + ') =',phi_value
