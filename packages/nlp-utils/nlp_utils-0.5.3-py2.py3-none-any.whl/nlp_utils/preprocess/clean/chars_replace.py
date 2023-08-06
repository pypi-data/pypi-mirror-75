from typing import Union, List


class CharsReplace:
    def __init__(self, source: Union[list, str], target: Union[list, str]):
        if isinstance(source, str):
            source = list(source)
        if isinstance(target, str):
            target = list(target)

        assert len(source) == len(target)

        self.source = source
        self.target = target

        self.mapping = dict(zip(self.source, self.target))

    def __call__(self, data: list) -> list:
        return self.batch_process(data)

    def batch_process(self, data: List[List[str]]):
        return [self.process(i) for i in data]

    def process(self, data: list) -> list:
        return [self.mapping.get(i, i) for i in data]
