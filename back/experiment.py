from collections.abc import Callable

from back.constantes import ReponseSujet, StatusStimulus, TypeErreur, TypeSucces
from back.io import save_result
from back.resultat import Resultat


class Stimulus:
    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.statut: str = StatusStimulus.non_vu
        self.lag: int = 0
        self.lag_initial: int = 0

    def mise_a_jour_status(self) -> None:
        if self.statut == StatusStimulus.non_vu:
            self.statut = StatusStimulus.vu
        elif self.statut == StatusStimulus.vu:
            self.statut = StatusStimulus.vu_deux_fois


def le_sujet_repond() -> str:
    reponse_sujet = input("Avez vous déjà vu ce visage ?")
    if reponse_sujet == "Y":
        return ReponseSujet.vu
    return ReponseSujet.non_vu


class Experience:
    def __init__(
        self,
        liste_stimuli: list[Stimulus],
        lag_initial: int,
        fonction_question_au_sujet: Callable[..., str],
    ) -> None:
        self.pool_non_vus = liste_stimuli  ###########
        self.pool_vus: list[Stimulus] = []  ###########
        self.lag_global = lag_initial
        self.tour: int = 0
        self.liste_resultat: list[Resultat] = []
        self.fonction_question_au_sujet = fonction_question_au_sujet

    def mise_a_jour_lag_pool_vu(self) -> None:
        """
        On abaisse de 1 le lag de tous les stimuli présents dans pool_vus
        """
        for stimulus in self.pool_vus:
            stimulus.lag -= 1
            if stimulus.lag < 0:
                stimulus.lag = 0

    def type_erreur_du_sujet(
        self,
        reponse_sujet: str,
        status_stimulus: str,
    ) -> str:
        if status_stimulus == StatusStimulus.non_vu:
            if reponse_sujet == ReponseSujet.non_vu:
                return TypeErreur.rejet_correct
            return TypeErreur.fausse_alarme
        if reponse_sujet == ReponseSujet.non_vu:
            return TypeErreur.omission
        return TypeErreur.detection_correct

    def is_sujet_right(
        self,
        reponse_sujet: str,
        status_stimulus: str,
    ) -> TypeSucces:
        type_erreur = self.type_erreur_du_sujet(reponse_sujet, status_stimulus)
        print(type_erreur)
        if type_erreur in [
            TypeErreur.detection_correct,
        ]:
            return TypeSucces.succes
        if type_erreur == TypeErreur.rejet_correct:
            return TypeSucces.osef
        return TypeSucces.echec

    def traitement_reponse_sujet(
        self,
        reponse_du_sujet: str,
        stimulus: Stimulus,
    ) -> None:
        """
        Le lag global est adapté à la bonne ou mauvaise réponse du sujet au stimulus
        donné.
        Puis on met à jour le status de ce stimulus (non_vu -> vu -> vu_deux_fois)
        """
        if self.is_sujet_right(reponse_du_sujet, stimulus.statut) == TypeSucces.succes:
            self.lag_global += 1
        elif self.is_sujet_right(reponse_du_sujet, stimulus.statut) == TypeSucces.echec:
            self.lag_global -= 1
        print(f"Réponse sujet: {reponse_du_sujet} || Satus stimulus: {stimulus.statut}")
        resultat = Resultat(
            tour=self.tour,
            lag_global=self.lag_global,
            lag_initial_stimulus=stimulus.lag_initial,
            numero_stimulus=stimulus.numero,
            reponse_correct=str(stimulus.statut),
            reponse_sujet=str(reponse_du_sujet),
            type_erreur_tds=str(
                self.type_erreur_du_sujet(reponse_du_sujet, stimulus.statut)
            ),
        )
        self.liste_resultat.append(resultat)

        stimulus.mise_a_jour_status()
        if stimulus.statut == StatusStimulus.vu_deux_fois:
            self.pool_vus.remove(stimulus)

    def choix_prochain_stimulus(self) -> Stimulus:
        print(
            f"#pool vus: {len(self.pool_vus)}, #pool non vus: {len(self.pool_non_vus)}"
        )
        for stimulus in self.pool_vus:
            if stimulus.lag == 0:
                return stimulus
        stimulus = self.pool_non_vus[0]
        stimulus.lag = self.lag_global
        stimulus.lag_initial = self.lag_global
        self.pool_vus.append(stimulus)
        self.pool_non_vus.pop(0)
        return stimulus

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
        reponse_du_sujet = self.fonction_question_au_sujet()
        self.traitement_reponse_sujet(
            reponse_du_sujet=reponse_du_sujet, stimulus=stimulus_choisi
        )

    def is_condition_arret_remplie(self) -> bool:
        """Renvoie True si l'experience doit s'arrêter.

        Returns:
            bool:
        """
        if len(self.pool_non_vus) > 0:
            return False
        return True

    def deroulement_expe(self) -> None:
        """
        D'abord, suppression des stimuli vu deux du pool_vue
        Puis, on enclenche self.deroulement_un_tout tant que les deux listes pool_vus et
        pool_non_vus ne sont pas vides.
        Avant, on supprime de la liste tous les stimuli vu deux fois du pool_vus
        """
        while not self.is_condition_arret_remplie():
            for stimulus in self.pool_vus:
                if stimulus.statut == StatusStimulus.vu_deux_fois:
                    self.pool_vus.remove(stimulus)
            self.deroulement_un_tour()
            self.tour += 1
        save_result(self.liste_resultat)


if __name__ == "__main__":
    l_stimuli = [Stimulus(i) for i in range(10)]
    Experience(
        liste_stimuli=l_stimuli,
        lag_initial=3,
        fonction_question_au_sujet=le_sujet_repond,
    ).deroulement_expe()
