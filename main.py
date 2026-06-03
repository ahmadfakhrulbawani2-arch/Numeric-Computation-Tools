import os
import sys
from src import \
  run_secand, \
  run_bisection, \
  run_NR, \
  run_NR_modified, \
  run_regulaFalsi

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


HEADER = r"""

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         PROGRAM KOMPUTASI NUMERIK                                          │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Author      : Ahmad Fakhrul Bawani                                                                        │
│  NRP         : 5025251143                                                                                  │
│  License     : Open Source (MIT)                                                                           │
│  Source Code : https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-Tools/tree/main             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                               © 2026. All Rights Reserved for Academic Purposes.                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  _  ______  __  __   _   _ _   _ __   ______   __  
 | |/ / __ \|  \/  | | \ | | | | |  \/  |___ \ / /_ 
 | ' / |  | | |\/| | |  \| | | | | |\/| | __) | '_ \
 | . \ |__| | |  | | | |\  | |_| | |  | |/ __/| (_) |
 |_|\_\____/|_|  |_| |_| \_|\___/|_|  |_|_____|\___/ 
                                                    

"""

def draw_menu(menu_items, selected_index):
  clear_screen()
  # Kotak Metadata kebanggaanmu
  print(HEADER)
  
  print("\n Gunakan [↑/↓] Panah untuk Navigasi, [Enter] untuk Memilih, [Q] untuk Keluar\n")
  print("─" * 108)
  
  # Cetak item menu dengan pointer selector
  for i, item in enumerate(menu_items):
    if i == selected_index:
      # Kasih warna hijau (\033[92m) dan tanda panah mentereng ke item yang dipilih
      print(f" \033[92m►  {item}\033[0m")
    else:
      print(f"    {item}")
  print("─" * 108)

# --- ALUR UTAMA ---
if __name__ == "__main__":
  menu_options = [
    "Chapter-2.1 Bisection Method", #1
    "Chapter-2.2 Regula Falsi", #2
    "Chapter-3.1 Newton Raphson", #3
    "Chapter-3.2 Secand Method", #4
    "Chapter-4.1 Newton Raphson Modified", #5
    "Chapter-4.2 Factorization Method", #6
    "Quit"
  ]
  
  current_select = 0
  
  while True:
    draw_menu(menu_options, current_select)
    key = get_key()
    
    if key == 'up':
      # Geser ke atas, kalau mentok balik ke paling bawah
      current_select = (current_select - 1) % len(menu_options)
    elif key == 'down':
      # Geser ke bawah, kalau mentok balik ke paling atas
      current_select = (current_select + 1) % len(menu_options)
    elif key == 'q':
      print("\n Keluar dari program. Sampai jumpa, Bre!")
      break
    elif key == 'enter':
      clear_screen()
      
      # Eksekusi aksi berdasarkan indeks menu yang dipilih
      if current_select == 0:
        print(f"=== [MENU {current_select + 1}: Bisection Method] ===")
        run_bisection()
        
      elif current_select == 1:
        print("=== [MENU 2: Regula Falsi] ===")
        run_regulaFalsi()
        
      elif current_select == 2:
        print("=== [MENU 3: Newton Raphson] ===")
        run_NR()
      elif current_select == 3:
        print(f"=== [MENU {current_select + 1}: Secand Method] ===")
        run_secand()
      elif current_select == 4:
        print(f"=== [MENU {current_select + 1}: Newton Raphson Modified] ===")
        run_NR_modified()
      elif current_select == 5:
        print(f"=== [MENU {current_select + 1}: Factorization Method] ===")

      elif current_select == len(menu_options) - 1: # Opsi "Keluar dari Program"
        print("\n Keluar dari program. Sampai jumpa, Bre!")
        break
        
      input("\nTekan Enter sekali lagi untuk kembali ke menu utama...")