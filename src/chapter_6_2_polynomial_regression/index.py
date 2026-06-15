# SPDX-License-Identifier: MIT

from src.utils import *
import src.utils.Style as style
import csv
import sys
import io
import datetime
import time  # Ditambahkan karena ada fungsi time.sleep()

# MACRO VARIABLES
IO_DIR = "polynomial_regression"
IN_PATH = f"./input/{IO_DIR}/main_table.csv"
IN_CLOUD_PATH = f"./input/{IO_DIR}/cloud_table.csv"
OUT_PATH = f"{IO_DIR}/result.txt"

PROG_NAME = "Polynomial Regression"
REGRESSION_COLORS = [
    (255, 255, 255),
    (128, 128, 128),
    (30, 30, 30),
]
REGRESSION_ART = rf"""
     _     _                                         
    | |   (_)_ __   ___  __ _ _ __                   
    | |   | | '_ \ / _ \/ _` | '__|                  
    | |___| | | | |  __/ (_| | |                     
    |_____|_|_| |_|\___|\__,_|_|                     
     ____                               _
    |  _ \ ___  __ _ _ __ ___  ___ ___(_) ___  _ __  
    | |_) / _ \/ _` | '__/ _ \/ __/ __| |/ _ \| '_ \ 
    |  _ <  __/ (_| | |  __/\__ \__ \ | (_) | | | | |
    |_| \_\___|\__, |_|  \___||___/___/_|\___/|_| |_|
               |___/                                 


"""

ADDITIONAL_HEADER = f"\
    Input directory: {IN_PATH}\n\
    File output: {OUT_PATH}\n"

buffer = io.StringIO()

ERR_TOLERANCE = 0.0001
class Csv_Data:
    def __init__(self):
        self.x_data = []
        self.y_data = []

# ================================================
# CAUTION: SET MAX ORDER SO IT IS NOT EXCEED TIME LIMIT
# ================================================
class Reg_Data:
    # ================================================
    # constructor
    # ================================================
    def __init__(self, datas: Csv_Data, _order: int):
        _len_x = len(datas.x_data)
        _len_y = len(datas.y_data)
        if _len_x <= 0 or _len_y <= 0:
            print("Error, caught no data is valid")
            log_activities(f"Caught no data in {PROG_NAME}", "ERROR")
            return

        _data_x = datas.x_data
        _data_y = datas.y_data

        # attributes
        self.data_amount = min(len(_data_x), len(_data_y))
        self.data_x = _data_x[:self.data_amount]
        self.data_y = _data_y[:self.data_amount]
        self.order = _order
        
        # --- FIX 1: Alokasikan ukuran list default 0 biar gak IndexError ---
        self.x_sigma_by_order: List[float] = [0.0] * ((2 * _order) + 1)
        self.xy_sigma_by_order: List[float] = [0.0] * (_order + 1)
        
        self.x_sigma_by_order[0] = float(self.data_amount)
        self.__generate_sigma_arr_data()
        
        self.sigma_obe_arr_data: List[List[float]] = []
        self.__generate_2d_obe_arr_data()
        self.results_coeffs: List[float] = []

    # ================================================
    # private
    # ================================================
    def __generate_sigma_arr_data(self):
        r = self.order
        n = self.data_amount

        # --- FIX 2: Perbaikan logika loop pemangkatan X agar pas dengan indeks row+col ---
        for i in range(1, (2 * r) + 1):
            for x in self.data_x:
                _curr_x = x ** i
                self.x_sigma_by_order[i] += _curr_x
        
        # --- FIX 3: Membawa n ke range(n) agar bisa di-loop ---
        for i in range(r + 1): 
            for j in range(n):
                _cur_x = self.data_x[j] ** i
                _curr_y = self.data_y[j]
                self.xy_sigma_by_order[i] += _cur_x * _curr_y
    
    def __generate_2d_obe_arr_data(self):
        r = self.order
        x_sum_data = self.x_sigma_by_order
        xy_sum_data = self.xy_sigma_by_order

        # generate left and right part
        for row in range(r+1):
            _curr_row = []
            for col in range(r+1):
                _curr_row.append(x_sum_data[row+col])
            _curr_row.append(xy_sum_data[row])
            self.sigma_obe_arr_data.append(_curr_row)

    def __ngelakoni_obe(self) -> None:
        try:
            res = iterateGaussJordan(self.sigma_obe_arr_data, PROG_NAME, "a")
            self.results_coeffs = [row[-1] for row in res]
            print("\n === Didapatkan koefisien akhir ===")
            for i, a in enumerate(self.results_coeffs):
                print(f"a{i} = {a:.4f}")
                time.sleep(.2)
        except (ValueError, ZeroDivisionError) as err:
            log_activities(f"{err} in {PROG_NAME}", "ERROR")
            self.results_coeffs = []
            return 

    # ================================================
    # public
    # ================================================
    def _show_data(self):
        Lazy_Loading("Calculating all X sum and XY sum...", .5)
        for i, x in enumerate(self.x_sigma_by_order):
            print(f"sigma X ^ {i} = {x}")
            time.sleep(.2)
        
        Lazy_Loading("Building OBE array...", .2)
        Print_2d_obe_Matrix(self.sigma_obe_arr_data, PROG_NAME, "a")

    def _calc_expr(self):
        Lazy_Loading("Initializing OBE Gauss...", .2)
        self.__ngelakoni_obe()
        
        if not self.results_coeffs:
            print("[ERROR] Gagal menghitung persamaan fungsi karena matriks bermasalah.")
            return

        print(f"Hasil akhir: ")
        sys.stdout.write("    y = ")
        for i, coef in enumerate(self.results_coeffs):
            if i == 0:
                sys.stdout.write(f"{coef:.4f} ")
            elif i == 1:
                sys.stdout.write(f"{coef:+.4f}x ")
            else:
                sys.stdout.write(f"{coef:+.4f}x^{i} ")


# --- HELPER AMBIL INPUT ORDER DARI USER ---
def hitung_max_order_valid(banyak_data: int) -> int:
    """Membatasi order regresi agar tidak melebihi (jumlah data - 1)"""
    print(f"\n[INFO] Jumlah data valid saat ini: {banyak_data}")
    input_ord = input(f"Masukkan order polinomial yang diinginkan (Max Ordo: {banyak_data - 1}): ").strip()
    
    while not InputValidator.is_numeric(input_ord) or int(input_ord) < 1 or int(input_ord) >= banyak_data:
        print(f"{AnsiColors.RED}Ordo harus berupa angka, minimal 1, dan tidak boleh melebihi/sama dengan jumlah data!{AnsiColors.RESET}")
        input_ord = input(f"Masukkan kembali order polinomial: ").strip()
        
    return int(input_ord)


def reg_processing(raw_data: Csv_Data):
    if not isinstance(raw_data, Csv_Data):
        log_activities(f"Unallowed data type in {PROG_NAME}", "ERROR")
        raise TypeError("Unallowed data type")
    
    total_data = min(len(raw_data.x_data), len(raw_data.y_data))
    if total_data < 2:
        print(f"{AnsiColors.RED}Data terlalu sedikit untuk melakukan regresi! Minimal butuh 2 pasang data.{AnsiColors.RESET}")
        return

    print(f"X = {raw_data.x_data}")
    time.sleep(0.2)
    print(f"Y = {raw_data.y_data}")
    print()
    time.sleep(0.2)
    
    # --- FIX 4: Mengambil input order secara dinamis sebelum inisialisasi Reg_Data ---
    pilihan_order = hitung_max_order_valid(total_data)
    
    print()
    the_data = Reg_Data(raw_data, pilihan_order)
    print()
    the_data._show_data()
    print()
    the_data._calc_expr()
    print()
    sys.stdout.write("\n\n\033[5A")
    sys.stdout.flush()
    time.sleep(0.1)
    style.dalam_menu_kalkulasi = False


def csv_processing(PATH):
    raw_data = Csv_Data()
    try:
        with open(file=PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            header = [h.strip().lower() for h in header]

            try:
                x_idx = header.index("x")
                y_idx = header.index("y")
            except ValueError:
                log_activities(
                    f"Error: CSV file must have 'x' and 'y' column (case insensitive) in {PROG_NAME}",
                    "ERROR",
                )
                raise ValueError(
                    "CSV file must have 'x' and 'y' column (case insensitive)"
                )

            for row in reader:
                if not row or len(row) <= max(x_idx, y_idx):
                    continue
                try:
                    raw_data.x_data.append(float(row[x_idx]))
                    raw_data.y_data.append(float(row[y_idx]))
                except ValueError:
                    print(f"Skipping improper row-{row}")
            
            Lazy_Loading(f"Scanning {PATH}", 0.2)
            print()
            time.sleep(0.2)
            print("=== Data fetched successfully ===")
            time.sleep(0.2)
            print()
            # --- FIX 5: Pemanggilan reg_processing diperbaiki parameter pass-nya ---
            reg_processing(raw_data)
            
    except FileNotFoundError:
        log_activities(f"File not found in {PROG_NAME}.", "ERROR")
        raise FileNotFoundError(f"File/Path not found")
    return


def input_manual():
    print_text_gradient_angle(REGRESSION_ART, REGRESSION_COLORS)
    time.sleep(0.2)
    PrintIntroProg2(PROG_NAME)
    print()
    time.sleep(0.2)
    inputUser: str = input(
        f"Please input how many data you have, or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
    ).strip()
    if inputUser.lower() == "q":
        print("User quit the program...")
        log_activities(f"Quitting {PROG_NAME} program...")
        return

    while not InputValidator.is_numeric(inputUser) or int(inputUser) < 2:
        if inputUser.lower() == "q":
            print("User quit the program...")
            log_activities(f"Quitting {PROG_NAME} program...")
            return
        inputUser = input(
            f"Please input number only (minimal 2 data) or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
        )

    byk_data = int(inputUser)
    raw_data = Csv_Data()
    for i in range(byk_data):
        x_val = input(f"X{i+1}: ").strip()
        y_val = input(f"Y{i+1}: ").strip()

        while not InputValidator.is_numeric(x_val) or not InputValidator.is_numeric(y_val):
            print(f"{AnsiColors.RED}Please input number only{AnsiColors.RESET}")
            x_val = input(f"X{i+1}: ").strip()
            y_val = input(f"Y{i+1}: ").strip()

        raw_data.x_data.append(float(x_val))
        raw_data.y_data.append(float(y_val))

    reg_processing(raw_data)
    return


def fetch_data_from_files():
    time.sleep(0.2)
    print_text_gradient_angle(REGRESSION_ART, REGRESSION_COLORS)
    time.sleep(0.2)
    PrintIntroProg2(PROG_NAME)
    time.sleep(0.2)
    print()
    print(f"fetching data from {IN_PATH}")
    print(f"Make sure you have put correct format or it will error")
    print()
    csv_processing(IN_PATH)
    return


def fetch_from_drive():
    print_text_gradient_angle(REGRESSION_ART, REGRESSION_COLORS)
    time.sleep(0.2)
    PrintIntroProg2(PROG_NAME)
    print()
    time.sleep(0.2)
    inputUrl: str = input(
        f"Please input file URL (Google Drive text file only, all extension, {AnsiColors.BOLD}{AnsiColors.BG_WHITE}and public{AnsiColors.RESET}) or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
    ).strip()
    if inputUrl.lower() == "q":
        print("User quit the program...")
        log_activities(f"Quitting {PROG_NAME} program...")
        return

    time.sleep(0.2)
    print(f"fetching data from {inputUrl}")
    time.sleep(0.2)
    print(f"Make sure you have put correct format or it will error")
    print()
    canDownload = download_from_gdrive(PROG_NAME, inputUrl, IN_CLOUD_PATH)

    if not canDownload:
        print("Sorry, we can't download/write your spesific URL path")
        log_activities(f"Can't download file from {PROG_NAME}")
        return

    csv_processing(IN_CLOUD_PATH)
    return


# === Main ===
def polynomial_regression():
    Lazy_Loading("Opening files...")
    main_menu = [
        "Input manual data",
        "Fetch data from files",
        "Fetch data from Google Drive",
        "Feth run logs",
        "Quit",
    ]

    curr_select = 0

    style.Clock_Widget()
    draw_menu(
        main_menu,
        curr_select,
        "",
        REGRESSION_ART,
        REGRESSION_COLORS,
        awal_jalan=True,
        additional_header=ADDITIONAL_HEADER,
    )

    while True:
        len_menu = len(main_menu)
        last_idx = len_menu - 1
        menu = ""
        style.stop_jam.clear()
        style.dalam_menu_kalkulasi = False
        style.Clock_Widget()
        key = get_key()

        if key == "up":
            curr_select = (curr_select - 1) % len(main_menu)
            draw_menu(main_menu, curr_select, "", REGRESSION_ART, REGRESSION_COLORS)
        elif key == "down":
            curr_select = (curr_select + 1) % len(main_menu)
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
                    log_activities("Running Polynomial Regression with manual input")
                    menu = "manual input"
                case 1:
                    fetch_data_from_files()
                    log_activities(
                        "Running Polynomial Regression with fetching input file"
                    )
                    menu = "input file"
                case 2:
                    fetch_from_drive()
                    log_activities(
                        "Running Polynomial Regression with fetching Google Drive file"
                    )
                    menu = "cloud file"
                case 3:
                    open_output(OUT_PATH, PROG_NAME)
                    menu = "Misc"
                case last_idx:
                    style.stop_jam.set()
                    clear_screen()
                    print(f"\n Keluar dari program {PROG_NAME}")
                    log_activities(f"Closing program {PROG_NAME}...")
                    break

            print("")
            style.dalam_menu_kalkulasi = False
            if menu == "Misc":
                sys.stdout.write("\n\n\033[2A")
                sys.stdout.flush()
                pilihan = (
                    input(
                        f"{AnsiColors.BOLD}[Enter or any key]{AnsiColors.RESET} to back to main menu,\n\
or press {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
                    )
                    .strip()
                    .lower()
                )
            else:
                pilihan = (
                    input(
                        f"\nPress {AnsiColors.BOLD}[s]{AnsiColors.RESET} to save result,\n\
{AnsiColors.BOLD}[Enter or any key]{AnsiColors.RESET} to back to main menu,\n\
or press {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
                    )
                    .strip()
                    .lower()
                )

            if pilihan == "q":
                style.stop_jam.set()
                clear_screen()
                print("\nKeluar dari program. Sampai jumpa, Bre!")
                log_activities(f"Closing program {PROG_NAME}...")
                break
            elif pilihan == "s":
                clear_screen()
                write_result(menu, buffer, OUT_PATH, PROG_NAME)

            style.dalam_menu_kalkulasi = False
            clear_screen()
            draw_menu(
                main_menu,
                curr_select,
                "",
                REGRESSION_ART,
                REGRESSION_COLORS,
                awal_jalan=True,
                additional_header=ADDITIONAL_HEADER,
            )


if __name__ == "__main__":
    polynomial_regression()