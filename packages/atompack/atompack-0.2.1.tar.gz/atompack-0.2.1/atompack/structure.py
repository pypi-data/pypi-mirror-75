from typing import List, Optional, Tuple

import numpy as np

from _cell import cell_contains
from _pbc import pbc_nearest_neighbor
from atompack.atom import Atom
from atompack.errors import (PositionOccupiedError, PositionOutsideError, PositionUnoccupiedError)


class Structure(object):
    """Representation of an atomic structure with boundaries which may be periodic.
    
    Args:
        atoms: List of atoms in the structure.
            Mutating `atoms` is a logical error if the change results in atoms overlapping with eachother or atoms existing out of bounds.
        basis: 3x3 matrix defining the boundaries of the structure.
            Mutating `basis` is a logical error if the change forces atoms out of bounds.
        pbc: Boolean array that indicates which boundaries are considered periodic.
        tolerance: Radius of tolerance for operations on the structure.
            Mutating `tolerance` is a logical error if the change results in atoms overlapping with eachother or atoms existing out of bounds.
    """

    def __init__(self,
                 atoms: Optional[List[Atom]] = None,
                 basis: Optional[np.ndarray] = None,
                 pbc: Optional[Tuple[bool, bool, bool]] = None,
                 tolerance: Optional[float] = None) -> None:
        if atoms is None:
            atoms = []
        self.atoms = atoms
        if basis is None:
            basis = np.identity(3)
        self.basis = basis
        if pbc is None:
            pbc = (False, False, False)
        self.pbc = pbc
        if tolerance is None:
            tolerance = 1.0e-6
        self.tolerance = tolerance

    def __getitem__(self, key: int) -> Atom:
        return self.atoms[key]

    def __setitem__(self, key: int, value: Atom) -> None:
        self.atoms[key] = value

    def __delitem__(self, key: int) -> None:
        del self.atoms[key]

    def __iter__(self) -> 'Structure':
        self._iter = 0
        return self

    def __len__(self) -> int:
        return len(self.atoms)

    def __next__(self) -> Atom:
        if self._iter == len(self):
            raise StopIteration
        res = self.atoms[self._iter]
        self._iter += 1
        return res

    def insert(self, atom: Atom) -> None:
        """Inserts an atom into the structure safely with bounds checking.
        
        Args:
            atom: Atom inserted into the structure.

        Raises:
            `atompack.errors.PositionOccupiedError`: If the position is already occupied.
            `atompack.errors.PositionOutsideError`: If the position is out of bounds.

        Example:
            >>> from atompack.atom import Atom
            >>> from atompack.structure import Structure
            >>> 
            >>> structure = Structure()
            >>> atom = Atom()
            >>> structure.insert(atom)
            >>>
            >>> assert len(structure) == 1
        """
        if len(self.atoms) == 0:
            self.atoms.append(atom)
            return
        if not cell_contains(self.basis, atom.position, self.tolerance):
            raise PositionOutsideError(atom.position)
        distance, _ = pbc_nearest_neighbor(atom.position, self._positions(), self.basis, self.pbc)
        if distance < self.tolerance:
            raise PositionOccupiedError(atom.position)
        self.atoms.append(atom)

    def remove(self, position: np.ndarray) -> Atom:
        """Removes and returns an atom from the structure.
        
        Args:
            position: Position to remove the atom from.

        Raises:
            `atompack.errors.PositionUnoccupiedError`: If the position is not occupied.

        Example:
            >>> from atompack.atom import Atom
            >>> from atompack.structure import Structure
            >>> import numpy as np
            >>>
            >>> atoms = [Atom(symbol="Fe")]
            >>> structure = Structure(atoms=atoms)
            >>> removal_position = np.zeros(3)
            >>> atom = structure.remove(removal_position)
            >>>
            >>> assert atom.symbol == "Fe"
            >>> assert len(structure) == 0
        """
        if len(self.atoms) == 0:
            raise PositionUnoccupiedError(position)
        distance, index = pbc_nearest_neighbor(position, self._positions(), self.basis, self.pbc)
        if distance > self.tolerance:
            raise PositionUnoccupiedError(position)
        atom = self.atoms[index]
        del self.atoms[index]
        return atom

    def select(self, position: np.ndarray) -> int:
        """Returns the index of an atom.
        
        Args:
            position: Position to select the atom from.

        Raises:
            `atompack.errors.PositionUnoccupiedError`: If the position is not occupied.

        Example:
            >>> from atompack.atom import Atom
            >>> from atompack.structure import Structure
            >>> import numpy as np
            >>>
            >>> atoms = [Atom(symbol="Fe")]
            >>> structure = Structure(atoms=atoms)
            >>> selection_position = np.zeros(3)
            >>> index = structure.select(selection_position)
            >>>
            >>> assert structure[index].symbol == "Fe"
        """
        if len(self.atoms) == 0:
            raise PositionUnoccupiedError(position)
        distance, index = pbc_nearest_neighbor(position, self._positions(), self.basis, self.pbc)
        if distance > self.tolerance:
            raise PositionUnoccupiedError(position)
        return index

    def _positions(self):
        return np.array([atom.position for atom in self.atoms])
