import os


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
