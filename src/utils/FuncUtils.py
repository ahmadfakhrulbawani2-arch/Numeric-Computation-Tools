from typing import List
import math

def DerivativeF(coeffs: List[float]) -> List[float]:
  return [coeffs[i] * i for i in range(1, len(coeffs))]


def CalcFunc(coeffs: List[float], x: float) -> float:
  return sum(coeffs[i] * (x ** i) for i in range(len(coeffs)))

def Calc_Converngence_Rate(err: List[float]) -> float | None:
  if len(err) < 3: 
    return None
  
  e_n1: float = err[-1] 
  e_n: float = err[-2]
  e_n_1: float = err[-3]

  return math.log(e_n1 / e_n) / math.log(e_n / e_n_1)