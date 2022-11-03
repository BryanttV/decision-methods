"""Operations Research Final Project"""
from copy import deepcopy

import numpy as np
from tabulate import tabulate

from text import WELCOME_INPUT


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    """Creates a matrix (m x n) with integer numbers

    Args:
        * rows (int): Number of rows
        * cols (int): Number of columns

    Returns:
        * matrix (list[list[int]]): The created matrix
    """
    matrix = np.empty([rows, cols])

    for i in range(rows):
        while True:
            try:
                matrix[i, :] = [*input().split()]
                break
            except ValueError as v:
                print(f"{v} is not a valid input.")

    return matrix.tolist()


def generate_print_matrix(
    matrix: list[list[int]], cols: int
) -> list[list[int | str] | list[str]]:
    """Generates a print matrix with headers.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers
        * cols (int): Number of columns

    Returns:
        * Tuple[list[str], list[list[int | str]]]: Print matrix
    """
    headers = [f"S{i}" for i in range(1, cols + 1)]
    headers.insert(0, "")

    print_matrix: list[list[int | str] | list[str]] = deepcopy(matrix)  # type: ignore

    for idx, row in enumerate(print_matrix, 1):
        row.insert(0, f"A{idx}")

    print_matrix.insert(0, headers)

    return print_matrix


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


def savage(matrix: list[list[int]]) -> list[int]:
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

    matrix = np.transpose(transp_matrix).tolist()

    return optimistic(matrix)


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


def validate_integer_input(name: str, message: str) -> int:
    """Validates the value of a integer variable.

    Args:
        * name (str): Name of variable to validate

    Returns:
        * int: Valid integer value
    """
    while True:
        try:
            if (variable := int(input(message))) > 0:
                return variable
            else:
                print(f"The {name} variable must be greater than zero!")
        except ValueError:
            print(f"The {name} variable must be an integer!")


def validate_option(option: int, rows: int, cols: int) -> list[list[int]]:
    """Validates a option and generates the integer matrix.

    Args:
        * option (int): Option selected in the input
        * rows (int): Number of rows in the matrix
        * cols (int): Number of columns in the matrix

    Returns:
        * list[list[int]]: Matrix with integer numbers
    """
    while True:
        match option:
            case 1:
                matrix = create_matrix(rows, cols)
                break
            case 2:
                while True:
                    try:
                        low = input("Enter the lower limit: ")
                        high = input("Enter the upper limit: ")
                        matrix = np.random.randint(
                            int(low), int(high), size=(rows, cols)
                        ).tolist()
                        break
                    except ValueError:
                        print("Limits must be integer values!")
                break
            case _:
                option = validate_integer_input(name="option", message=WELCOME_INPUT)

    return matrix


def print_results_matrix(
    print_matrix: list[list[int | str] | list[str] | list[float] | list[int]],
    results: list[int] | list[float],
) -> None:
    """Print the results matrix of specific method

    Args:
        * print_matrix (list[list[int]]): The original print matrix
        * results (list[int  |  float]): Results (expected values) of an decision method
    """
    print_results_matrix = deepcopy(print_matrix)
    print_results_matrix[0].append("EV")
    for idx, row in enumerate(print_results_matrix[1:]):
        row.append(results[idx])

    print(tabulate(print_results_matrix, tablefmt="fancy_grid"))


def main():
    """Main function"""
    rows = validate_integer_input("rows", "Enter the numbers of rows: ")
    cols = validate_integer_input("columns", "Enter the numbers of columns: ")

    while True:
        try:
            coef = float(input("Enter the optimism coefficient: "))
            if not 0 <= coef <= 1:
                print("The number must be between 0 and 1!")
            else:
                break
        except ValueError:
            print("The value must be a number!")

    option = validate_integer_input(name="option", message=WELCOME_INPUT)
    matrix = validate_option(option, rows, cols)
    print_matrix = generate_print_matrix(matrix, cols)
    print(tabulate(print_matrix, tablefmt="fancy_grid"))

    print_results_matrix(print_matrix, laplace(matrix))
    print_results_matrix(print_matrix, pessimistic(matrix))
    print_results_matrix(print_matrix, optimistic(matrix))
    print_results_matrix(print_matrix, hurwicz(matrix, coef))
    print_results_matrix(print_matrix, savage(matrix))


if __name__ == "__main__":
    main()
