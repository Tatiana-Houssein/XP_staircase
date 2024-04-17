import random as rd
from dataclasses import dataclass


@dataclass
class TacheInterferenteData:
    number_1: int
    number_2: int
    result: int
    question: str


def question_tache_interferente() -> str:
    tache_inter_data = create_tache_interferente_data()
    n1 = tache_inter_data.number_1
    n2 = tache_inter_data.number_2
    return f"{n1} + {n2} ="


def create_tache_interferente_data() -> TacheInterferenteData:
    number_1 = rd.randint(11, 40)  # noqa: S311
    number_2 = rd.randint(11, 60)  # noqa: S311
    return TacheInterferenteData(
        number_1, number_2, number_1 + number_2, f"{number_1} + {number_2} = "
    )
