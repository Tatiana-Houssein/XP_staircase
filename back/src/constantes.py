from back.src.enum_constantes import StateMetaExperiment, StrategyIA
from back.src.ia import TableStochastic

AUGMENTATION_LAG = 1
DIMINUTION_LAG = 2
LAG_INITIAL = 3
TAILLE_POOL_NON_VU = 140  # 160
TEMPS_EXPOSITION = 0.3  # en milliseconds
PICKLE_NAME = "experiment.pkl"
PREFIX_STIMULUS = "visages/visage-"  # tokens/token_
TABLEAU_PROPORTION_SUR = TableStochastic(1, 1000, 1000, 1)
DICT_STATE_META_TO_STRATEGY_IA = {
    StateMetaExperiment.first: StrategyIA.sans_ia,
    StateMetaExperiment.second: StrategyIA.sans_fausses_alarmes,
    StateMetaExperiment.third: StrategyIA.sans_ommissions,
    StateMetaExperiment.finish: StrategyIA.sans_ia,
}
