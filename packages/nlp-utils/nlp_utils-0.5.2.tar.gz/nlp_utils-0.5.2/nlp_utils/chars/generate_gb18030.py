import unicodedata
import itertools
import json


def generate_bytes_list(*dim_list):
    range_list = [range(i[0], i[1] + 1) for i in dim_list]
    product = list(itertools.product(*range_list))
    print(len(product))
    return product


data = list(
    itertools.chain(
        generate_bytes_list((0x00, 0x7F)),
        generate_bytes_list((0xB0, 0xF7), (0xA1, 0xFE)),
        generate_bytes_list((0x81, 0xA0), (0x40, 0xFE)),
        generate_bytes_list((0xAA, 0xFE), (0x40, 0xA0)),
        generate_bytes_list((0x81, 0x82), (0x30, 0x39), (0x81, 0xFE), (0x30, 0x39)),
        generate_bytes_list((0x95, 0x98), (0x30, 0x39), (0x81, 0xFE), (0x30, 0x39)),
    )
)

# data = list(
#     itertools.chain(
#         generate_bytes_list((0x00, 0x7F)),
#         generate_bytes_list((0x81, 0xFE), (0x40, 0x7E)),
#         generate_bytes_list((0x81, 0xFE), (0x80, 0xFE)),
#         generate_bytes_list((0x81, 0x84), (0x30, 0x39), (0x81, 0xFE), (0x30, 0x39)),
#     )
# )

print(len(data))

data_array = []
for byte_list in data:
    d = bytearray()
    for byte in byte_list:
        d.append(byte)
    data_array.append(d)

errors = 0
chars = []
for i in data_array:
    try:
        chars.append(i.decode("gb18030"))
    except UnicodeDecodeError:
        errors += 1
        continue
print(len(chars))
print(errors)

visible_chars = []
for i in chars:
    c = unicodedata.category(i)
    # https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    if c in ["Cc"]:
        continue
    print(i, c)
    visible_chars.append(i)

print(len(visible_chars))


with open("gb18030.json", "wt") as fd:
    json.dump(visible_chars, fd, ensure_ascii=False)
