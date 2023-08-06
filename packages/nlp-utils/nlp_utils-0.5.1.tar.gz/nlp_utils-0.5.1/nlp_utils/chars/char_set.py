from typing import List
import pkg_resources


def read_list_from_file(data) -> List[str]:
    data_file = pkg_resources.resource_filename(
        __name__, "char_set_data/{}.txt".format(data)
    )
    with open(data_file, "rt") as fd:
        result = fd.read().splitlines()

    return result


gb2312 = read_list_from_file("GB2312")

# level 1: 3500; level 2: 3000; level 3: 1605
universal_stanard = read_list_from_file("通用規範漢字表")
