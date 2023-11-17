from src.resultat import Resultat
import pandas as pd


class Stimulus:
    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.statut: str = "non vu"
        self.correct_responses = self.correct_response()
        self.lag = 0

    def correct_response(self) -> str:
        if self.statut == "non vu":
            self.correct_responses = "N"
        else:
            self.correct_responses = "Y"
        return self.correct_responses

    def mise_a_jour_status(self) -> None:
        if self.statut == "non vu":
            self.statut = "vu"
        elif self.statut == "vu":
            self.statut = "vu deux fois"


class Experience:
    def __init__(self, liste_stimuli: list[Stimulus], lag_initial: int) -> None:
        self.pool_non_vus = liste_stimuli  ###########
        self.pool_vus: list[Stimulus] = []  ###########
        self.lag_global = lag_initial
        self.tour: int = 0
        self.liste_resultat: list[Resultat] = []

    def attribution_du_lag(self, stimulus: Stimulus) -> None:
        """
        Attribution des lag quand il est non-vu on lui attribue un lag correspondant au lag général de l'expe
        """
        if stimulus.statut == "non vu":
            stimulus.lag = self.lag_global

    def mise_a_jour_lag_pool_vu(self) -> None:
        """
        On abaisse de 1 le lag de tous les stimuli présents dans pool_vus
        """
        for stimulus in self.pool_vus:
            stimulus.lag -= 1
            if stimulus.lag < 0:
                stimulus.lag = 0

    def le_sujet_repond(self) -> str:
        return input("Avez vous déjà vu ce visage ?")

    def question_au_sujet_maj_lag_global_et_status_stimulus(
        self, stimulus: Stimulus
    ) -> None:
        """
        Le lag global est adapté à la bonne ou mauvaise réponse du sujet au stimulus donné,
        Puis on met à jour le status de ce stimulus (non_vu -> vu -> vu_deux_fois)
        """
        reponse_du_sujet: str = self.le_sujet_repond()
        if reponse_du_sujet == stimulus.correct_response():
            self.lag_global += 1
        else:
            self.lag_global -= 1
        print(f"Sujet: {reponse_du_sujet} VS Correct {stimulus.correct_response()}")
        resultat = Resultat(
            tour=self.tour,
            lag_global=self.lag_global,
            numero_stimulus=stimulus.numero,
            reponse_correct=stimulus.correct_response(),
            reponse_sujet=reponse_du_sujet,
        )
        self.liste_resultat.append(resultat)

        stimulus.mise_a_jour_status()

    def prochain_stimulus(self) -> Stimulus:
        for stimulus in self.pool_vus:
            if stimulus.lag == 0:
                return stimulus
        stimulus = self.pool_non_vus[0]
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
        stimulus_choisi = self.prochain_stimulus()
        self.attribution_du_lag(stimulus_choisi)  #######
        print(f"Stimulus {stimulus_choisi.numero}, status : {stimulus_choisi.statut}")
        self.mise_a_jour_lag_pool_vu()  #####
        self.question_au_sujet_maj_lag_global_et_status_stimulus(stimulus_choisi)

    def deroulement_expe(self) -> None:
        """
        D'abord, suppression des stimuli vu deux du pool_vue
        Puis, on enclenche self.deroulement_un_tout tant que les deux listes pool_vus et pool_non_vus ne sont pas vides
        Avant, on supprime de la liste tous les stimuli vu deux fois du pool_vus
        """
        while len(self.pool_non_vus) > 0:
            for stimulus in self.pool_vus:
                if stimulus.statut == "vu deux fois":
                    self.pool_vus.remove(stimulus)
            self.deroulement_un_tour()
            self.tour += 1

        # sauvegarde de la liste des résultats
        df_result = pd.DataFrame(
            self.liste_resultat,
            columns=[
                "tour",
                "lag_global",
                "numero_stimulus",
                "reponse_correct",
                "reponse_sujet",
            ],
        )
        df_result.to_csv("data/results.csv", index=False)
