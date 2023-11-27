import os

import pandas as pd

from back.resultat import Resultat


def get_next_number_for_wrtitning_csv() -> int:
    csv: list[str] = list(os.listdir("data"))
    if csv == []:
        return 0
    next_number = 0
    for result in csv:
        if int(result.split(".")[0][8:]) > next_number:
            next_number = int(result.split(".")[0][8:])
    return next_number


if __name__ == "__main__":
    print(get_next_number_for_wrtitning_csv())


def save_result(liste_resultat: list[Resultat]) -> None:
    # sauvegarde de la liste des résultats
    df_result = pd.DataFrame(
        liste_resultat,
        columns=[
            "tour",
            "lag_global",
            "lag_initial_stimulus",
            "numero_stimulus",
            "reponse_correct",
            "reponse_sujet",
            "type_erreur_tds",
        ],
    )
    next_csv_number = get_next_number_for_wrtitning_csv() + 1
    csv_path = f"data/results_{next_csv_number}.csv"
    df_result.to_csv(csv_path, index=False)
