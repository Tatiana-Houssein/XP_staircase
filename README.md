# XP_staircase

Script d'un protocole staircase en reconnaissance de visages
Pour lancer le front dans le navigateur, ouvri un git bash à la racine du projet sur VSCode puis taper ```python -m streamlit run front_streamlit/streamlite_front.py```  (Ctrl C pour quitter)

# Environnement de travail
Si l'environnement conda n'est pas ou plus à jour, alors il faut taper dans le terminal git bash ```conda env create -f environment.yml```. Ensuite activer l'environnement : ```conda activate xp-staircase```.  2e manip : Attention vérifier que l'env est aussi activé dans l'IDE (en bas à droite).

Ensuite il faut activer le ```pre-commit```: si jamais fait avant ```pre-commit install```. Pour exécuter le pre-commit avant de commit du code : ```pre-commit run --all-files```.

# IA

dans le module ```src/ia_experiment```, on a crée une classe héritière de Experience où l'utilisateur est une IA.
pour visualiser les résultats : ```python -m tests.test_experiment```
