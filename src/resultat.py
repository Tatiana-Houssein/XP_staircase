from dataclasses import dataclass

@dataclass
class Resultat:
    tour: int
    lag_global: int
    numero_stimulus: int
    reponse_correct: str
    reponse_sujet: str
