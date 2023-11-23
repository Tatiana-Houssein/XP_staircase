import random

import streamlit as st
import streamlit.components.v1 as components

from back.experiment import (
    Experience,
    ReponseSujet,
    StatusStimulus,
    Stimulus,
    TypeSucces,
    save_result,
)
from back.resultat import Resultat
from front.experiment_js import js_script_optimized

col1, col2, col3, col4 = st.columns(4)
LIMIT_BEFORE_DATA_SAVING = 160


def api_sauvegarde_du_resultat() -> None:
    """Fonction spécifique du front pour écrire le CSV de résultat."""
    st.session_state["id_face"] = -1
    liste_resultat = st.session_state["experiment"].liste_resultat
    save_result(liste_resultat)


def display_face(id_face: int) -> None:
    path = f"tokens/token_{id_face}.png"
    st.image(path)


if "experiment" not in st.session_state:
    list_id = list(range(1, 120))
    random.shuffle(list_id)
    l_stim = [Stimulus(i) for i in list_id]
    st.session_state["experiment"] = Experience(
        l_stim,
        5,
    )


if "current_stimulus" not in st.session_state:
    st.session_state["current_stimulus"] = st.session_state[
        "experiment"
    ].prochain_stimulus()

if "id_face" not in st.session_state:
    st.session_state["id_face"] = st.session_state["current_stimulus"].numero


def anwser_to_face_recognition(reponse_du_sujet: str) -> None:
    experiment: Experience = st.session_state["experiment"]
    print(f"EEEEEEEEEEEEEEEEEEEE {experiment.tour} EEEEEEEEEEEEEEEEE")
    current_stimulus: Stimulus = st.session_state["current_stimulus"]
    if (
        experiment.is_sujet_right(reponse_du_sujet, current_stimulus.statut)
        == TypeSucces.succes
    ):
        experiment.lag_global += 1
    elif (
        experiment.is_sujet_right(reponse_du_sujet, current_stimulus.statut)
        == TypeSucces.echec
    ):
        experiment.lag_global -= 1
    resultat = Resultat(
        tour=experiment.tour,
        lag_global=experiment.lag_global,
        lag_initial_stimulus=current_stimulus.lag_initial,
        numero_stimulus=current_stimulus.numero,
        reponse_correct=str(current_stimulus.statut),
        reponse_sujet=str(reponse_du_sujet),
        type_erreur_tds=str(
            experiment.type_erreur_du_sujet(reponse_du_sujet, current_stimulus.statut)
        ),
    )
    experiment.liste_resultat.append(resultat)
    experiment.mise_a_jour_lag_pool_vu()
    current_stimulus.mise_a_jour_status()
    if current_stimulus.statut == StatusStimulus.vu_deux_fois:
        experiment.pool_vus.remove(current_stimulus)
    current_stimulus = experiment.prochain_stimulus()
    experiment.tour += 1
    st.session_state["experiment"] = experiment
    st.session_state["current_stimulus"] = current_stimulus

    st.session_state["id_face"] = current_stimulus.numero


def answer_vu() -> None:
    if st.session_state["experiment"].is_condition_arret_remplie():
        api_sauvegarde_du_resultat()
    else:
        anwser_to_face_recognition(ReponseSujet.vu)


def answer_non_vu() -> None:
    if st.session_state["experiment"].is_condition_arret_remplie():
        api_sauvegarde_du_resultat()
    else:
        anwser_to_face_recognition(ReponseSujet.non_vu)


components.html(
    js_script_optimized,
    height=0,
    width=0,
)
with st.sidebar:
    st.button("L", on_click=answer_non_vu, key="L")
    st.button("R", on_click=answer_vu, key="R")
    st.button("LEFT", on_click=answer_non_vu, key="LEFT", use_container_width=True)
    st.button("RIGHT", on_click=answer_vu, key="RIGHT", use_container_width=True)

display_face(st.session_state["id_face"])
