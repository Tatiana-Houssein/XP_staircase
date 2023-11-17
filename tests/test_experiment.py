from src.experiment import Experience, Stimulus
import random as rd

class ExperienceTest(Experience):
    def __init__(self, liste_stimuli: list[Stimulus], lag_initial: int, performance_ia: float) -> None:
        super().__init__(liste_stimuli, lag_initial)
        self.perforance_ia = performance_ia
    
    def question_au_sujet_maj_lag_global_et_status_stimulus(self, stimulus: Stimulus)-> None:
        """
        L'IA répond correctement à chaque fois.
        """
        u = rd.random()
        print(f"lag global: {self.lag_global}")
        if u < self.perforance_ia: # l'IA répond correctement
            reponse_du_sujet:str = stimulus.correct_response()
        else:
            if stimulus.correct_response() == 'Y':
                reponse_du_sujet = 'N'
            else:
                reponse_du_sujet = 'Y'
        if reponse_du_sujet == stimulus.correct_response():
            self.lag_global += 1
        else: 
            self.lag_global -= 1
        print(f"Sujet: {reponse_du_sujet} VS Correct {stimulus.correct_response()}")
        stimulus.mise_a_jour_status()


if __name__ == "__main__":

    liste_stimuli = []
    for i in range(1000):
        liste_stimuli.append(Stimulus(str(i)))
    experience_test = ExperienceTest(liste_stimuli,10, 0.51)
    experience_test.deroulement_expe()
