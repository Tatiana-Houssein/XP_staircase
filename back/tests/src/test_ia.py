from back.src.enum_constantes import StatusStimulus
from back.src.ia import (
    TableCardinal,
    TableStochastic,
    compute_d_prime,
    find_new_detection_correct_corresponding_original_d_prime,
    normal_cumulative_distribution_function,
    normal_inverse_cumulative_distribution_function,
)
import numpy as np


def test_tableau_cardinal_class():
    # Given
    tableau_original = TableCardinal(10, 100, 200, 20)
    # When
    result_o2f = tableau_original.transfert_ommissions_to_fausses_alarmes()
    result_f2o = tableau_original.transfert_fausses_alarmes_to_ommissions()
    # Then
    assert result_o2f == TableCardinal(1, 100, 200, 29)
    assert result_f2o == TableCardinal(29, 100, 200, 1)


def test_normal_inverse_function():
    # Given
    x = 0.9
    # When
    result = normal_inverse_cumulative_distribution_function(x)
    # Then
    assert np.isclose(result, 1.2815515655446004)


def test_normal_inverse_function_zero():
    # Given
    x = 0.0
    # When
    result = normal_inverse_cumulative_distribution_function(x)
    # Then
    assert np.isfinite(result) == False


def test_normal_function():
    # Given
    x = 1.2815515655446004
    # When
    result = normal_cumulative_distribution_function(x)
    # Then
    assert np.isclose(result, 0.9)


def test_compute_d_prime():
    # Given
    proportion_detection_correctes = 0.49
    proportion_fausses_alarmes = 0.01
    # When
    result = compute_d_prime(proportion_detection_correctes, proportion_fausses_alarmes)
    # Then
    assert np.isclose(result, 2.3012789657821298)


def test_find_new_detection_correct():
    # Given
    orgininal_d_prime = 2.3012789657821298
    modified_fausse_alarm = 0.1
    # When
    result = find_new_detection_correct_corresponding_original_d_prime(
        orgininal_d_prime, modified_fausse_alarm
    )
    # Then
    assert np.isclose(result, 0.8460711185265115)


def test_method_get_tableau_fitting_given_d_prime():
    # Given
    ommissions = 0
    detections_correctes = 0.49
    rejets_corrects = 0.49
    fausses_alarmes = 0.02
    tableau_original = TableStochastic(
        ommissions,
        detections_correctes,
        rejets_corrects,
        fausses_alarmes,
    )
    # When
    result = tableau_original.get_tableau_fitting_given_d_prime(2.3012789657821298)
    # Then
    assert result.ommissions == 0
    assert np.isclose(result.detections_correctes, 0.5977509828053289)
    assert np.isclose(result.rejets_corrects, 0.3822490171946711)
    assert np.isclose(result.fausses_alarmes, 0.02)
    assert np.isclose(result.d_prime, 2.3012789657821298)


def test_tableau_porportion_cas_hasard():
    # Given
    ommissions = 0.25
    detections_correctes = 0.25
    rejets_corrects = 0.25
    fausses_alarmes = 0.25
    tableau_original = TableStochastic(
        ommissions,
        detections_correctes,
        rejets_corrects,
        fausses_alarmes,
    )
    # When
    result = tableau_original.d_prime
    # Then
    assert result == 0


def test_method_get_tableau_fitting_given_d_prime_cas_hasard():
    # Given
    ommissions = 0.0
    detections_correctes = 0.25
    rejets_corrects = 0.25
    fausses_alarmes = 0.5
    tableau_original = TableStochastic(
        ommissions,
        detections_correctes,
        rejets_corrects,
        fausses_alarmes,
    )
    # When
    result = tableau_original.get_tableau_fitting_given_d_prime(0)
    # Then
    assert result.ommissions == 0
    assert np.isclose(result.fausses_alarmes, 0.5)
    assert np.isclose(result.detections_correctes, 0.5)
    assert np.isclose(result.rejets_corrects, 0.0)
    assert np.isclose(result.d_prime, 0)


def test_probabilite_lever_flag_vu_selon_status_reel():
    # Given
    tableau = TableStochastic(0, 1, 20, 20)
    # When
    result_status_vu = tableau.probabilite_flag_ia_vu(
        StatusStimulus.vu
    )
    result_status_non_vu = tableau.probabilite_flag_ia_vu(
        StatusStimulus.non_vu
    )
    # Then
    assert result_status_vu == 1
    assert result_status_non_vu == 0.5
