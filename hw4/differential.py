import numpy as np
import random

sBox = np.array([14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7])
pBox = np.array([0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15])

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


if __name__ == "__main__":
  print 'linear attack'
  bits = 16
  round_num = 5
  key_number = round_num + 1

  rev_sBox = np.array([y[0] for y in sorted(enumerate(sBox),key=lambda x: x[1])])
  rev_pBox = np.array([y[0] for y in sorted(enumerate(pBox),key=lambda x: x[1])])
  keys = randomKey(bits,key_number)
  print "keys:", keys

  plaintext_number = 500
  plaintext = []
  ciphertext = []
  bin_differential = [0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0]
  differential = bin2int(bin_differential)
  bin_target = [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0]
  target = bin2int(bin_target)
  target_prob = 27.0/1024

  print "differential:", differential
  print "target:", target
  print 'generate', plaintext_number, "plaintext and ciphertext ..."
  bias = {}
  true_key_pair = ((keys[-1] >> 8) % 16, keys[-1] % 16)
  print "the last round key:", int2bin(keys[-1])
  for key2 in range(16):
    #key2 = true_key_pair[0]
    for key4 in range(16):
      #key4 = true_key_pair[1]
      count = 0
      key = (key2 << 8) + key4
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
      bias[(key2,key4)] = prob
      print (key2,key4),"prob:",prob

  guess_key_pair = sorted(bias,key=lambda x: bias[x], reverse=True)

  print "true key:", keys[-1]
  print true_key_pair, bias[true_key_pair]
  print "candidates:"
  print "1st: ", guess_key_pair[0], bias[guess_key_pair[0]]
  print "2nd: ", guess_key_pair[1], bias[guess_key_pair[1]]
  print "3rd: ", guess_key_pair[2], bias[guess_key_pair[2]]


  #y = decrypt(e,rev_sBox,rev_pBox,round_num,keys)
  #print 'y:', y
