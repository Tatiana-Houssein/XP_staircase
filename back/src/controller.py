import pickle
import random

from back.config import PICKEL_PATH
from back.src.constantes import LAG_INITIAL, TAILLE_POOL_NON_VU
from back.src.experiment import Experience, Stimulus, le_sujet_repond


def start_new_experiment() -> Experience:
    list_id = list(range(1, TAILLE_POOL_NON_VU))
    random.shuffle(list_id)
    return Experience(
        liste_stimuli=[Stimulus(i) for i in list_id],
        lag_initial=LAG_INITIAL,
        fonction_question_au_sujet=le_sujet_repond,
    )


def save_experiment(experiment: Experience) -> None:
    with open(PICKEL_PATH, "wb") as f:
        pickle.dump(experiment, f)


def load_experiment() -> Experience:
    with open(PICKEL_PATH, "rb") as f:
        return pickle.load(f)  # noqa: S301
