import time
from typing import List
from src.utils.FuncUtils import CalcFunc, Calc_Converngence_Rate

MAX_ITERATION: int = 50
TOLERANCE: float = 1e-6

def print_iter(iter: int, c: float, fc: float, rate: float) -> None:
  if rate is not None:
    print(f"Iteration-{iter}: c = {c:.6f}, f(c) = {fc:.6f} | convergence rate: {rate:.6f}")
  else:
    print(f"Iteration-{iter}: c = {c:.6f}, f(c) = {fc:.6f}")
  time.sleep(0.2)
  return None

def bisection_method(eq: List[int], a: float, b: float) -> float | None:
  new_eq: List[int] = list(reversed(eq))
  fa: float = CalcFunc(new_eq, a)
  fb: float = CalcFunc(new_eq, b)
  
  if fa * fb > 0:
    print("f(a) * f(b) > 0, can't guarantee root in interval")
    return None

  iter = 1
  prev_c: float = 0.0
  errors: List[int] = []
  while iter <= MAX_ITERATION:
    c: float = (a + b) / 2
    fc: float = CalcFunc(new_eq, c)

    # calc convergence rate
    err: float | None = None
    if iter > 1: 
      errors.append(abs(c - prev_c))
      if len(errors) >= 3:
        err = Calc_Converngence_Rate(errors)
      else:
        err = None
    else: 
      err = None

    print_iter(iter, c, fc, err)

    if abs(fc) < TOLERANCE or abs(b - a)/2 < TOLERANCE:
      return c

    if fa * fc < 0:
      b = c
      fb = fc
    else:
      a = c
      fa = fc

    iter += 1

  print("Maximum iterations reached")
  return None

if __name__ == "__main__":
  while True:
    user_input = input("\nInput function coefficients (space separated) or 'q' to exit: ").strip()
    if user_input.lower() == "q":
      print("Exiting program...")
      break

    try:
      eq = list(map(int, user_input.split()))
      aInit = float(input("Input interval start (a): "))
      bInit = float(input("Input interval end (b): "))

      print("\n======= Bisection Method =======\n")
      root = bisection_method(eq, aInit, bInit)
      if root is not None:
        print(f"\nRoot found: x = {root:.6f}")

    except ValueError:
      print("Invalid input. Please enter numbers only or 'q' to exit.")