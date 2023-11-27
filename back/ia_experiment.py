import random as rd
from collections.abc import Callable

import numpy as np

from back.constantes import ReponseSujet, StatusStimulus
from back.experiment import Experience, Stimulus


def probabilite_de_reussite(x: float, lag_limit: int) -> float:
    return (np.arctan(lag_limit - x) + np.pi / 2) / np.pi


def fonction_reponse_ia(stimulus: Stimulus, lag_limit: int) -> str:
    proba_reussite = probabilite_de_reussite(stimulus.lag_initial, lag_limit)
    u = rd.random()  # noqa: S311
    if u < proba_reussite:  # l'IA répond correctement
        if stimulus.statut == StatusStimulus.non_vu:
            return ReponseSujet.non_vu
        return ReponseSujet.vu
    if stimulus.statut == StatusStimulus.non_vu:
        return ReponseSujet.vu
    return ReponseSujet.non_vu


class ExperienceTest(Experience):
    def __init__(
        self,
        liste_stimuli: list[Stimulus],
        lag_initial: int,
        fonction_question_au_sujet: Callable[[Stimulus, int], str],
        lag_limit: int,
    ) -> None:
        super().__init__(liste_stimuli, lag_initial, fonction_question_au_sujet)
        self.lag_limit = lag_limit

    def deroulement_un_tour(self) -> None:
        """
        Un tour de jeu.
        D'abord on choisi le prochain stimulus à afficher.
        Puis on pose la question sur ce stimulus.
        Suivant la réponse (bonne ou mauvaise) on ajuste le lag global.
        """
        stimulus_choisi = self.choix_prochain_stimulus()
        print(f"Lag: {self.lag_global}, status : {stimulus_choisi.statut}")
        self.mise_a_jour_lag_pool_vu()
        reponse_du_sujet = self.fonction_question_au_sujet(
            stimulus_choisi, self.lag_limit
        )
        self.traitement_reponse_sujet(
            reponse_du_sujet=reponse_du_sujet, stimulus=stimulus_choisi
        )


if __name__ == "__main__":
    liste_stimuli: list[Stimulus] = [Stimulus(i) for i in range(100)]
    experience_test = ExperienceTest(
        liste_stimuli=liste_stimuli,
        lag_initial=2,
        fonction_question_au_sujet=fonction_reponse_ia,
        lag_limit=15,
    )
    experience_test.deroulement_expe()
