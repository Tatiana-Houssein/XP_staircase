import pickle
from typing import Any

from back.config import PICKEL_PATH
from back.src.enum_constantes import ReponseSujet
from back.src.ia import get_ia_flag
from back.src.meta_experiment import MetaExperiment
from back.src.tache_interferente import question_tache_interferente


def create_new_experiment() -> None:
    meta_experiment = MetaExperiment()
    save_experiment(meta_experiment)


def save_experiment(meta_experiement: MetaExperiment) -> None:
    with open(PICKEL_PATH, "wb") as f:
        pickle.dump(meta_experiement, f)


def load_experiment() -> MetaExperiment:
    with open(PICKEL_PATH, "rb") as f:
        return pickle.load(f)  # noqa: S301


def call_back_next_stimulus() -> dict[str, Any]:
    meta_experiment = load_experiment()
    meta_experiment.experiment.update_current_stimulus()
    save_experiment(meta_experiment)
    flag_ia = get_ia_flag(
        tableau_proportion_resultat_experience=meta_experiment.tableau_proportion,
        status_stimulus=meta_experiment.experiment.current_stimulus.statut,
        strategy_ia=meta_experiment.strategy_ia,
    )

    print(
        f"CURRENT: {meta_experiment.experiment.current_stimulus.id}, NEXT: {meta_experiment.experiment.guess_next_stimulus_id()}"  # noqa: E501
    )
    return {
        "metaExperimentState": meta_experiment.state,
        "currentId": meta_experiment.experiment.current_stimulus.id,
        "currentIaDisplay": flag_ia,
        "nextId": meta_experiment.experiment.guess_next_stimulus_id(),
        "nextIaDisplay": "non",
        "questionInterferente": question_tache_interferente(),
    }


def call_back_answer(deja_vu: bool) -> None:  # noqa: FBT001
    answer = ReponseSujet.vu if deja_vu else ReponseSujet.non_vu
    meta_experiment = load_experiment()
    meta_experiment.experiment.traitement_reponse_sujet(answer)
    save_experiment(meta_experiment)
