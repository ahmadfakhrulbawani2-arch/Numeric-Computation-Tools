from typing import List
from src.utils import *

import numpy as np
from datetime import datetime

PROG_NAME = "Numeric Factorization (Lin Method) Root Finding"
DIR_NAME = "faktorisasi"

# UTILS
def calc_error(old_vals, new_vals) -> float:
  return max(
    abs(n - o)
    for o, n in zip(old_vals, new_vals)
  )


# DEGREE 3
def lin_deg_3(
  eq: List[float],
  acc: float,
  max_iter: int,
  csv_file
):

  # x^3 + A2x^2 + A1x + A0
  A2, A1, A0 = eq[1:]

  a0 = 1.0
  b1 = 0.0
  b0 = 1.0

  csv_file.write("iter,a0,b1,b0,error\n")

  converged = False

  for i in range(1, max_iter + 1):
    old_vals = [a0, b1, b0]
    try:
      b1 = A2 - a0
      b0 = (A0 / a0)
      a0 = (A1 - b0) / b1

    except ZeroDivisionError:
      print("Division by zero detected")
      return None

    new_vals = [a0, b1, b0]
    err = calc_error(old_vals, new_vals)
    csv_file.write(f"{i},{a0},{b1},{b0},{err}\n")

    now: datetime = GetTimeNow()
    print(f"[{now}] Iter {i:3d} |  a0={a0:.2f}  b1={b1:.2f}  b0={b0:.2f}  %Ea={err:.2f}")

    if err < acc:
      converged = True
      break

  if not converged:
    print("Method did not converge")
    return None

  factor1 = [1, b1, b0]
  factor2 = [1, a0]
  roots1 = np.roots(factor1)
  roots2 = np.roots(factor2)
  roots = np.concatenate((roots1, roots2))

  return roots

# DEGREE 4
def lin_deg_4(
  eq: List[float],
  acc: float,
  max_iter: int,
  csv_file
):

  # x^4 + A3x^3 + A2x^2 + A1x + A0
  A3, A2, A1, A0 = eq[1:]

  # starter
  a0 = 1.0
  a1 = 0.0
  b0 = 1.0
  b1 = 0.0

  csv_file.write("iter,a0,a1,b0,b1,error\n")

  converged = False

  for i in range(1, max_iter + 1):

    old_vals = [a0, a1, b0, b1]

    try:
      b0 = A0 / a0
      b1 = (A1 - a1 * b0) / a0
      a1 = A3 - b1
      a0 = A2 - b0 - a1 * b1

    except ZeroDivisionError:
      print("Division by zero detected")
      return None

    new_vals = [a0, a1, b0, b1]

    err = calc_error(old_vals, new_vals)

    csv_file.write(f"{i},{a0},{a1},{b0},{b1},{err}\n")

    now = datetime.now()
    print(f"[{now}] Iter {i:3d} |  a0={a0:.2f}  a1={a1:.2f}  b0={b0:.2f}  b1={b1:.2f}  %Ea={err:.2f}")

    if err < acc:
      converged = True
      break

  if not converged:
    print("Method did not converge")
    return None
  
  factor1 = [1, b1, b0]
  factor2 = [1, a1, a0]
  roots1 = np.roots(factor1)
  roots2 = np.roots(factor2)
  roots = np.concatenate((roots1, roots2))

  return roots

# DEGREE 5
def lin_deg_5(
  eq: List[float],
  acc: float,
  max_iter: int,
  csv_file
):

  # x^5 + A4x^4 + A3x^3 + A2x^2 + A1x + A0
  A4, A3, A2, A1, A0 = eq[1:]

  a0 = 1.0
  b1 = 0.0
  b0 = 1.0
  c1 = 0.0
  c0 = 1.0

  csv_file.write("iter,a0,b1,b0,c1,c0,error\n")
  converged = False

  for i in range(1, max_iter + 1):
    old_vals = [a0, b1, b0, c1, c0]
    try:
      c1 = A4 - a0 - b1
      c0 = (A3 - a0 * A4 + (a0 ** 2) - b0 - c1 * b1)
      b1 = (A2 - a0 * c0 - b0 * c1) / c0
      b0 = (A1 - a0 * b1 * c0 - b0 * c1) / c0
      a0 = A0 / (b0 * c0)

    except ZeroDivisionError:
      print("Division by zero detected")
      return None

    new_vals = [a0, b1, b0, c1, c0]

    err = calc_error(old_vals, new_vals)
    csv_file.write(f"{i},{a0},{b1},{b0},{c1},{c0},{err}\n")
    now = datetime.now()
    print(f"[{now}] Iter {i:3d} |  a0={a0:.2f}  b1={b1:.2f}  b0={b0:.2f}  c1={c1:.2f}  c0={c0:.2f}  %Ea={err:.2f}")

    if err < acc:
      converged = True
      break

  if not converged:
    print("Method did not converge")
    return None

  factor1 = [1, a0]
  factor2 = [1, b1, b0]
  factor3 = [1, c1, c0]
  roots1 = np.roots(factor1)
  roots2 = np.roots(factor2)
  roots3 = np.roots(factor3)
  roots = np.concatenate((roots1, roots2, roots3))

  return roots

def lin_method_driver(
  eq: List[float],
  acc: float,
  max_iter: int,
  degree: int
):

  csv_file = open(
    f"./out/{DIR_NAME}/iterations.csv",
    "w"
  )

  roots = None

  match degree:

    case 3:
      roots = lin_deg_3(
        eq,
        acc,
        max_iter,
        csv_file
      )

    case 4:
      roots = lin_deg_4(
        eq,
        acc,
        max_iter,
        csv_file
      )

    case 5:
      roots = lin_deg_5(
        eq,
        acc,
        max_iter,
        csv_file
      )

  csv_file.close()

  return roots

HEADER = """
 _   _                           _                         
| \ | |_   _ _ __ ___   ___ _ __(_) ___                    
|  \| | | | | '_ ` _ \ / _ \ '__| |/ __|                   
| |\  | |_| | | | | | |  __/ |  | | (__                    
|_|_\_|\__,_|_| |_| |_|\___|_|  |_|\___|              
 _____          _             _          _   _         
|  ___|_ _  ___| |_ ___  _ __(_)______ _| |_(_) ___  _ __  
| |_ / _` |/ __| __/ _ \| '__| |_  / _` | __| |/ _ \| '_ \ 
|  _| (_| | (__| || (_) | |  | |/ / (_| | |_| | (_) | | | |
|_|  \__,_|\___|\__\___/|_|  |_/___\__,_|\__|_|\___/|_| |_|

"""

def factorization_main():
  Lazy_Loading("Opening files...")
  res_file = open(f"./out/{DIR_NAME}/root.txt", "a")
  PrintIntroProg(HEADER, PROG_NAME)

  while True:
    user_input = input("\nInput function coefficients (space separated) or 'q' to exit and 'h' for help: ").strip()
    if user_input == 'q':
      print("Exiting program...")
      break

    elif user_input == 'h':
      print(f"\n======= {PROG_NAME} Help =======\n")
      print(
        "1. Example:\n"
        "1 -10 35 -50 24\n"
        "= x^4 - 10x^3 + 35x^2 - 50x + 24\n"
      )
      print("2. Polynomial MUST be monic (highest coefficient = 1)\n")
      print("3. Available degree: 3, 4, and 5\n")
      continue

    try:
      eq: List[float] = list(map(float, user_input.split()))
      degree = len(eq) - 1

      if degree < 3:
        print("Cannot solve equation below degree 3\n")
        continue
      elif degree > 5:
        print("Degree above 5 is not available yet\n")
        continue
      elif eq[0] != 1:
        print("Highest degree coefficient must be 1\n")
        continue

      err_tol = float(input("Input tolerance (maximum 0.001): "))
      max_iter = int(input("Input max iterations: "))
      print(f"\n======= {PROG_NAME} =======\n")
      PrintSingleEq(eq)
      roots = lin_method_driver(eq,err_tol,max_iter,degree)

      now: datetime = GetTimeNow()
      if roots is not None:
        print(f"\n[{now}] Roots found:\n")
        res_file.write(f"\n[{now}] Roots:\n")

        for r in roots:
          print(f"{r}")
          res_file.write(f"{r}\n")

      else:
        print(f"\n[{now}] Method failed")
        res_file.write(f"\n[{now}] Method failed\n")

    except ValueError as e:
      print("Invalid input. Please enter numbers only.")
      print(f"Error: {e}")

  res_file.close()

if __name__ == "__main__":
  factorization_main()