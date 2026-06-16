# SPDX-License-Identifier: MIT

from src.utils import *
import src.utils.Style as style
import csv
import sys
import io
import datetime
import time  # Ditambahkan karena ada fungsi time.sleep()

# ======================================================================
# This will be the metadata
# ======================================================================

class META_DATA:
    # MACRO VARIABLES
    IO_DIR = "spl_gauss"
    IN_PATH = f"./input/{IO_DIR}/main_table.csv"
    IN_CLOUD_PATH = f"./input/{IO_DIR}/cloud_table.csv"
    OUT_PATH = f"{IO_DIR}/result.txt"

    PROG_NAME = "Gauss-Seidel Method"
    REGRESSION_COLORS = [
        (255, 0, 127),  # Neon Pink / Garis Regresi Utama
        (0, 230, 118),  # Spring Green / Data Points
        (18, 18, 24),  # Deep Obsidian / Background
    ]
    REGRESSION_ART = rf"""

       ____                           
      / ___| __ _ _   _ ___ ___       
     | |  _ / _` | | | / __/ __|      
     | |_| | (_| | |_| \__ \__ \      
      \____|\__,_|\__,_|___/___/      
         ____       _     _      _ 
        / ___|  ___(_) __| | ___| |
        \___ \ / _ \ |/ _` |/ _ \ |
         ___) |  __/ | (_| |  __/ |
        |____/ \___|_|\__,_|\___|_|

        {PROG_NAME}

    """

    ADDITIONAL_HEADER = f"\
        Input directory: {IN_PATH}\n\
        File output: {OUT_PATH}\n"

    MAX_ITERATIONS = 0

# ======================================================================
# This will be data structure
# ======================================================================

class XY_Dataset:
    def __init__(self):
        self.data_cnt = 0
        self.x_data = []
        self.y_data = []

class Eq_Dataset:
    def __init__(self):
        self.eq_cnt: int = 1
        self.equations: List[List[int]] = [[]]

g_xy_dataset = XY_Dataset()
g_xy_dataset = Eq_Dataset()

# ======================================================================
# CAUTION: SET MAX ORDER SO IT IS NOT EXCEED TIME LIMIT
# ======================================================================
MAX_ORDO = 10

# ======================================================================
# This will be polynomial regression using gauss-seidel
# ======================================================================
class Regression_Gaus_Seidel:
    def main():
        pass
    

# ======================================================================
# This will be only gauss-seidel from the equation
# ======================================================================

class Gauss_Seidel_Iterate:
    def main():
        pass

# ======================================================================
# This will be fetch from drive, file, and manual
# ======================================================================

class Program_IO:
    def _fetch_from_gdrive():
        pass

    def _fetch_from_file():
        pass

    def _manually_input():
        pass

# ======================================================================
# This will be main function
# ======================================================================
class Manage_Log_File:
    def _open_regression():
        pass
    def _open_linear_eq():
        pass
    def _del_regression():
        pass
    def _del_regression():
        pass
    def _merge():
        pass

# ======================================================================
# This will be centered log message and err msg
# ======================================================================
class Log_Err_Msg:
    def __init__(self, _progname, _input_method, _err, _custom_msg):
        self.progname = _progname
        self.input_method = _input_method
        self.err_msg = _err
        self.custom_msg = _custom_msg
        
        # Deklarasi template pesan di dalam dictionary
        self._templates = {
            "run_program_msg": "Running {progname} with {input_method}",
            "file_not_found_msg": "Error: {progname} cannot find the log file",
            "closing_main_prog_msg": "Closing program {progname}",
            "no_data_err_msg": "Caught no data in {progname}",
            "custom_err_msg": "{err_msg} in {progname}",
            "bad_data_type_msg": "Unallowed data type in {progname}",
            "csv_err_msg": "CSV Error: {custom_msg} in {progname}",
            "closing_sub_prog_msg": "Quitting {progname} program..."
        }

    def __getattribute__(self, name):
        # Ambil dictionary _templates terlebih dahulu dengan aman
        templates = object.__getattribute__(self, '_templates')
        
        # Jika atribut yang dicari ada di dalam daftar template kita
        if name in templates:
            template_string = templates[name]
            # Isi template secara dinamis memakai property milik self saat ini
            return template_string.format(
                progname = object.__getattribute__(self, 'progname'),
                input_method = object.__getattribute__(self, 'input_method'),
                err_msg = object.__getattribute__(self, 'err_msg'),
                custom_msg = object.__getattribute__(self, 'custom_msg')
            )
        
        return object.__getattribute__(self, name)


# ======================================================================
# This will be main function
# ======================================================================

def Main_Gauss_Seidel():
    print()
    Lazy_Loading("Opening files...")
    # first item in each menu is the header
    main_menu = [
        ["Polynomial Regression",
            "Input manual data",                                                #0
            "Fetch data from files",                                            #1
            "Fetch data from Google Drive"                                      #2
        ],
        ["Only solving linear Equation", 
            "Input manual data",                                                #3
            "Fetch data from files",                                            #4 
            "Fetch data from Google Drive"                                      #5
        ],
        ["Manage log file", 
            "Open polynomial_regression run",                                   #6
            "Open linear equation run",                                         #7
            "Merge polynomial_regression <- linear equation",                   #8
            f"{AnsiColors.RED}Clear polynomial_regression{AnsiColors.RESET}",   #9
            f"{AnsiColors.RED}Clear linear equation{AnsiColors.RESET}"          #10
        ]
        ["this-is-item Quit"]                                                   #11
    ]

    curr_select = 0
    style.Clock_Widget()
    multiset_draw_menu(
        main_menu,
        curr_select,
        "",
        META_DATA.REGRESSION_ART,
        META_DATA.REGRESSION_COLORS,
        awal_jalan=True,
        additional_header=META_DATA.ADDITIONAL_HEADER,
    )
    len_menu = sum(len(items) for items in main_menu)
    last_idx = len_menu - 1
    for i, menu in enumerate(main_menu):
        if i >= len_menu:
            break
        for j, item in enumerate(menu):
            if j == 0 and "this-is-item" not in item:
                continue  # Jangan dihitung sebagai pilihan kalau dia header biasa
            total_selectable_items += 1

    while True:
        META_DATA.PROG_NAME = "Gauss-Seidel Method"
        menu = ""
        style.stop_jam.clear()
        style.dalam_menu_kalkulasi = False
        style.Clock_Widget()
        key = get_key()

        if key == "up":
            curr_select = (curr_select - 1) % total_selectable_items
            multiset_draw_menu(main_menu, curr_select, "", META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        elif key == "down":
            curr_select = (curr_select + 1) % total_selectable_items
            multiset_draw_menu(main_menu, curr_select, "", META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        elif key == "q":
            style.stop_jam.set()
            clear_screen()
            print("\n Keluar dari program. Sampai jumpa, Bre!")
            break
        elif key == "enter":
            style.dalam_menu_kalkulasi = True
            clear_screen()

            # ubah progname sesuaikan konteks
            if curr_select < 3:
                META_DATA.PROG_NAME += "for Regression"
            elif curr_select < 6 and curr_select >= 3:
                META_DATA.PROG_NAME += "for Linear Equation"


            match curr_select:
                case 0:
                    Program_IO._manually_input()
                    Regression_Gaus_Seidel.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "manual input", "", "")
                    log_activities(log.run_program_msg)
                case 1:
                    Program_IO._fetch_from_file()
                    Regression_Gaus_Seidel.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "fetch from file", "", "")
                    log_activities(log.run_program_msg)

    return

if __name__ == "__main__":
    Main_Gauss_Seidel()
