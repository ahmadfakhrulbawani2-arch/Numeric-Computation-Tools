# SPDX-License-Identifier: MIT

import os
import sys
from src import (
    run_secand,
    run_bisection,
    run_NR,
    run_NR_modified,
    run_regulaFalsi,
    factorization_main,
    Lazy_Loading,
    log_activities,
    read_logs,
    AnsiColors,
    stop_jam,
    draw_menu,
    clear_screen,
    get_key,
    linear_regression,
    polynomial_regression,
    Main_Gauss_Seidel,
)
import src.utils.Style as style

# --- VARIABEL WARNA ---

rainbow_colors = [
    (255, 0, 0),  # Merah
    (255, 255, 0),  # Kuning
    (0, 255, 0),  # Hijau
    (0, 255, 255),  # Cyan
    (0, 0, 255),  # Biru
    (255, 0, 255),  # Magenta
]

cyberpunk_colors = [
    (255, 0, 128),  # Pink Neon
    (128, 0, 255),  # Ungu
    (0, 255, 255),  # Cyan Neon
    (243, 230, 0),  # Kuning Neon
]

ASCII_HEADER = rf"""
  _  __ ____   __  __  _   _  _   _  __  __ _____   __  
 | |/ // __ \ |  \/  || \ | || | | ||  \/  ||___ \ / /_ 
 | ' /| |  | || |\/| ||  \| || | | || |\/| |  __) |  _ \
 | . \| |__| || |  | || |\  || |_| || |  | | / __ | (_) |
 |_|\_\\____/ |_|  |_||_| \_| \___/ |_|  |_||_____ \___/

            Hello, Nice to meet you 👋
            We don't use rainbow cause we reject 🌈

"""

STATS = rf"""

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

JUMLAH_MENU = 11


# --- ALUR UTAMA ---
if __name__ == "__main__":

    menu_options = [
        "Chapter-2.1 Bisection Method",
        "Chapter-2.2 Regula Falsi",
        "Chapter-3.1 Newton Raphson",
        "Chapter-3.2 Secand Method",
        "Chapter-4.1 Newton Raphson Modified",
        "Chapter-4.2 Factorization Method",
        "Chapter-6.1 Linear Regression",
        "Chapter-6.2 Polynomial Regression",
        "Chapter-7.1 Gauss-Seidel Method",
        "Open program history",
        "Quit",
    ]

    current_select = 0

    # Kasih widget jam di thread berbeda
    style.Clock_Widget()

    # Gambar menu pertama kali
    draw_menu(
        menu_options,
        current_select,
        STATS,
        ASCII_HEADER,
        cyberpunk_colors,
        awal_jalan=True,
    )

    while True:
        style.stop_jam.clear()
        style.dalam_menu_kalkulasi = False
        style.Clock_Widget()
        key = get_key()

        if key == "up":
            current_select = (current_select - 1) % len(menu_options)
            draw_menu(
                menu_options, current_select, STATS, ASCII_HEADER, cyberpunk_colors
            )
        elif key == "down":
            current_select = (current_select + 1) % len(menu_options)
            draw_menu(
                menu_options, current_select, STATS, ASCII_HEADER, cyberpunk_colors
            )
        elif key == "q":
            stop_jam.set()
            clear_screen()
            print("\n Keluar dari program. Sampai jumpa, Bre!")
            break
        elif key == "enter":
            style.dalam_menu_kalkulasi = True
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
            elif current_select == 6:
                print(f"=== [MENU 7: Linear Regression Method] ===")
                log_activities("Opening Linear Regression")
                linear_regression()
            elif current_select == 7:
                print(f"=== [MENU 8: Polynomial Regression Method] ===")
                log_activities("Opening Polynomial Regression")
                polynomial_regression()
            elif current_select == 8:
                print(f"=== [MENU 9: Gauss-Seidel Method] ===")
                log_activities("Gauss-Seidel Method")
                Main_Gauss_Seidel()
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

            pilihan = (
                input(
                    f"\nTekan {AnsiColors.BOLD}[Enter]{AnsiColors.RESET} untuk kembali ke menu, atau ketik {AnsiColors.BOLD}[q]{AnsiColors.RESET} untuk keluar: "
                )
                .strip()
                .lower()
            )

            if pilihan == "q":
                stop_jam.set()
                clear_screen()
                print("\nKeluar dari program. Sampai jumpa, Bre!")
                log_activities("Closing program...")
                break

            style.dalam_menu_kalkulasi = False
            draw_menu(
                menu_options,
                current_select,
                STATS,
                ASCII_HEADER,
                cyberpunk_colors,
                awal_jalan=True,
            )
