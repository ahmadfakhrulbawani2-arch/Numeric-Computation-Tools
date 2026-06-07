from src.utils import *
import src.utils.Style as style

REGRESSION_COLORS = [
    (255, 255, 255),
    (128, 128, 128),
    (30, 30, 30),
]
REGRESSION_ART = rf"""
  ____                               _               
 |  _ \ ___  __ _ _ __ ___ ___  ___ (_) ___  _ __    
 | |_) / _ \/ _` | '__/ _ / __|/ __|| |/ _ \| '_ \   
 |  _ <  __/ (_| | | |  __\__ \\__ \| | (_) | | | |  
 |_| \_\___|\__, |_|  \___|___/|___/|_|\___/|_| |_|  
            |___/                                    

"""


def input_manual():
    return


def fetch_data_from_files():
    return


def fetch_from_drive():
    return


if __name__ == "__main__":
    Lazy_Loading("Opening files...")
    main_menu = [
        "Input manual data",
        "Fetch data from files",
        "Fetch data from Google Drive",
    ]

    curr_select = 0

    style.Clock_Widget()
    draw_menu(
        main_menu, curr_select, "", REGRESSION_ART, REGRESSION_COLORS, awal_jalan=True
    )

    while True:
        len_menu = len(main_menu)
        last_idx = len_menu - 1
        style.stop_jam.clear()
        style.dalam_menu_kalkulasi = False
        style.Clock_Widget()
        key = get_key()

        if key == "up":
            current_select = (current_select - 1) % len(main_menu)
            draw_menu(main_menu, curr_select, "", REGRESSION_ART, REGRESSION_COLORS)
        elif key == "down":
            current_select = (current_select + 1) % len(main_menu)
            draw_menu(main_menu, curr_select, "", REGRESSION_ART, REGRESSION_COLORS)
        elif key == "q":
            style.stop_jam.set()
            clear_screen()
            print("\n Keluar dari program. Sampai jumpa, Bre!")
            break
        elif key == "enter":
            style.dalam_menu_kalkulasi = True
            clear_screen()

            match curr_select:
                case 0:
                    input_manual()
                    log_activities("Running Numeric Regression with manual input")
                case 1:
                    fetch_data_from_files()
                    log_activities(
                        "Running Numeric Regression with fetching input file"
                    )
                case 2:
                    fetch_from_drive()
                    log_activities(
                        "Running Numeric Regression with fetching Google Drive file"
                    )
                case last_idx:
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
                main_menu,
                curr_select,
                "",
                REGRESSION_ART,
                REGRESSION_COLORS,
                awal_jalan=True,
            )
