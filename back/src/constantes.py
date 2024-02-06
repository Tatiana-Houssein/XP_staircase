from back.src.ia import TableauProportionResultatExperience

AUGMENTATION_LAG = 1
DIMINUTION_LAG = 2
LAG_INITIAL = 3
TAILLE_POOL_NON_VU = 15  # 160
TEMPS_EXPOSITION = 0.3  # en milliseconds
PICKLE_NAME = "experiment.pkl"
PREFIX_STIMULUS = "visages/visage-"  # tokens/token_
TABLEAU_PROPORTION_SUR = TableauProportionResultatExperience(1, 1000, 1000, 1)
