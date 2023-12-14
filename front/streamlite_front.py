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


def anwser_to_face_recognition(reponse_du_sujet: str, number: int) -> None:
    """Mîme le comportement de la méthode déroulement_un_tour.

    Mais l'ordre de la séquence doit être légèrement modifié içi.

    Args:
        reponse_du_sujet (str):
    """
    experiment: Experience = st.session_state["experiment"]
    current_stimulus: Stimulus = st.session_state["current_stimulus"]
    print(f"n° stim: {current_stimulus.numero}, tour: {experiment.tour}")
    experiment.traitement_reponse_sujet(
        reponse_du_sujet=reponse_du_sujet,
        stimulus=current_stimulus,
        nombre_sujet=number,
    )
    current_stimulus = experiment.choix_prochain_stimulus()
    experiment.mise_a_jour_lag_pool_vu()
    experiment.tour += 1
    st.session_state["experiment"] = experiment
    st.session_state["current_stimulus"] = current_stimulus

    st.session_state["id_face"] = current_stimulus.numero


def answer_number(number: int) -> None:
    print(len(st.session_state["experiment"].pool_non_vus))
    if st.session_state["experiment"].is_condition_arret_remplie():
        api_sauvegarde_du_resultat()
    print(f"---------------C L I C K----{number}--------------------")
    if number < 6:  # noqa: PLR2004
        anwser_to_face_recognition(
            reponse_du_sujet=ReponseSujet.non_vu,
            number=number,
        )
    else:
        anwser_to_face_recognition(
            reponse_du_sujet=ReponseSujet.vu,
            number=number,
        )


components.html(
    js_script_optimized,
    height=0,
    width=0,
)


with col1:
    st.write(" ")


with col2:  # noqa: SIM117
    with st.empty():
        display_face(st.session_state["id_face"])
        time.sleep(TEMPS_EXPOSITION)
        display_face(0)

with col3:
    st.write(" ")

c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns(10)
with c1:
    st.button("100% non vu", on_click=answer_number, args=(1,))
with c2:
    st.button("90% non vu", on_click=answer_number, args=(2,))
with c3:
    st.button("80% non vu", on_click=answer_number, args=(3,))
with c4:
    st.button("70% non vu", on_click=answer_number, args=(4,))
with c5:
    st.button("50% non vu", on_click=answer_number, args=(5,))
with c6:
    st.button("50% vu", on_click=answer_number, args=(6,))
with c7:
    st.button("70% vu", on_click=answer_number, args=(7,))
with c8:
    st.button("80% vu", on_click=answer_number, args=(8,))
with c9:
    st.button("90 vu", on_click=answer_number, args=(9,))
with c10:
    st.button("100% vu ", on_click=answer_number, args=(10,))
