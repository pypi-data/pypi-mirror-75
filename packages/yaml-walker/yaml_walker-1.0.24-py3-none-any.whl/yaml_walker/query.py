import re
from copy import deepcopy

from yaml_walker.tools.get_error_info import get_error_info
from yaml_walker.api.lookup import node_lookup, _lookup_in_list, _lookup_abs


class YpathError(KeyError):
    pass


class Query:
    EXPRESION_SEPARATOR = r'([\.|\[\]])+'
    DELIMITERS = ['.', '[', ']']
    DELIMITER_ACTIONS = {
        '.': node_lookup,
        '[': _lookup_in_list,
        ']': None
    }

    def __init__(self, path_pattern, re_option=re.IGNORECASE, **kwargs):
        self._node_path = []
        self._base_expression = ''
        self.parse(path_pattern, re_option)
        print("")

    def __str__(self):
        return f"{self.__class__.__name__}: {self._base_expression}"

    def parse(self, path_string: str, re_option=re.IGNORECASE):
        self._base_expression = path_string
        delimited_pattern = re.split(self.EXPRESION_SEPARATOR, path_string)
        if delimited_pattern[-1] == '':
            delimited_pattern.pop()

        action = None
        for index, item in enumerate(delimited_pattern):
            if item in self.DELIMITERS:
                # action = self.DELIMITER_ACTIONS[item]
                continue
            # action = node_lookup

            call_back: _lookup_abs = node_lookup(item)
            if call_back.shall_be_last_pattern and index < len(list([i for i in delimited_pattern if i not in self.DELIMITER_ACTIONS])):
                raise YpathError(f"Wrong pattern; Wildcard element must be last one ({path_string})")
            self._node_path.append(call_back)

    def __call__(self, data: dict, return_name=False):
        try:
            _temp_data = deepcopy(data)
            for cb in self._node_path:
                _temp_data = cb(_temp_data)
            return _temp_data
        except KeyError as e:
            raise YpathError(f"Pattern '{self._base_expression}' error occur element '{e.args[0]}'")
        except Exception as e:
            f, l = get_error_info()
            raise Exception(f"Unexpected error: {e}; File: {f}:{l}")


if __name__ == '__main__':
    pattern = 'nodes.ENB_+.access_services[name=nms]data'
    y2 = Query(pattern)
    print(f"{y2}")