from __future__ import annotations

import random as rd
from dataclasses import dataclass

from scipy.stats import norm

from back.src.enum_constantes import FlagIA, StatusStimulus, StrategyIA


def get_ia_flag(
    tableau_proportion_resultat_experience: TableProportionResultExperiment,
    status_stimulus: str,
    strategy_ia: StrategyIA,
) -> FlagIA:
    if strategy_ia == StrategyIA.sans_ia:
        return FlagIA.pas_de_flag
    probabilite_vu_par_ia = (
        tableau_proportion_resultat_experience.probabilite_flag_ia_vu(
            status_reel=status_stimulus
        )
    )
    u = rd.random()  # noqa: S311
    if u < probabilite_vu_par_ia:
        return FlagIA.vu
    return FlagIA.non_vu


@dataclass
class TableCardinalResultExperiment:
    """Tableau des cardinaux des résultats.

    Attention : ommissions et fausses alarmes sont au minimum à 1 !!
    """

    ommissions: int
    detections_correctes: int
    rejets_corrects: int
    fausses_alarmes: int

    def transfert_ommissions_to_fausses_alarmes(self) -> TableCardinalResultExperiment:
        transferred_ommissions = self.ommissions - 1
        return TableCardinalResultExperiment(
            1,
            self.detections_correctes,
            self.rejets_corrects,
            self.fausses_alarmes + transferred_ommissions,
        )

    def transfert_fausses_alarmes_to_ommissions(self) -> TableCardinalResultExperiment:
        transferred_fausses_alarmes = self.fausses_alarmes - 1
        return TableCardinalResultExperiment(
            self.ommissions + transferred_fausses_alarmes,
            self.detections_correctes,
            self.rejets_corrects,
            1,
        )

    def get_corresponding_tableau_proportion(self) -> TableProportionResultExperiment:
        total = (
            self.ommissions
            + self.detections_correctes
            + self.rejets_corrects
            + self.fausses_alarmes
        )
        return TableProportionResultExperiment(
            self.ommissions / total,
            self.detections_correctes / total,
            self.rejets_corrects / total,
            self.fausses_alarmes / total,
        )


@dataclass
class TableProportionResultExperiment:
    ommissions: float
    detections_correctes: float
    rejets_corrects: float
    fausses_alarmes: float

    @property
    def d_prime(self) -> float:
        return compute_d_prime(self.detections_correctes, self.fausses_alarmes)

    def probabilite_flag_ia_vu(self, status_reel: str) -> float:
        if status_reel == StatusStimulus.vu:
            return self.detections_correctes / (
                self.detections_correctes + self.ommissions
            )
        return self.fausses_alarmes / (self.fausses_alarmes + self.rejets_corrects)

    def get_tableau_fitting_given_d_prime(
        self, original_d_prime: float
    ) -> TableProportionResultExperiment:
        new_detection_correct = (
            find_new_detection_correct_corresponding_original_d_prime(
                original_d_prime, self.fausses_alarmes
            )
        )
        new_rejet_correct = (
            1 - self.ommissions - self.fausses_alarmes - new_detection_correct
        )

        return TableProportionResultExperiment(
            self.ommissions,
            new_detection_correct,
            new_rejet_correct,
            self.fausses_alarmes,
        )


def compute_d_prime(
    proportion_detection_correctes: float, proportion_fausses_alarmes: float
) -> float:
    """Given DC and FA, return d'.

    d' = phi(DC) - phi(FA),

    where phi est Norm.S.inv.
    """
    phi_dc = normal_inverse_cumulative_distribution_function(
        proportion_detection_correctes
    )
    phi_fa = normal_inverse_cumulative_distribution_function(proportion_fausses_alarmes)
    return phi_dc - phi_fa


def find_new_detection_correct_corresponding_original_d_prime(
    original_d_prime: float,
    modified_fausse_alarme: float,
) -> float:
    """Return a proportion of detection_correct who fit d'.

    On a d' = phi(x) - phi(y)
    avec
    * phi fonction normale inverse
    * x les DC
    * y les FA

    Si on impose y' de nouvelles FA et que l'on souhaite garder d',
    Alors on cherche x' tel que :
    phi(x') = d' + phi(y')
    'où x' = phi^{-1}(d' + phi(y'))

    Args:
        original_d_prime (float): le d' orginel a fitter
        modified_fausse_alarme (float): la prop de FA modifiée

    Returns:
        float: _description_
    """
    return normal_cumulative_distribution_function(
        original_d_prime
        + normal_inverse_cumulative_distribution_function(modified_fausse_alarme)
    )


def normal_inverse_cumulative_distribution_function(x: float) -> float:
    """Equivalent de l'Excel Norm.S.inv

    Args:
        x (float): _description_

    Returns:
        float: _description_
    """
    return norm.ppf(x)


def normal_cumulative_distribution_function(x: float) -> float:
    """Equivalent de l'Excel Norm.S

    Args:
        x (float): _description_

    Returns:
        float: _description_
    """
    return norm.cdf(x)
