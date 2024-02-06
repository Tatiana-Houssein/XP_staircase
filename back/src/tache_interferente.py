import random as rd


def question_tache_interferente() -> str:
    n1, n2 = tache_interferente_numbers()
    return f"{n1} + {n2} ="


def tache_interferente_numbers() -> tuple[int, int]:
    number_1 = rd.randint(10, 99)  # noqa: S311
    number_2 = rd.randint(10, 99)  # noqa: S311
    return number_1, number_2
