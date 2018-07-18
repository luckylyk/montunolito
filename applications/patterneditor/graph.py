

class GraphIndex(object):
    def __init__(self, index, parent):
        self._row = index[0]
        self._column = index[1]


class GraphRow(object):
    def __init__(self, indexes):
        self._indexes = [GraphIndex(index, self) for index in indexes]