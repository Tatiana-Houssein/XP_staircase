import pickle
from dataclasses import asdict
from typing import Any

from back.config import PICKEL_PATH
from back.src.enum_constantes import ReponseSujet, StateMetaExperiment
from back.src.ia import get_ia_flag
from back.src.io import load_form_data, save_form, save_result
from back.src.meta_experiment import MetaExperiment
from back.src.tache_interferente import (
    create_tache_interferente_data,
    question_tache_interferente,
)


def create_new_experiment() -> None:
    meta_experiment = MetaExperiment()
    save_experiment(meta_experiment)


def save_experiment(meta_experiement: MetaExperiment) -> None:
    with open(PICKEL_PATH, "wb") as f:
        pickle.dump(meta_experiement, f)


def load_experiment() -> MetaExperiment:
    with open(PICKEL_PATH, "rb") as f:
        return pickle.load(f)  # noqa: S301


def save_form_data(
    form_data: dict[str, Any],
) -> None:
    meta_experiment = load_experiment()
    yaml_path_file = f"data/{meta_experiment.date}/form.yaml"
    # Load existing form data
    existing_data = load_form_data(yaml_path_file=yaml_path_file)

    # Merge new form data with existing data
    existing_data.update(form_data)

    # Save merged data to YAML file
    save_form(form_data=existing_data, yaml_path_file=yaml_path_file)


def call_back_next_stimulus() -> dict[str, Any]:
    meta_experiment = load_experiment()
    if meta_experiment.experiment.guess_next_stimulus_id() == -1:
        save_result(
            liste_resultat=meta_experiment.experiment.liste_resultat,
            root_directory=f"data/{meta_experiment.date}",
            csv_file_name=str(meta_experiment.state),
        )

        meta_experiment.update_meta_experiment_state()
        print(meta_experiment.tableau_proportion)
    if meta_experiment.state != StateMetaExperiment.finish:
        meta_experiment.experiment.update_current_stimulus()
    meta_experiment.current_flag_ia = get_ia_flag(
        tableau_proportion_resultat_experience=meta_experiment.tableau_proportion,
        status_stimulus=meta_experiment.experiment.current_stimulus.statut,
        strategy_ia=meta_experiment.strategy_ia,
    )
    save_experiment(meta_experiment)
    print(
        f"CURRENT: {meta_experiment.experiment.current_stimulus.id}, NEXT: {meta_experiment.experiment.guess_next_stimulus_id()}"  # noqa: E501
    )
    return {
        "metaExperimentState": meta_experiment.state,
        "currentId": meta_experiment.experiment.current_stimulus.id,
        "currentIaDisplay": meta_experiment.current_flag_ia,
        "nextId": meta_experiment.experiment.guess_next_stimulus_id(),
        "nextIaDisplay": "non",
        "questionInterferente": question_tache_interferente(),
    }


def call_back_answer(chosen_number: int) -> None:
    answer = ReponseSujet.vu if chosen_number >= 4 else ReponseSujet.non_vu  # noqa: PLR2004
    meta_experiment = load_experiment()
    meta_experiment.experiment.traitement_reponse_sujet(
        answer,
        nombre_sujet=chosen_number,
        flag_ia=meta_experiment.current_flag_ia,
    )
    save_experiment(meta_experiment)


def get_dict_tache_interferente() -> dict[str, Any]:
    """Return a dict of the tache_interfrente paramters

    Returns:
        _type_: _description_
    """
    tache_inter = create_tache_interferente_data()
    return asdict(tache_inter)
