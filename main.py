"""Operations Research Final Project"""
from copy import deepcopy
from typing import Tuple

import numpy as np
from colorama import Fore, Style, init
from tabulate import tabulate

from text import WELCOME_INPUT

init(autoreset=True)

MAX_LIMIT = int(10e11) - 1
MIN_LIMIT = - MAX_LIMIT


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    """Creates a matrix (m x n) with integer numbers.

    Args:
        * rows (int): Number of rows
        * cols (int): Number of columns

    Returns:
        * matrix (list[list[int]]): The created matrix
    """
    matrix = np.empty([rows, cols])

    msg = (
        "\nThe entry must have spaces between them for each "
        "row, e.g.: 1 2 3 (if the row has 3 columns)\n"
    )
    print(info(msg))

    for idx in range(rows):
        while True:
            print(f"Please enter values of row {idx+1}: ", end="")
            try:
                matrix[idx, :] = [*input().split()]
                break
            except ValueError as value:
                print(error(f"\n{value} is not a valid input.\n"))

    return matrix.tolist()


# Decision Methods ---------------------------------------------------------------------------


def laplace(matrix: list[list[int]]) -> list[float]:
    """Laplace method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    prob = 1 / len(matrix[0])

    expc_values = []
    for row in matrix:
        expc_value = 0.0
        for number in row:
            expc_value += number * prob
        expc_values.append(round(expc_value, 2))

    return expc_values


def hurwicz(matrix: list[list[int]], opt_coef: float) -> list[float]:
    """Hurwicz method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers
        * opt_coef (float): Optimism coefficient

    Returns:
        * expc_values list[int]: Final results
    """
    pess_coef = 1 - opt_coef
    return [round((max(row) * opt_coef + min(row) * pess_coef), 2) for row in matrix]


def savage(matrix: list[list[int]]) -> Tuple[list[int], list[int]]:
    """Savage method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * (list[int]): Final results
    """
    transp_matrix = np.transpose(np.array(matrix))

    for idx, col in enumerate(transp_matrix):
        maxim = max(col)
        for jdx, number in enumerate(col):
            transp_matrix[idx][jdx] = maxim - number

    sorrows_matrix = np.transpose(transp_matrix).tolist()

    return sorrows_matrix, optimistic(sorrows_matrix)


def optimistic(matrix: list[list[int]]) -> list[int]:
    """Optimistic method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    return [max(row) for row in matrix]


def pessimistic(matrix: list[list[int]]) -> list[int]:
    """Pessimistic method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    return [min(row) for row in matrix]


# Style --------------------------------------------------------------------------


def info(text: str):
    """Info message"""
    return Style.BRIGHT + Fore.LIGHTGREEN_EX + text


def error(text: str):
    """Error message"""
    return Style.BRIGHT + Fore.LIGHTRED_EX + text


def warning(text: str):
    """Warning message"""
    return Style.BRIGHT + Fore.LIGHTMAGENTA_EX + text


def light(text: str):
    """Light message"""
    return Style.BRIGHT + Fore.LIGHTWHITE_EX + text


# Validations --------------------------------------------------------------------


def validate_rows_and_cols() -> Tuple[int, int]:
    """Validates rows and columns"""
    while True:
        try:
            rows = int(input("Enter the numbers of rows: "))
            cols = int(input("Enter the numbers of columns: "))

            if rows <= 0 or cols <= 0:
                print(error("\nThe rows and columns must be greater than 0!\n"))
                continue

            if rows > 50 or cols > 50:
                print(error("\nThe rows and columns must be less than or equal to 50!\n"))
                continue

            return rows, cols
        except ValueError:
            print(error("\nThe rows and columns must be an integer!\n"))


def validate_optimism_coef() -> int | float:
    """Validates the optimism coefficient."""
    print(info("\nThe decimal number is with '.' e.g.: 0.85\n"))

    while True:
        try:
            coef = float(input("Enter the optimism coefficient: "))

            if not 0 <= coef <= 1:
                print(error("\nThe number must be between 0 and 1!\n"))
                continue

            return coef

        except ValueError:
            print(error("\nThe value must be a number!\n"))


def validate_limits_of_matrix() -> Tuple[int, int]:
    """Validates limits of the randomly matrix."""
    msg = f"\nThe number of low and high limits must be between {MIN_LIMIT} and {MAX_LIMIT}.\n"
    print(info(msg))

    while True:
        try:
            low = int(input("Enter the lower limit: "))
            high = int(input("Enter the upper limit: "))

            if high < low:
                raise Exception(error("\nThe upper limit must be greater than lower limit!\n"))

            if low == high:
                raise Exception(error("\nThe low and high limits can't be the same.\n"))

            if not MIN_LIMIT <= low <= MAX_LIMIT or not MIN_LIMIT <= high <= MAX_LIMIT:
                raise Exception(
                    error(
                        "\nThe limit variables must be greater "
                        f"than {MIN_LIMIT} and less {MAX_LIMIT}!\n"
                    )
                )

            return low, high
            
        except ValueError:
            print(error("\nLimits must be integer values!\n"))
        except Exception as excp:
            print(excp)


def generate_matrix(rows: int, cols: int) -> list[list[int]]:
    """Generates the integer matrix from an option.

    Args:
        * rows (int): Number of rows in the matrix
        * cols (int): Number of columns in the matrix

    Returns:
        * list[list[int]]: Matrix with integer numbers
    """
    while True:

        option = input(WELCOME_INPUT)

        if option not in ("1", "2"):
            print(error("\nThe value is not correct, the correct options can only be 1 or 2."))
            continue

        if option == "1":
            matrix = create_matrix(rows, cols)

        if option == "2":
            low, high = validate_limits_of_matrix()
            matrix = np.random.randint(low, high, size=(rows, cols)).tolist()

        return matrix


def generate_print_matrix(matrix: list[list[int]]) -> list[list[int | str] | list[str]]:
    """Generates a print matrix with headers.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * Tuple[list[str], list[list[int | str]]]: Print matrix
    """
    headers = [f"S{i}" for i in range(1, len(matrix) + 1)]
    headers.insert(0, "X")

    print_matrix: list[list[int | str] | list[str]] = deepcopy(matrix)  # type: ignore

    for idx, row in enumerate(print_matrix, 1):
        row.insert(0, f"A{idx}")

    print_matrix.insert(0, headers)

    print(error("\nOriginal Matrix"))
    print(tabulate(print_matrix, tablefmt="fancy_grid"))

    return print_matrix


def print_results_matrix(
    method: str,
    print_matrix: list[list[int | str] | list[str] | list[float] | list[int]],
    results: list[int] | list[float],
    is_savage: bool = False
) -> None:
    """Print the results matrix of specific method

    Args:
        * method (str): The method name
        * print_matrix (list[list[int]]): The original print matrix
        * results (list[int  |  float]): Results (expected values) of an decision method
        * is_savage (bool): A flag to choose if is savage method
    """
    print(error(f"\n{method} Method"))

    criteria = max
    if is_savage:
        sorrows_matrix, results = results
        criteria = min
        print(error("\nSorrows Matrix"))
        print(tabulate(sorrows_matrix, tablefmt="fancy_grid"))

    pr_matrix = deepcopy(print_matrix)
    pr_matrix[0].append("EV")

    for idx, row in enumerate(pr_matrix[1:]):
        row.append(results[idx])

    print(tabulate(pr_matrix, tablefmt="fancy_grid"))
    print(
        light("-> The best expected value for the"),
        info(f"{method} method"),
        light("is"),
        warning(f"{criteria(results)}"),
        light("with"),
        info(f"A{results.index(criteria(results))+1}"),
    )


def main():
    """Main function"""
    while True:
        print(info("\nThe number of rows and columns must be between 1 and 50.\n"))

        rows, cols = validate_rows_and_cols()
        coef = validate_optimism_coef()
        matrix = generate_matrix(rows, cols)

        print_matrix = generate_print_matrix(matrix)

        print_results_matrix("Laplace", print_matrix, laplace(matrix))
        print_results_matrix("Pessimistic", print_matrix, pessimistic(matrix))
        print_results_matrix("Optimistic", print_matrix, optimistic(matrix))
        print_results_matrix("Hurwicz", print_matrix, hurwicz(matrix, coef))
        print_results_matrix("Savage", print_matrix, savage(matrix), is_savage=True)

        while (choose := input(light("\nContinue [1] Exit [2]: "))) not in ("1", "2"):
            print(error("\nThe value is not correct, the correct options can only be 1 or 2."))

        if choose == "2":
            print("Bye!")
            import time

            time.sleep(3)
            break


if __name__ == "__main__":
    main()
