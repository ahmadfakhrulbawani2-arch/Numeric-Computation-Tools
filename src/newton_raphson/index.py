import time
from typing import List
from src.utils import *

MAX_ITERATION: int = 50


# This return Xn = Xn-1 - (f(Xn-1) / f'(Xn-1))
def newton_raphson(eq: List[int], xInit: float) -> float | None:
    new_eq: List[int] = list(reversed(eq))
    fx0: float = CalcFunc(new_eq, xInit)
    arrDerivedEq: List[int] = DerivativeF(new_eq)

    if not arrDerivedEq:
        print("Unable to solve as the derivative of given input is 0")
        return None

    fPrimex0: float = CalcFunc(arrDerivedEq, xInit)
    if fPrimex0 == 0:
        print("Derivative value is zero")
        return None

    res: float = xInit - (fx0 / fPrimex0)
    return res


# This return equation string
def get_eq_state(eq: List[int]) -> str:
    new_eq: List[int] = list(reversed(eq))
    sEq = ""

    # reverse the loop to reverse the printed eq
    for i in range(len(new_eq) - 1, -1, -1):
        if new_eq[i]:
            if i > 1:
                sEq += f"({new_eq[i]})X^{i} + "
            elif i == 1:
                sEq += f"({new_eq[i]})X + "
            else:
                sEq += f"({new_eq[i]}) + "

    return "Equation f(x) = " + sEq.rstrip(" + ")


def printIter(res: float, iter: int, err_rate: float) -> None:
    if err_rate is not None:
        print(
            f"Iteration-{iter} X{iter} = {res:.4f} | convergence rate ≈ {err_rate:.4f}"
        )
    else:
        print(f"Iteration-{iter} X{iter} = {res:.4f}")
    time.sleep(0.2)  # delay 0.2 second
    return None


# This return the root of input func
def main(eq: List[int], x_init: float) -> float | None:
    errors: List[float] = []  # store convergence rate every iterations
    iter: int = 1
    prev_x: float = x_init
    curr_x: float | None = newton_raphson(
        eq, prev_x
    )  # Because newton_raphson can return None

    if curr_x is None:
        return None

    print("\n========= Newton-Raphson Finding Iteration =========\n")
    print(f"Initial value of X0 is {x_init}\n")

    new_eq = list(reversed(eq))

    while abs(CalcFunc(new_eq, curr_x)) > 1e-6 and iter < MAX_ITERATION:
        prev_x = curr_x
        curr_x = newton_raphson(eq, prev_x)

        if curr_x is None:
            return None

        errors.append(abs(curr_x - prev_x))
        err_rate: float | None = Calc_Converngence_Rate(errors)
        printIter(curr_x, iter, err_rate)
        iter += 1

    if iter == MAX_ITERATION:
        print(f"Maximum number of iteration reached of {MAX_ITERATION} iterations!")
        return None

    return curr_x


def print_sol(nRes: float | None, nEq: List[int]) -> None:
    if nRes is None:
        return
    sEqState = get_eq_state(nEq)
    print(f"\nThe root of {sEqState} from Newton-Raphson computation is x = {nRes}")


HEADER = """
 _   _               _                  
| \ | | _____      _| |_ ___  _ __      
|  \| |/ _ \ \ /\ / / __/ _ \| '_ \     
| |\  |  __/\ V  V /| || (_) | | | |    
|_| \_|\___| \_/\_/  \__\___/|_| |_|    
 ____             _                       
|  _ \ __ _ _ __ | |__  ___  ___  _ __  
| |_) / _` | '_ \| '_ \/ __|/ _ \| '_ \ 
|  _ < (_| | |_) | | | \__ \ (_) | | | |
|_| \_\__,_| .__/|_| |_|___/\___/|_| |_|
           |_|                          

"""


def run_NR():
    Lazy_Loading("Opening files...")
    PrintIntroProg(HEADER, "Newton-Raphson Root Finding Method")
    while True:
        user_input = input(
            "\nInput function coeffissients (split with space, integer only) or 'q' to exit: "
        ).strip()

        if user_input.lower() == "q":
            print("Exiting program...")
            break

        try:
            arrEq = list(map(int, user_input.split()))
            nInitVal: List[float] = list(
                map(
                    float,
                    input(
                        "Input initial root guess (x0), you can input more than one: "
                    ).split(),
                )
            )

            for x0 in nInitVal:
                res = main(arrEq, x0)
                print_sol(res, arrEq)

        except ValueError:
            print("Invalid input. Please enter numbers only or 'q' to exit.")


# main driver only solve 1 root
if __name__ == "__main__":
    run_NR
