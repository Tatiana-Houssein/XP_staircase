from enum import StrEnum


class TypeErreur(StrEnum):
    detection_correct = "detection correct"  # sujet vu & stimulus vu
    omission = "omission"  # sujet non vu VS stimulus vu
    fausse_alarme = "fausse alarme"  # sujet vu VS stimulus non vu
    rejet_correct = "rejet correct"  # sujet non vu VS stimulus non vu


class StatusStimulus(StrEnum):
    vu = "vu"
    non_vu = "non vu"
    vu_deux_fois = "vu deux fois"


class ReponseSujet(StrEnum):
    vu = "vu"
    non_vu = "non vu"


class ReponseIA(StrEnum):
    vu = "vu"
    non_vu = "non vu"


class TypeReponseSujet(StrEnum):
    succes = "succes"
    echec = "echec"
    osef = "osef"
