
import re

from yaml_walker.api.lookup import node_lookup
from yaml_walker.tools.get_error_info import get_error_info
import logging
logger = logging.getLogger(__name__)


class YQueryError(KeyError):
    pass


class Ypath:
    EXPRESION_SEPARATOR = r'([\.|\[\]])+'
    DELIMITERS = ['.', '[', ']']

    def __init__(self, path_pattern):
        self._node_path = []
        self._base_expression = ''
        self.parse(path_pattern)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._base_expression}"

    def parse(self, path_string: str):
        self._base_expression = path_string
        delimited_pattern = [st for st in re.split(self.EXPRESION_SEPARATOR, path_string) if st != '']
        logger.debug(f"Pattern: {', '.join(delimited_pattern)}")
        for index, item in enumerate(delimited_pattern):
            if item in self.DELIMITERS:
                continue

            call_back = node_lookup(item)
            if call_back.shall_be_last_pattern and \
                    index < len(list([i for i in delimited_pattern if i not in self.DELIMITERS])):
                raise YQueryError(
                    f"Wrong pattern; Wildcard element must be last one ({path_string}) [Pattern: {path_string}]")
            self._node_path.append(call_back)

    def __call__(self, data: dict, return_name=False):
        try:
            _temp_data = data
            for cb in self._node_path:
                _temp_data = cb(_temp_data)
            return _temp_data
        except KeyError as e:
            raise YQueryError(f"Pattern '{self._base_expression}' error occur element '{e.args[0]}'")
        except Exception as e:
            f, l = get_error_info()
            raise Exception(f"Unexpected error: {e}; File: {f}:{l}")
