from back.src.constantes import TAILLE_POOL_NON_VU
from back.src.enum_constantes import StateMetaExperiment
from back.src.experiment import get_dict_of_list_stimuli_for_meta_experiment


def test_get_dict_of_list_stimuli_for_meta_experiment():
    dict_result = get_dict_of_list_stimuli_for_meta_experiment()

    if TAILLE_POOL_NON_VU % 3 == 0:

        assert len(dict_result[StateMetaExperiment.first]) == int(TAILLE_POOL_NON_VU / 3)
        assert len(dict_result[StateMetaExperiment.second]) == int(TAILLE_POOL_NON_VU / 3)
        assert len(dict_result[StateMetaExperiment.third]) == int(TAILLE_POOL_NON_VU / 3)
    elif TAILLE_POOL_NON_VU % 3 == 1:
        assert len(dict_result[StateMetaExperiment.first]) == int(TAILLE_POOL_NON_VU / 3)
        assert len(dict_result[StateMetaExperiment.second]) == int(TAILLE_POOL_NON_VU / 3)
        assert len(dict_result[StateMetaExperiment.third]) == int(TAILLE_POOL_NON_VU / 3)+1
    elif TAILLE_POOL_NON_VU % 3 == 2:
        assert len(dict_result[StateMetaExperiment.first]) == int(TAILLE_POOL_NON_VU / 3)
        assert len(dict_result[StateMetaExperiment.second]) == int(TAILLE_POOL_NON_VU / 3)+1
        assert len(dict_result[StateMetaExperiment.third]) == int(TAILLE_POOL_NON_VU / 3)+1
