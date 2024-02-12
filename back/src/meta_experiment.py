from back.src.constantes import (
    DICT_STATE_META_TO_STRATEGY_IA,
    LAG_INITIAL,
    TABLEAU_PROPORTION_SUR,
)
from back.src.enum_constantes import StateMetaExperiment, StrategyIA, TypeErreur
from back.src.experiment import (
    Experiment,
    get_dict_of_list_stimuli_for_meta_experiment,
    le_sujet_repond,
)
from back.src.ia import (
    TableCardinalResultExperiment,
    TableProportionResultExperiment,
)
from back.src.io import save_result
from back.src.resultat import ResultExperiment


def go_to_next_state_meta_experiment(
    current_state: StateMetaExperiment
) -> StateMetaExperiment:
    if current_state == StateMetaExperiment.first:
        return StateMetaExperiment.second
    if current_state == StateMetaExperiment.second:
        return StateMetaExperiment.third
    return StateMetaExperiment.finish


def extract_table_cardinaux_from_list_result(
    list_result: list[ResultExperiment]
) -> TableCardinalResultExperiment:
    ommission = 0
    detection_correct = 0
    rejet_correct = 0
    fausse_alarme = 0
    for result in list_result:
        if result.type_erreur_tds == TypeErreur.omission:
            ommission += 1
        elif result.type_erreur_tds == TypeErreur.detection_correct:
            detection_correct += 1
        elif result.type_erreur_tds == TypeErreur.rejet_correct:
            rejet_correct += 1
        else:
            fausse_alarme += 1
    return TableCardinalResultExperiment(
        ommission, detection_correct, rejet_correct, fausse_alarme
    )


class MetaExperiment:
    def __init__(self) -> None:
        self.state: StateMetaExperiment = StateMetaExperiment.first
        self.dict_state_list_stimuli = get_dict_of_list_stimuli_for_meta_experiment()
        self.experiment: Experiment = self.initialisation_new_experiment()
        self.tableau_proportion: TableProportionResultExperiment = (
            TABLEAU_PROPORTION_SUR
        )
        self.strategy_ia: StrategyIA = StrategyIA.sans_ia

    def initialisation_new_experiment(self) -> Experiment:
        return Experiment(
            liste_stimuli=self.dict_state_list_stimuli[self.state],
            lag_initial=LAG_INITIAL,
            fonction_question_au_sujet=le_sujet_repond,
        )

    def update_meta_experiment_state(self) -> None:
        if self.experiment.current_stimulus.id == -1:
            save_result(self.experiment.liste_resultat)
            self.state = go_to_next_state_meta_experiment(self.state)
            self.strategy_ia = DICT_STATE_META_TO_STRATEGY_IA[self.state]
            tableau_cardinaux = extract_table_cardinaux_from_list_result(
                self.experiment.liste_resultat
            )
            if self.strategy_ia == StrategyIA.sans_fausses_alarmes:
                tableau_cardinaux = extract_table_cardinaux_from_list_result(
                    self.experiment.liste_resultat
                ).transfert_fausses_alarmes_to_ommissions()
            else:
                tableau_cardinaux = extract_table_cardinaux_from_list_result(
                    self.experiment.liste_resultat
                ).transfert_ommissions_to_fausses_alarmes()
            self.tableau_proportion = (
                tableau_cardinaux.get_corresponding_tableau_proportion()
            )
            self.experiment = self.initialisation_new_experiment()
