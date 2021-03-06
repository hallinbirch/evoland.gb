#!/usr/bin/env python

import os
import sys
from xml.etree import ElementTree


def print_help():
    print("Extracts objects from Tiled (.tmx) map files\n")
    print("USAGE:")
    print("    ./scripts/extract-objects.py <LAYER_NAME> <VARIABLE_NAME> <INPUT_MAP> <OUTPUT_C_FILE> <OUTPUT_H_FILE>")


def get_object_list(map_path, layer_name):
    tree = ElementTree.parse(map_path)
    map_ = tree.getroot()

    for layer in map_:
        if layer.tag != "objectgroup":
            continue
        if "name" not in layer.attrib or layer.attrib["name"] != layer_name:
            continue
        for obj in layer:
            yield (
                    float(obj.attrib["x"]) // 16 * 2,
                    float(obj.attrib["y"]) // 16 * 2,
                    int(obj[0].text),
                    obj.attrib["name"])


def generate_c(objects, variable_name):
    result = "// File generated by scripts/extract-objects.py\n"
    result += "// DO NOT EDIT!\n\n"
    result += "#include <types.h>\n\n"
    result += "const UINT8 %s[] = {\n" % variable_name.upper()
    result += "    // x, y, object_id\n"
    for x, y, object_id, comment in get_object_list(INPUT_MAP, LAYER_NAME):
        result += "    %3i, %3i, %3i,  // %s\n" % (x, y, object_id, comment)
    result += "};\n"
    return result


def generate_h(objects, variable_name, h_file_name):
    fname = os.path.basename(h_file_name).replace(".", "_").upper()
    result = "// File generated by scripts/extract-objects.py\n"
    result += "// DO NOT EDIT!\n\n"
    result += "#ifndef _%s\n" % fname
    result += "#define _%s\n\n" % fname
    result += "#include <types.h>\n\n"
    result += "extern const UINT8 %s[];\n" % variable_name.upper()
    result += "#define %s_COUNT %i\n" % (variable_name.upper(), len(objects))
    result += "\n"
    result += "#endif\n"
    return result


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print_help()
        sys.exit(1)

    LAYER_NAME = sys.argv[1]
    VARIABLE_NAME = sys.argv[2]
    INPUT_MAP = sys.argv[3]
    OUTPUT_C_FILE = sys.argv[4]
    OUTPUT_H_FILE = sys.argv[5]

    objects = list(get_object_list(INPUT_MAP, LAYER_NAME))
    c_code = generate_c(objects, VARIABLE_NAME)
    h_code = generate_h(objects, VARIABLE_NAME, OUTPUT_H_FILE)

    with open(OUTPUT_C_FILE, "w") as file_:
        file_.write(c_code)

    with open(OUTPUT_H_FILE, "w") as file_:
        file_.write(h_code)
