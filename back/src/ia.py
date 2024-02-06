from __future__ import annotations

from dataclasses import dataclass

from scipy.stats import norm

from back.src.enum_constantes import StatusStimulus


@dataclass
class TableauCardinalResultatExperience:
    """Tableau des cardinaux des résultats.

    Attention : ommissions et fausses alarmes sont au minimum à 1 !!
    """

    ommissions: int
    detections_correctes: int
    rejets_corrects: int
    fausses_alarmes: int

    def transfert_ommissions_to_fausses_alarmes(
        self
    ) -> TableauCardinalResultatExperience:
        transferred_ommissions = self.ommissions - 1
        return TableauCardinalResultatExperience(
            1,
            self.detections_correctes,
            self.rejets_corrects,
            self.fausses_alarmes + transferred_ommissions,
        )

    def transfert_fausses_alarmes_to_ommissions(
        self
    ) -> TableauCardinalResultatExperience:
        transferred_fausses_alarmes = self.fausses_alarmes - 1
        return TableauCardinalResultatExperience(
            self.ommissions + transferred_fausses_alarmes,
            self.detections_correctes,
            self.rejets_corrects,
            1,
        )


@dataclass
class TableauProportionResultatExperience:
    ommissions: float
    detections_correctes: float
    rejets_corrects: float
    fausses_alarmes: float

    @property
    def d_prime(self) -> float:
        return compute_d_prime(self.detections_correctes, self.fausses_alarmes)

    def probabilite_de_lever_le_flag_vu_selon_status_reel(
        self, status_reel: StatusStimulus
    ) -> float:
        if status_reel == StatusStimulus.vu:
            return self.detections_correctes / (
                self.detections_correctes + self.ommissions
            )
        return self.fausses_alarmes / (self.fausses_alarmes + self.rejets_corrects)

    def get_tableau_fitting_given_d_prime(
        self, original_d_prime: float
    ) -> TableauProportionResultatExperience:
        new_detection_correct = (
            find_new_detection_correct_corresponding_original_d_prime(
                original_d_prime, self.fausses_alarmes
            )
        )
        new_rejet_correct = (
            1 - self.ommissions - self.fausses_alarmes - new_detection_correct
        )

        return TableauProportionResultatExperience(
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
