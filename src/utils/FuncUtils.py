import time
from halo import Halo
from typing import List
import math
import os
import sys

EPSILON: float = 1e-12

# replacing print(f"")
def printf(format_string: str) -> None:
  # 1. Ambil scope (namespace) dari tempat fungsi printf() ini dipanggil
  frame = sys._getframe(1)
  local_vars = frame.f_locals
  global_vars = frame.f_globals
  
  # 2. Lakukan formatting manual menggunakan namespace tersebut
  # .format_map otomatis mencocokkan teks di dalam {} dengan nama variabel yang ada
  try:
    # Gabungkan global dan local vars (local override global jika namanya sama)
    context = {**global_vars, **local_vars}
    print(format_string.format_map(context), end="\n")
  except KeyError as e:
    # Antisipasi kalau kamu nulis {variabel} tapi variabelnya belum di-define
    print(f"\n[Printf Error]: Variabel {e} belum di-define!\n")

def DerivativeF(coeffs: List[float]) -> List[float]:
    return [coeffs[i] * i for i in range(1, len(coeffs))]


# reverse the coeffs first
def CalcFunc(coeffs: List[float], x: float) -> float:
    return sum(coeffs[i] * (x**i) for i in range(len(coeffs)))


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


# just for styling 
def Lazy_Loading(texts: str, duration=1.5) -> None:
    # os.system('cls' if os.name == 'nt' else 'clear')
    spinner = Halo(text=texts, color="cyan", spinner="dots")
    # Mulai muter
    spinner.start()
    # Simulasi proses matematika/loading (misal 3 detik)
    time.sleep(duration)
    # Selesai dengan status sukses (Centang Hijau)
    spinner.succeed("Ok done...")
    time.sleep(0.5)
    # os.system('cls' if os.name == 'nt' else 'clear')

# this is true loading animation
class TrueLoader:
    def __init__(self, color="cyan", spinner="dots"):
        self.color = color
        self.spinner_type = spinner
        self.spinner = None

    def start(self, text: str) -> None:
        if self.spinner is None:
            self.spinner = Halo(text=text, color=self.color, spinner=self.spinner_type)
            self.spinner.start()
        else:
            self.spinner.text = text
            self.spinner.start()

    def stop(self, success_text: str = "Ok done...") -> None:
        if self.spinner:
            self.spinner.succeed(success_text)
            time.sleep(0.5)
