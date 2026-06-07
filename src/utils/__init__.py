import time
from halo import Halo
def thisLazy_Loading(texts: str, duration=1.5) -> None:
  # os.system('cls' if os.name == 'nt' else 'clear')
  spinner = Halo(text=texts, color='cyan', spinner='dots')
  # Mulai muter
  spinner.start()
  # Simulasi proses matematika/loading (misal 3 detik)
  time.sleep(duration)
  # Selesai dengan status sukses (Centang Hijau)
  spinner.succeed('Ok done...')
  time.sleep(0.5)
  # os.system('cls' if os.name == 'nt' else 'clear')

thisLazy_Loading("Unpacking numeric computation package...")
from .FuncUtils import *
from .IoUtils import *
from .Logger import *
from .Style import *

log_activities("Success unpacking numeric computation package")