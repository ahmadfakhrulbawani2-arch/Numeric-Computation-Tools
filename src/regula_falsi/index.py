from typing import List
from src.utils.FuncUtils import *
from src.utils.IoUtils import *
from src.utils.Logger import *

MAX_ITERATION_CNT = 100
TOLERANCE = 1e-6


# increment search for minimizing interval. Always reverse the eq fisrt
def increment_search(eq: List[int], a: float, b: float) -> float | None:
    # open normalize.csv
    csv_file = open("./out/regula-falsi/normalize.csv", "w")
    csv_file.write("iter,new_b,new_f(b)\n")

    x: float = a
    fx_prev: float = CalcFunc(eq, a)
    step: float = 0.1
    newB: float | None = None
    iter: int = 1
    while x <= b:
        x += step
        fx_curr = CalcFunc(eq, x)
        PrintIterations(iter, ("new_b", "new_f(b)"), x, fx_curr)
        csv_file.write(f"{iter},{x},{fx_curr}\n")

        eval: float = fx_curr * fx_prev
        if eval < 0:
            newB = x
            print(f"\nf(a) * f(b) = {eval} < 0, new value of b/xHighest is = {newB}")
            break

        fx_prev = fx_curr
        iter += 1

    csv_file.close()
    return newB


# return the root
def regula_falsi(eq: List[int], xLowest: float, xHighest: float) -> float | None:
    # open csv file
    csv_file = open("./out/regula-falsi/regula_falsi.csv", "w")
    csv_file.write("iter,a,b,xr,f_xr\n")

    rEq: List[int] = list(reversed(eq))
    # find the upper bound (b or xHighest) that make f(a) * f(b) < 0 (a is xLowest)
    print(f"Minimizing interval [{xLowest}, {xHighest}]\n")
    xHighest = increment_search(rEq, xLowest, xHighest)
    print()

    # return none if can't find the root
    if xHighest == None:
        print(
            "Unable to solve because the input interval found no root of the function"
        )
        log_activities(
            "[Regula falsi] Unable to solve because the input interval found no root of the function",
            "WARNING",
        )
        return None

    for iter in range(1, MAX_ITERATION_CNT + 1, 1):
        fa: float = CalcFunc(rEq, xLowest)
        fb: float = CalcFunc(rEq, xHighest)
        xr: float = xHighest - ((fb * (xHighest - xLowest)) / (fb - fa))
        f_xr: float = CalcFunc(rEq, xr)

        PrintIterations(iter, ("a", "b", "Xr", "f(Xr)"), xLowest, xHighest, xr, f_xr)

        csv_file.write(f"{iter},{xLowest},{xHighest},{xr},{f_xr}\n")

        # if f(xr) = 0 (or approaching 0) then we found the root and return it
        if abs(f_xr) < TOLERANCE:
            csv_file.close()
            return xr

        # if not we change the interval with xr.
        # What we want is to keep the interval [a, b] satisfy f(a) * f(b) < 0
        # So if f(a) * f(xr) < 0 we change the b and vice versa
        else:
            if fa * f_xr < 0:
                xHighest = xr
            else:
                xLowest = xr

    csv_file.close()


HEADER = """
 ____                  _        
|  _ \ ___  __ _ _   _| | __ _  
| |_) / _ \/ _` | | | | |/ _` | 
|  _ <  __/ (_| | |_| | | (_| | 
|_| \_\___|\__, |\__,_|_|\__,_| 
           |___/
 _____     _     _              
|  ___|_ _| |___(_)             
| |_ / _` | / __| |             
|  _| (_| | \__ \ |             
|_|  \__,_|_|___/_|             

"""


def run_regulaFalsi():
    res_file = open("./out/regula-falsi/root.txt", "w")
    PrintIntroProg(HEADER, "Regula Falsi (false position) Root Finding Method")
    log_activities("Running Regula falsi...")

    while True:
        user_input = input(
            "\nInput function coefficients (space separated) or 'q' to exit: "
        ).strip()
        if user_input.lower() == "q":
            print("Exiting program...")
            break

        try:
            eq = list(map(int, user_input.split()))
            xLowest = float(input("Input interval start (a): "))
            xHighest = float(input("Input interval end (b): "))

            print("\n======= Regula Falsi (False Position) =======\n")
            PrintSingleEq(eq)
            root = regula_falsi(eq, xLowest, xHighest)
            if root is not None:
                print(f"\nRoot found: x = {root:.6f}")
                res_file.write(f"\nRoot found: x = {root:.6f}")
            else:
                break

        except ValueError:
            print("Invalid input. Please enter numbers only or 'q' to exit.")
            log_activities("[Regula Falsi] Invalid input", "ERROR")

    res_file.close()


# main input driver
if __name__ == "__main__":
    run_regulaFalsi()
