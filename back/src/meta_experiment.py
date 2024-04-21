import os
from datetime import datetime

from back.src.constantes import (
    DICT_STATE_META_TO_STRATEGY_IA,
    LAG_INITIAL,
    TABLEAU_PROPORTION_SUR,
)
from back.src.enum_constantes import FlagIA, StateMetaExperiment, StrategyIA, TypeErreur
from back.src.experiment import (
    Experiment,
    get_dict_of_list_stimuli_for_meta_experiment,
    le_sujet_repond,
)
from back.src.ia import (
    TableCardinal,
    TableStochastic,
)
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
) -> TableCardinal:
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
    return TableCardinal(
        max(1, ommission), detection_correct, rejet_correct, max(1, fausse_alarme)
    )


def get_table_proportion_fitting_d_prime_from_list_result(
    d_prime_to_fit: float,
    list_result: list,
    strategy_ia: StrategyIA,
) -> TableStochastic:
    print(f"d' phase 1 : {d_prime_to_fit}")
    print(
        f"new table card pre transf: {extract_table_cardinaux_from_list_result(list_result)}"  # noqa: E501
    )
    if strategy_ia == StrategyIA.sans_fausses_alarmes:
        table_cardinaux = extract_table_cardinaux_from_list_result(
            list_result
        ).transfert_fausses_alarmes_to_ommissions()
    else:
        table_cardinaux = extract_table_cardinaux_from_list_result(
            list_result
        ).transfert_ommissions_to_fausses_alarmes()
    print(f"table card post transfert : {table_cardinaux}")
    table_prop_pre_fit = table_cardinaux.get_corresponding_table_stochastic()
    print(f"new d' pre-fit : {table_prop_pre_fit.d_prime}")
    table_prop_post_fit = table_prop_pre_fit.get_tableau_fitting_given_d_prime(
        d_prime_to_fit
    )
    print(f"d' fité {table_prop_post_fit.d_prime}")
    return table_prop_post_fit


class MetaExperiment:
    def __init__(self) -> None:
        self.date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")  # noqa: DTZ005
        self.state: StateMetaExperiment = StateMetaExperiment.first
        self.dict_state_list_stimuli = get_dict_of_list_stimuli_for_meta_experiment()
        self.experiment: Experiment = self.initialisation_new_experiment()
        self.tableau_proportion: TableStochastic = TABLEAU_PROPORTION_SUR
        self.strategy_ia: StrategyIA = StrategyIA.sans_ia
        self.current_flag_ia = FlagIA.pas_de_flag
        self.setup_directories()

    def setup_directories(self) -> None:
        print(f"create data/{self.date} directory")
        os.makedirs(f"data/{self.date}")  # noqa: PTH103

    def initialisation_new_experiment(self) -> Experiment:
        return Experiment(
            liste_stimuli=self.dict_state_list_stimuli[self.state],
            lag_initial=LAG_INITIAL,
            fonction_question_au_sujet=le_sujet_repond,
        )

    def update_meta_experiment_state(self) -> None:
        if self.experiment.guess_next_stimulus_id() == -1:
            # TOFIX: save_result(self.experiment.liste_resultat)  # noqa: ERA001
            if self.state == StateMetaExperiment.first:
                self.table_cardinaux_phase_1 = extract_table_cardinaux_from_list_result(
                    self.experiment.liste_resultat
                )
                print(f"table_card_ini {self.table_cardinaux_phase_1}")
                self.d_prime_phase_1 = self.table_cardinaux_phase_1.get_corresponding_table_stochastic().d_prime  # noqa: E501
                print(f"d' ini: {self.d_prime_phase_1}")
            self.state = go_to_next_state_meta_experiment(self.state)
            self.strategy_ia = DICT_STATE_META_TO_STRATEGY_IA[self.state]

            self.tableau_proportion = (
                get_table_proportion_fitting_d_prime_from_list_result(
                    d_prime_to_fit=self.d_prime_phase_1,
                    list_result=self.experiment.liste_resultat,
                    strategy_ia=self.strategy_ia,
                )
            )
            if self.state != StateMetaExperiment.finish:
                self.experiment = self.initialisation_new_experiment()
                print(self.experiment.guess_next_stimulus_id())
