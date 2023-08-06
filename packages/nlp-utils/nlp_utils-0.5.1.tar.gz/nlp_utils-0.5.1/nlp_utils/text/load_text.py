from typing import List


def load_text(text_file: str) -> List[str]:
    with open(text_file, "rt") as fd:
        data = fd.read()

    return data.splitlines()
