class PositionError(Exception):

    def __init__(self, position):
        self.position = position


class PositionOccupiedError(PositionError):

    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return "Position '{}' is occupied.".format(self.position)


class PositionUnoccupiedError(PositionError):

    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return "Position '{}' is unoccupied.".format(self.position)


class PositionOutsideError(PositionError):

    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return "Position '{}' is outside of the allowable bounding area.".format(self.position)
