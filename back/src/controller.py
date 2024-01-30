import pickle

from back.config import PICKEL_PATH
from back.src.constantes import LAG_INITIAL
from back.src.enum_constantes import ReponseSujet
from back.src.experiment import (
    Experience,
    initialisation_liste_des_stimuli,
    le_sujet_repond,
)


def create_new_experiment() -> None:
    experiment = Experience(
        liste_stimuli=initialisation_liste_des_stimuli(),
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


def call_back_next_stimulus() -> dict[str, int]:
    experiment = load_experiment()
    experiment.update_current_stimulus()
    print(f"BBB, {experiment.current_stimulus.id}")
    save_experiment(experiment)
    return {
        "id": experiment.current_stimulus.id,
        "nextId": experiment.guess_next_stimulus_id(),
        "lagInitial": experiment.current_stimulus.lag_initial,
    }


def call_back_answer(deja_vu: bool) -> None:  # noqa: FBT001
    answer = ReponseSujet.vu if deja_vu else ReponseSujet.non_vu
    experiment = load_experiment()
    print(experiment.lag_global)
    experiment.traitement_reponse_sujet(answer)
    save_experiment(experiment)
    print(experiment.lag_global)
