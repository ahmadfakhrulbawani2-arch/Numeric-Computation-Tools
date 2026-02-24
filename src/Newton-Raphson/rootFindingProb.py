from src.utils.FuncUtils import DerivativeF
from src.utils.FuncUtils import CalcFunc

# currently available only for power 3 for testing
def main(nEq, nInit):
  nEqLen = len(nEq)
  nEq = list(reversed(nEq))
  nFx0 = CalcFunc(nEq, nInit)
  nFPrimex0 = 0
  if nEqLen > 4:
    print("Sorry currently can't handle beyond 2-nd power")
    return
  else:
    arrDerivedEq = DerivativeF(nEq)
    if arrDerivedEq == 0:
      print("Unable to solve as the derivative of given input is 0")
      return
    
    nFPrimex0 = CalcFunc(arrDerivedEq, nInit)
    res = nInit - (nFx0 / nFPrimex0)
  
  return res


if __name__ == "__main__":
  arrEq = list(map(int, input("Masukkan koefisien (spasi): ").split()))
  nInitVal = int(input("Masukkan nilai awal x0: "))
  res = main(arrEq, nInitVal)
  print(f"Hasil root finding menggunakan Newton-Raphson adalah = {res}")