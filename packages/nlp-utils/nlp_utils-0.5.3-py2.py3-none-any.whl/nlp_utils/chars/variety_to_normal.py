import pkg_resources
import json
from typing import Dict, Text

small_to_full_punc: Dict[Text, Text] = {
    "﹒": ".",  # small full stop (U+FE52) => 'FULL STOP' (U+002E), period, dot, decimal point
    "﹣": "-",  # small hyphen-minus (U+FE63) => The hyphen-minus (-)
    "﹚": ")",  # small right parenthesis (U+FE5A) => Right Parenthesis )
    "": "",
}

zht_to_zhs_datafile = pkg_resources.resource_filename(
    __name__, "../resources/zht_to_zhs.json"
)
with open(zht_to_zhs_datafile) as fd:
    zht_to_zhs: Dict[Text, Text] = json.load(fd)

number_to_normal_datafile = pkg_resources.resource_filename(
    __name__, "../resources/number_to_normal.json"
)
with open(number_to_normal_datafile) as fd:
    number_to_normal: Dict[Text, Text] = json.load(fd)

fullwidth_to_halfwidth_datafile = pkg_resources.resource_filename(
    __name__, "../resources/fullwidth_to_halfwidth.json"
)
with open(fullwidth_to_halfwidth_datafile) as fd:
    fullwidth_to_halfwidth: Dict[Text, Text] = json.load(fd)
