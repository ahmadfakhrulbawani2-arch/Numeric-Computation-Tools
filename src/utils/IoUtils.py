from typing import List

# this print intro statement
def PrintIntroProg(title: str) -> None:
  print(f"Welcome to {title}. Please input the equation (only support up to x^0, dosen't support x^-1, etc...)")

# This return equation string
def GetEqState(eq: List[int]) -> str:
  new_eq: List[int] = list(reversed(eq))
  sEq = ""

  # reverse the loop to reverse the printed eq
  for i in range(len(new_eq)-1, -1, -1): 
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
  evals: List[str] = [
    f"{label} = {value}" for label, value in zip(vars, params)
  ]

  evals_str: str = ", ".join(evals)
  log = f"Iteration-{iter}: {evals_str}"
  print(log)

