
import re
from collections import OrderedDict

from yaml_walker.tools.comparer import Comparer
from yaml_walker.tools.get_error_info import get_error_info
# import logging
# logger = logging.getLogger(__name__)


class node_lookup:
    def __init__(self, element):
        self._element = element
        # logger.debug(f"Element: {self._element}")
        assert self._element is not None and self._element != '', "Empty element provided"
        self._wild_card_pattern = re.findall(r'[+|*|?]+', self._element)

    def __str__(self):
        return f"{self._element} "

    @property
    def shall_be_last_pattern(self):
        return bool(self._wild_card_pattern)

    def _dict_lookup(self, data):
        try:
            if not self._wild_card_pattern:
                if self._element == ' ':
                    return list(data.values())
                if isinstance(data, dict):
                    assert self._element in data.keys()
                    return data[self._element]
                    # _res = {}
                    # for k, v in data.items():
                    #     if k == self._element:
                    #         _res[k] = v
                    # return _res
                elif isinstance(data, list):
                    _res = []
                    for _elem in data:
                        _res.append(self(_elem))
                    return _res
            else:
                replacements = {r'+': r'.+', r'*': r'.*', r'?': r"[\s\d_\-]{1}"}
                expression = self._element
                _result = {}
                for _str, _pattern in replacements.items():
                    expression = expression.replace(_str, _pattern)
                for k, v in data.items():
                    if re.match(expression, k):
                        _result.update({k: v})
                return _result
        except AssertionError:
            raise KeyError(self._element)

    def _list_lookup(self, _data: list):
        _res = []
        assert isinstance(_data, (list, tuple)), f"Data expected to by list (Real: {_data})"
        try:
            ec = Comparer(self._element)
            for _elem in _data:
                for k_elem, v_elem in _elem.items():
                    if k_elem == ec.parameter:
                        if ec(v_elem):
                            _res.append(_elem)
            return _res[0] if len(_res) == 1 else _res
        except Exception as e:
            f, l = get_error_info()
            raise type(e)(f"{e}; File: {f}:{l}")

    def __call__(self, data):
        if isinstance(data, dict):
            return self._dict_lookup(data)
        elif isinstance(data, (list, tuple)):
            return self._list_lookup(data)
