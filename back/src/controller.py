import pickle
from typing import Any

from back.config import PICKEL_PATH
from back.src.constantes import LAG_INITIAL, TABLEAU_PROPORTION_SUR
from back.src.enum_constantes import ReponseSujet, StrategyIA
from back.src.experiment import (
    Experience,
    initialisation_liste_des_stimuli,
    le_sujet_repond,
)
from back.src.ia import get_ia_flag
from back.src.tache_interferente import question_tache_interferente


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


def call_back_next_stimulus() -> dict[str, Any]:
    experiment = load_experiment()
    experiment.update_current_stimulus()
    print(f"BBB, {experiment.current_stimulus.id}")
    save_experiment(experiment)
    flag_ia = get_ia_flag(
        tableau_proportion_resultat_experience=TABLEAU_PROPORTION_SUR,
        status_stimulus=experiment.current_stimulus.statut,
        strategy_ia=StrategyIA.sans_fausses_alarmes,
    )
    return {
        "currentId": experiment.current_stimulus.id,
        "currentIaDisplay": flag_ia,
        "nextId": experiment.guess_next_stimulus_id(),
        "nextIaDisplay": "non",
        "questionInterferente": question_tache_interferente(),
    }


def call_back_answer(deja_vu: bool) -> None:  # noqa: FBT001
    answer = ReponseSujet.vu if deja_vu else ReponseSujet.non_vu
    experiment = load_experiment()
    print(experiment.lag_global)
    experiment.traitement_reponse_sujet(answer)
    save_experiment(experiment)
    print(experiment.lag_global)
