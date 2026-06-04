import time
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

Lazy_Loading("Unpacking numeric computation package...")
from .FuncUtils import *
from .IoUtils import *
from .Logger import *
from .Style import print_text_gradient_angle, AnsiColors, Clock_Widget, stop_jam, dalam_menu_kalkulasi

log_activities("Success unpacking numeric computation package")