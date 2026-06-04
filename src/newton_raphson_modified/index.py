from typing import List
from src.utils import *
import numpy as np

from typing import List
import numpy as np

def newton_raphson_modified(
  eq: List[int],
  xInit: float,
  acc: float,
  max_iter: int
) -> float:

    csv_file = open("./out/newton-raphson-modified/iterations.csv", "w")
    errors: List[float] = [] # store convergence rate every iterations
    rEq: List[int] = list(reversed(eq))
    dEq: List[int] = DerivativeF(rEq)
    ddEq: List[int] = DerivativeF(dEq)

    if not dEq:
      print("Unable to solve as the derivative of given input is 0")
      return None

    # initial guesses
    x_curr = xInit

    # ambil akar real saja
    roots = np.roots(eq)
    real_roots = roots[np.isreal(roots)].real
    if real_roots.size == 0:
      return None

    print(f"\nInitial values: x0 = {x_curr:.6f}\n")

    csv_file.write("iter,x_curr,x_new,%Et,convergence\n")

    root: float = x_curr

    for iter in range(1, max_iter + 1):

      f_prev = CalcFunc(rEq, x_curr)
      f_dEq = CalcFunc(dEq, x_curr)
      f_ddEq = CalcFunc(ddEq, x_curr)
      numerator: float = f_prev * f_dEq
      denumerator: float = pow(f_dEq, 2) - (f_prev * f_ddEq)

        # hindari division by zero
      if (denumerator) == 0:
        print("Division by zero detected!")
        break

      # NR modified formula
      x_new: float = x_curr - (numerator/denumerator)

      # cari nearest real root
      nearest_root = real_roots[
        np.argmin(np.abs(real_roots - x_new))
      ]

      err_true = CalcTrueError(nearest_root, x_new)
      errors.append(abs(x_new - x_curr))
      err_rate: float | None = Calc_Converngence_Rate(errors)

      PrintIterations(
        iter,
        ("x_curr", "x_new(root)", "%Et", "convergence_rate"),
        x_curr,
        x_new,
        err_true,
        err_rate
      )

      csv_file.write(
        f"{iter},{x_curr},{x_new},{err_true},{'-' if err_rate is None else err_rate}\n"
      )

      # stopping condition
      if err_true <= acc:
        root = x_new
        break

      # update values
      x_curr = x_new
      
      root = x_new
    csv_file.close()
    return root

HEADER = """
 _   _               _                  
| \ | | _____      _| |_ ___  _ __      
|  \| |/ _ \ \ /\ / / __/ _ \| '_ \     
| |\  |  __/\ V  V /| || (_) | | | |    
|_|_\_|\___| \_/\_/  \__\___/|_| |_|    
 ____             _                     
|  _ \ __ _ _ __ | |__  ___  ___  _ __  
| |_) / _` | '_ \| '_ \/ __|/ _ \| '_ \ 
|  _ < (_| | |_) | | | \__ \ (_) | | | |
|_| \_\__,_| .__/|_|_|_|___/\___/|_| |_|
|  \/  | __|_| __| (_)/ _(_) ___  __| | 
| |\/| |/ _ \ / _` | | |_| |/ _ \/ _` | 
| |  | | (_) | (_| | |  _| |  __/ (_| | 
|_|  |_|\___/ \__,_|_|_| |_|\___|\__,_| 

"""
def run_NR_modified():
  Lazy_Loading("Opening files...")
  res_file = open("./out/newton-raphson-modified/root.txt", "a")
  PrintIntroProg(HEADER, "Newton Raphson Modified Method Root Finding Method")
  while True: 
    user_input = input("\nInput function coefficients (space separated) or 'q' to exit and 'h' for help: ").strip()
    if user_input == 'q':
      print("exiting program...")
      break
    elif user_input == 'h':
      print("\n======= Newton Raphson Modified Method Root Finding Help =======\n")
      print("1. You need to only input function coeffs\n")
      print("   For example: 1 2 3 means 1x^2 + 2x + 3,\n   -8 9 3 2 1 means -8x^4 + 9x^3 + 3x^2 + 2x + 1\n")
      print("2. You'll need to guess your initial interval value for domain. This is for narrowing the iterations.\nI will add interval value recomendation in the future\n")
      print("3. Press 'q' to exit because the program keeps running in a loop\n")
      print("Any bugs? Let me know by making an issue in this repo, really appreciate your feedbacks\n")

    try:
      eq: List[int] = list(map(int, user_input.split()))
      xInit: float = float(input("Input initial root guess (x0): "))
      err_tol: float = float(input("Input tolerance (Et/Error true, lowest = 0.0001): "))
      max_iter: int = int(input("Input max iterations: "))
      # Debug
      # print(f"Input is: {xLo}, {xHi}, {err_tol}, {max_iter}")

      print("\n======= Newton Raphson Modified Method Root Finding =======\n")
      PrintSingleEq(eq)
      root = newton_raphson_modified(eq, xInit, err_tol, max_iter)

      now: datetime = GetTimeNow()
      if root is not None:
        print(f"\n[{now}] Root found: {root:.6f}")
        res_file.write(f"\n[{now}] Root found: {root:.6f}")
      else:
        print(f"\n[{now}] Root not found")
        res_file.write(f"\n[{now}] Root not found")
        break
    except ValueError as e:
      print("Invalid input. Please enter numbers only or q to exit.")
      print(f"Error: {e}")
  res_file.close()

if __name__ == "__main__":
  run_NR_modified()