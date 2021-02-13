# Copyright (c) 2021 Paweł Piskorz
# Licensed under the MIT License
# See attached LICENSE file

__all__ = ('generate_component', 'fill_h_funcions_data')

import os
import json


class Worker():
    def __init__(self, info_file):
        with open('config.json') as f:
            self.config = json.load(f)
        with open(info_file) as f:
            self.info = json.load(f)
        self.info_path = info_file.split('/')[0:-1]
        self.info_path = '/'.join(self.info_path)


    def _get_full_marker(self, marker):
        return self.config["prefix_marker"] + marker + self.config["sufix_marker"]


    def _get_function_comment(self, function):
        return []


    def _marker_component_name(self, line, marker):
        try:
            new_line = [line.replace(self._get_full_marker(marker), self.info[marker])]
        except:
            raise Exception("Field COMPONENT_NAME is necessary")
        return new_line


    def _marker_no_prefix(self, line, marker):
        try:
            with open("{}/{}".format(self.info_path, self.info["{}_FILE".format(marker)]), "r") as f:
                data = f.readlines()
            data.append('\n')
        except:
            data = ["/*" + line.split('\n')[0] + "*/\n"]
        return data


    def _marker_short_prefix(self, line, marker):
        try:
            with open("{}/{}".format(self.info_path, self.info["{}_FILE".format(marker)]), "r") as f:
                data = f.readlines()
            for l in range(len(data)):
                data[l] = " * " + data[l]
            data.append('\n')
        except:
            data = [line]
        return data


    def _marker_long_prefix(self, line, marker):
        try:
            with open("{}/{}".format(self.info_path, self.info["{}_FILE".format(marker)]), "r") as f:
                data = f.readlines()
            for l in range(len(data)):
                data[l] = " *      " + data[l]
            data.append('\n')
        except:
            data = [line]
        return data


    def _marker_component_define_name(self, line, marker):
        try:
            new_line = [line.replace(self._get_full_marker(marker), "_{}_H_".format(self.info["COMPONENT_NAME"].upper()))]
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
        except:
            data = [line]
        return data


    def _marker_skip(self, line, marker):
        return ["/*" + line.split('\n')[0] + "*/\n"]


    marker_function = [
        {"marker":"COMPONENT_NAME",                   "function":_marker_component_name                 },
        {"marker":"LICENSE_INFORMATIONS",             "function":_marker_short_prefix                   },
        {"marker":"COMPONENT_DESCRIPTION",            "function":_marker_long_prefix                    },
        {"marker":"COMPONENT_COMMENTS",               "function":_marker_long_prefix                    },
        {"marker":"COMPONENT_EXAMPLE",                "function":_marker_long_prefix                    },
        {"marker":"COMPONENT_DEFINE_NAME",            "function":_marker_component_define_name          },
        {"marker":"COMPONENT_INCLUDES_H",             "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_DEFINES_H",              "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_EXTERNS_H",              "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_DATA_TYPES_H",           "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_INCLUDES_C",             "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_DEFINES_C",              "function":_marker_no_prefix                      },
        {"marker":"COMPONENT_PRIVATE_DEFINITIONS",    "function":_marker_skip                           },
        {"marker":"COMPONENT_PUBLIC_DEFINITIONS",     "function":_marker_component_public_definitions   },
        {"marker":"COMPONENT_PUBLIC_DECLARATIONS",    "function":_marker_skip                           }
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
    with open('config.json') as f:
        config = json.load(f)

    with open(info_file) as f:
        info = json.load(f)

    create_dir_structure(config, info["COMPONENT_NAME"])


    # create h file
    with open("template.h", "r") as f:
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


    with open("{0}/header/{0}.h".format(info["COMPONENT_NAME"]), "w+") as f:
        f.writelines(output)


    # create c file
    with open("template.c", "r") as f:
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

    with open("{0}/source/{0}.c".format(info["COMPONENT_NAME"]), "w+") as f:
        f.writelines(output)

    #other files
    files = [
        "{0}/tests/CMakeLists.txt",
        "{0}/CHANGES.rst",
        "{0}/LICENSE",
        "{0}/README.rst"
    ]

    for file in files:
        with open(file.format(info["COMPONENT_NAME"]), 'w') as f: 
            pass


def fill_h_funcions_data(c_file, h_file):
    print("This function is not yet implemented!")
