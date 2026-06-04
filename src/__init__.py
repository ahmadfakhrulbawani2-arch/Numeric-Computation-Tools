# Comment if you want to run spesific part

import os, time
from halo import Halo
def Lazy_Loading(texts: str) -> None:
  # os.system('cls' if os.name == 'nt' else 'clear')
  spinner = Halo(text=texts, color='cyan', spinner='dots')
  # Mulai muter
  spinner.start()
  # Simulasi proses matematika/loading (misal 3 detik)
  time.sleep(1.5)
  # Selesai dengan status sukses (Centang Hijau)
  spinner.succeed('Ok done...')
  time.sleep(0.5)
  # os.system('cls' if os.name == 'nt' else 'clear')

Lazy_Loading("Unpacking internal package...")

from src.faktorisasi.index import factorization_main
from src.bisection_method.index import run_bisection
from src.newton_raphson.index import run_NR
from src.newton_raphson_modified.index import run_NR_modified
from src.regula_falsi.index import run_regulaFalsi
from src.secant_method.index import run_secand
from src.utils import log_activities

log_activities("Success unpacking internal package")