from typing import List
import datetime
import re
import requests
from src.utils.FuncUtils import *
from src.utils.Style import print_text_gradient_angle, AnsiColors
from .Logger import log_activities
import os
from pathlib import *
import sys
import io

# class
# loader = TrueLoader()


# this is to get time.now
def GetTimeNow() -> str:
    return datetime.now().strftime("%H:%M:%S | %d-%m-%Y")


# this print intro statement
def PrintIntroProg(ascii: str = "", title: str = "Komnum26") -> None:
    print(ascii)
    print(
        f"Welcome to {title}. Please input the equation (only support up to x^0, dosen't support x^-1, etc...)"
    )

# this print intro style 2
def PrintIntroProg2(title: str = "Komnum26"):
    print(f"Welcome to {title}")
    print()


# This return equation string
def GetEqState(eq: List[int]) -> str:
    new_eq: List[int] = list(reversed(eq))
    sEq: str = ""

    # reverse the loop to reverse the printed eq
    for i in range(len(new_eq) - 1, -1, -1):
        if new_eq[i]:
            if i > 1:
                sEq += f"({new_eq[i]})X^{i} + "
            elif i == 1:
                sEq += f"({new_eq[i]})X + "
            else:
                sEq += f"({new_eq[i]}) + "

    return "f(x) = " + sEq.rstrip(" + ")


# the eq must be reversed first
def PrintSingleEq(eq: List[int]) -> None:
    eqStr: str = GetEqState(eq)
    print(f"The Equation is: {eqStr}")


# this print iteration step
def PrintIterations(iter: int, vars: List[str], *params) -> None:
    evals: List[str] = [f"{label} = {value}" for label, value in zip(vars, params)]

    evals_str: str = ",    ".join(evals)
    log: str = f"[{GetTimeNow()}] Iteration-{iter}: {evals_str}"
    print(log)


# download input.txt from cloud
def download_from_gdrive(
    PROG_NAME: str, url: str, output_path: str = "../input/input.txt"
) -> bool:
    """
    Mengunduh file dari Google Drive menggunakan Link Share biasa
    atau langsung menggunakan File ID. Mendukung format .txt, .csv, dll.
    """
    loader = TrueLoader() # pindah untuk menangani name konflik
    # RegEx untuk mengekstrak File ID jika user memasukkan URL penuh
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    file_id = match.group(1) if match else url

    # FIX: Gunakan URL export/download resmi dari Google Drive API
    # Jika file berukuran sangat besar (>100MB), perlu penanganan token virus (bisa dibahas nanti kalau butuh)
    direct_download_url = f"https://docs.google.com/uc?export=download&id={file_id}"

    loader.start(f"[Cloud] Downloading file from GDrive (ID: {file_id})...")
    log_activities(
        f"[Cloud] Downloading file from GDrive (ID: {file_id}) in {PROG_NAME}"
    )
    try:
        response = requests.get(direct_download_url, stream=True)
        response.raise_for_status()

        # Simpan file ke direktori lokal (aman untuk .txt, .csv, biner, dll karena "wb")
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        loader.stop(f"[Cloud] File successfully downloaded and saved to: {output_path}")
        log_activities(
            f"[Cloud] File successfully downloaded and saved to: {output_path} in {PROG_NAME}"
        )
        return True
    except Exception as e:
        print(f"[Error] Failed to download file: {e}")
        loader.stop("Download aborted ❌")
        log_activities(f"[Error] Failed to download file: {e} in {PROG_NAME}")
        return False


# Setup pembaca input keyboard cross-platform
if os.name == "nt":
    import msvcrt

    def get_key():
        """Membaca input tombol di Windows"""
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):  # Tombol fungsi atau arrow keys
            ch = msvcrt.getch()
            if ch == b"H":
                return "up"
            if ch == b"P":
                return "down"
        if ch == b"\r":
            return "enter"
        try:
            return ch.decode("utf-8").lower()
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
            if ch == "\x1b":  # Escape sequence untuk arrow keys
                ch2 = sys.stdin.read(2)
                if ch2 == "[A":
                    return "up"
                if ch2 == "[B":
                    return "down"
            if ch == "\r" or ch == "\n":
                return "enter"
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw_menu(
    menu_items: List[str],
    selected_index: int,
    STATS: str,
    ASCII_HEADER: str,
    header_colors: List[str],
    awal_jalan=False,
    additional_header="",
) -> None:
    if awal_jalan:
        clear_screen()
        print(STATS)
        print_text_gradient_angle(ASCII_HEADER, header_colors, 0)
        print(
            f"\n Gunakan [↑/↓] Panah untuk Navigasi, {AnsiColors.BOLD}[Enter]{AnsiColors.RESET} untuk Memilih, {AnsiColors.BOLD}[Q]{AnsiColors.RESET} untuk Keluar\n"
        )
        sys.stdout.write(additional_header)
        print("─" * 108)
    else:
        # Mengembalikan kursor naik ke atas agar menu tertimpa dengan halus tanpa reload global
        sys.stdout.write(f"\033[{len(menu_items) + 1}A")
        sys.stdout.flush()
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(f"\033[K \033[92m{AnsiColors.BOLD}►   {item}\033[0m")
        else:
            print(f"\033[K \033[90m    {item}\033[0m")
    print("\033[K" + "─" * 108)


def get_project_root() -> Path:
    # Ambil PWD / CWD saat ini
    current_dir = Path.cwd()

    # Lakukan looping naik ke atas (traverse up)
    for path in [current_dir] + list(current_dir.parents):
        # Cek apakah folder ini berisi penanda root project
        if (path / ".git").exists() or (path / "src").exists():
            return path

    # Jika tidak ketemu penanda, kembalikan CWD sebagai fallback
    return current_dir


# WARNING, this does not support dir creation
root_dir = get_project_root()

# writing result
def write_result(menu: str, buffer: io.StringIO, path: str, PROG_NAME: str):
    OUT_PATH = root_dir / "out" / path
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
            print()
            print(
                f"\nFile saved successfully in {AnsiColors.BG_BLACK}{AnsiColors.BOLD}{OUT_PATH}{AnsiColors.RESET}\n"
            )
            print("Going back to menu in 5 seconds...")
            print()
            time.sleep(5)
    except FileNotFoundError:
        log_activities(f"File not found in {PROG_NAME}. Failed to write", "ERROR")
        raise FileNotFoundError(f"File/Path not found")

# opening file output
def open_output(out_path: str, PROG_NAME: str):
    true_path = root_dir / "out" / out_path
    print(f"=== Output file of {PROG_NAME} ===")
    print()
    success_run_cnt = 0
    Lazy_Loading(f"Opening {PROG_NAME} logs...", duration=0.15)
    try:
        with open(file=true_path, mode="r", encoding="utf-8") as file:
            for line in file:
                if line.find("Calculation by") != -1:
                    success_run_cnt += 1
                print(line.strip())
                time.sleep(0.0025)
            print("=== TL;DR: ===")
            print(f"Success run count = {success_run_cnt}")
    except FileNotFoundError:
        log_activities(f"File not found in {PROG_NAME}. Failed to write", "ERROR")
        raise FileNotFoundError(f"File/Path not found")

# print matrix 2d obe with same variable like a0, a1, a2, ...
def Print_2d_obe_Matrix(matrix: List[List[int]], prog_name: str, variable: str) -> None:
    print(f"\n === Matrix {prog_name} ===")
    for row in matrix:
        left_part = ", ".join(f"{val:.2f}{variable}{i}" for i, val in enumerate(row[:-1]))
        right_part = f"{row[-1]:.2f}"
        print(f"    [ {left_part} | {right_part} ]")
        time.sleep(.2)