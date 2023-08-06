import json

import pkg_resources
from nlp_utils.preprocess.clean.chars_replace import CharsReplace
from nlp_utils.preprocess.lookup_table import LookupTable
from nlp_utils.preprocess.padding import SequencePaddding


class TextPreprocess:
    def __init__(self, pipeline: list):
        self.pipeline = pipeline

    def __call__(self, data):
        for processor in self.pipeline:
            data = processor(data)

        return data

    def vocab_size(self):
        lookup_table = None
        for p in self.pipeline:
            if isinstance(p, LookupTable):
                lookup_table = p
                break

        return lookup_table.size() if lookup_table else None


def fixed_len_preprocess(max_length=45):
    data_file = pkg_resources.resource_filename(
        __name__, "../resources/gb2312_dict.json"
    )
    with open(data_file) as fd:
        data = json.load(fd)

    padding = "<PAD>"
    oov_key = "<UNK>"
    lookup_table = [padding] + [oov_key] + data["words"]

    pre = data["preprocessing"]
    char_replace = list(
        zip(
            (i["source"], i["target"]) for i in [pre[2], pre[3], pre[4], pre[5], pre[6]]
        )
    )

    char_replace_src = char_replace[0]
    char_replace_target = char_replace[1]

    pipeline = [
        CharsReplace(char_replace_src, char_replace_target),
        SequencePaddding(padding, max_length),
        LookupTable(lookup_table, oov_key=oov_key),
    ]
    tp = TextPreprocess(pipeline)
    return tp


if __name__ == "__main__":
    data = "some text"
    tp = fixed_len_preprocess()
    reuslt = tp(data)
