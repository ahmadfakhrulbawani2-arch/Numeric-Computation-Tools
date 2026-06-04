import sys
import time
from typing import List
from src.utils import *
import src.utils.Style as clock_widget

MAX_ITERATION: int = 50
TOLERANCE: float = 1e-6

def print_iter(iter: int, c: float, fc: float, rate: float) -> None:
  with clock_widget.stdout_lock:
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
    with clock_widget.stdout_lock:
      print("f(a) * f(b) > 0, can't guarantee root in interval")
    log_activities("Can't get root", "ERROR")
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

RESET = "\033[0m"
BOLD = "\033[1m"
HEADER: str = fr'''
  ____ _____  _____ ______ _____ _______ _____ ____  _   _ 
 |  _ \_   _|/ ____|  ____/ ____|__   __|_   _/ __ \| \ | |
 | |_) || | | (___ | |__ | |       | |    | || |  | |  \| |
 |  _ < | |  \___ \|  __|| |       | |    | || |  | | . ` |
 | |_) || |_ ____) | |___| |____   | |   _| || |__| | |\  |
 |____/_____|_____/|______\_____|__|_|__|_____\____/|_| \_|
  __  __ ______ _______ _    _  ____  _____
 |  \/  |  ____|__   __| |  | |/ __ \|  __ \               
 | \  / | |__     | |  | |__| | |  | | |  | |              
 | |\/| |  __|    | |  |  __  | |  | | |  | |              
 | |  | | |____   | |  | |  | | |__| | |__| |              
 |_|  |_|______|  |_|  |_|  |_|\____/|_____/               
'''
def run_bisection():
  Lazy_Loading("Opening files...")
  PrintIntroProg(HEADER, "Bisection Method Root Finding Method")
  log_activities("Running bisection method", "SUCCESS")
  clock_widget.dalam_menu_kalkulasi = False
  Clock_Widget()
  while True:
    clock_widget.dalam_menu_kalkulasi = False

    # Cetak 1 baris kosong sebagai "slot" reserved untuk jam,
    # lalu naikan kursor 1 baris agar input() tepat di atasnya
    # print()
    # sys.stdout.write("\n\033[1A")
    # sys.stdout.flush()
    # time.sleep(0.1)
    # 1. Hidupkan jam saat menunggu input utama
    # clock_widget.dalam_menu_kalkulasi = False
    # time.sleep(0.1) # Kasih jeda dikit biar jam sempat nge-refresh posisinya
    
    # 2. SEBELUM nanya input, cetak enter kosong untuk tempat jam, 
    # lalu naikkan kursor kembali ke atas (\033[1A)
    # Ini trik pasif paling aman biar input() dan jam gak satu baris
    # print()
    # sys.stdout.write("\033[1A\033[K")
    # sys.stdout.flush()
    # --- TRIK PADDING ---
    # Cetak 2 baris kosong ekstra untuk ngasih space/padding di bawah terminal,
    # lalu naikkan kursor kembali ke atas sebanyak 2 baris (\033[2A) sebelum nanya input.
    # Ini memastikan baris paling akhir di layar tetap aman dihuni oleh jam.
    # 2. Bersihkan baris di bawah kursor (menghilangkan sisa jam yang beku)
    # \033[J artinya menghapus semua teks dari posisi kursor sampai akhir layar bawah
    # sys.stdout.write("\033[J")
    sys.stdout.write("\n\n\033[2A")
    sys.stdout.flush()
    user_input = input(f"\nInput function coefficients (space separated) or {BOLD}'q'{RESET} to exit: ").strip()
    if user_input.lower() == "q":
      clock_widget.stop_jam.set()
      print("Exiting program...")
      break

    try:
      eq = list(map(int, user_input.split()))
      clock_widget.dalam_menu_kalkulasi = False

      sys.stdout.write("\033[J")
      sys.stdout.write("\n\n\033[2A")
      sys.stdout.flush()
      aInit = float(input("Input interval start (a): "))

      sys.stdout.write("\033[J")
      sys.stdout.write("\n\n\033[2A")
      sys.stdout.flush()
      bInit = float(input("Input interval end (b): "))

      # # Bersihkan bawah kursor lagi sebelum nanya input baru
      # sys.stdout.write("\033[J")
      # sys.stdout.flush()
      # aInit = float(input("Input interval start (a): "))
      # # Bersihkan bawah kursor lagi sebelum nanya input baru
      # sys.stdout.write("\033[J")
      # sys.stdout.flush()
      # bInit = float(input("Input interval end (b): "))

      print("\n======= Bisection Method =======\n")
      PrintSingleEq(eq)
      clock_widget.dalam_menu_kalkulasi = True
      root = bisection_method(eq, aInit, bInit)
      if root is not None:
        print(f"\nRoot found: x = {root:.6f}")
        log_activities(f"Successfully get root: {root:.6f}", "SUCCESS")

    except ValueError:
      clock_widget.stop_jam.set()
      print("Invalid input. Please enter numbers only or 'q' to exit.")
      log_activities(f"Invalid input", "ERROR")
      clock_widget.dalam_menu_kalkulasi = False

if __name__ == "__main__":
  run_bisection()