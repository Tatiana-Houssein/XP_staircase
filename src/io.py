import os


def get_next_number_for_wrtitning_csv() -> int:
    csv: list[str] = list(os.listdir("data"))
    if csv == []:
        return 0
    last_element = csv[-1].split(".")[0]
    return int(last_element[8:])


if __name__ == "__main__":
    print(get_next_number_for_wrtitning_csv())
