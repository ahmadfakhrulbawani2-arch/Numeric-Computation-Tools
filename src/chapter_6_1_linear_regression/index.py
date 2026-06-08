from src.utils import *
import src.utils.Style as style
import csv
import sys
import io
import datetime

# MACRO VARIABLES
IO_DIR = "linear_regression"
IN_PATH = f"./input/{IO_DIR}/table.csv"
IN_CLOUD_PATH = f"./input/{IO_DIR}/cloud_table.csv"
OUT_PATH = f"./out/{IO_DIR}/result.txt"

PROG_NAME = "Linear Regression"
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
     ____                              _
    |  _ \ ___  __ _ _ __ ___  ___ ___(_) ___  _ __  
    | |_) / _ \/ _` | '__/ _ \/ __/ __| |/ _ \| '_ \ 
    |  _ <  __/ (_| | | |  __/\__ \__ \ | (_) | | | |
    |_| \_\___|\__, |_|  \___||___/___/_|\___/|_| |_|
               |___/                                 


"""

ADDITIONAL_HEADER = f"\
    Input directory: /input/linear_regression\n\
    File output: {OUT_PATH}\n"

buffer = io.StringIO()

class Csv_Data:
    x_data = []
    y_data = []

class Reg_Data:
    # constructor
    def __init__(self, datas: Csv_Data):
        len_x = len(datas.x_data)
        len_y = len(datas.y_data)
        if len_x <= 0 or len_y <= 0 or len_x != len_y:
            print("Error, caught no data")
            log_activities("Caught no data in ", "ERROR")
        data_x = datas.x_data 
        data_y = datas.y_data 
        
        self.data_amount = max(len(data_x), len(data_y))
        self.sum_x = sum(data_x)
        self.sum_y = sum(data_y)
        self.sum_xy = 0
        self.sum_x2 = 0
        try:
            self.avg_x = self.sum_x / self.data_amount
            self.avg_y = self.sum_y / self.data_amount
        except ZeroDivisionError:
            print("Error, caught division by zero")
            log_activities("Division by zero error", "ERROR")
            return

        for x, y in zip(data_x, data_y):
            self.sum_xy += (x * y)
            self.sum_x2 += (x ** 2)

    def _calc_a1(self) -> float | None:
        numerator = (self.data_amount * self.sum_xy) - (self.sum_x * self.sum_xy)
        denumerator = (self.data_amount * self.sum_x2) - (self.sum_x ** 2)
        result = 0.0
        try:
            result = numerator / denumerator
            return result
        except ZeroDivisionError:
            print("Error, caught division by zero")
            log_activities("Division by zero error", "ERROR")
            return None
    
    def _show_data(self):
        print(f"Sum X = {self.sum_x}")
        buffer.write(f"Sum X = {self.sum_x}\n")
        time.sleep(.2)
        print(f"Sum Y = {self.sum_y}")
        buffer.write(f"Sum Y = {self.sum_y}\m")
        time.sleep(.2)
        print(f"Sum X*Y = {self.sum_xy}")
        buffer.write(f"Sum X*Y = {self.sum_xy}\n")
        time.sleep(.2)
        print(f"Sum X^2 = {self.sum_x2}")
        buffer.write(f"Sum X^2 = {self.sum_x2}\n")
        time.sleep(.2)
        print(f"Average X = {self.avg_x}")
        buffer.write(f"Average X = {self.avg_x}\n")
        time.sleep(.2)
        print(f"Average Y = {self.avg_y}")
        buffer.write(f"Average Y = {self.avg_y}\n")
        time.sleep(.2)
        print(f"Banyak data = {self.data_amount}")
        buffer.write(f"Banyak data = {self.data_amount}\n")
        time.sleep(.2)

    def _calc_expr(self):
        a1 = self._calc_a1()
        print(f"Calculated a1 = {a1:.6f}")
        buffer.write(f"Calculated a1 = {a1:.6f}\n")
        time.sleep(.2)
        a0 = self.avg_y - (a1 * self.avg_x)
        print(f"Calculated a1 = {a1:.6f}")
        buffer.write(f"Calculated a1 = {a1:.6f}\n")
        time.sleep(.2)
        sys.stdout.write("Final Linear Regression result: \n\n")
        buffer.write("Final Linear Regression result: \n\n")
        time.sleep(.2)
        print(f"y = {a1:.6f}x + {a0:.6f}")
        buffer.write(f"y = {a1:.6f}x + {a0:.6f}\n")

def write_result(menu):
    try:
        with open(file=OUT_PATH, mode="a", encoding="utf-8") as file:
            sekarang = datetime.datetime.now()
            str_now = sekarang.strftime("%A, %d-%m-%Y | %H:%M:%S WIB")
            file.write(f"{str_now}\n")
            file.write(f"\nCalculation by {menu}\n")
            file.write(buffer.getvalue())
            sys.stdout.write("\033[J")
            sys.stdout.write("\n\n\033[4A")
            sys.stdout.flush()
            print(f"File saved successfully in {AnsiColors.BG_BLACK}{AnsiColors.BOLD}{OUT_PATH}{AnsiColors.RESET}")
            print("Going back to menu in 5 seconds...")
            print()
            time.sleep(5)
    except FileNotFoundError:
        log_activities(f"File not found in {PROG_NAME}. Failed to write", "ERROR")
        raise FileNotFoundError(f"File/Path not found")
    

def csv_processing(PATH):
    raw_data = Csv_Data()

    try:
        with open(file=PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            header = [h.strip().lower() for h in header]

            try:
                x_idx = header.index('x')
                y_idx = header.index('y')
            except ValueError:
                log_activities(f"Error: CSV file must have 'x' and 'y' column (case insensitive) in {PROG_NAME}", "ERROR")
                raise ValueError("CSV file must have 'x' and 'y' column (case insensitive)")
            
            for row in reader:
                if not row:
                    continue
                try:
                    raw_data.x_data.append(float(row[x_idx]))
                    raw_data.y_data.append(float(row[y_idx]))
                except ValueError:
                    print(f"Skipping improper row-{row}")
        Lazy_Loading(f"Scanning {PATH}", .2)
        print()
        time.sleep(.2)
        print("=== Data fetched successfully ===")
        time.sleep(.2)
        print()
        print(f"X = {raw_data.x_data}")
        time.sleep(.2)
        print(f"Y = {raw_data.y_data}")
        print()
        time.sleep(.2)
        Lazy_Loading("Calculating sum X-Y, avg X-Y, sum XY, sum X^2...", 0.5)
        print()
        the_data = Reg_Data(raw_data)
        print()
        print("=== Data calculated successfully ===")
        print()
        the_data._show_data()
        print()
        Lazy_Loading("Calculating a1...", 0.1)
        Lazy_Loading("Calculating final expression...", 0.1)
        print()
        the_data._calc_expr()
        print()
        sys.stdout.write("\n\n\033[4A")
        sys.stdout.flush()
        time.sleep(.1)
        style.dalam_menu_kalkulasi = False
        
    except FileNotFoundError:
        log_activities(f"File not found in {PROG_NAME}.", "ERROR")
        raise FileNotFoundError(f"File/Path not found")

    return

def input_manual():
    return


def fetch_data_from_files():
    time.sleep(.2)
    print_text_gradient_angle(REGRESSION_ART, REGRESSION_COLORS)
    time.sleep(.2)
    PrintIntroProg2(PROG_NAME)
    time.sleep(.2)
    print()
    print(f"fetching data from {IN_PATH}")
    print(f"Make sure you have put correct format or it will error")
    print()
    csv_processing(IN_PATH)
    return


def fetch_from_drive():
    print_text_gradient_angle(REGRESSION_ART, REGRESSION_COLORS)
    time.sleep(.2)
    PrintIntroProg2(PROG_NAME)
    print()
    time.sleep(.2)
    inputUrl: str = input(f"Silahkan input URL file (Google Drive text file only, all extension, {AnsiColors.BOLD}{AnsiColors.BG_WHITE} and public{AnsiColors.RESET}): ").strip()
    time.sleep(.2)
    print(f"fetching data from {inputUrl}")
    time.sleep(.2)
    print(f"Make sure you have put correct format or it will error")
    print()
    canDownload = download_from_gdrive(PROG_NAME, inputUrl, IN_CLOUD_PATH)

    if not canDownload:
        print("Sorry, we can't download/write your spesific URL path")
        log_activities(f"Can't download file from {PROG_NAME}")
        return 
    
    csv_processing(IN_CLOUD_PATH)
    return


def linear_regression():
    Lazy_Loading("Opening files...")
    main_menu = [
        "Input manual data",
        "Fetch data from files",
        "Fetch data from Google Drive",
        "Quit",
    ]

    curr_select = 0

    style.Clock_Widget()
    draw_menu(
        main_menu, curr_select, "", REGRESSION_ART, REGRESSION_COLORS, awal_jalan=True, additional_header=ADDITIONAL_HEADER
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
                    log_activities("Running Numeric Regression with manual input")
                    menu = "manual input"
                case 1:
                    fetch_data_from_files()
                    log_activities(
                        "Running Numeric Regression with fetching input file"
                    )
                    menu = "input file"
                case 2:
                    fetch_from_drive()
                    log_activities(
                        "Running Numeric Regression with fetching Google Drive file"
                    )
                    menu = "cloud file"
                case last_idx:
                    stop_jam.set()
                    clear_screen()
                    print(f"\n Keluar dari program {PROG_NAME}")
                    log_activities(f"Closing program {PROG_NAME}...")
                    break

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
                stop_jam.set()
                clear_screen()
                print("\nKeluar dari program. Sampai jumpa, Bre!")
                log_activities(f"Closing program {PROG_NAME}...")
                break
            elif pilihan == 's':
                write_result(menu)

            style.dalam_menu_kalkulasi = False
            draw_menu(
                main_menu,
                curr_select,
                "",
                REGRESSION_ART,
                REGRESSION_COLORS,
                awal_jalan=True,
                additional_header=ADDITIONAL_HEADER
            )

if __name__ == "__main__":
    linear_regression()
