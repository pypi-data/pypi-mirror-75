import re


class PatternReplace:
    def __init__(self, pattern: str, target: str):
        self.pattern = pattern
        self.target = target

        self.p = re.compile(self.pattern)

    def __call__(self, data: str) -> str:
        return self.p.sub(self.target, data)
