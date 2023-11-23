import random as rd

import numpy as np
from src.experiment import Experience, ReponseSujet, StatusStimulus, Stimulus
from src.resultat import Resultat


def probabilite_de_reussite(x: float, lag_limit: int) -> float:
    return (np.arctan(lag_limit - x) + np.pi / 2) / np.pi


class ExperienceTest(Experience):
    def __init__(
        self, liste_stimuli: list[Stimulus], lag_initial: int, lag_limit: int
    ) -> None:
        super().__init__(liste_stimuli, lag_initial)
        self.lag_limit = lag_limit

    def question_au_sujet_maj_lag_global_et_status_stimulus(
        self, stimulus: Stimulus
    ) -> None:
        """
        L'IA répond correctement à chaque fois.
        """
        proba_reussite = probabilite_de_reussite(stimulus.lag_initial, self.lag_limit)
        u = rd.random()  # noqa: S311
        print(
            f"Stm {stimulus.numero}, ini: {stimulus.lag_initial}, lag: {stimulus.lag}"
        )
        print(len(self.pool_non_vus), len(self.pool_vus))
        print(f"lag global avant: {self.lag_global}")
        print(f"Status stimulus: {stimulus.statut}")
        if u < proba_reussite:  # l'IA répond correctement
            if stimulus.statut == StatusStimulus.non_vu:
                reponse_du_sujet = ReponseSujet.non_vu
            else:
                reponse_du_sujet = ReponseSujet.vu
        elif u >= proba_reussite:
            if stimulus.statut == StatusStimulus.non_vu:
                reponse_du_sujet = ReponseSujet.vu
            else:
                reponse_du_sujet = ReponseSujet.non_vu
        print(f"Réponse IA: {reponse_du_sujet}")
        if self.is_sujet_right(reponse_du_sujet, stimulus.statut):
            self.lag_global += 1
        else:
            self.lag_global -= 1
        print(f"Lag Global après : {self.lag_global}")
        resultat = Resultat(
            tour=self.tour,
            lag_global=self.lag_global,
            numero_stimulus=stimulus.numero,
            reponse_correct=stimulus.statut,
            reponse_sujet=reponse_du_sujet,
        )
        self.liste_resultat.append(resultat)

        stimulus.mise_a_jour_status()


if __name__ == "__main__":
    liste_stimuli: list[Stimulus] = [Stimulus(i) for i in range(100)]
    experience_test = ExperienceTest(liste_stimuli, 2, 15)
    experience_test.deroulement_expe()
