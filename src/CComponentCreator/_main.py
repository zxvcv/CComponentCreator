# Copyright (c) 2021 Paweł Piskorz
# Licensed under the MIT License
# See attached LICENSE file

__all__ = ('generate_component', 'fill_h_funcions_data')

import os
import json
from functools import partial 


class Worker():
    def __init__(self, info_file):
        path_lib = os.path.realpath(__file__).replace('\\', '/').split('/')[0:-1]
        path_lib = '/'.join(path_lib)
        with open('{}/config.json'.format(path_lib)) as f:
            self.config = json.load(f)
        with open(info_file) as f:
            self.info = json.load(f)
        self.info_path = info_file.split('/')[0:-1]
        self.info_path = '/'.join(self.info_path)


    def _get_full_marker(self, marker):
        return self.config["prefix_marker"] + marker + self.config["sufix_marker"]


    def _set_marker_as_continued(self, marker, prefix):
        if prefix != "":
            return self._get_full_marker(marker)
        else:
            return "/*" + self._get_full_marker(marker) + "*/"


    def _get_function_comment(self, function):
        return []


    def _marker_component_name(self, line, marker):
        try:
            new_line = [line.replace(self._get_full_marker(marker), self.info[marker])]
        except:
            raise Exception("Field COMPONENT_NAME is necessary")
        return new_line


    def _marker_component(self, line, marker, prefix, leave_marker=True):
        try:
            with open("{}/{}".format(self.info_path, self.info["{}_FILE".format(marker)]), "r") as f:
                data = f.readlines()
            for l in range(len(data)):
                data[l] = prefix + data[l]
            data += "\n"
        except:
            data = ""
        if leave_marker:
            data += prefix +  self._set_marker_as_continued(marker, prefix) + "\n"
        return data


    def _marker_component_define_name(self, line, marker):
        try:
            new_line = [line.replace(self._get_full_marker(marker), "{}_H_".format(self.info["COMPONENT_NAME"].upper()))]
        except:
            raise Exception("Field COMPONENT_NAME is necessary")
        return new_line


    def _marker_component_public_definitions(self, line, marker):
        try:
            data = []
            with open("{}/{}".format(self.info_path, self.info["{}_FILE".format(marker)]), "r") as f:
                _data = f.readlines()
            for l in range(len(_data)):
                data += [_data[l]]
                if l == len(_data)-1:
                    data += ['\n']
                data += ['{\n', '    \n', '}\n']
                if l < len(_data) - 1:
                    data += ['\n', '\n']
            data += self._set_marker_as_continued(marker, "") + "\n"
        except:
            data = self._set_marker_as_continued(marker, "") + "\n"
        return data


    def _marker_skip(self, line, marker):
        return ["/*" + line.split('\n')[0] + "*/\n"]

    marker_function = [
        {"marker":"COMPONENT_NAME",                   "function":_marker_component_name                                 },
        {"marker":"LICENSE_INFORMATIONS",             "function":partial(_marker_component, prefix = " * ")             },
        {"marker":"COMPONENT_DESCRIPTION",            "function":partial(_marker_component, prefix = " *      ")        },
        {"marker":"COMPONENT_COMMENTS",               "function":partial(_marker_component, prefix = " *      ")        },
        {"marker":"COMPONENT_EXAMPLE",                "function":partial(_marker_component, prefix = " *      ")        },
        {"marker":"COMPONENT_DEFINE_NAME",            "function":_marker_component_define_name                          },
        {"marker":"COMPONENT_INCLUDES_H",             "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_DEFINES_H",              "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_EXTERNS_H",              "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_DATA_TYPES_H",           "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_INCLUDES_C",             "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_DEFINES_C",              "function":partial(_marker_component, prefix = "")                },
        {"marker":"COMPONENT_PRIVATE_DEFINITIONS",    "function":_marker_skip                                           },
        {"marker":"COMPONENT_PUBLIC_DEFINITIONS",     "function":_marker_component_public_definitions                   },
        {"marker":"COMPONENT_PUBLIC_DECLARATIONS",    "function":_marker_skip                                           },
        {"marker":"LICENSE_INFORMATIONS_CMAKE", "function":partial(_marker_component, prefix = "# ", leave_marker=False)}
    ]


    def handle_found_marker(self, line, marker):
        for m in self.marker_function:
            if m["marker"] == marker:
                executable = m["function"]
                return executable(self, line, marker)


def create_dir_structure(config, component_name):
    for path in config["dirs"]:
        os.makedirs(path.format(component_name))

def generate_component(info_file):
    path_lib = os.path.realpath(__file__).replace('\\', '/').split('/')[0:-1]
    path_lib = '/'.join(path_lib)
    with open('{}/config.json'.format(path_lib)) as f:
        config = json.load(f)

    with open(info_file) as f:
        info = json.load(f)

    create_dir_structure(config, info["COMPONENT_NAME"])

    files = [
        {"source":"template.h",             "destination":"header/{}.h".format(info["COMPONENT_NAME"])  },
        {"source":"template.c",             "destination":"source/{}.c".format(info["COMPONENT_NAME"])  },
        {"source":"CMakeLists_main.txt",    "destination":"CMakeLists.txt"                              },
        {"source":"CMakeLists_test.txt",    "destination":"tests/CMakeLists.txt"                        }
    ]

    for file in files:
        with open("{}/{}".format(path_lib, file["source"]), "r") as f:
            data = f.readlines()

        worker = Worker(info_file)

        output = []
        for line in data:
            is_match = False
            for marker in config["markers"]:
                pattern = config["prefix_marker"] + marker + config["sufix_marker"]
                match = line.find(pattern)
                if match != -1:
                    new_lines = worker.handle_found_marker(line, marker)
                    for l in new_lines:
                        output.append(l)
                    is_match = True
                    break
            if not is_match:
                output.append(line)

        with open("{0}/{1}".format(info["COMPONENT_NAME"], file["destination"]), "w+") as f:
            f.writelines(output)

    #other files
    files = [
        "{0}/CHANGES.rst",
        "{0}/LICENSE",
        "{0}/README.rst"
    ]

    for file in files:
        with open(file.format(info["COMPONENT_NAME"]), 'w') as f: 
            pass


def fill_h_funcions_data(c_file, h_file):
    print("This function is not yet implemented!")
