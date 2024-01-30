import random
from collections.abc import Callable

from back.src.constantes import (
    AUGMENTATION_LAG,
    DIMINUTION_LAG,
    LAG_INITIAL,
    TAILLE_POOL_NON_VU,
)
from back.src.enum_constantes import (
    ReponseSujet,
    StatusStimulus,
    TypeErreur,
    TypeReponseSujet,
)
from back.src.io import save_result
from back.src.resultat import Resultat


class Stimulus:
    def __init__(self, stimulus_id: int) -> None:
        self.id = stimulus_id
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


def initialisation_liste_des_stimuli() -> list[Stimulus]:
    """Retourne une liste de stimuli de taille TAILLE_NON_VU.

    L'ordre est aléatoire

    Returns:
        list[Stimulus]:
    """
    liste_id = list(range(1, TAILLE_POOL_NON_VU))
    random.shuffle(liste_id)
    return [Stimulus(i) for i in liste_id]


class Experience:
    def __init__(
        self,
        liste_stimuli: list[Stimulus],
        lag_initial: int,
        fonction_question_au_sujet: Callable[..., str],
    ) -> None:
        self.pool_non_vus = liste_stimuli
        self.pool_vus_une_fois: list[Stimulus] = []
        self.pool_vus_deux_fois: list[Stimulus] = []
        self.lag_global = lag_initial
        self.tour: int = 0
        self.liste_resultat: list[Resultat] = []
        self.fonction_question_au_sujet = fonction_question_au_sujet
        self.update_current_stimulus()

    def mise_a_jour_lag_pool_vu(self) -> None:
        """
        On abaisse de 1 le lag de tous les stimuli présents dans pool_vus.
        """
        for stimulus in self.pool_vus_une_fois:
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
        nombre_sujet: int = -1,
    ) -> None:
        """
        Le lag global est adapté à la bonne ou mauvaise réponse du sujet au stimulus
        donné.
        Puis on met à jour le status de ce stimulus (non_vu -> vu -> vu_deux_fois)
        """
        print(self.is_sujet_right(reponse_du_sujet, self.current_stimulus.statut))
        if (
            self.is_sujet_right(reponse_du_sujet, self.current_stimulus.statut)
            == TypeReponseSujet.succes
        ):
            self.lag_global += AUGMENTATION_LAG
        elif (
            self.is_sujet_right(reponse_du_sujet, self.current_stimulus.statut)
            == TypeReponseSujet.echec
        ):
            self.lag_global -= DIMINUTION_LAG
            if self.lag_global < 0:
                self.lag_global = 0
        print(
            f"Rép suj: {reponse_du_sujet} || Stat stim: {self.current_stimulus.statut}"
        )
        print(
            f"L_glo: {self.lag_global}, l_ini stim: {self.current_stimulus.lag_initial}"
        )
        resultat = Resultat(
            tour=self.tour,
            lag_global=self.lag_global,
            lag_initial_stimulus=self.current_stimulus.lag_initial,
            numero_stimulus=self.current_stimulus.id,
            reponse_correct=str(self.current_stimulus.statut),
            reponse_sujet=str(reponse_du_sujet),
            type_erreur_tds=str(
                self.get_type_erreur_du_sujet(
                    reponse_du_sujet, self.current_stimulus.statut
                )
            ),
            nombre_sujet=nombre_sujet,
        )
        self.liste_resultat.append(resultat)

        self.current_stimulus.mise_a_jour_status()
        if self.current_stimulus.statut == StatusStimulus.vu_deux_fois:
            self.pool_vus_une_fois.remove(self.current_stimulus)
            self.pool_vus_deux_fois.append(self.current_stimulus)

    def choix_prochain_stimulus(self) -> Stimulus:
        """Renvoie le futur stimulus.

        Si un stimulus du pool vu a lag de 0, c'est lui même.
        Sinon on ajoute le premier stimulus du pool non vu.

        Ne mets pas à jour le stimulus actuel (current stimulus) !

        Mets à jour les liste vu et non_vus !

        TODO: fonction impure, la modification des liste est dangereuse.

        Returns:
            Stimulus:
        """
        print(
            f"#pool vu: {len(self.pool_vus_une_fois)}, #pool non vu: {len(self.pool_non_vus)}"  # noqa: E501
        )
        for stimulus in self.pool_vus_une_fois:
            if stimulus.lag == 0:
                return stimulus
        stimulus = self.pool_non_vus[0]
        stimulus.lag = self.lag_global
        stimulus.lag_initial = self.lag_global
        self.pool_vus_une_fois.append(stimulus)
        self.pool_non_vus.pop(0)
        return stimulus

    def guess_next_stimulus_id(self) -> int:
        """Renvoie l'id du futur stimulus.

        Ne mets pas à jour le stimulus actuel (current_stimulus) !

        Returns:
            int
        """
        for stimulus in self.pool_vus_une_fois:
            if stimulus.lag == 0:
                return stimulus.id
        return self.pool_non_vus[0].id

    def update_current_stimulus(self) -> None:
        """Met à jour le stimulus actuel.

        current_stimulus mis à jour.
        lag des stimuli vus mis à jour.
        """
        self.current_stimulus = self.choix_prochain_stimulus()
        self.mise_a_jour_lag_pool_vu()

    def deroulement_un_tour(self) -> None:
        """
        Un tour de jeu.
        D'abord on choisi le prochain stimulus à afficher.
        Puis on pose la question sur ce stimulus.
        Suivant la réponse (bonne ou mauvaise) on ajuste le lag global.
        """
        self.update_current_stimulus()
        print(f"Lag: {self.lag_global}, status : {self.current_stimulus.statut}")
        reponse_du_sujet = self.fonction_question_au_sujet()
        self.traitement_reponse_sujet(reponse_du_sujet=reponse_du_sujet)

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
            for stimulus in self.pool_vus_une_fois:
                if stimulus.statut == StatusStimulus.vu_deux_fois:
                    self.pool_vus_une_fois.remove(stimulus)
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
