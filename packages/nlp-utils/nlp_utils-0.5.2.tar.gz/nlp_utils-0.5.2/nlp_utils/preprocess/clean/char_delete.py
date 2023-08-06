class CharsDelete:
    def __init__(self, chars):
        self.chars = chars

    def __call__(self, data: str) -> str:
        for char in self.chars:
            data = data.replace(char, "")

        return data
