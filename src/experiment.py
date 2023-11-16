class Stimulus:
    def __init__(self, numero: str) -> None:
        self.numero = numero
        self.statut: str = "non vu"
        self.correct_responses = self.correct_response()
        self.lag = 0
    def correct_response(self)-> str:
        if self.statut == "non vu":
            self.correct_responses = "N"
        else :
            self.correct_responses = "Y"
        return self.correct_responses
    def mise_a_jour_status(self) -> None:
        if self.statut == "non vu":
            self.statut = "vu"
        elif self.statut == "vu":
            self.statut = "vu deux fois"
        

class Experience:
    def __init__(self, liste_stimuli : list[Stimulus], lag_initial:int) -> None:
        self.pool_non_vus = liste_stimuli ###########
        self.pool_vus : list[Stimulus] = []  ###########  
        self.lag_global = lag_initial

    def mise_a_jour_des_listes(self, stimulus : Stimulus)-> None: ################
        if stimulus == "vu":
            self.pool_non_vus.remove(stimulus)
            self.pool_vus.append(stimulus)

    def le_sujet_repond(self)->str:
        return(input("Avez vous déjà vu ce visage ?"))        

    def question_au_sujet_maj_lag_global_et_status_stimulus(self, stimulus: Stimulus)-> None:
        """
        Le lag global est adapté à la bonne ou mauvaise réponse du sujet au stimulus donné,
        Puis on met à jour le status de ce stimulus (non_vu -> vu -> vu_deux_fois)
        """
        reponse_du_sujet:str = self.le_sujet_repond()
        if reponse_du_sujet == stimulus.correct_response():
            self.lag_global += 1
            print(reponse_du_sujet, stimulus.correct_response())
        else : 
            self.lag_global -= 1
            print(reponse_du_sujet, stimulus.correct_response())
        stimulus.mise_a_jour_status()
    
    def prochain_stimulus(self)->Stimulus:
        for stimulus in self.pool_vus:
            if stimulus.lag == 0:
                return stimulus
        stimulus = self.pool_non_vus[0]
        self.pool_vus.append(stimulus)
        self.pool_non_vus.pop(0)
        return stimulus
            
    def deroulement_un_tour(self)-> None:
        """
        Un tour de jeu.
        D'abord on choisi le prochain stimulus à afficher.
        Puis on pose la question sur ce stimulus.
        Suivant la réponse (bonne ou mauvaise) on ajuste le lag global.
        """
        stimulus_choisi = self.prochain_stimulus()
        print(stimulus_choisi.numero)
        print(stimulus_choisi.statut)
        self.question_au_sujet_maj_lag_global_et_status_stimulus(stimulus_choisi)

    def vrai_si_tous_vu_deux_fois(self)-> bool:
        """
        Vérife si tous les stimuli du pool_vu sont:
            - tous vu_deux_fois -> Return True
            - au moins un 'vu' ou 'non_vu' -> Return False        
        """
        if self.pool_vus == []:
            return False
        for stimulus in self.pool_vus:
            if stimulus.statut in ["vu", "non vu"]:
                # donc pas "vu deux fois"
                return False
        return True
    
    def deroulement_expe(self) -> None:
        """
        D'abord, suppression des stimuli vu deux du pool_vue
        Puis, on enclenche self.deroulement_un_tout tant que les deux listes pool_vus et pool_non_vus ne sont pas vides
        Avant, on supprime de la liste tous les stimuli vu deux fois du pool_vus 
        """
        for stimulus in self.pool_vus:
            if stimulus.statut == "vu deux fois":
                self.pool_vus.remove(stimulus)
        while len(self.pool_vus) > 0 or len(self.pool_non_vus) > 0 :
            self.deroulement_un_tour()