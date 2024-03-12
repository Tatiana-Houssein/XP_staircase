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
    TableCardinalResultExperiment,
    TableProportionResultExperiment,
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
        max(1, ommission), detection_correct, rejet_correct, max(1, fausse_alarme)
    )


class MetaExperiment:
    def __init__(self) -> None:
        self.date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")  # noqa: DTZ005
        self.state: StateMetaExperiment = StateMetaExperiment.first
        self.dict_state_list_stimuli = get_dict_of_list_stimuli_for_meta_experiment()
        self.experiment: Experiment = self.initialisation_new_experiment()
        self.tableau_proportion: TableProportionResultExperiment = (
            TABLEAU_PROPORTION_SUR
        )
        self.strategy_ia: StrategyIA = StrategyIA.sans_ia
        self.current_flag_ia = FlagIA.pas_de_flag
        self.setup_directories()

    def setup_directories(self) -> None:
        print(self.date)
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
            self.state = go_to_next_state_meta_experiment(self.state)
            self.strategy_ia = DICT_STATE_META_TO_STRATEGY_IA[self.state]
            tableau_cardinaux = extract_table_cardinaux_from_list_result(
                self.experiment.liste_resultat
            )
            print(f"card reel {tableau_cardinaux}")
            tableau_prop_ini = tableau_cardinaux.get_corresponding_tableau_proportion()
            print(f"prop ini {tableau_prop_ini}")
            d_prime = tableau_prop_ini.d_prime
            print(f"d' ini {d_prime}")
            if self.strategy_ia == StrategyIA.sans_fausses_alarmes:
                tableau_cardinaux = extract_table_cardinaux_from_list_result(
                    self.experiment.liste_resultat
                ).transfert_fausses_alarmes_to_ommissions()
            else:
                tableau_cardinaux = extract_table_cardinaux_from_list_result(
                    self.experiment.liste_resultat
                ).transfert_ommissions_to_fausses_alarmes()
            print(f"card transfert {tableau_cardinaux}")
            tableau_prop_tran = tableau_cardinaux.get_corresponding_tableau_proportion()
            print(f"prop apres tran avant fit {tableau_prop_tran}")
            print(f"d' tran {tableau_prop_tran.d_prime}")
            self.tableau_proportion = (
                tableau_prop_tran.get_tableau_fitting_given_d_prime(d_prime)
            )
            print(f"prop fitté {self.tableau_proportion}")
            print(f"d' fité {self.tableau_proportion.d_prime}")
            if self.state != StateMetaExperiment.finish:
                self.experiment = self.initialisation_new_experiment()
                print(self.experiment.guess_next_stimulus_id())
