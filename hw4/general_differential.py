import numpy as np
import random
import pprint
import sys

#sBox = np.array([14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7])
sBox = np.random.permutation(16)
#pBox = np.array([0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15])
pBox = np.random.permutation(16)

def int2bin(u,bits=16):
  bin_u = bin(u)[2:]
  if len(bin_u) < bits:
    bin_u = '0' * (bits-len(bin_u)) + bin_u
  tmp_u = np.array([int(x) for x in list(bin_u)])
  return tmp_u

def bin2int(bin_u):
  u = int(''.join([str(x) for x in bin_u]),2)
  return u

def passSBox(u,tmp_sBox,bits=16): # u is the input, v is the output
  #print "make sure the length of input to be 16 bits"
  #print u
  assert(u < 2**bits)
  v = 0
  for i in range(bits/4):
    tmp_u = (u >> (4*i)) % (2**4)
    tmp_v = tmp_sBox[tmp_u]
    v += tmp_v << (4*i)
  return v

def passPBox(u,tmp_pBox): # u is the input, v is the output
  #print "make sure the length of input to be 16 bits"
  #print u
  assert(u < 2**16)
  tmp_u = int2bin(u)
  tmp_v = tmp_u[tmp_pBox]
  v = bin2int(tmp_v)
  return v

def encrypt(x,tmp_sBox,tmp_pBox,round_num,keys):
  w = x
  for i in range(round_num-2):
    #print i
    u = w ^ keys[i]
    v = passSBox(u,tmp_sBox)
    w = passPBox(v,tmp_pBox)

  u = w ^ keys[-2]
  v = passSBox(u,tmp_sBox)
  y = v ^ keys[-1]
  return y

def decrypt(y,tmp_rev_sBox,tmp_rev_pBox,round_num,keys):
  v = y ^ keys[-1]
  u = passSBox(v,tmp_rev_sBox)
  w = u ^ keys[-2]
  for i in range(round_num-3,-1,-1):
    #print i
    v = passPBox(w,tmp_rev_pBox)
    u = passSBox(v,tmp_rev_sBox)
    w = u ^ keys[i]
  x = w
  return x

def randomKey(bits,key_number):
  keys = []
  for i in range(key_number):
    keys.append(random.randint(0,2**bits-1))
  return keys

def randomSameKey(bits,key_number):
  keys = []
  key = random.randint(0,2**bits-1)
  for i in range(key_number):
    keys.append(key)
  return keys

def buildTable(tmp_sBox,bits=16):
  table = {}
  for diff in range(bits):
    table[diff] = {}
    for x in range(bits):
      table[diff][x] = 0
    for x in range(bits):
      x2 = x ^ diff
      y = passSBox(x,tmp_sBox)
      y2 = passSBox(x2,tmp_sBox)
      out = y ^ y2
      table[diff][out] += 1
  table_list = []
  for i in range(bits):
    tmp_list = []
    for j in range(bits):
      tmp_list.append(table[i][j])
    table_list.append(tmp_list)
  return np.array(table_list)

def passSBoxWithTable(u,table,bits=16): # u is 16 bits number
  v = 0
  prob = 1
  for i in range(bits/4):
    uu = (u >> (i*4)) % 16
    u_table = table[uu]
    v_out = np.argmax(u_table)
    prob *= np.max(u_table)/float(16)
    v += v_out << (i*4)
  return v,prob

def encryptWithTable(x,table,tmp_pBox,round_num):
  w = x
  key = 0
  prob = 1
  for i in range(round_num-2):
    #print i
    u = w ^ key
    v,tmp_prob = passSBoxWithTable(u,table)
    w = passPBox(v,tmp_pBox)
    prob *= tmp_prob

  y = w
  return y, prob

def findPath(table, tmp_pBox, round_num, bits=16):
  max_index = np.argmax(table[1:,1:])
  x_index = max_index/(bits-1) + 1
  xs = []
  probs = []
  targets = []
  targets_len = []
  for i in range(bits/4):
    x = x_index << (4*i)
    y, prob = encryptWithTable(x,table,tmp_pBox,round_num)
    y_list = []
    count = 0
    for j in range(bits/4-1,-1,-1):
      y_list.append((y >> (j*4)) % 16)
      if ((y >> (j*4)) % 16) != 0:
        count += 1
    assert(len(y_list) == bits/4)
    targets_len.append(count)
    xs.append(x)
    targets.append(y)
    probs.append(prob)
  probs = np.array(probs)
  targets_len = np.array(targets_len)
  index = np.argmax(probs)
  differential = xs[index]
  target = targets[index]
  target_prob = probs[index]
  return differential, target, target_prob

def seperateKey(key,bits=16):
  key_list = []
  for i in range(bits/4-1,-1,-1):
    key_list.append((key >> (i*4)) % 16)
  return key_list

if __name__ == "__main__":
  print 'linear attack'
  bits = 16
  round_num = 5
  key_number = round_num + 1

  rev_sBox = np.array([y[0] for y in sorted(enumerate(sBox),key=lambda x: x[1])])
  rev_pBox = np.array([y[0] for y in sorted(enumerate(pBox),key=lambda x: x[1])])
  keys = randomKey(bits,key_number)
  print "keys:", keys
  print "sBox:",sBox
  print "pBox:",pBox
  table = buildTable(sBox)
  print "table:"
  pprint.pprint(table)
  differential, target, target_prob = findPath(table, pBox, round_num, bits)

  plaintext_number = 500
  plaintext = []
  ciphertext = []
  #bin_differential = [0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0]
  #differential = bin2int(bin_differential)
  #bin_target = [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0]
  #target = bin2int(bin_target)
  #target_prob = 27.0/1024

  print 
  print "differential:", differential, seperateKey(differential)
  print "target:", target, seperateKey(target)
  print "target prob:", target_prob
  print 'generate', plaintext_number, "plaintext and ciphertext ..."
  if target_prob < 0.01:
    print "probability is too small (the distribution is too good to be vulnerable), it's possible that the DC can't work."
    print "please try another sBox and pBox"
    sys.exit(0)
  bias = {}
  true_key = keys[-1]
  #true_key_pair = ((keys[-1] >> 12) % 16, (keys[-1] >> 8) % 16, (keys[-1] >> 4) % 16, keys[-1] % 16)
  true_key_pair = seperateKey(true_key)
  #target_pair = ((target >> 12) % 16, (target >> 8) % 16, (target >> 4) % 16, target % 16)
  target_pair = seperateKey(target)
  print "the last round key:", true_key, seperateKey(true_key)
  print ""
  for key in range(2**16):
    (key1,key2,key3,key4) = ((key >> 12) % 16, (key >> 8) % 16, (key >> 4) % 16, key % 16)
    if (target_pair[0] == 0) and (key1 != 0):
      continue
    if (target_pair[1] == 0) and (key2 != 0):
      continue
    if (target_pair[2] == 0) and (key3 != 0):
      continue
    if (target_pair[3] == 0) and (key4 != 0):
      continue
    count = 0
    for i in range(plaintext_number):
      m1 = random.randint(0,2**bits-1)
      m2 = m1 ^ differential
      #plaintext.append(m)
      #print 'm:', m
      c1 = encrypt(m1,sBox,pBox,round_num,keys)
      c2 = encrypt(m2,sBox,pBox,round_num,keys)
      v1 = c1 ^ key
      v2 = c2 ^ key
      u1 = passSBox(v1,rev_sBox)
      u2 = passSBox(v2,rev_sBox)
      diff = u1 ^ u2
      if diff == target:
        count += 1
    prob = float(count) / plaintext_number
    bias[key] = prob
    print (key1,key2,key3,key4),"prob:",prob

  guess_key_pair = sorted(bias,key=lambda x: bias[x], reverse=True)

  filter_true_key_pair = (np.array(target_pair) > 0) * np.array(true_key_pair)
  filter_true_key = 0
  for x in filter_true_key_pair:
    filter_true_key *= 16
    filter_true_key += x
  
  print ""
  print "true key", true_key, true_key_pair
  valid_digit = [(x>0) for x in seperateKey(target)]
  print "valid digit:", valid_digit
  print "target true key:", filter_true_key_pair, "with bias:", bias[filter_true_key]
  #print true_key_pair, bias[true_key_pair]
  print "candidates:"
  print "1st: ", guess_key_pair[0], seperateKey(guess_key_pair[0]), bias[guess_key_pair[0]]
  print "2nd: ", guess_key_pair[1], seperateKey(guess_key_pair[1]), bias[guess_key_pair[1]]
  print "3rd: ", guess_key_pair[2], seperateKey(guess_key_pair[2]), bias[guess_key_pair[2]]


  #y = decrypt(e,rev_sBox,rev_pBox,round_num,keys)
  #print 'y:', y
