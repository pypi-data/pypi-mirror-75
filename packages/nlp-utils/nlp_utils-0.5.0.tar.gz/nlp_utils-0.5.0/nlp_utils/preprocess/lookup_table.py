import json
from typing import Union, List, Tuple, Hashable, Any


class LookupTable(object):
    """Bidirectional Lookup Table with out-of-vocabulary (OOV) supporting.

    this class support `lookup()` and `inverse_lookup()` with OOV supporting

    Attributes:
        table: A dict contains mapping for `lookup()` to query.
        inverse_table: A dict contains mapping for `inverse_lookup` to query.
        oov: A hashable object as return value for `lookup()` when OOV
             if it's not None.
        oov_key: A hashable object act as query key for `lookup()` when OOV
            if it's not None and `oov` is None.
        inverse_oov: A hashable object as return value for `inverse_lookup()`
            when OOV if it's not None.
        inverse_oov_key: A hashable object act as query key for
            `inverse_lookup()` if it's not None and `inverse_oov` is None.
    """

    def __init__(
        self,
        table: Union[dict, list, tuple],
        oov=None,
        oov_key=None,
        inverse_oov=None,
        inverse_oov_key=None,
    ):
        """
        Args:
            table: A dictionary represented as dict or sequence, list/tuple will
                convert to dict by using index as key, `lookup()` will mapping
                it's key to value, `inverse_lookup()` will mapping it's value to
                key.
            oov: A hashable object (typically a int) or None, if it is not a
                None, will use this as return value in `lookup()`, when the
                query out-of-vocabulary (OOV).
            oov_key: A hashable object (typically a str) or None, if it is not
                None, will use this as key to query value in `lookup()` when OOV,
                this arg will be used if and only if `oov` is set to None.
            inverse_oov: A hashable object (typically a str) or None, if it is
                not None, will use this as return value in `inverse_lookup()`
                when OOV.
            inverse_oov_key: A hashable object (typically an int) or None, if
                it's not None, will use this as key to query value in
                `inverse_lookup()` when OOV, this arg will be used if and only if
                `inverse_oov` is set to None.

        Raises:
            ValueError: An argument checking error occurred.
        """

        if isinstance(table, (list, tuple)):
            table = {v: k for k, v in enumerate(table)}
        if not isinstance(table, dict):
            raise ValueError(
                "table argument do not accept type: {}".format(type(table))
            )

        if oov is not None and oov_key is not None:
            raise ValueError("Only one of oov and oov_key can be set to non None")
        if inverse_oov is not None and inverse_oov_key is not None:
            raise ValueError(
                "Only one of inverse_oov and inverse_oov_key can be set to non None"
            )

        self.table = table
        self.inverse_table = {v: k for k, v in table.items()}
        if len(self.table) != len(self.inverse_table):
            raise ValueError(
                "table values are duplicated, reverse table cannot be created"
            )

        self.oov = oov
        self.oov_key = oov_key
        self.inverse_oov = inverse_oov
        self.inverse_oov_key = inverse_oov_key

        if self.oov is not None and self.oov not in self.table.values():
            print("WARNING: oov not in table")
        if self.oov_key is not None and self.oov_key not in self.table.keys():
            raise ValueError("WARNING: oov_key not in table")
        if (
            self.inverse_oov is not None
            and self.inverse_oov not in self.inverse_table.values()
        ):
            print("WARNING: inverse_oov not in inverse_table")
        if (
            self.inverse_oov_key is not None
            and self.inverse_oov_key not in self.inverse_table.keys()
        ):
            raise ValueError("WARNING: inverse_oov_key not in inverse_table")

    def __call__(self, key):
        return self.batch_lookup(key)

    def batch_lookup(self, key):
        """
        Raises:
            KeyError:  when `ovv` and `oov_key` is not set, unhandleable OOV occurs.
        """

        return [self.lookup(i) for i in key]

    def lookup(
        self, key: Union[Hashable, List[Hashable], Tuple[Hashable]]
    ) -> Union[Any, List[Any]]:
        """
        Raises:
            KeyError:  when `ovv` and `oov_key` is not set, unhandleable OOV occurs.
        """

        if isinstance(key, (list, tuple)):
            return tuple(self._do_lookup(i) for i in key)
        return self._do_lookup(key)

    def _do_lookup(self, key: Hashable) -> Any:
        try:
            return self.table[key]
        except KeyError:
            # TODO(Xiaoquan Kong): Add callbacks when OOV occurs
            if self.oov is not None:
                return self.oov
            elif self.oov_key is not None:
                return self.table[self.oov_key]
            else:
                raise

    def batch_inverse_lookup(self, key):
        """
        Raises:
            KeyError:  when `ovv` and `oov_key` is not set, unhandleable OOV occurs.
        """

        return [self.inverse_lookup(i) for i in key]

    def inverse_lookup(
        self, key: Union[Hashable, List[Hashable], Tuple[Hashable]]
    ) -> Union[Any, List[Any]]:
        """
        Raises:
            KeyError:  when `ovv` and `oov_key` is not set, unhandleable OOV occurs.
        """

        if isinstance(key, (list, tuple)):
            return tuple(self._do_inverse_lookup(i) for i in key)
        return self._do_inverse_lookup(key)

    def _do_inverse_lookup(self, key: Hashable) -> Any:
        try:
            return self.inverse_table[key]
        except KeyError:
            # TODO(Xiaoquan Kong): Add callbacks when OOV occurs
            if self.inverse_oov is not None:
                return self.inverse_oov
            elif self.inverse_oov_key is not None:
                return self.inverse_table[self.inverse_oov_key]
            else:
                raise

    def size(self) -> int:
        return len(self.table)

    @classmethod
    def read_from_file(cls, data_file, kwargs: dict = {}):
        with open(data_file, "rt") as fd:
            paired_dict = json.load(fd)

            return cls(paired_dict, **kwargs)

    # alias for compatible
    load_from_file = read_from_file

    def write_to_file(self, data_file):
        with open(data_file, "wt") as fd:
            # set ensure_ascii=False for human readability of dumped file
            json.dump(self.table, fd, ensure_ascii=False)

    def dump_to_file(self, data_file):
        # alias for compatible
        return self.write_to_file(data_file)

    def get_config(self):
        return {
            "oov": self.oov,
            "oov_key": self.oov_key,
            "inverse_oov": self.inverse_oov,
            "inverse_oov_key": self.inverse_oov_key,
        }
