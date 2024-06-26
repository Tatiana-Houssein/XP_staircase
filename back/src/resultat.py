from dataclasses import dataclass


@dataclass
class ResultExperiment:
    tour: int
    lag_global: int  # après réponse du sujet
    lag_initial_stimulus: int
    numero_stimulus: int
    reponse_correct: str
    reponse_sujet: str
    type_erreur_tds: str
    nombre_sujet: int
    flag_ia: str
