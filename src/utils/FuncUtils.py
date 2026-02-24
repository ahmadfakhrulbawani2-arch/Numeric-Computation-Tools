def DerivativeF(nEq):
  nFPrime = []
  for i in range(1, len(nEq)):
    nFPrime.append(nEq[i] * i) 
  return nFPrime

def CalcFunc(nEq, x):
  nRes = 0
  for i in range(len(nEq)):  
    nRes += nEq[i] * (x ** i)
  return nRes