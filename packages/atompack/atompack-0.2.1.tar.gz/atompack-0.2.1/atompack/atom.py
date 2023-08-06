from typing import Optional

import numpy as np


class Atom(object):
    """Representation of an atom with dynamic attributes.
    
    Notes:
        Any `kwargs` passed to `__init__()` are dynamically set as instance variables.
        This enables arbitrary atomic data to be associated with each instance in an elegant and pythonic way.

    Args:
        position: Location vector in 3D cartesian space.
            Mutating `position` is a logical error if the change results in atoms overlapping or a translation out of bounds.
    """

    def __init__(self, position: Optional[np.ndarray] = None, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        if position is None:
            position = np.zeros(3)
        self.position = position
