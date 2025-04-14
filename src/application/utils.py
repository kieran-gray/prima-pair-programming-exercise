from typing import Iterable


def chunk_list(list: list[str], chunk_size: int = 1) -> Iterable[list[str]]:
    length = len(list)
    for index in range(0, len(list), chunk_size):
        yield list[index : min(index + chunk_size, length)]
