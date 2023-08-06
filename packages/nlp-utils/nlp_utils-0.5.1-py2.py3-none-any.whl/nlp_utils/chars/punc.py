# Data from https://zh.wikipedia.org/wiki/%E6%A0%87%E7%82%B9%E7%AC%A6%E5%8F%B7
cn_punc = [
    "。",
    "？",
    "！",
    "，",
    "、",
    "；",
    "：",
    "“",
    "”",
    "﹃",
    "﹄",
    "‘ ",
    "’",
    "﹁",
    "﹂",
    "（",
    "）",
    "［",
    "］",
    "〔",
    "〕",
    "【",
    "】",
    "——",
    "……",
    "－",
    "-",
    "～",
    "·",
    "《",
    "》",
    "〈",
    "〉",
    "﹏",
    "﹏",
    "＿",
    "＿",
    ".",
]


# Data are from https://en.wikipedia.org/wiki/Punctuation
en_punc = [
    "[",
    "]",
    "[",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "\\",
    "^",
    "_",
    "`",
    "|",
    "{",
    "}",
    "~",
    "-",
    "]",
]


if __name__ == "__main__":
    import json

    with open("en_punc.json", "wt") as fd:
        json.dump(en_punc, fd)

    with open("cn_punc.json", "wt") as fd:
        json.dump(cn_punc, fd)
