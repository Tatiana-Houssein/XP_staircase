import csv

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from front.experiment_js import js_script_optimized
from src.experiment import (
    Experience,
    ReponseSujet,
    StatusStimulus,
    Stimulus,
)
from src.resultat import Resultat

col1, col2, col3, col4 = st.columns(4)
LIMIT_BEFORE_DATA_SAVING = 15


def save_result(liste_resultat: list[Resultat]) -> pd.DataFrame:
    # sauvegarde de la liste des résultats
    return pd.DataFrame(
        liste_resultat,
        columns=[
            "tour",
            "lag_global",
            "numero_stimulus",
            "reponse_correct",
            "reponse_sujet",
        ],
    )


def display_face(id_face: int) -> None:
    path = f"tokens/token_{id_face}.png"
    st.image(path)


if "experiment" not in st.session_state:
    l_stim = [Stimulus(i) for i in range(1, 120)]
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

if st.session_state["experiment"].tour == LIMIT_BEFORE_DATA_SAVING:
    print("TADAAAA")
    data = save_result(st.session_state["experiment"].liste_resultat)
    with open("Database.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data.to_numpy().tolist())


def anwser_to_face_recognition(reponse_du_sujet: str) -> None:
    experiment: Experience = st.session_state["experiment"]
    print(f"EEEEEEEEEEEEEEEEEEEE {experiment.tour} EEEEEEEEEEEEEEEEE")
    current_stimulus: Stimulus = st.session_state["current_stimulus"]
    if experiment.is_sujet_right(reponse_du_sujet, current_stimulus.statut):
        experiment.lag_global += 1
    else:
        experiment.lag_global -= 1
    resultat = Resultat(
        tour=experiment.tour,
        lag_global=experiment.lag_global,
        numero_stimulus=current_stimulus.numero,
        reponse_correct=current_stimulus.statut,
        reponse_sujet=reponse_du_sujet,
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
    anwser_to_face_recognition(ReponseSujet.vu)


def answer_non_vu() -> None:
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
