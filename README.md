# XP_staircase

Script d'un protocole staircase en reconnaissance de visages

# Environnement de travail
Si l'environnement conda n'est pas ou plus à jour, alors il faut taper dans le terminal git bash ```conda env create -f environment.yml```. Ensuite activer l'environnement : ```conda activate xp-staircase```

Ensuite il faut activer le ```pre-commit```: si jamais fait avant ```pre-commit install```. Pour exécuter le pre-commit avant de commit du code : ```pre-commit run --all-files```.

# IA

dans le module ```src/ia_experiment```, on a crée une classe héritière de Experience où l'utilisateur est une IA.
pour visualiser les résultats : ```python -m tests.test_experiment```
