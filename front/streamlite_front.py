import random
import time

import streamlit as st
import streamlit.components.v1 as components

from back.configuration import LAG_INITIAL, TAILLE_POOL_NON_VU, TEMPS_EXPOSITION
from back.constantes import ReponseSujet
from back.experiment import (
    Experience,
    Stimulus,
)
from back.io import save_result
from front.experiment_js import js_script_optimized

col1, col2, col3 = st.columns(3)


def api_sauvegarde_du_resultat() -> None:
    """Fonction spécifique du front pour écrire le CSV de résultat."""
    print("-------------SVG CSV---------------------")
    st.session_state["id_face"] = -1  # Affiche logo de fin.
    liste_resultat = st.session_state["experiment"].liste_resultat
    save_result(liste_resultat)


def display_face(id_face: int) -> None:
    path = f"tokens/token_{id_face}.png"
    st.image(path)


if "experiment" not in st.session_state:
    # Crée une variable experiment dans le dict des session_state
    list_id = list(range(1, TAILLE_POOL_NON_VU))
    random.shuffle(list_id)
    l_stim = [Stimulus(i) for i in list_id]
    st.session_state["experiment"] = Experience(
        liste_stimuli=l_stim,
        lag_initial=LAG_INITIAL,
        fonction_question_au_sujet=lambda x: f"str{x}",  # a defaut fonction con
    )

if "current_stimulus" not in st.session_state:
    # Crée une variable current_stimulus dans le dict des session_state
    st.session_state["current_stimulus"] = st.session_state[
        "experiment"
    ].choix_prochain_stimulus()

if "id_face" not in st.session_state:
    # Crée une variable id_face dans le dict des session_state
    st.session_state["id_face"] = st.session_state["current_stimulus"].numero


def anwser_to_face_recognition(reponse_du_sujet: str) -> None:
    """Mîme le comportement de la méthode déroulement_un_tour.

    Mais l'ordre de la séquence doit être légèrement modifié içi.

    Args:
        reponse_du_sujet (str):
    """
    print("---------------C L I C K----------------------------")
    experiment: Experience = st.session_state["experiment"]
    current_stimulus: Stimulus = st.session_state["current_stimulus"]
    print(f"n° stim: {current_stimulus.numero}, tour: {experiment.tour}")
    experiment.traitement_reponse_sujet(
        reponse_du_sujet=reponse_du_sujet,
        stimulus=current_stimulus,
    )
    current_stimulus = experiment.choix_prochain_stimulus()
    experiment.mise_a_jour_lag_pool_vu()
    experiment.tour += 1
    st.session_state["experiment"] = experiment
    st.session_state["current_stimulus"] = current_stimulus

    st.session_state["id_face"] = current_stimulus.numero


def answer_vu() -> None:
    if st.session_state["experiment"].is_condition_arret_remplie():
        api_sauvegarde_du_resultat()
    else:
        anwser_to_face_recognition(reponse_du_sujet=ReponseSujet.vu)


def answer_non_vu() -> None:
    if st.session_state["experiment"].is_condition_arret_remplie():
        api_sauvegarde_du_resultat()
    else:
        anwser_to_face_recognition(reponse_du_sujet=ReponseSujet.non_vu)


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

with col1:
    st.write(" ")


with col2:  # noqa: SIM117
    with st.empty():
        display_face(st.session_state["id_face"])
        time.sleep(TEMPS_EXPOSITION)  # 0.5 millisecond
        display_face(0)

with col3:
    st.write(" ")
