from fractions import gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

def f(x,g,h,p,alpha,beta):
  if x < p/3:
    return x * g % p, (alpha + 1) % (p-1), beta
  elif x >= p/3 and x < 2*p/3:
    return pow(x,2,p), (2 * alpha) % (p-1), 2 * beta % (p-1)
  else:
    return x * h % p, alpha, (beta + 1) % (p-1)

def addition(x1,y1,x2,y2,p,A):
  if x1 != x2:
    inv = modinv((x2-x1)%p,p)
    if inv == -1:
      return -1,-1
    lamb = inv * (y2-y1) % p
    x = (pow(lamb,2,p) - x1 - x2) % p
    y = (lamb * (x1 - x) - y1) % p
    return x,y
  if x1 == x2:
    inv = modinv(2*y1,p)
    if inv == -1:
      return -1,-1
    lamb = (3 * pow(x1,2,p) + A) * inv % p
    x = (pow(lamb,2,p) - 2 * x1) % p
    y = (lamb * (x1 - x) - y1) % p
    return x,y

def multiply(x,y,p,A,multi):
  x_out = x
  y_out = y
  for i in range(multi-1):
    #print x_out,y_out
    new_x_out,new_y_out = addition(x_out,y_out,x,y,p,A)
    if new_x_out == -1:
      print 'found'
      return i+1,(x_out,y_out,x,y),False
    x_out = new_x_out
    y_out = new_y_out
  return x_out,y_out,True

def find(x_out,y_out,x,y,p):
  if x_out == x:
    g = gcd(2*y_out,p)
  else:
    g = gcd((x_out-x)%p,p)
  return g,p/g

if __name__ == '__main__':
  x = 2                 # initial P
  y = 12                # initial P
  p = 26167             # integer needed to be factored
  A = 4                 # X^3 + A*X + B
  x_out = x
  y_out = y
  max_iteration = 100   # tolerated maximum iteration num
  for i in range(max_iteration):
    x_out,y_out,flag = multiply(x_out,y_out,p,A,i+2)
    if flag == False:
      q,r = find(y_out[0],y_out[1],y_out[2],y_out[3],p)
      break
  print p,'=',q,'*',r
