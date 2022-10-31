"""Operations Research Final Project"""
from copy import deepcopy
from typing import Tuple
import numpy as np
from tabulate import tabulate

from text import welcome_input


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    """Creates a matrix (m x n) with integer numbers

    Args:
        * rows (int): Number of rows
        * cols (int): Number of columns

    Returns:
        * matrix (list[list[int]]): The created matrix
    """
    matrix = []
    for row in range(rows):
        aux = []
        for col in range(cols):
            while True:
                try:
                    number = int(
                        input(f"Digite el numero para la posicion [{row+1}, {col+1}]: ")
                    )
                    break
                except ValueError:
                    print("¡Digite solo numeros enteros!")
            aux.append(number)
        matrix.append(aux)

    return matrix


def generate_print_matrix(
    matrix: list[list[int]], cols: int
) -> Tuple[list[str], list[list[int | str]]]:
    """Generates a print matrix with headers.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers
        * cols (int): Number of columns

    Returns:
        * Tuple[list[str], list[list[int | str]]]: Print matrix
    """
    headers = [f"S{i}" for i in range(1, cols + 1)]
    print_matrix: list[list[int | str]] = deepcopy(matrix)  # type: ignore

    for idx, row in enumerate(print_matrix, 1):
        row.insert(0, f"A{idx}")

    return headers, print_matrix


def laplace(matrix: list[list[int]]) -> list[int]:
    """Laplace method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    prob = 1 / len(matrix[0])

    expc_values = []
    for row in matrix:
        expc_value = 0
        for number in row:
            expc_value += number * prob
        expc_values.append(expc_value)

    return expc_values


def hurwicz(matrix: list[list[int]], opt_coef: float) -> list[int]:
    """Hurwicz method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers
        * opt_coef (float): Optimism coefficient

    Returns:
        * expc_values list[int]: Final results
    """
    expc_values = []
    pess_coef = 1 - opt_coef

    for row in matrix:
        expc_values.append(max(row) * opt_coef + min(row) * pess_coef)

    return expc_values


def savage(matrix: list[list[int]]) -> list[int]:
    """Savage method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * (list[int]): Final results
    """
    transp_matrix = np.transpose(np.array(matrix))

    for col in range(len(transp_matrix)):
        maxim = max(transp_matrix[col])
        for number in range(len(transp_matrix[0])):
            transp_matrix[col][number] = maxim - transp_matrix[col][number]

    matrix = list(np.transpose(transp_matrix))

    return optimistic(matrix)


def optimistic(matrix: list[list[int]]) -> list[int]:
    """Optimistic method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    expc_values = []
    for row in matrix:
        expc_values.append(max(row))

    return expc_values


def pessimistic(matrix: list[list[int]]) -> list[int]:
    """Pessimistic method.

    Args:
        * matrix (list[list[int]]): Custom matrix with integer numbers

    Returns:
        * expc_values (list[int]): Final results
    """
    expc_values = []
    for row in matrix:
        expc_values.append(min(row))

    return expc_values


def main():
    """Main function"""
    rows = int(input("Ingrese la cantidad de filas: "))
    cols = int(input("Ingrese la cantidad de columnas: "))

    option = int(input(welcome_input))

    match option:

        case 1:
            matrix = create_matrix(rows, cols)
        case 2:
            low = int(input("Ingrese el limite inferior: "))
            high = int(input("Ingrese el limite superior: "))
            matrix = np.random.randint(low, high, size=(rows, cols)).tolist()
        case _:
            matrix = []

    headers, print_matrix = generate_print_matrix(matrix, cols)
    print(tabulate(print_matrix, headers=headers, tablefmt="fancy_grid"))

    print(laplace(matrix))
    print(pessimistic(matrix))
    print(optimistic(matrix))
    print(savage(matrix))

    while True:
        try:
            coef = float(input("Digite el coeficiente de optimismo: "))
            if not 0 <= coef <= 1:
                print("¡El numero debe estar entre 0 y 1!")
            else:
                break
        except ValueError:
            print("¡El valor debe ser un número!")

    print(hurwicz(matrix, coef))


if __name__ == "__main__":
    main()
