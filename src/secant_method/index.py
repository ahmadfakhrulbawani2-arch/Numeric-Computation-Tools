from typing import List
from src.utils.FuncUtils import *
from src.utils.IoUtils import *
import numpy as np

from typing import List
import numpy as np

def secant_method(
    eq: List[int],
    xLo: float,
    xHi: float,
    acc: float,
    max_iter: int
) -> float:

    csv_file = open("./out/secant-method/iterations.csv", "w")

    rEq: List[int] = list(reversed(eq))

    # initial guesses
    x_prev: float = xLo
    x_curr: float = xHi

    # ambil akar real saja
    roots = np.roots(eq)
    real_roots = roots[np.isreal(roots)].real

    print(f"\nInitial values: x0 = {x_prev:.6f}, x1 = {x_curr:.6f}\n")

    csv_file.write("iter,x_prev,x_curr,x_new,%Et\n")

    root: float = x_curr

    for iter in range(1, max_iter + 1):

        f_prev = CalcFunc(rEq, x_prev)
        f_curr = CalcFunc(rEq, x_curr)

        # hindari division by zero
        if (f_curr - f_prev) == 0:
            print("Division by zero detected!")
            break

        # secant formula
        x_new = x_curr - (
            (x_curr - x_prev) / (f_curr - f_prev)
        ) * f_curr

        # cari nearest real root
        nearest_root = real_roots[
            np.argmin(np.abs(real_roots - x_new))
        ]

        err_true = abs((nearest_root - x_new) / nearest_root)

        PrintIterations(
            iter,
            ("x_prev", "x_curr", "x_new(root)", "%Et"),
            x_prev,
            x_curr,
            x_new,
            err_true
        )

        csv_file.write(
            f"{iter},{x_prev},{x_curr},{x_new},{err_true}\n"
        )

        # stopping condition
        if err_true <= acc:
            root = x_new
            break

        # update values
        x_prev = x_curr
        x_curr = x_new

        root = x_new

    csv_file.close()

    return root

def run_secand():
  res_file = open("./out/secant-method/root.txt", "a")
  PrintIntroProg("Secant Method Root Finding Method")
  while True: 
    user_input = input("\nInput function coefficients (space separated) or 'q' to exit and 'h' for help: ").strip()
    if user_input == 'q':
      print("exiting program...")
      break
    elif user_input == 'h':
      print("\n======= Secant Method Root Finding Help =======\n")
      print("1. You need to only input function coeffs\n")
      print("   For example: 1 2 3 means 1x^2 + 2x + 3,\n   -8 9 3 2 1 means -8x^4 + 9x^3 + 3x^2 + 2x + 1\n")
      print("2. You'll need to guess your initial interval value for domain. This is for narrowing the iterations.\nI will add interval value recomendation in the future\n")
      print("3. Press 'q' to exit because the program keeps running in a loop\n")
      print("Any bugs? Let me know by making an issue in this repo, really appreciate your feedbacks\n")

    try:
      eq: List[int] = list(map(int, user_input.split()))
      xLo: float = float(input("Input of xLower (int/float): "))
      xHi: float = float(input("Input of xHi (int/float): "))
      err_tol: float = float(input("Input tolerance (Et/Error true, lowest = 0.0001): "))
      max_iter: int = int(input("Input max iterations: "))
      # Debug
      # print(f"Input is: {xLo}, {xHi}, {err_tol}, {max_iter}")

      while xLo >= xHi:
        print("\nxLo must be lower than xHi!!!\n")
        xLo = float(input("Input of xLower (int/float): "))
        xHi = float(input("Input of xHi (int/float): "))

      print("\n======= Secant Method Root Finding =======\n")
      PrintSingleEq(eq)
      root = secant_method(eq, xLo, xHi, err_tol, max_iter)

      now: datetime = GetTimeNow()
      if root is not None:
        print(f"\n[{now}] Root found: {root:.6f}")
        res_file.write(f"\n[{now}]Root found: {root:.6f}")
        res_file.close()
      else:
        print(f"\n[{now}] Root not found")
        res_file.write(f"\n[{now}]Root not found")
        res_file.close()
        break
    except ValueError:
      print("Invalid input. Please enter numbers only or q to exit.")

if __name__ == "__main__":
  run_secand