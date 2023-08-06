import collections
from typing import Union, List, Tuple, Hashable, Any

from nlp_utils.preprocess import lookup_table

OOV = collections.namedtuple("OOV", ["value", "id"])
Padding = collections.namedtuple("Padding", ["value", "id"])


class VocabularyLookupTable(lookup_table.LookupTable):
    def __init__(self, dictionary, oov_id, oov_value):
        super().__init__(dictionary, oov=oov_id)

        self.oov_id = oov_id
        self.oov_value = oov_value

    def _do_inverse_lookup(self, key: Hashable) -> Any:
        try:
            return self.inverse_table[key]
        except KeyError:
            if key == self.oov_id:
                return self.oov_value

            raise


class Vocabulary:
    def __init__(self, dictionary: list, oov: str = None, padding: str = None):
        """oov must in dictionary, padding must in dictionary"""

        if len(dictionary) != len(set(dictionary)):
            raise ValueError("dictionary contains duplicated value")

        self.dictionary = dictionary

        # assign oov
        self.oov = None
        if oov is not None:
            self._set_oov(oov)

        # assign padding
        self.padding = None
        if padding is not None:
            self._set_padding(padding)

        self.table = VocabularyLookupTable(
            dictionary,
            oov_id=self.oov.id if self.oov else None,
            oov_value=self.oov.value if self.oov else None,
        )

    def _set_oov(self, value: str):
        # check
        assert value in self.dictionary

        oov_id = self.dictionary.index(value)
        self.oov = OOV(value, oov_id)

    def _set_padding(self, value: str):
        # check
        assert value in self.dictionary

        padding_id = self.dictionary.index(value)
        self.padding = Padding(value, padding_id)

    def lookup(self, items):
        return self.table.batch_lookup(items)

    def inverse_lookup(self, items):
        return self.table.batch_inverse_lookup(items)

    def get_config(self) -> dict:
        return {
            "dictionary": self.dictionary,
            "oov": self.oov.value if self.oov else None,
            "padding": self.padding.value if self.padding else None,
        }

    @classmethod
    def from_config(cls, config) -> "Vocabulary":
        return cls(**config)

    def size(self) -> int:
        return len(self.dictionary)

    def dictionary_to_list(self) -> list:
        return self.dictionary
