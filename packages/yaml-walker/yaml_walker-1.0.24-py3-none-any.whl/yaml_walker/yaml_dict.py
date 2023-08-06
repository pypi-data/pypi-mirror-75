from yaml_walker import YQuery


class YamlDict:
    # class _yaml_node:
    def __init__(self, data, item=None):
        self._node = data if item is None else YQuery(item)(data)

    def _get_y_query_item(self, item):
        if isinstance(item, YamlDict):
            temp_query = self._node
        else:
            temp_query = YQuery(item)
        return YamlDict(temp_query(self._node))

    def __str__(self):
        return str(self._node)

    def __getattr__(self, item):
        return self._get_y_query_item(item)

    def __getitem__(self, item):
        return self._get_y_query_item(item)

    # def __init__(self, data):
    #     self._root = self._yaml_node(data)
    #
    # def __getattr__(self, item):
    #     return getattr(self._root, item, None)
    #
    # def __getitem__(self, item):
    #     return self._root[item]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return None
        return exc_type(exc_val, exc_tb)