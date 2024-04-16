# XP_staircase

Script d'un protocole staircase en reconnaissance de visages
Pour lancer le front dans le navigateur, ouvrir un git bash à la racine du projet sur VSCode puis taper
 * ```python -m flask --app back.api.app run```
 * Depuis le front (```cd front_angular```): ```ng serve```



# Environnement de travail
Si l'environnement conda n'est pas ou plus à jour, alors il faut taper dans le terminal git bash ```conda env create -f environment.yml```. Ensuite activer l'environnement : ```conda activate xp-staircase```.  2e manip : Attention vérifier que l'env est aussi activé dans l'IDE (en bas à droite).

Ensuite il faut activer le ```pre-commit```: si jamais fait avant ```pre-commit install```. Pour exécuter le pre-commit avant de commit du code : ```pre-commit run --all-files```.

Pour lancer les tests du back : ```python -m pytest```
