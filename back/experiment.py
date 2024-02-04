import random
from collections.abc import Callable
from enum import StrEnum

from back.configuration import AUGMENTATION_LAG, DIMINUTION_LAG, LAG_INITIAL
from back.constantes import (
    ReponseIA,
    ReponseSujet,
    StatusStimulus,
    TypeErreur,
    TypeReponseSujet,
)
from back.io import save_result
from back.resultat import Resultat


def generer_nombres_avec_retenue() -> tuple:
    nombre1 = random.randint(10, 99)  # noqa: S311
    chiffre1 = nombre1 % 10
    nombre2 = random.randint(10 - chiffre1, 99)  # noqa: S311
    return nombre1, nombre2


def generer_operation() -> None:
    nombre1, nombre2 = generer_nombres_avec_retenue()
    print(f"Opération : {nombre1} + {nombre2}")


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
        self.pool_non_vus = liste_stimuli
        self.pool_vus: list[Stimulus] = []
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

    def get_type_erreur_du_sujet(
        self,
        reponse_sujet: str,
        status_stimulus: str,
    ) -> str:
        """Renvoie le type d'erreur du sujet.

        Dépend de la réponse du sujet et du status du stimulus.
        Peut-être detection ou rejet correct, ommission, fausse alarme.

        Args:
            reponse_sujet (str):
            status_stimulus (str):

        Returns:
            str:
        """
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
    ) -> TypeReponseSujet:
        """Traite la réponse. Renvoie succes, echec ou osef.

        Args:
            reponse_sujet (str):
            status_stimulus (str):

        Returns:
            TypeReponseSujet:
        """
        type_erreur = self.get_type_erreur_du_sujet(reponse_sujet, status_stimulus)
        print(type_erreur)
        if type_erreur in [
            TypeErreur.detection_correct,
        ]:
            return TypeReponseSujet.succes
        if type_erreur == TypeErreur.rejet_correct:
            return TypeReponseSujet.osef
        return TypeReponseSujet.echec

    def traitement_reponse_sujet(
        self,
        reponse_du_sujet: str,
        stimulus: Stimulus,
        nombre_sujet: int = -1,
    ) -> None:
        """
        Le lag global est adapté à la bonne ou mauvaise réponse du sujet au stimulus
        donné.
        Puis on met à jour le status de ce stimulus (non_vu -> vu -> vu_deux_fois)
        """
        if (
            self.is_sujet_right(reponse_du_sujet, stimulus.statut)
            == TypeReponseSujet.succes
        ):
            self.lag_global += AUGMENTATION_LAG
        elif (
            self.is_sujet_right(reponse_du_sujet, stimulus.statut)
            == TypeReponseSujet.echec
        ):
            self.lag_global -= DIMINUTION_LAG
            if self.lag_global < 0:
                self.lag_global = 0
        # 'print(f"Rép sujet: {reponse_du_sujet} || Status stimulus: {stimulus.statut}")
        print(f"Lag actuel: {self.lag_global}, lag ini stim: {stimulus.lag_initial}")
        resultat = Resultat(
            tour=self.tour,
            lag_global=self.lag_global,
            lag_initial_stimulus=stimulus.lag_initial,
            numero_stimulus=stimulus.numero,
            reponse_correct=str(stimulus.statut),
            reponse_sujet=str(reponse_du_sujet),
            type_erreur_tds=str(
                self.get_type_erreur_du_sujet(reponse_du_sujet, stimulus.statut)
            ),
            nombre_sujet=nombre_sujet,
        )
        self.liste_resultat.append(resultat)

        stimulus.mise_a_jour_status()
        if stimulus.statut == StatusStimulus.vu_deux_fois:
            self.pool_vus.remove(stimulus)

    def choix_rep_ia(self) -> StrEnum:
        """
        Choix de ce que va présenter IA comme réponse
        """
        u = random.randint(0, 1)  # noqa: S311
        if u == 0:
            return ReponseIA.vu
        return ReponseIA.non_vu

    def choix_prochain_stimulus(self) -> Stimulus:
        """Choisis le prochain stimulus a devoir être présenté.

        Si un stimulus du pool vu a lag de 0, c'est lui.
        Sinon on ajoute un stuimulus du pool non vu.

        Returns:
            Stimulus:
        ET déterminer quel rep IA
        """
        print(
            f"#pool vus: {len(self.pool_vus)}, #pool non vus: {len(self.pool_non_vus)}"
        )
        reponse_ia = self.choix_rep_ia()
        print(reponse_ia)
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
        lag_initial=LAG_INITIAL,
        fonction_question_au_sujet=le_sujet_repond,
    ).deroulement_expe()
