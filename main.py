"""Operations Research Final Project"""
from copy import deepcopy

from colorama import Fore, init, Style
import numpy as np
from tabulate import tabulate
from typing import Iterable

from text import WELCOME_INPUT

init(autoreset=True)


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    """Creates a matrix (m x n) with integer numbers

    Args:
        * rows (int): Number of rows
        * cols (int): Number of columns

    Returns:
        * matrix (list[list[int]]): The created matrix
    """
    matrix = np.empty([rows, cols])
    print(
        Style.BRIGHT
        + Fore.RED
        + "The entry must have spaces between them for each row, "
        "e.g.: 1 2 3 (if the row has 3 columns)"
    )
    for i in range(rows):
        while True:
            print(f"Please enter values of row {i+1}: ", end="")
            try:
                matrix[i, :] = [*input().split()]
                break
            except ValueError as value:
                print(f"{value} is not a valid input.")

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


def validate_integer_input(
        name: str,
        message: str,
        min_limit: int = 0,
        max_limit: int = 50
    ) -> int:
    """Validates the value of a integer variable.

    Args:
        * name (str): Name of variable to validate
        * message (str): Error message

    Returns:
        * int: Valid integer value
    """
    while True:
        try:
            if min_limit < (variable := int(input(message))) <= max_limit:
                return variable
            else:
                if name != "option":
                    print(f"The {name} variable must be greater "
                        f"than {min_limit} and less {max_limit}!")
                print("The value is not correct, the correct options can only be 1 or 2.")
        except ValueError:
            print(f"The {name} variable must be an integer!")


def validate_limit_number(*numbers: tuple[int]) -> list[int]:
    """Validates limit numbers of rows and colums.

    Args:
        * numbers (tuple[int]): Numbers to validate.

    Returns:
        * list[int]: Lower and upper numbers.
        
    Raise:
        * str: If some validation ocurred.
    """
    
    numbers = [*map(int, numbers)]
    
    if len(set(numbers)) == 1:
        raise Exception(Style.BRIGHT + Fore.RED + "\nThe low and high limits can't be the same")

    for num in numbers:
        if not -9999999999 <= num <= 9999999999:
            raise Exception("The limit variables must be greater "
                            "than -9999999999 and less 9999999999!")

    return numbers


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
                    print(
                        Style.BRIGHT
                        + Fore.GREEN
                        + "\nThe number of low and high limits must be between "
                        "-9999999999 and 9999999999.\n"
                    )
                    try:
                        low, high = validate_limit_number(
                            input("Enter the lower limit: "), input("Enter the upper limit: ")
                        )
                        
                        if high < low:
                            raise Exception("The upper limit must be greater than lower limit!")

                        matrix = np.random.randint(
                            low, high, size=(rows, cols)
                        ).tolist()
                        break
                    except ValueError:
                        print("Limits must be integer values!")
                    except Exception as e:
                        print(e)
                break
            case _:
                option = validate_integer_input(name="option", message=WELCOME_INPUT)

    return matrix


def print_results_matrix(
    method: str,
    print_matrix: list[list[int | str] | list[str] | list[float] | list[int]],
    results: list[int] | list[float],
    min_result: bool = False
) -> None:
    """Print the results matrix of specific method

    Args:
        * method (str): The method name
        * print_matrix (list[list[int]]): The original print matrix
        * results (list[int  |  float]): Results (expected values) of an decision method
        * min_result (bool): A flag to choose the max or min expected value
    """
    print("\n", Style.BRIGHT + Fore.RED + f"{method} Method" + Style.RESET_ALL)

    pr_matrix = deepcopy(print_matrix)
    pr_matrix[0].append("EV")

    for idx, row in enumerate(pr_matrix[1:]):
        row.append(results[idx])

    results_function = min if min_result else max

    print(tabulate(pr_matrix, tablefmt="fancy_grid"))
    print(
        "> The best expected value for the",
        Style.BRIGHT + Fore.LIGHTGREEN_EX + f"{method} method",
        Fore.WHITE + "is",
        Style.BRIGHT + Fore.LIGHTMAGENTA_EX + f"{results_function(results)}",
        "with",
        Style.BRIGHT + Fore.LIGHTGREEN_EX + f"A{results.index(results_function(results))+1}",
    )


def main():
    """Main function"""
    while True:
        print(
            Style.BRIGHT
            + Fore.GREEN
            + "\nThe number of rows and columns must be between 0 and 50.\n"
        )
        rows = validate_integer_input("rows", "Enter the numbers of rows: ")
        cols = validate_integer_input("columns", "Enter the numbers of columns: ")

        while True:
            print(Style.BRIGHT + Fore.RED + "\nThe decimal number is with '.' e.g.: 3.14\n")
            try:
                coef = float(input("Enter the optimism coefficient: "))
                if not 0 <= coef <= 1:
                    print("The number must be between 0 and 1!")
                else:
                    break
            except ValueError:
                print("The value must be a number!")

        option = validate_integer_input(
            name="option",
            message=WELCOME_INPUT,
            min_limit=1,
            max_limit=2
        )
        matrix = validate_option(option, rows, cols)
        print_matrix = generate_print_matrix(matrix, cols)
        print(Style.BRIGHT + Fore.RED + "\nOriginal Matrix" + Style.RESET_ALL)
        print(tabulate(print_matrix, tablefmt="fancy_grid"))

        print_results_matrix("Laplace", print_matrix, laplace(matrix))
        print_results_matrix("Pessimistic", print_matrix, pessimistic(matrix))
        print_results_matrix("Optimistic", print_matrix, optimistic(matrix))
        print_results_matrix("Hurwicz", print_matrix, hurwicz(matrix, coef))
        print_results_matrix("Savage", print_matrix, savage(matrix), min_result=True)

        while (choose := input("\ncontinue [1] exit [2]: ")) not in "12" or choose == "":
            print("The value is not correct, the correct options can only be 1 or 2.")

        if choose == "2":
            print("Bye!")
            import time;time.sleep(3)
            break

if __name__ == "__main__":
    main()
