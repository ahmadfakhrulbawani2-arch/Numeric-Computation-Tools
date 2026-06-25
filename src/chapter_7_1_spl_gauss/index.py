# SPDX-License-Identifier: MIT
# ======================================================================
# Code format convention:
# _function_name, one _ means public function
# __function_name, two _ means private function
# Always use snake case!
# Combine snake case and Pascal case for class and struct
# Always use OOP!
# ======================================================================

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
    IO_DIR_REG = "reg_gauss"
    IO_DIR_SPL = "spl_gauss"
    IN_PATH_REG = f"./input/{IO_DIR_REG}/main_table.csv"
    IN_PATH_SPL = f"./input/{IO_DIR_SPL}/main_table.csv"
    IN_CLOUD_PATH_REG = f"./input/{IO_DIR_REG}/cloud_table.csv"
    IN_CLOUD_PATH_SPL = f"./input/{IO_DIR_SPL}/cloud_table.csv"
    OUT_PATH_SPL = f"{IO_DIR_SPL}/result.txt"
    OUT_PATH_REG = f"{IO_DIR_REG}/result.txt"

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

    ADDITIONAL_HEADER = rf"""
    input_dir:
        - Polynomial regression: {IN_PATH_REG}
        - Linear equation case: {IN_PATH_SPL}
    output_dir:
        - Polynomial regression: {OUT_PATH_REG}
        - Linear equation case: {OUT_PATH_SPL}

"""

    MAX_ITERATIONS = 0

# ======================================================================
# This will be centered log message and err msg
# ======================================================================
class Log_Err_Msg:
    """
    Centralize logging and error messages
    run_program_msg
    file_not_found_msg
    closing_main_prog_msg
    no_data_err_msg
    custom_err_msg
    bad_data_type_msg
    csv_err_msg
    closing_sub_prog_msg
    csv_invalid
    download_failed
    txt_invalid
    """
    def __init__(self, _progname, _input_method, _err, _custom_msg):
        self.progname = _progname
        self.input_method = _input_method
        self.err_msg = _err
        self.custom_msg = _custom_msg

        # Deklarasi template pesan di dalam dictionary
        self._templates = {
            "run_program_msg": "Running {progname} by {input_method}", # in every program star
            "file_not_found_msg": "Error: {progname} cannot find the log file", # file not found err
            "closing_main_prog_msg": "Closing program {progname}", # for closing main program
            "no_data_err_msg": "Caught no data in {progname} or data not enough", # if no data in prog_data or not enough data
            "custom_err_msg": "{err_msg} in {progname}", # also custom err
            "bad_data_type_msg": "Unallowed data type in {progname}", # data type mismatch
            "csv_err_msg": "CSV Error: {custom_msg} in {progname}", # other csv err
            "closing_sub_prog_msg": "Quitting {progname} by {input_method}...", # closing sub prog
            "csv_invalid": "Error: CSV format is not valid by {input_method} in {progname}", # invalid csv
            "download_failed": "Error: Failed to download by {input_method} in {progname}", # failed download
            "txt_invalid": "Error: TXT format is not valid by {input_method} in {progname}",
        }

    def __getattribute__(self, name):
        # Ambil dictionary _templates terlebih dahulu dengan aman
        templates = object.__getattribute__(self, "_templates")

        # Jika atribut yang dicari ada di dalam daftar template kita
        if name in templates:
            template_string = templates[name]
            # Isi template secara dinamis memakai property milik self saat ini
            return template_string.format(
                progname=object.__getattribute__(self, "progname"),
                input_method=object.__getattribute__(self, "input_method"),
                err_msg=object.__getattribute__(self, "err_msg"),
                custom_msg=object.__getattribute__(self, "custom_msg"),
            )

        return object.__getattribute__(self, name)


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
        self.equations: List[List[float]] = [[]]

class Prog_Data:
    EXIT_W_SAVE = 1
    g_xy_dataset = XY_Dataset()
    g_eq_dataset = Eq_Dataset()
    byk_data = 0
    max_iter = 100 # variable
    true_cloud_in_path = ""
    true_out_path = ""

# ======================================================================
# CAUTION: SET MAX ORDER SO IT IS NOT EXCEED TIME LIMIT
# ======================================================================
MAX_ORDO = 10

# ======================================================================
# This will be polynomial regression using gauss-seidel
# ======================================================================
class Reg_Data:
    # ================================================
    # constructor
    # ================================================
    def __init__(self, _order: int):
        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "", "", "")
        datas = Prog_Data.g_xy_dataset
        _len_x = len(datas.x_data)
        _len_y = len(datas.y_data)
        if _len_x <= 2 or _len_y <= 2:
            print(self.log.no_data_err_msg)
            log_activities(self.log.no_data_err_msg, "ERROR")
            return

        _data_x = datas.x_data
        _data_y = datas.y_data

        # attributes
        self.data_amount = min(len(_data_x), len(_data_y))
        self.data_x = _data_x[: self.data_amount]
        self.data_y = _data_y[: self.data_amount]
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
                _curr_x = x**i
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
        for row in range(r + 1):
            _curr_row = []
            for col in range(r + 1):
                _curr_row.append(x_sum_data[row + col])
            _curr_row.append(xy_sum_data[row])
            self.sigma_obe_arr_data.append(_curr_row)

    def __ngelakoni_gauss_seidel(self) -> None:
        try:
            res = iterateGaussSeidel(self.sigma_obe_arr_data, META_DATA.PROG_NAME, "a", Prog_Data.max_iter)
            self.results_coeffs = res
            print("\n === Didapatkan koefisien akhir ===\n")
            g_buffer.write("\n === Didapatkan koefisien akhir ===\n")
            for i, a in enumerate(self.results_coeffs):
                print(f"a{i} = {a:.4f}")
                time.sleep(0.2)
        except (ValueError, ZeroDivisionError) as err:
            log_activities(f"{err} in {META_DATA.PROG_NAME}", "ERROR")
            self.results_coeffs = []
            return

    # ================================================
    # public
    # ================================================
    def _show_data(self):
        Lazy_Loading("Calculating all X sum and XY sum...", 0.5)
        print()
        for i, x in enumerate(self.x_sigma_by_order):
            print(f"sigma X^{i} = {x}")
            g_buffer.write(f"sigma X ^ {i} = {x}")
            time.sleep(0.2)

        print()
        Lazy_Loading("Building OBE array...", 0.2)
        Print_2d_obe_Matrix(self.sigma_obe_arr_data, META_DATA.PROG_NAME, "a")

    def _calc_expr(self):
        Lazy_Loading("Initializing OBE Gauss...", 0.2)
        print()
        self.__ngelakoni_gauss_seidel()

        if not self.results_coeffs:
            print(
                "[ERROR] Gagal menghitung persamaan fungsi karena matriks bermasalah."
            )
            return

        print(f"Hasil akhir: ")
        g_buffer.write(f"Hasil akhir: \n")
        sys.stdout.write("    y = ")
        g_buffer.write("    y = ")
        for i, coef in enumerate(self.results_coeffs):
            sign = "+ " if coef >= 0 else "- "
            _coef = abs(coef)
            if i == 0:
                sys.stdout.write(f"{sign}{_coef:.4f} ")
                g_buffer.write(f"{sign}{_coef:.4f} ")
            elif i == 1:
                sys.stdout.write(f"{sign}{_coef:.4f}x ")
                g_buffer.write(f"{sign}{_coef:.4f}x ")
            else:
                sys.stdout.write(f"{sign}{_coef:.4f}x^{i} ")
                g_buffer.write(f"{sign}{_coef:.4f}x^{i} ")
        sys.stdout.write("\n\n")
        g_buffer.write(f"\n\n")

class Regression_Gaus_Seidel:
    def __init__(self):
        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "", "", "")


    # --- HELPER AMBIL INPUT ORDER DARI USER ---
    def __hitung_max_order_valid(self, banyak_data: int) -> int:
        print(f"\n[INFO] Valid data count: {banyak_data}")
        style.dalam_menu_kalkulasi = False
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        input_ord = input(
            f"Input desired polynomial degree/order (Max Ordo: {MAX_ORDO - 1}): "
        ).strip()

        while (
            not InputValidator.is_numeric(input_ord)
            or int(input_ord) < 1
            or int(input_ord) >= MAX_ORDO
        ):
            style.dalam_menu_kalkulasi = True
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            sys.stdout.flush()
            print(
                f"{AnsiColors.RED}Ordo cannot be less than one and higher that the limit!{AnsiColors.RESET}"
            )
            style.dalam_menu_kalkulasi = False
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            sys.stdout.flush()
            input_ord = input(f"Input valid polynomial order again: ").strip()

        style.dalam_menu_kalkulasi = True
        sys.stdout.write(
            "\n\n\033[2A"
        )  # leaving clock trail so I know when it start running
        sys.stdout.flush()
        return int(input_ord)

    def main(self):
        data_set = Prog_Data.g_xy_dataset
        if not isinstance(data_set, XY_Dataset):
            log_activities(self.log.bad_data_type_msg, "ERROR")
            raise TypeError(self.log.bad_data_type_msg)
        
        Prog_Data.byk_data = min(len(data_set.x_data), len(data_set.y_data))
        if Prog_Data.byk_data < 2:
            e = self.log.no_data_err_msg
            print(e)
            log_activities(e, "ERROR")
            return
        
        # show data
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        print(f"X = {data_set.x_data}")
        time.sleep(0.2)
        print(f"Y = {data_set.y_data}")
        print()
        time.sleep(0.2)

        pilihan_order = self.__hitung_max_order_valid(Prog_Data.byk_data)
        print()
        the_data = Reg_Data(pilihan_order)
        print()
        the_data._show_data()
        print()
        the_data._calc_expr()
        print()
        sys.stdout.write("\n\n\033[5A")
        sys.stdout.flush()
        time.sleep(0.1)
        style.dalam_menu_kalkulasi = False

# ======================================================================
# This will be only gauss-seidel from the equation
# ======================================================================

# spl
class Gauss_Seidel_Iterate:
    def __init__(self):
        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "", "", "")

    def __ngelakoni_gauss_seidel(self) -> None:
        try:
            res = iterateGaussSeidel(Prog_Data.g_eq_dataset, META_DATA.PROG_NAME, "a", Prog_Data.max_iter)
            self.results_coeffs = res
            print("\n === Didapatkan koefisien akhir ===\n")
            g_buffer.write("\n === Didapatkan koefisien akhir ===\n")
            for i, a in enumerate(self.results_coeffs):
                print(f"a{i} = {a:.4f}")
                time.sleep(0.2)
        except (ValueError, ZeroDivisionError) as err:
            log_activities(f"{err} in {META_DATA.PROG_NAME}", "ERROR")
            self.results_coeffs = []
            return

    def __calc_expr(self):
        Lazy_Loading("Initializing OBE Gauss...", 0.2)
        print()
        self.__ngelakoni_gauss_seidel()

        if not self.results_coeffs:
            print(
                "[ERROR] Gagal menghitung persamaan fungsi karena matriks bermasalah."
            )
            return

        print(f"Hasil akhir: ")
        g_buffer.write(f"Hasil akhir: \n")
        sys.stdout.write("    y = ")
        g_buffer.write("    y = ")
        for i, coef in enumerate(self.results_coeffs):
            sign = "+ " if coef >= 0 else "- "
            _coef = abs(coef)
            if i == 0:
                sys.stdout.write(f"{sign}{_coef:.4f} ")
                g_buffer.write(f"{sign}{_coef:.4f} ")
            elif i == 1:
                sys.stdout.write(f"{sign}{_coef:.4f}x ")
                g_buffer.write(f"{sign}{_coef:.4f}x ")
            else:
                sys.stdout.write(f"{sign}{_coef:.4f}x^{i} ")
                g_buffer.write(f"{sign}{_coef:.4f}x^{i} ")
        sys.stdout.write("\n\n")
        g_buffer.write(f"\n\n")

    def main(self):
        eq_data = Prog_Data.g_eq_dataset
        if not isinstance(eq_data, Eq_Dataset):
            log_activities(self.log.bad_data_type_msg, "ERROR")
            raise TypeError(self.log.bad_data_type_msg)
        style.dalam_menu_kalkulasi = False
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        for eq in Prog_Data.g_eq_dataset.equations:
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            sys.stdout.flush()
            PrintSingleEq(eq)
        style.dalam_menu_kalkulasi = True
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        self.__calc_expr()
        print()
        sys.stdout.write("\n\n\033[5A")
        sys.stdout.flush()
        time.sleep(0.1)
        style.dalam_menu_kalkulasi = False
        print("Test iterate gauss seidel main")


# ======================================================================
# This will be fetch from drive, file, and manual
# ======================================================================

# io
class Program_IO:
    """
    Untuk input output program
    """
    def __init__(self):
        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "", "", "")

    def __eq_processing(self, PATH):
        """
        Masukin data eq input ke variable dari file .txt secara private di kelas ini saja
        """
        try:
            with open(file=PATH, mode="r", encoding="utf-8") as file:
                temp_dataset = []
                
                for line in file:
                    # Lewati baris kosong jika ada
                    if not line.strip():
                        continue
                    
                    # Validasi per baris atau langsung validasi elemennya
                    if InputValidator.is_numeric_coeffs(line):
                        # Pecah per baris dan ubah ke float
                        row_data = [float(v) for v in line.split()]
                        temp_dataset.append(row_data)
                    else:
                        e = self.log.txt_invalid
                        log_activities(e, "ERROR")
                        raise ValueError(e)
                
                # Masukkan ke variabel global/class jika semua baris valid
                Prog_Data.g_eq_dataset = temp_dataset

        except FileNotFoundError as e:
            log_activities(self.log.file_not_found_msg, "ERROR")
            raise FileNotFoundError(e)

    def __csv_processing(self,PATH):
        """
        Pengolahan data csv dari file .csv secara private di kelas ini saja
        """
        try:
            with open(file=PATH, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)
                header = [h.strip().lower() for h in header]

                try:
                    x_idx = header.index("x")
                    y_idx = header.index("y")
                except ValueError as e:
                    log_activities(self.log.csv_invalid, "ERROR")
                    raise ValueError(e)
                for row in reader:
                    if not row or len(row) <= max(x_idx, y_idx):
                        continue
                    try:
                        Prog_Data.g_xy_dataset.x_data.append(float(row[x_idx]))
                        Prog_Data.g_xy_dataset.y_data.append(float(row[y_idx]))
                    except ValueError:
                        print(f"Skipping improper row-{row}")

                Lazy_Loading(f"Scanning {PATH}", 0.2)
                print()
                time.sleep(0.2)
                print("=== Data fetched successfully ===")
                time.sleep(0.2)
                print()
        except FileNotFoundError as e:
            log_activities(self.log.file_not_found_msg, "ERROR")
            raise FileNotFoundError(e)

    def _fetch_from_gdrive(self):
        """Input otomatis data regresi atau equation dari gdrive"""
        print_text_gradient_angle(META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        time.sleep(0.2)
        PrintIntroProg2(META_DATA.PROG_NAME)
        print()
        time.sleep(0.2)
        style.dalam_menu_kalkulasi = False
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        input_url: str = input(
            f"Please input file URL (Google Drive text file only, all extension, {AnsiColors.BOLD}{AnsiColors.BG_WHITE}and public{AnsiColors.RESET}) or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
        ).strip()
        if input_url.lower() == "q":
            Prog_Data.EXIT_W_SAVE = 0
            log_activities(self.log.closing_sub_prog_msg)
            return
    
        style.dalam_menu_kalkulasi = True
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        time.sleep(.2)
        print(f"fetching data from {input_url}")
        time.sleep(0.2)
        print(f"Make sure you have put correct format or it will error")
        print()
        can_download = download_from_gdrive(META_DATA.PROG_NAME, input_url, Prog_Data.true_cloud_in_path)

        if not can_download:
            print(self.log.failed_download)
            log_activities(self.log.failed_download, "ERROR")
            return

        if("for Regression" in META_DATA.PROG_NAME): 
            self.__csv_processing(Prog_Data.true_cloud_in_path)
        else:
            self.__eq_processing(Prog_Data.true_cloud_in_path)
        return

    def _fetch_from_file(self):
        """Input otomatis data regresi atau equation dari file"""
        time.sleep(.2)
        print_text_gradient_angle(META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        time.sleep(0.2)
        PrintIntroProg2(META_DATA.PROG_NAME)
        print()
        time.sleep(0.2)
        print()
        print(f"fetching data from {Prog_Data.true_cloud_in_path}")
        print(f"Make sure you have put correct format or it will error")
        print()
        if("for Regression" in META_DATA.PROG_NAME): 
            self.__csv_processing(Prog_Data.true_cloud_in_path)
        else:
            self.__eq_processing(Prog_Data.true_cloud_in_path)
        return

    def _manually_input_data(self):
        """Input manual data regresi"""
        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "manual input", "", "")
        print_text_gradient_angle(META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        time.sleep(0.2)
        PrintIntroProg2(META_DATA.PROG_NAME)
        print()
        time.sleep(0.2)
        # i want to show the clock
        style.dalam_menu_kalkulasi = False
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        input_user: str = input(
            f"Please input how many data you have, or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
        ).strip()
        if input_user.lower() == "q":
            Prog_Data.EXIT_W_SAVE = 0
            log_activities(self.log.closing_sub_prog_msg)
            return
        
        while not InputValidator.is_numeric(input_user) or int(input_user) < 2:
            if input_user.lower() == "q":
                Prog_Data.EXIT_W_SAVE = 0
                log_activities(self.log.closing_sub_prog_msg)
                return
            
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            input_user = input(
                f"Please input number only (minimal 2 data) or {AnsiColors.BOLD}[q]{AnsiColors.RESET} to exit: "
            )

        Prog_Data.byk_data = int(input_user)
        for i in range(Prog_Data.byk_data):
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            x_val = input(f"X{i+1}: ").strip()
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            y_val = input(f"Y{i+1}: ").strip()
            while not InputValidator.is_numeric(x_val) or not InputValidator.is_numeric(y_val):
                sys.stdout.write("\033[J")
                sys.stdout.write("\n\n\033[2A")
                print(f"{AnsiColors.RED}Please input number only{AnsiColors.RESET}")
                sys.stdout.write("\033[J")
                sys.stdout.write("\n\n\033[2A")
                x_val = input(f"X{i+1}: ").strip()
                sys.stdout.write("\033[J")
                sys.stdout.write("\n\n\033[2A")
                y_val = input(f"Y{i+1}: ").strip()
            Prog_Data.g_xy_dataset.x_data.append(float(x_val))
            Prog_Data.g_xy_dataset.y_data.append(float(y_val))
        # always turn off the clock
        style.dalam_menu_kalkulasi = True
        return
    
    def _manually_input_eq(self):
        """Input manual untuk kasus SPL tanpa data regresi"""

        self.log = Log_Err_Msg(META_DATA.PROG_NAME, "manual input", "", "")
        print_text_gradient_angle(META_DATA.REGRESSION_ART, META_DATA.REGRESSION_COLORS)
        time.sleep(0.2)
        PrintIntroProg2(META_DATA.PROG_NAME)
        print()
        time.sleep(0.2)
        # i want to show the clock
        style.dalam_menu_kalkulasi = False
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()
        pilihan_order = Regression_Gaus_Seidel().__hitung_max_order_valid(Prog_Data.byk_data)
        print()
        for _ in pilihan_order:
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[2A")
            sys.stdout.flush()
            input_user: str = input(
                f"\nInput function coefficients (space separated) or {AnsiColors.BOLD}'q'{AnsiColors.RESET} to exit: "
            ).strip()

            if input_user.lower() == "q":
                Prog_Data.EXIT_W_SAVE = 0
                log_activities(self.log.closing_sub_prog_msg)
                return
            while not InputValidator.is_numeric_coeffs(input_user):
                if input_user.lower() == "q":
                    Prog_Data.EXIT_W_SAVE = 0
                    log_activities(self.log.closing_sub_prog_msg)
                    return
                
                sys.stdout.write("\033[J")
                sys.stdout.write("\n\n\033[2A")
                input_user = input(
                    f"Please input function coefficients (space separated) or {AnsiColors.BOLD}'q'{AnsiColors.RESET} to exit: "
                )
            Prog_Data.g_eq_dataset.equations.append([float(val) for val in input_user.split()])
        
        style.dalam_menu_kalkulasi = True
        sys.stdout.write("\033[J")
        sys.stdout.write("\n\n\033[2A")
        sys.stdout.flush()


# ======================================================================
# This will be file manager function
# ======================================================================
class Manage_Log_File:
    def _open_regression():
        print("Test open regression")

    def _open_linear_eq():
        print("Test open linear")

    def _del_regression():
        print("Test del regression")

    def _del_linear_eq():
        print("Test del linear eq")

    def _merge():
        print("Test merge")


# ======================================================================
# This will be main function
# ======================================================================


def Main_Gauss_Seidel():
    Prog_Data.EXIT_W_SAVE = 1
    print()
    Lazy_Loading("Opening files...")
    # first item in each menu is the header
    main_menu = [
        [
            "Polynomial Regression",
            "Input manual data",  # 0
            "Fetch data from files",  # 1
            "Fetch data from Google Drive",  # 2
        ],
        [
            "Only solving linear Equation",
            "Input manual data",  # 3
            "Fetch data from files",  # 4
            "Fetch data from Google Drive",  # 5
        ],
        [
            "Manage log file",
            "Open polynomial_regression run",  # 6
            "Open linear equation run",  # 7
            "Merge polynomial_regression <- linear equation",  # 8
            f"{AnsiColors.RED}Clear polynomial_regression{AnsiColors.RESET}",  # 9
            f"{AnsiColors.RED}Clear linear equation{AnsiColors.RESET}",  # 10
        ],
        ["this-is-item Quit"],  # 11
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
    total_selectable_items = 0
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
            multiset_draw_menu(
                main_menu,
                curr_select,
                "",
                META_DATA.REGRESSION_ART,
                META_DATA.REGRESSION_COLORS,
            )
        elif key == "down":
            curr_select = (curr_select + 1) % total_selectable_items
            multiset_draw_menu(
                main_menu,
                curr_select,
                "",
                META_DATA.REGRESSION_ART,
                META_DATA.REGRESSION_COLORS,
            )
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
                META_DATA.PROG_NAME += " for Regression"
                Prog_Data.true_cloud_in_path = META_DATA.IN_CLOUD_PATH_REG
                Prog_Data.true_out_path = META_DATA.OUT_PATH_REG
            elif curr_select < 6 and curr_select >= 3:
                META_DATA.PROG_NAME += " for Linear Equation"
                Prog_Data.true_cloud_in_path = META_DATA.IN_CLOUD_PATH_SPL
                Prog_Data.true_out_path = META_DATA.OUT_PATH_SPL

            io = Program_IO()
            reg = Regression_Gaus_Seidel()
            spl = Gauss_Seidel_Iterate()

            match curr_select:
                case 0:
                    io._manually_input_data()
                    reg.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "manual input", "", "")
                    log_activities(log.run_program_msg)


                case 1:
                    io._fetch_from_file()
                    reg.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "fetch from file", "", "")
                    log_activities(log.run_program_msg)


                case 2:
                    io._fetch_from_gdrive()
                    reg.main()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME, "fetch from google drive", "", ""
                    )
                    log_activities(log.run_program_msg)


                case 3:
                    io._manually_input_eq()
                    spl.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "manual input", "", "")
                    log_activities(log.run_program_msg)


                case 4:
                    io._fetch_from_file()
                    spl.main()
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "fetch from file", "", "")
                    log_activities(log.run_program_msg)


                case 5:
                    io._fetch_from_gdrive()
                    spl.main()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME, "fetch from google drive", "", ""
                    )
                    log_activities(log.run_program_msg)


                case 6:
                    Manage_Log_File._open_regression()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME, "Manage Log File", "opening regression", ""
                    )
                    log_activities(log.run_program_msg)


                case 7:
                    Manage_Log_File._open_linear_eq()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME,
                        "Manage Log File",
                        "opening linear equation",
                        "",
                    )
                    log_activities(log.run_program_msg)


                case 8:
                    Manage_Log_File._merge()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME, "Manage Log File", "merging log file", ""
                    )
                    log_activities(log.run_program_msg)
                    Prog_Data.EXIT_W_SAVE = 0


                case 9:
                    Manage_Log_File._del_regression()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME,
                        "Manage Log File",
                        "clearing regression log file",
                        "",
                    )
                    log_activities(log.run_program_msg)
                    Prog_Data.EXIT_W_SAVE = 0


                case 10:
                    Manage_Log_File._del_linear_eq()
                    log = Log_Err_Msg(
                        META_DATA.PROG_NAME,
                        "Manage Log File",
                        "clearing linear equation log file",
                        "",
                    )
                    log_activities(log.run_program_msg)
                    Prog_Data.EXIT_W_SAVE = 0


                case last_idx:
                    style.stop_jam.set()
                    clear_screen()
                    print(f"\n Keluar dari program {META_DATA.PROG_NAME}")
                    log = Log_Err_Msg(META_DATA.PROG_NAME, "", "", "")
                    log_activities(log.closing_main_prog_msg)
                    Prog_Data.EXIT_W_SAVE = 0
                    break



            print("")
            style.dalam_menu_kalkulasi = False
            if Prog_Data.EXIT_W_SAVE == 0:
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
                log_activities(f"Closing program {META_DATA.PROG_NAME}...")
                break
            elif pilihan == "s":
                clear_screen()
                write_result(menu, Prog_Data.true_out_path, META_DATA.PROG_NAME)

            style.dalam_menu_kalkulasi = False
            clear_screen()
            multiset_draw_menu(
                main_menu,
                curr_select,
                "",
                META_DATA.REGRESSION_ART,
                META_DATA.REGRESSION_COLORS,
                awal_jalan=True,
                additional_header=META_DATA.ADDITIONAL_HEADER,
            )
    return


if __name__ == "__main__":
    Main_Gauss_Seidel()
