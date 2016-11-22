from fractions import gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    return x % m
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def f(x,g,h,p,alpha,beta):
  if x < p/3:
    return x * g % p, (alpha + 1) % (p-1), beta
  elif x >= p/3 and x < 2*p/3:
    return pow(x,2,p), (2 * alpha) % (p-1), 2 * beta % (p-1)
  else:
    return x * h % p, alpha, (beta + 1) % (p-1)

if __name__ == '__main__':
  g = 2
  h = 2495
  p = 5011
  x = 1
  alpha_x = 0
  beta_x = 0
  y = 1
  alpha_y = 0
  beta_y = 0
  collision = False
  i = 0
  while not collision:
    print i,x,y,alpha_x,beta_x,alpha_y,beta_y
    x,alpha_x,beta_x = f(x,g,h,p,alpha_x,beta_x)

    y,alpha_y,beta_y = f(y,g,h,p,alpha_y,beta_y)
    y,alpha_y,beta_y = f(y,g,h,p,alpha_y,beta_y)
    i += 1
    if x == y:
      break
    
  print i,x,y,alpha_x,beta_x,alpha_y,beta_y

  alpha_diff = (alpha_x - alpha_y) % (p-1)
  beta_diff = (beta_y - beta_x) % (p-1)
  print g,'with pow',alpha_diff, 'equals to',h,'with pow',beta_diff
  ab_gcd = gcd(alpha_diff,beta_diff)
  print 'gcd is:',ab_gcd

  tmp_beta_multiply = modinv(beta_diff,(p-1))
  additional_multiply = ab_gcd / (beta_diff*tmp_beta_multiply % (p-1))
  tmp_beta_multiply *= additional_multiply
  #print 'check:',beta_diff*tmp_beta_multiply%(p-1),'==',ab_gcd
  tmp_solution = tmp_beta_multiply * alpha_diff / ab_gcd % (p-1)
  #print pow(g,tmp_solution*ab_gcd,p),'==',pow(h,ab_gcd,p)
  for i in range(ab_gcd):
    solution = (tmp_solution + i * (p-1)/ab_gcd) % (p-1)
    print 'checking possible solution:', solution,'...'
    remainder = pow(g,solution,p)
    #print remainder
    if remainder == h:
      print 'solution is:', solution
      break
