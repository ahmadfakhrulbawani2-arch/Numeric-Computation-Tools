import time
from halo import Halo
from typing import List
import math
import os
import sys
import io

EPSILON: float = 1e-12


# replacing print(f"")
def printf(format_string: str) -> None:
    # 1. Ambil scope (namespace) dari tempat fungsi printf() ini dipanggil
    frame = sys._getframe(1)
    local_vars = frame.f_locals
    global_vars = frame.f_globals

    # 2. Lakukan formatting manual menggunakan namespace tersebut
    # .format_map otomatis mencocokkan teks di dalam {} dengan nama variabel yang ada
    try:
        # Gabungkan global dan local vars (local override global jika namanya sama)
        context = {**global_vars, **local_vars}
        print(format_string.format_map(context), end="\n")
    except KeyError as e:
        # Antisipasi kalau kamu nulis {variabel} tapi variabelnya belum di-define
        print(f"\n[Printf Error]: Variabel {e} belum di-define!\n")


def DerivativeF(coeffs: List[float]) -> List[float]:
    return [coeffs[i] * i for i in range(1, len(coeffs))]


# reverse the coeffs first
def CalcFunc(coeffs: List[float], x: float) -> float:
    return sum(coeffs[i] * (x**i) for i in range(len(coeffs)))


def Calc_Converngence_Rate(err: List[float]) -> float | None:
    if len(err) < 3:
        return None

    e_n1 = max(err[-1], EPSILON)
    e_n = max(err[-2], EPSILON)
    e_n_1 = max(err[-3], EPSILON)

    denumerator = math.log(e_n / e_n_1)

    if denumerator == 0:
        return None

    return math.log(e_n1 / e_n) / denumerator


def CalcTrueError(real_root: float, approx_root: float) -> float:
    if abs(real_root) < EPSILON:
        return abs(approx_root)

    return abs((real_root - approx_root) / real_root)


# just for styling
def Lazy_Loading(texts: str, duration=1.5) -> None:
    # os.system('cls' if os.name == 'nt' else 'clear')
    spinner = Halo(text=texts, color="cyan", spinner="dots")
    # Mulai muter
    spinner.start()
    # Simulasi proses matematika/loading (misal 3 detik)
    time.sleep(duration)
    # Selesai dengan status sukses (Centang Hijau)
    spinner.succeed("Ok done...")
    time.sleep(0.5)
    # os.system('cls' if os.name == 'nt' else 'clear')


# this is true loading animation
class TrueLoader:
    def __init__(self, color="cyan", spinner="dots"):
        self.color = color
        self.spinner_type = spinner
        self.spinner = None

    def start(self, text: str) -> None:
        if self.spinner is None:
            self.spinner = Halo(text=text, color=self.color, spinner=self.spinner_type)
            self.spinner.start()
        else:
            self.spinner.text = text
            self.spinner.start()

    def stop(self, success_text: str = "Ok done...") -> None:
        if self.spinner:
            self.spinner.succeed(success_text)
            time.sleep(0.5)


# input validator thanks Gemini
import re


class InputValidator:
    @staticmethod
    def is_numeric(teks: str) -> bool:
        """Hanya menerima angka saja (0-9), tidak boleh ada huruf atau simbol."""
        return bool(re.match(r"^\d+$", teks))

    @staticmethod
    def is_alpha(teks: str) -> bool:
        """Hanya menerima huruf saja (a-z, A-Z), tidak boleh ada angka atau simbol."""
        return bool(re.match(r"^[a-zA-Z]+$", teks))

    @staticmethod
    def is_alphanumeric(teks: str) -> bool:
        """Hanya menerima kombinasi huruf dan angka, tidak boleh ada simbol/spasi."""
        return bool(re.match(r"^[a-zA-Z0-9]+$", teks))

    @staticmethod
    def is_valid_variable(teks: str) -> bool:
        """
        Syarat: Diawali oleh huruf, sisanya boleh huruf atau angka.
        Tidak boleh diawali angka dan tidak boleh ada karakter aneh/spasi.
        """
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", teks))

    @staticmethod
    def is_clean_text(teks: str) -> bool:
        """Menerima huruf, angka, dan spasi (cocok buat input nama/kalimat tanpa simbol aneh)."""
        return bool(re.match(r"^[a-zA-Z0-9\s]+$", teks))


# calculating using Operasi Baris Elementer
from typing import List


def iterateGaussJordan(
    matrix: List[List[float]], prog_name: str, var_symbol: str
) -> List[List[float]]:
    from .IoUtils import Print_2d_obe_Matrix, g_buffer
    swap = 0  # hitung berapa kali tukar baris
    row = len(matrix)
    col = len(matrix[0])
    M = [r[:] for r in matrix]  # copy matrix ke M agar data awal aman
    step = 1
    TOLERANCE = 1e-12  # Batas toleransi presisi komputer untuk angka 0

    # ========================================================
    # TAHAP 1: ELIMINASI MAJU & NORMALISASI 1 UTAMA
    # ========================================================
    for j in range(row):
        pivot = M[j][j]

        # Jika pivot mendekati nol, cari baris di bawahnya untuk ditukar
        if abs(pivot) < TOLERANCE:
            found_new_pivot = False
            for i in range(j + 1, row):
                if abs(M[i][j]) > TOLERANCE:
                    print(
                        f"Iterasi ke-{step}: Tukar baris ke-{j+1} dengan baris ke-{i+1} (Pivot awal bernilai 0)"
                    )
                    g_buffer.writelines(f"Iterasi ke-{step}: Tukar baris ke-{j+1} dengan baris ke-{i+1} (Pivot awal bernilai 0)")
                    M[j], M[i] = M[i], M[j]  # menukar baris
                    Print_2d_obe_Matrix(M, prog_name, var_symbol)
                    print()
                    step += 1
                    swap += 1
                    pivot = M[j][j]
                    found_new_pivot = True
                    break

            # --- ERROR HANDLING CRITICAL 1 ---
            # Jika setelah di-loop ke bawah tetap tidak ada angka != 0,
            # artinya SPL ini singular (tidak punya solusi unik / solusi tak hingga)
            if not found_new_pivot:
                error_msg = f"Matriks Singular terdeteksi di kolom {j+1}. Pivot bernilai 0 dan tidak ada baris pembanding."
                print(f"\n[ERROR] {error_msg}")
                # log_activities(f"Gauss-Jordan Failed: {error_msg} in {prog_name}", "ERROR")
                raise ValueError(error_msg)

        # --- ERROR HANDLING CRITICAL 2 ---
        # Double check untuk mengamankan proses pembagian berikutnya
        if abs(pivot) < TOLERANCE:
            error_msg = (
                f"Pembagian dengan nol terdeteksi pada elemen diagonal M[{j}][{j}]."
            )
            print(f"\n[ERROR] {error_msg}")
            raise ZeroDivisionError(error_msg)

        # Normalisasi pivot menjadi 1 utama
        # Kita pakai abs(pivot - 1.0) > TOLERANCE karena float tidak bisa di-compare langsung keras '!='
        if abs(pivot - 1.0) > TOLERANCE:
            print(f"Iterasi ke-{step}: Normalisasi baris ke-{j+1} / ({pivot:.2f})")
            g_buffer.writelines(f"Iterasi ke-{step}: Normalisasi baris ke-{j+1} / ({pivot:.2f})")
            print()
            g_buffer.writelines(" ")
            # Ambil nilai pivot asli sebelum diubah di dalam loop kolom
            current_pivot = pivot
            for c in range(col):
                M[j][c] /= current_pivot
            Print_2d_obe_Matrix(M, prog_name, var_symbol)
            print()
            step += 1

        # Eliminasi ke semua baris di bawahnya
        for r in range(j + 1, row):
            if r == j or abs(M[r][j]) < TOLERANCE:
                continue

            pengali = M[r][j]
            print(
                f"Iterasi ke-{step}: Baris ke-{r+1} - ({pengali:.2f}) * Baris ke-{j+1}"
            )
            g_buffer.writelines(f"Iterasi ke-{step}: Baris ke-{r+1} - ({pengali:.2f}) * Baris ke-{j+1}")
            print()
            g_buffer.writelines(" ")
            for c in range(col):
                M[r][c] -= pengali * M[j][c]

            Print_2d_obe_Matrix(M, prog_name, var_symbol)
            print()
            step += 1

    # ========================================================
    # TAHAP 2: ELIMINASI MUNDUR (MENGNOLKAN BAGIAN ATAS DIAGONAL)
    # ========================================================
    for j in range(row - 1, -1, -1):
        pivot = M[j][j]

        # --- ERROR HANDLING CRITICAL 3 ---
        # Memastikan saat proses mundur, 1 utama tidak rusak atau malah bernilai 0
        if abs(pivot) < TOLERANCE:
            error_msg = (
                f"Matriks rusak di tahap substitusi mundur pada diagonal [{j}][{j}]."
            )
            print(f"\n[ERROR] {error_msg}")
            raise ValueError(error_msg)

        for r in range(j - 1, -1, -1):
            if r == j or abs(M[r][j]) < TOLERANCE:
                continue

            pengali = M[r][j]
            print(
                f"Iterasi ke-{step}: Baris ke-{r+1} - ({pengali:.2f}) * Baris ke-{j+1}"
            )
            g_buffer.writelines(f"Iterasi ke-{step}: Baris ke-{r+1} - ({pengali:.2f}) * Baris ke-{j+1}")
            print(" ")
            g_buffer.writelines(" ")
            for c in range(col):
                M[r][c] -= pengali * M[j][c]

            Print_2d_obe_Matrix(M, prog_name, var_symbol)
            print()
            step += 1

    print("Matrix diagonal akhir:")
    g_buffer.writelines("Matrix diagonal akhir:")
    print()
    g_buffer.writelines(" ")
    Print_2d_obe_Matrix(M, prog_name, var_symbol)
    print()
    g_buffer.writelines(" ")
    return M
