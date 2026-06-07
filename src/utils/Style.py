from rich.console import Console
from rich.text import Text
import math
import os
import sys
import threading
import datetime
import time

# --- Rich Gradient Color ---


class AnsiColors:
    """ANSI color codes"""

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    RESET = "\033[0m"
    # Standard Backgrounds
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # High Intensity (Bright) Backgrounds
    BG_LIGHT_BLACK = "\033[100m"
    BG_LIGHT_RED = "\033[101m"
    BG_LIGHT_GREEN = "\033[102m"
    BG_LIGHT_YELLOW = "\033[103m"
    BG_LIGHT_BLUE = "\033[104m"
    BG_LIGHT_PURPLE = "\033[105m"
    BG_LIGHT_CYAN = "\033[106m"
    BG_LIGHT_WHITE = "\033[107m"


def text_gradient_angle(teks, list_warna, sudut_derajat=45):
    objek_teks = Text()
    jumlah_warna = len(list_warna)

    if jumlah_warna < 2:
        raise ValueError("List warna minimal harus berisi 2 warna!")

    # Ubah derajat ke radian untuk operasi sin/cos
    radian = math.radians(sudut_derajat)
    cos_f = math.cos(radian)
    sin_f = math.sin(radian)

    # Pecah teks berdasarkan baris untuk tahu koordinat Y
    baris_list = teks.splitlines()
    total_baris = len(baris_list)

    for y, baris in enumerate(baris_list):
        total_kolom = len(baris)

        for x, karakter in enumerate(baris):
            # Normalisasi koordinat X dan Y ke rentang 0 sampai 1
            nx = x / (total_kolom - 1) if total_kolom > 1 else 0
            ny = y / (total_baris - 1) if total_baris > 1 else 0

            # Hitung proyeksi posisi berdasarkan sudut
            posisi_global = nx * cos_f + ny * sin_f

            # Batasi hasil proyeksi agar tetap di rentang 0.0 - 1.0
            posisi_global = max(
                0.0,
                min(
                    1.0,
                    (
                        (posisi_global + 1) / 2
                        if sudut_derajat != 0 and sudut_derajat != 90
                        else posisi_global
                    ),
                ),
            )
            if sudut_derajat == 45:
                # Tuning khusus sudut 45 derajat agar sebarannya pas di tengah
                posisi_global = (nx + ny) / 2

            # Cari segmen warna
            posisi_segmen = posisi_global * (jumlah_warna - 1)
            indeks_warna = int(posisi_segmen)
            indeks_berikutnya = min(indeks_warna + 1, jumlah_warna - 1)
            rasio_lokal = posisi_segmen - indeks_warna

            w_awal = list_warna[indeks_warna]
            w_akhir = list_warna[indeks_berikutnya]

            r = int(w_awal[0] + (w_akhir[0] - w_awal[0]) * rasio_lokal)
            g = int(w_awal[1] + (w_akhir[1] - w_awal[1]) * rasio_lokal)
            b = int(w_awal[2] + (w_akhir[2] - w_awal[2]) * rasio_lokal)

            objek_teks.append(karakter, style=f"rgb({r},{g},{b})")

        # Tambahkan kembali enter di setiap akhir baris, kecuali baris terakhir
        if y < total_baris - 1:
            objek_teks.append("\n")

    return objek_teks


console = Console()


def print_text_gradient_angle(texts, colors, angle=45):
    header_berwarna = text_gradient_angle(texts, colors, angle)
    console.print(header_berwarna)


# --- Clock Widget ---
# Variabel kontrol global untuk thread jam
stdout_lock = threading.Lock()
dalam_menu_kalkulasi = False
stop_jam = threading.Event()


def update_jam_realtime(stop_event):
    while not stop_event.is_set():
        if not dalam_menu_kalkulasi:
            with stdout_lock:
                sekarang = datetime.datetime.now()
                waktu_skrg = sekarang.strftime("%A, %d-%m-%Y | %H:%M:%S WIB")
                jam = sekarang.hour

                if 5 <= jam < 12:
                    greet = "Good Morning 🌄"
                    color_code = AnsiColors.BG_YELLOW
                elif 12 <= jam < 17:
                    greet = "Good Afternoon 🏙️"
                    color_code = AnsiColors.BG_LIGHT_BLUE
                elif 17 <= jam < 19:
                    greet = "Good Evening 🌆"
                    color_code = AnsiColors.BG_LIGHT_PURPLE
                else:
                    greet = "Good Night 🌃"
                    color_code = AnsiColors.BG_PURPLE

                jam_str = f"{color_code}[ {greet} | {waktu_skrg} ]{AnsiColors.RESET}"

                # Tulis jam di baris baru, lalu naikan kursor kembali 1 baris ke atas
                # \033[2K = hapus seluruh baris saat ini (bersihkan jam lama)
                # \033[1A = naikan kursor 1 baris ke atas (kembali ke baris prompt)
                sys.stdout.write(
                    f"\033[s"  # 1. simpan posisi kursor (posisi user sedang ngetik)
                    f"\033[1B\r\033[2K"  # 2. turun 1 baris, ke kolom 0, hapus baris itu
                    f"{jam_str}"  # 3. tulis jam
                    f"\033[u"  # 4. kembalikan kursor ke posisi user tadi
                )
                sys.stdout.flush()
        time.sleep(1)


def Clock_Widget():
    thread_jam = threading.Thread(target=update_jam_realtime, args=(stop_jam,))
    thread_jam.daemon = True
    thread_jam.start()
