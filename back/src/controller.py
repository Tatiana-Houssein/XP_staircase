import pickle
import random

from back.config import PICKEL_PATH
from back.src.constantes import LAG_INITIAL, TAILLE_POOL_NON_VU
from back.src.enum_constantes import ReponseSujet
from back.src.experiment import Experience, Stimulus, le_sujet_repond


def create_new_experiment() -> None:
    list_id = list(range(1, TAILLE_POOL_NON_VU))
    random.shuffle(list_id)

    experiment = Experience(
        liste_stimuli=[Stimulus(i) for i in list_id],
        lag_initial=LAG_INITIAL,
        fonction_question_au_sujet=le_sujet_repond,
    )
    print(f"AAA, {experiment.current_stimulus}")
    save_experiment(experiment)


def save_experiment(experiment: Experience) -> None:
    with open(PICKEL_PATH, "wb") as f:
        pickle.dump(experiment, f)


def load_experiment() -> Experience:
    with open(PICKEL_PATH, "rb") as f:
        return pickle.load(f)  # noqa: S301


def call_back_next_stimulus() -> int:
    experiment = load_experiment()
    experiment.update_current_stimulus()
    print(f"BBB, {experiment.current_stimulus.numero}")
    save_experiment(experiment)
    return experiment.current_stimulus.numero


def call_back_answer(deja_vu: bool) -> None:  # noqa: FBT001
    answer = ReponseSujet.vu if deja_vu else ReponseSujet.non_vu
    experiment = load_experiment()
    print(experiment.lag_global)
    experiment.traitement_reponse_sujet(answer)
    save_experiment(experiment)
    print(experiment.lag_global)
