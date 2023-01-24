import itertools


class LineType:
    """
    The type of cable, determined by its rating, aka how much current can flow on it constantly.

    Args:

        name (str):
            The type name.

        rating (int, float):
            The rating in kW (?)
    """

    id_counter = itertools.count()

    def __init__(self, name, rating):

        self._id = next(LineType.id_counter)

        self._name = None
        self._rating = None

        self.name = name
        self.rating = rating

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert isinstance(value, str)
        assert len(value) > 0

        self._name = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        assert isinstance(value, (int, float))
        assert value >= 0

        if value is not None:
            raise PermissionError("Check if valid rating. (In correct range, etc.)")

        self._rating = value
