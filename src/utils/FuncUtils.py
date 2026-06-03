import time
from halo import Halo
from typing import List
import math
import datetime
import os

EPSILON: float = 1e-12
LOG_FILE: str = "../../activities.log"

def DerivativeF(coeffs: List[float]) -> List[float]:
  return [coeffs[i] * i for i in range(1, len(coeffs))]

# reverse the coeffs first
def CalcFunc(coeffs: List[float], x: float) -> float:
  return sum(coeffs[i] * (x ** i) for i in range(len(coeffs)))

def Calc_Converngence_Rate(err: List[float]) -> float | None:
  if len(err) < 3:
    return None

  e_n1 = max(err[-1], EPSILON)
  e_n = max(err[-2], EPSILON)
  e_n_1 = max(err[-3], EPSILON)

  denumerator = math.log(e_n / e_n_1)

  if denumerator == 0:
    return None

  return math.log(e_n1 / e_n) / denumerator

def CalcTrueError(real_root: float, approx_root: float) -> float:
  if abs(real_root) < EPSILON:
    return abs(approx_root)

  return abs((real_root - approx_root) / real_root)

def log_activities(action: str, status: str = "INFO") -> None:
  log_file = open(LOG_FILE, "a")

  clock_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  status = status.upper()
  # Set kode warna ANSI berdasarkan status
  color_code: str = ""
  if "ERROR" in status:
    color_code = "\033[91m"   # Merah
  elif "SUCCESS" in status:
    color_code = "\033[92m"   # Hijau
  elif "WARNING" in status:
    color_code = "\033[93m"   # Kuning
  else:
    color_code = ""           # Tanpa warna (INFO/Standar)

  if color_code:
    log_file.write(f"{color_code}[{clock_now}] [{status}] {action}\033[0m\n")
  else:
    log_file.write(f"[{clock_now}] [{status}] {action}\n")

def Lazy_Loading(texts: str) -> None:
  spinner = Halo(text=texts, color='cyan', spinner='dots')
  # Mulai muter
  spinner.start()
  # Simulasi proses matematika/loading (misal 3 detik)
  time.sleep(3)
  # Selesai dengan status sukses (Centang Hijau)
  spinner.succeed('Perhitungan kelar, Bos!')
  print("Ok Done...")
  time.sleep(0.5)
  os.system('cls' if os.name == 'nt' else 'clear')