import os
import sys
import threading
import datetime
import time
from src import \
  run_secand, \
  run_bisection, \
  run_NR, \
  run_NR_modified, \
  run_regulaFalsi
from src.utils.FuncUtils import Lazy_Loading

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
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"

ME   = "\033[91m"
JI   = "\033[38;5;208m"
KU   = "\033[93m"
HI   = "\033[92m"
BI   = "\033[94m"
NI   = "\033[96m"
U    = "\033[95m"

def get_header():
  return fr"""

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         PROGRAM KOMPUTASI NUMERIK                                          │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  {RED}Author      : Ahmad Fakhrul Bawani{RESET}                                                                        │
│  {GREEN}NRP         : 5025251143{RESET}                                                                                  │
│  {BLUE}License     : Open Source (MIT){RESET}                                                                           │
│  Source Code : https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-Tools/tree/main             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                               © 2026. All Rights Reserved for Academic Purposes.                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 {ME} _  __{JI} ____{KU}   __  __{HI}  _   _ {BI} _   _{CYAN} __   __{NI} _____  {U}  __  {RESET}
 {ME}| |/ /{JI}/ __ \{KU} |  \/  |{HI}| \ | |{BI}| | | |{CYAN}|  \/  |{NI}|___ \ {U} / /_ {RESET}
 {ME}| ' /{JI}| |  | |{KU}| |\/| |{HI}|  \| |{BI}| | | |{CYAN}| |\/| |{NI}  __) |{U}|  _ \{RESET}
 {ME}| . \{JI}| |__| |{KU}| |  | |{HI}| |\  |{BI}| |_| |{CYAN}| |  | |{NI} / __/{U} | (_) |{RESET}
 {ME}|_|\_\{JI}\____/{KU} |_|  |_|{HI}|_| \_|{BI} \___/{CYAN} |_|  |_|{NI}|_____|{U} \___/{RESET}

                            Hi Human, nice to meet you 👋
"""

JUMLAH_MENU = 7  # Total item termasuk pilihan "Quit"

def draw_menu(menu_items, selected_index, awal_jalan=False):
  if awal_jalan:
    clear_screen()
    print(get_header())
    print(f"\n Gunakan [↑/↓] Panah untuk Navigasi, {BOLD}[Enter]{RESET} untuk Memilih, {BOLD}[Q]{RESET} untuk Keluar\n")
    print("─" * 108)
  else:
    # Mengembalikan kursor naik ke atas agar menu tertimpa dengan halus tanpa reload global
    sys.stdout.write(f"\033[{JUMLAH_MENU + 1}A")
    sys.stdout.flush()

  for i, item in enumerate(menu_items):
    if i == selected_index:
      print(f"\033[K \033[92m{BOLD}►   {item}\033[0m")
    else:
      print(f"\033[K \033[90m    {item}\033[0m")
  print("\033[K" + "─" * 108)

# Variabel kontrol global untuk thread jam
dalam_menu_kalkulasi = False

def update_jam_realtime(stop_event):
  while not stop_event.is_set():
    if not dalam_menu_kalkulasi:
      sekarang = datetime.datetime.now()
      waktu_skrg = sekarang.strftime("%d-%m-%Y | %H:%M:%S WIB")
      jam = sekarang.hour
      
      # Penentuan ucapan salam berdasarkan jam saat ini
      if 5 <= jam < 12:
        greet = "Good Morning 🌄"
      elif 12 <= jam < 17:
        greet = "Good Afternoon 🏙️"
      elif 17 <= jam < 19:
        greet = "Good Evening 🌃"
      else:
        greet = "Good Night"
        
      # Menembak jam dinamis + greeting ke baris paling bawah terminal
      sys.stdout.write(f"\033[s\033[999;1H\033[K{JI}[ {greet} | {waktu_skrg} ]\033[0m\033[u")
      sys.stdout.flush()
    time.sleep(1)

# --- ALUR UTAMA ---
if __name__ == "__main__":
  Lazy_Loading("Loading program list...")

  menu_options = [
    "Chapter-2.1 Bisection Method",
    "Chapter-2.2 Regula Falsi",
    "Chapter-3.1 Newton Raphson",
    "Chapter-3.2 Secand Method",
    "Chapter-4.1 Newton Raphson Modified",
    "Chapter-4.2 Factorization Method",
    "Quit"
  ]
  
  current_select = 0

  stop_jam = threading.Event()
  thread_jam = threading.Thread(target=update_jam_realtime, args=(stop_jam,))
  thread_jam.daemon = True 
  thread_jam.start()
  
  # Gambar menu pertama kali
  draw_menu(menu_options, current_select, awal_jalan=True)
  
  while True:
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
      dalam_menu_kalkulasi = True
      clear_screen()
      
      if current_select == 0:
        print(f"=== [MENU 1: Bisection Method] ===")
        run_bisection()
      elif current_select == 1:
        print("=== [MENU 2: Regula Falsi] ===")
        run_regulaFalsi()
      elif current_select == 2:
        print("=== [MENU 3: Newton Raphson] ===")
        run_NR()
      elif current_select == 3:
        print(f"=== [MENU 4: Secand Method] ===")
        run_secand()
      elif current_select == 4:
        print(f"=== [MENU 5: Newton Raphson Modified] ===")
        run_NR_modified()
      elif current_select == 5:
        print(f"=== [MENU 6: Factorization Method] ===")
        # Jalankan fungsi faktorisasi di sini
      elif current_select == len(menu_options) - 1:
        stop_jam.set()
        clear_screen()
        print("\n Keluar dari program. Sampai jumpa, Bre!")
        break
        
      pilihan = input(f"\nTekan {BOLD}[Enter]{RESET} untuk kembali ke menu, atau ketik {BOLD}[q]{RESET} untuk keluar: ").strip().lower()
      
      if pilihan == 'q':
        stop_jam.set()
        clear_screen()
        print("\nKeluar dari program. Sampai jumpa, Bre!")
        break
      
      dalam_menu_kalkulasi = False
      draw_menu(menu_options, current_select, awal_jalan=True)