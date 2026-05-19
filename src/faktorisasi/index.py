from typing import List, Tuple, Optional
from src.utils.FuncUtils import *
from src.utils.IoUtils import *
import numpy as np
import os

def lin_method_deg3(eq: List[int], acc: float, max_iter: int, csv_file) -> Optional[Tuple[float, float, float]]:
  # eq: [A3, A2, A1, A0] -> x^3 + A2x^2 + A1x + A0
  A2, A1, A0 = eq[1], eq[2], eq[3]
  
  # Starter awal bernilai 0 sesuai rumus di file TeX kamu
  b0 = 0.0
  a1, a0 = 0.0, 0.0

  csv_file.write("iter,a1,a0,b0,error\n")
  print(f"\nInitial values: b0 = {b0:.6f}\n")

  for iter in range(1, max_iter + 1):
    b0_prev = b0

    # Siklus rumus dari TeX awalmu
    a1 = A2 - b0
    
    # Proteksi division by zero jika a0 bernilai 0 saat iterasi
    if a0 == 0:
      a0 = 0.0001
      
    a0 = A1 - (a1 * b0)
    b0 = A0 / a0

    err = abs(b0 - b0_prev)

    print(f"Iter {iter:02d} | a1: {a1:.6f} | a0: {a0:.6f} | b0: {b0:.6f} | Err: {err:.6f}")
    csv_file.write(f"{iter},{a1},{a0},{b0},{err}\n")

    if err <= acc:
      return a1, a0, b0

  return None

def lin_method_deg4(eq: List[int], acc: float, max_iter: int, csv_file) -> Optional[Tuple[float, float]]:
  # eq: [A4, A3, A2, A1, A0]
  A3, A2, A1, A0 = eq[1], eq[2], eq[3], eq[4]
  
  a1, a0 = 0.0, 0.0
  b1, b0 = 0.0, 0.0

  csv_file.write("iter,a1,a0,b1,b0,error\n")
  print(f"\nInitial values: a1 = {a1:.6f}, a0 = {a0:.6f}\n")

  for iter in range(1, max_iter + 1):
    a1_prev, a0_prev = a1, a0

    if a0 == 0:
      a0 = 0.0001

    b0 = A0 / a0
    b1 = (A1 - (a1 * b0)) / a0
    a1 = A3 - b1
    a0 = A2 - b0 - (a1 * b1)

    err = max(abs(a1 - a1_prev), abs(a0 - a0_prev))

    print(f"Iter {iter:02d} | a1: {a1:.6f} | a0: {a0:.6f} | b1: {b1:.6f} | b0: {b0:.6f} | Err: {err:.6f}")
    csv_file.write(f"{iter},{a1},{a0},{b1},{b0},{err}\n")

    if err <= acc:
      return a1, a0

  return None

def lin_method_deg5(eq: List[int], acc: float, max_iter: int, csv_file) -> Optional[Tuple[float, float, float]]:
  # eq: [A5, A4, A3, A2, A1, A0]
  A4, A3, A2, A1, A0 = eq[1], eq[2], eq[3], eq[4], eq[5]

  a0 = 0.0
  b1, b0 = 0.0, 0.0
  c1, c0 = 0.0, 0.0

  csv_file.write("iter,c1,c0,b1,b0,a0,error\n")
  print(f"\nInitial values: c1 = {c1:.6f}, c0 = {c0:.6f}, a0 = {a0:.6f}\n")

  for iter in range(1, max_iter + 1):
    a0_prev = a0

    if c0 == 0:
      c0 = 0.0001
    if b0 == 0:
      b0 = 0.0001

    c1 = A4 - a0 - b1
    c0 = A3 - (a0 * A4) + (a0 ** 2) - b0 - (c1 * b1)
    b1 = (A2 - (a0 * c0) - (b0 * c1)) / c0
    b0 = (A1 - (a0 * b1 * c0) - (b0 * c1)) / c0
    a0 = A0 / (b0 * c0)

    err = abs(a0 - a0_prev)

    print(f"Iter {iter:02d} | c1: {c1:.6f} | c0: {c0:.6f} | b1: {b1:.6f} | b0: {b0:.6f} | a0: {a0:.6f} | Err: {err:.6f}")
    csv_file.write(f"{iter},{c1},{c0},{b1},{b0},{a0},{err}\n")

    if err <= acc:
      return c1, c0, a0

  return None

def lin_method_driver(eq: List[int], acc: float, max_iter: int) -> Optional[str]:
  if eq[0] != 1:
    lead_coeff = eq[0]
    eq = [coef / lead_coeff for coef in eq]

  deg = len(eq) - 1
  os.makedirs("./out/lin-method", exist_ok=True)
  csv_file = open("./out/lin-method/iterations.csv", "w")

  if deg == 3:
    print("\n======= Running Lin Method for Degree 3 =======")
    result = lin_method_deg3(eq, acc, max_iter, csv_file)
    csv_file.close()
    if result:
      a1, a0, b0 = result
      return f"Faktor: (x + {b0:.6f})(x^2 + {a1:.6f}x + {a0:.6f})"
  elif deg == 4:
    print("\n======= Running Lin Method for Degree 4 =======")
    result = lin_method_deg4(eq, acc, max_iter, csv_file)
    csv_file.close()
    if result:
      a1, a0 = result
      return f"Faktor: (x^2 + {a1:.6f}x + {a0:.6f}) (sisa kuadratik pasangannya)"
  elif deg == 5:
    print("\n======= Running Lin Method for Degree 5 =======")
    result = lin_method_deg5(eq, acc, max_iter, csv_file)
    csv_file.close()
    if result:
      c1, c0, a0 = result
      return f"Faktor: (x + {a0:.6f})(x^2 + {c1:.6f}x + {c0:.6f})"
  else:
    csv_file.close()
    print(f"\nMetode Lin di kode ini di-scale khusus untuk derajat 3, 4, atau 5. Input kamu derajat {deg}.")
    return None

if __name__ == "__main__":
  res_file = open("./out/lin-method/factors.txt", "a")
  PrintIntroProg("Lin Method (Coefficient Iteration) Factorization")
  
  while True:
    user_input = input("\nInput function coefficients (space separated) or 'q' to exit: ").strip()
    if user_input == 'q':
      print("exiting program...")
      break

    try:
      eq: List[int] = list(map(int, user_input.split()))
      deg = len(eq) - 1
      
      if deg not in [3, 4, 5]:
        print("Please input coefficients for exactly degree 3, 4, or 5!")
        continue

      err_tol: float = float(input("Input tolerance (lowest = 0.0001): "))
      max_iter: int = int(input("Input max iterations: "))

      print("\n======= Lin Method Factorization =======")
      PrintSingleEq(eq) 
      
      factor_res = lin_method_driver(eq, err_tol, max_iter)
      now = GetTimeNow()

      if factor_res is not None:
        print(f"\n[{now}] Result -> {factor_res}")
        res_file.write(f"\n[{now}] {factor_res}")
      else:
        print(f"\n[{now}] Factorization failed or diverged.")
        res_file.write(f"\n[{now}] Factorization failed")
        
    except ValueError as e:
      print("Invalid input. Please enter numbers only.")
      print(f"Error: {e}")
      
  res_file.close()