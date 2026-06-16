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

    PROG_NAME = "Gauss-Seidel Linear Equation"
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


# ======================================================================
# CAUTION: SET MAX ORDER SO IT IS NOT EXCEED TIME LIMIT
# ======================================================================
MAX_ORDO = 10

# ======================================================================
# This will be polynomial regression using gauss-seidel
# ======================================================================
class Regression_Gaus_Seidel:
    def __init__(self):
        pass
    

# ======================================================================
# This will be only gauss-seidel from the equation
# ======================================================================

class Gauss_Seidel_Iterate:
    def __init__(self):
        pass

# ======================================================================
# This will be fetch from drive, file, and manual
# ======================================================================

class Program_IO:
    def fetch_from_gdrive():
        pass

    def fetch_from_file():
        pass

    def manually_input():
        pass

# ======================================================================
# This will be main function
# ======================================================================

def Main_Gauss_Seidel():
    pass

if __name__ == "__main__":
    Main_Gauss_Seidel()
