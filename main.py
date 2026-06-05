import os
import sys
from src import \
  run_secand, \
  run_bisection, \
  run_NR, \
  run_NR_modified, \
  run_regulaFalsi, \
  factorization_main, \
  Lazy_Loading, \
  log_activities, read_logs, \
  print_text_gradient_angle, AnsiColors, Clock_Widget, stop_jam
import src.utils.Style as clock_widget


# Setup pembaca input keyboard cross-platform
if os.name == 'nt':
  import msvcrt
  def get_key():
    """Membaca input tombol di Windows"""
    ch = msvcrt.getch()
    if ch in (b'\x00', b'\xe0'): # Tombol fungsi atau arrow keys
      ch = msvcrt.getch()
      if ch == b'H': return 'up'
      if ch == b'P': return 'down'
    if ch == b'\r': return 'enter'
    try:
      return ch.decode('utf-8').lower()
    except:
      return None
else:
  import tty
  import termios
  def get_key():
    """Membaca input tombol di Linux / macOS"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
      if ch == '\x1b': # Escape sequence untuk arrow keys
        ch2 = sys.stdin.read(2)
        if ch2 == '[A': return 'up'
        if ch2 == '[B': return 'down'
      if ch == '\r' or ch == '\n': return 'enter'
      return ch.lower()
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

# --- VARIABEL WARNA ---

rainbow_colors = [
  (255, 0, 0),     # Merah
  (255, 255, 0),   # Kuning
  (0, 255, 0),     # Hijau
  (0, 255, 255),   # Cyan
  (0, 0, 255),     # Biru
  (255, 0, 255)    # Magenta
]

cyberpunk_colors = [
  (255, 0, 128),  # Pink Neon
  (128, 0, 255),  # Ungu
  (0, 255, 255),   # Cyan Neon
  (243, 230, 0)   # Kuning Neon
]

ASCII_HEADER = fr'''
  _  __ ____   __  __  _   _  _   _  __  __ _____   __  
 | |/ // __ \ |  \/  || \ | || | | ||  \/  ||___ \ / /_ 
 | ' /| |  | || |\/| ||  \| || | | || |\/| |  __) |  _ \
 | . \| |__| || |  | || |\  || |_| || |  | | / __ | (_) |
 |_|\_\\____/ |_|  |_||_| \_| \___/ |_|  |_||_____ \___/

            Hello, Nice to meet you 👋
            We don't use rainbow cause we reject 🌈

'''

STATS = fr"""

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         PROGRAM KOMPUTASI NUMERIK                                          │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  {AnsiColors.RED}Author      : Ahmad Fakhrul Bawani{AnsiColors.RESET}                                                                        │
│  {AnsiColors.GREEN}NRP         : 5025251143{AnsiColors.RESET}                                                                                  │
│  {AnsiColors.BLUE}License     : Open Source (MIT){AnsiColors.RESET}                                                                           │
│  Source Code : https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-Tools/tree/main             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                               © 2026. All Rights Reserved for Academic Purposes.                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

"""

JUMLAH_MENU = 8
def draw_menu(menu_items, selected_index, awal_jalan=False):
  if awal_jalan:
    clear_screen()
    print(STATS)
    print_text_gradient_angle(ASCII_HEADER, cyberpunk_colors, 0)
    print(f"\n Gunakan [↑/↓] Panah untuk Navigasi, {AnsiColors.BOLD}[Enter]{AnsiColors.RESET} untuk Memilih, {AnsiColors.BOLD}[Q]{AnsiColors.RESET} untuk Keluar\n")
    print("─" * 108)
  else:
    # Mengembalikan kursor naik ke atas agar menu tertimpa dengan halus tanpa reload global
    sys.stdout.write(f"\033[{JUMLAH_MENU + 1}A")
    sys.stdout.flush()

  for i, item in enumerate(menu_items):
    if i == selected_index:
      print(f"\033[K \033[92m{AnsiColors.BOLD}►   {item}\033[0m")
    else:
      print(f"\033[K \033[90m    {item}\033[0m")
  print("\033[K" + "─" * 108)

# --- ALUR UTAMA ---
if __name__ == "__main__":

  menu_options = [
    "Chapter-2.1 Bisection Method",
    "Chapter-2.2 Regula Falsi",
    "Chapter-3.1 Newton Raphson",
    "Chapter-3.2 Secand Method",
    "Chapter-4.1 Newton Raphson Modified",
    "Chapter-4.2 Factorization Method",
    "Open program history",
    "Quit",
  ]
  
  current_select = 0

  # Kasih widget jam di thread berbeda
  clock_widget.Clock_Widget()
  
  # Gambar menu pertama kali
  draw_menu(menu_options, current_select, awal_jalan=True)
  
  while True:
    clock_widget.stop_jam.clear()
    clock_widget.dalam_menu_kalkulasi = False
    clock_widget.Clock_Widget()
    key = get_key()
    
    if key == 'up':
      current_select = (current_select - 1) % len(menu_options)
      draw_menu(menu_options, current_select)
    elif key == 'down':
      current_select = (current_select + 1) % len(menu_options)
      draw_menu(menu_options, current_select)
    elif key == 'q':
      stop_jam.set()
      clear_screen()
      print("\n Keluar dari program. Sampai jumpa, Bre!")
      break
    elif key == 'enter':
      clock_widget.dalam_menu_kalkulasi = True
      clear_screen()
      
      if current_select == 0:
        print(f"=== [MENU 1: Bisection Method] ===")
        ("Opening Bisection Method")
        log_activities("Opening Bisection Method")
        run_bisection()
      elif current_select == 1:
        print("=== [MENU 2: Regula Falsi] ===")
        log_activities("Opening Regula Falsi")
        run_regulaFalsi()
      elif current_select == 2:
        print("=== [MENU 3: Newton Raphson] ===")
        log_activities("Opening Newton Raphson")
        run_NR()
      elif current_select == 3:
        print(f"=== [MENU 4: Secand Method] ===")
        log_activities("Opening Secand Method")
        run_secand()
      elif current_select == 4:
        print(f"=== [MENU 5: Newton Raphson Modified] ===")
        log_activities("Opening Newton Raphson Modified")
        run_NR_modified()
      elif current_select == 5:
        print(f"=== [MENU 6: Factorization Method] ===")
        log_activities("Opening Factorization Method")
        factorization_main()
      elif current_select == JUMLAH_MENU - 2:
        Lazy_Loading("Opening log file...")
        log_activities("Opening log file...")
        read_logs()
      elif current_select == JUMLAH_MENU - 1:
        stop_jam.set()
        clear_screen()
        print("\n Keluar dari program. Sampai jumpa, Bre!")
        log_activities("Closing program...")
        break
        
      pilihan = input(f"\nTekan {AnsiColors.BOLD}[Enter]{AnsiColors.RESET} untuk kembali ke menu, atau ketik {AnsiColors.BOLD}[q]{AnsiColors.RESET} untuk keluar: ").strip().lower()
      
      if pilihan == 'q':
        stop_jam.set()
        clear_screen()
        print("\nKeluar dari program. Sampai jumpa, Bre!")
        log_activities("Closing program...")
        break
      
      clock_widget.dalam_menu_kalkulasi = False
      draw_menu(menu_options, current_select, awal_jalan=True)