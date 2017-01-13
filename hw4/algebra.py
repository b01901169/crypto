import random
import numpy as np
import itertools
from sympy import *
from scipy.linalg import lu

def generateSolution(number,module):
  solutions = []
  for i in range(number):
    solutions.append(random.randint(0,module-1))
  return solutions

def assignCoefficient(variables,solutions,order,module):
  #coefficients = {}
  const_value = 0
  variable_number = len(variables)
  f = 0
  for i in range(order,0,-1):
    vec = [range(variable_number)] * i
    for element in itertools.product(*vec):
      element = list(element)
      if not element == sorted(element):
        continue
      tmp_coefficient = random.randint(0,module-1)
      #coefficients[str(element)] = tmp_coefficient
      tmp_add = tmp_coefficient
      for variable_index in element:
        tmp_add *= variables[variable_index]
      f += tmp_add

      tmp_value = tmp_coefficient
      for j in range(len(element)):
        tmp_value *= solutions[element[j]]
      const_value = (const_value + tmp_value) % module
  const_value = (-const_value) % module
  #coefficients['const'] = const_value
  f += const_value
  return f

def raisePolynomials(variables,order):
  variable_number = len(variables)
  raise_polynomials = []
  largest_polynomials = []
  for i in range(order,0,-1):
    vec = [range(variable_number)] * i
    for element in itertools.product(*vec):
      element = list(element)
      element_set = set(element)
      if element == sorted(element):
        f = 1
        for j in element:
          f *= variables[j]
        if (len(element_set) == 1) and (list(element_set)[0] == (len(variables)-1)):
          largest_polynomials.append(f)
        else:
          raise_polynomials.append(f)
  return raise_polynomials + largest_polynomials + [1]

def getCoefficientMatrix(polynomials,monomials):
  cm = []
  for polynomial in polynomials:
    coeff = []
    p = Poly(polynomial)
    for monomial in monomials:
      coeff.append(p.coeff_monomial(monomial))
    cm.append(coeff)
  return cm

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

def gaussElimination(origin_rc,module=None):
  rc = origin_rc
  shape = rc.shape
  zero_row = [0] * shape[1]
  pre_row = zero_row
  pivot_row = 0
  print 'gauss elimination ...'
  while 1:
    error = False
    if pivot_row >= shape[1]:
      break
    row = rc[pivot_row]
    if (row == zero_row).all():
      #print rc
      break
    else:
      nonzero = np.where(row)
      if len(nonzero[0]) > 0:
        position = nonzero[0][0]
        #print position
      else:
        #print 'all zero:', row
        break
      #print "pivot_row:",pivot_row,"position:",position
      #print "row:",row
      pivot = row[position]
      #print position 
      if module:
        inverse = modinv(int(pivot),module)
      else:
        inverse = 1/float(pivot)
      for i in range(pivot_row+1,shape[0]):
        if module:
          rc[i] = (rc[i] - row * inverse * rc[i][position]) % module
        else:
          rc[i] = rc[i] - row * inverse * rc[i][position]
      find = False
      pivot_row += 1
      for next_position in range(position+1,shape[1]):
        for i in range(pivot_row+1,shape[0]):
          if rc[i][next_position] != 0:
            tmp = np.array(rc[i])
            rc[i] = rc[pivot_row]
            rc[pivot_row] = tmp
            find = True
          if find:
            break
        if find:
          break
      if not find:
        #print "not find:", pivot_row, position
        #print rc
        break
  #print "last row = ", rc[pivot_row-1]
  return rc,pivot_row-1

if __name__ == "__main__":
  # ========== the following part is the customized variables ===========
  variable_number = 3 # needed to be smaller than 10 XD
  x = Symbol('x')
  y = Symbol('y')
  z = Symbol('z')
  variables = [x,y,z] # variables
  equation_number = 5 # number of the equations
  module = 7 # modular XD
  order = 2 # origin equations order
  raise_order = 3 # order to be raised
  # =====================================================================
  total_order = order + raise_order
  solutions = generateSolution(variable_number,module)
  print 'random solutions:', solutions
  polynomials = []
  for i in range(equation_number):
    f = assignCoefficient(variables,solutions,order,module)
    polynomials.append(f)
    print "equation " + str(i)," :", f

  raise_monomials = raisePolynomials(variables,raise_order)

  total_polynomials = []
  for p in polynomials:
    for q in raise_monomials:
      total_polynomials.append(p*q)

  total_monomials = raisePolynomials(variables,order + raise_order)

  cm = getCoefficientMatrix(total_polynomials, total_monomials)
  cm = np.array(cm)

  new_cm, pivot_row = gaussElimination(cm,module)
  vec = new_cm[pivot_row]

  shape = cm.shape
  if (np.where(vec)[0] >= shape[1] - total_order).all():
    z_vec = vec[-(total_order+1):]
    possible_solution = []

    # ==================== z part =========================
    f = 0
    for i in range(len(total_monomials)):
      f += vec[i] * total_monomials[i]
    print "solve z by solving:",f

    for zz in range(module):
      s = 0
      for j in range(total_order+1):
        s = (s + z_vec[j] * zz**(total_order - j)) % module
      if s == 0:
        possible_solution.append(zz)
    #print possible_solution
    if len(possible_solution) == 1:
      true_z = possible_solution[0]
    else:
      print "many possible solutions of z QQ:", possible_solution
    
    # ==================== y part ==========================
    for y_pivot_row in range(pivot_row,-1,-1):
      y_vec = new_cm[y_pivot_row]
      if y_vec[-(total_order+2)] != 0:
        break
    f = 0
    for i in range(len(total_monomials)):
      f += y_vec[i] * total_monomials[i]
    print "solve y by solving:",f

    y_coeff = y_vec[-(total_order+2)]
    y_vec = y_vec[-(total_order+1):]
    sy = 0
    for j in range(total_order+1):
      sy = (sy + y_vec[j] * true_z**(total_order-j)) % module
    y_coeff_inverse = modinv(y_coeff,module)
    sy = (-sy * y_coeff_inverse) % module
    true_y = sy
  
    # ==================== x part ==========================
    for x_pivot_row in range(pivot_row,-1,-1):
      x_vec = new_cm[x_pivot_row]
      if x_vec[-(total_order+3)] != 0:
        break
    f = 0
    for i in range(len(total_monomials)):
      f += x_vec[i] * total_monomials[i]
    print "solve x by solving:",f

    x_coeff = x_vec[-(total_order+3)]
    x_y_coeff = x_vec[-(total_order+2)]
    x_vec = x_vec[-(total_order+1):]
    sx = 0
    for j in range(total_order+1):
      sx = (sx + x_vec[j] * true_z**(total_order-j)) % module
    sx = (sx + x_y_coeff * true_y) % module
    x_coeff_inverse = modinv(x_coeff,module)
    sx = (-sx * x_coeff_inverse) % module
    true_x = sx

    # ==================== solutions =======================
    print "solved (x,y,z):", (true_x,true_y,true_z)

  else:
    print "fail..."

