from typing import List
from src.utils.FuncUtils import *
from src.utils.IoUtils import *
import numpy as np

def secant_method(eq: List[int], xLo: float, xHi: float, acc: float, max_iter: int) -> float:
  csv_file = open("./out/secant-method/iterations.csv", "w")
  root: float = 0.00
  rEq: List[int] = list(reversed(eq))

  # starting calc
  next_x: float = 0.00
  prev_x: float = xLo
  f_xPrev: float = CalcFunc(rEq, prev_x)
  init_x: float = (xLo + xHi)/2
  f_xInit: float = CalcFunc(rEq, init_x)
  # calc real roots
  real_roots: List[float] = np.roots(eq).real
  print(f"\nInitial value for x is: {init_x:.6f}\n")
  csv_file.write(f"\nInitial value for x is: {init_x:.6f}\n")
  csv_file.write("iter,x_prev,x_0,x_new(root),%Et\n")
  for iter in(1, max_iter+1, 1):
    next_x = init_x - ((prev_x - init_x)/(f_xPrev - f_xInit)) * f_xInit

    # find nearest root from next_x
    nearest_root: float = real_roots[np.argmin(np.abs(real_roots - next_x))]
    err_true: float = abs((nearest_root - next_x)/nearest_root)
    PrintIterations(
      iter,
      ("x_prev", "x_0", "x_new(root)", "%Et"),
      prev_x, init_x, next_x, err_true
    )

    csv_file.write(f"{iter},{prev_x},{init_x},{next_x},{err_true}\n")





if __name__ == "__main__":
  res_file = open("./out/secant-method/root.txt", "w")
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

      if root is not None:
        print(f"\nRoot found: {root:.6f}")
        res_file.write(f"\nRoot found: {root:.6f}")
      else:
        print("\nRoot not found")
        res_file.write("\nRoot not found")
        break
    except ValueError:
      print("Invalid input. Please enter numbers only or q to exit.")

  res_file.close()