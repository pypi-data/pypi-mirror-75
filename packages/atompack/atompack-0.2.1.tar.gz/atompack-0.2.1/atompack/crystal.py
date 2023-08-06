from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.spatial.transform import Rotation

from _pbc import pbc_nearest_neighbor
from atompack.atom import Atom
from atompack.structure import Structure


def metric_tensor(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> np.ndarray:
    return np.array([[a * a, a * b * np.cos(gamma), a * c * np.cos(beta)],
                     [a * b * np.cos(gamma), b * b, b * c * np.cos(alpha)],
                     [a * c * np.cos(beta), b * c * np.cos(alpha), c * c]])


class Crystal(Structure):
    """Representation of a crystalline lattice.
    
    Note:
        It is a logical error to mutate any of these attributes because the result of any changes will not be reflected in the shape of the basis or the content of the atoms list.

    Args:
        lattice_data: Atomic data used to initialize atoms at each lattice site.
        lattice_sites: Fractional coordinates of atoms in the lattice.
        a: Length of the x direction.
        b: Length of the y direction.
        c: Length of the z direction.
        alpha: Angle between y and z directions in radians.
        beta: Angle between x and z directions in radians.
        gamma: Angle between x and y directions in radians.
        duplicates: Number of duplications to apply to the finished structure along each direction.
        orientation: 3x3 matrix indicating the alignment of the lattice vectors.

    Example:
        >>> from atompack.crystal import Crystal
        >>> import numpy as np
        >>>
        >>> lattice_data = [{"symbol": "Cr", "magmom": 1.0}, {"symbol": "Cr", "magmom": -1.0}]
        >>> lattice_sites = np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]])
        >>> a = b = c = 2.85
        >>> alpha = beta = gamma = np.pi / 2
        >>> crystal = Crystal(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma)
        >>>
        >>> assert np.allclose(crystal[0].position, np.array([0.0, 0.0, 0.0]))
        >>> assert np.allclose(crystal[1].position, np.array([1.425, 1.425, 1.425]))
    """

    def __init__(
            self,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            b: float,
            c: float,
            alpha: float,
            beta: float,
            gamma: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> None:
        if duplicates is None:
            duplicates = (1, 1, 1)
        if orientation is None:
            orientation = np.identity(3)
        if pbc is None:
            pbc = (False, False, False)
        atoms, basis = self._build(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation,
                                   pbc, tolerance)
        super().__init__(atoms, basis, pbc, tolerance)

    @classmethod
    def triclinic(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            b: float,
            c: float,
            alpha: float,
            beta: float,
            gamma: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with triclinic constraints.
        
        a != b != c

        alpha != beta != gamma
        """
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def monoclinic(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            b: float,
            c: float,
            beta: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with monoclinic constraints.
        
        a != b != c
        
        alpha == gamma == pi/2
        
        beta != pi / 2
        """
        alpha = gamma = np.pi / 2
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def orthorhombic(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            b: float,
            c: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with orthorhombic constraints.
        
        a != b != c
        
        alpha == beta == gamma == pi / 2
        """
        alpha = beta = gamma = np.pi / 2
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def tetragonal(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            c: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with tetragonal constraints.
        
        a == b != c
        
        alpha == beta == gamma == pi / 2
        """
        b = a
        alpha = beta = gamma = np.pi / 2
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def rhombohedral(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            alpha: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with rhombohedral constraints.
        
        a == b == c
        
        alpha == beta == gamma != pi / 2
        """
        b = c = a
        beta = gamma = alpha
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def hexagonal(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            c: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with hexagonal constraints.
        
        a == b != c
        
        alpha == beta == pi / 2
        
        gamma == 2 * pi / 3
        """
        b = a
        alpha = beta = np.pi / 2
        gamma = 2 * np.pi / 3
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    @classmethod
    def cubic(
            cls,
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            duplicates: Optional[Tuple[int, int, int]] = None,
            orientation: Optional[np.ndarray] = None,
            pbc: Optional[Tuple[bool, bool, bool]] = None,
            tolerance: float = 1.0e-6,
    ) -> 'Crystal':
        """Initializes a crystal with cubic constraints.
        
        a == b == c
        
        alpha == beta == gamma == pi / 2
        """
        b = c = a
        alpha = beta = gamma = np.pi / 2
        return cls(lattice_data, lattice_sites, a, b, c, alpha, beta, gamma, duplicates, orientation, pbc, tolerance)

    # TODO: Make a C extension to do this.
    @staticmethod
    def _build(
            lattice_data: List[Dict[str, Any]],
            lattice_sites: np.ndarray,
            a: float,
            b: float,
            c: float,
            alpha: float,
            beta: float,
            gamma: float,
            duplicates: Tuple[int, int, int],
            orientation: np.ndarray,
            pbc: Tuple[bool, bool, bool],
            tolerance: float,
    ) -> Tuple[List[Atom], np.ndarray]:
        """Construct a crystalline lattice and populate it with atoms."""
        # calculate lattice vectors from metric tensor
        lattice_vectors = np.sqrt(metric_tensor(a, b, c, alpha, beta, gamma))

        # calculate the magnitude of each lattice vector
        lattice_vectors_magnitude = np.linalg.norm(lattice_vectors, axis=0)

        # calculate the unit vector of each lattice vector
        lattice_vectors_hat = lattice_vectors / lattice_vectors_magnitude

        # calculate rotation matrix between natural orientation and desired orientation
        rotation = Rotation.align_vectors(lattice_vectors_hat, orientation)[0]

        # align the lattice vectors with the desired orientation by applying the
        lattice_vectors_oriented = np.matmul(orientation, lattice_vectors)

        # use QR decomposition to calculate an orthogonal representation of the oriented lattice vectors
        _, r = np.linalg.qr(lattice_vectors_oriented.T)
        lattice_vectors_oriented = np.abs(r) * np.array(duplicates)
        lattice_vectors_oriented_magnitude = np.linalg.norm(lattice_vectors_oriented, axis=0)

        # determine smallest possible size
        minimum_orthogonal_size = np.ceil(
            lattice_vectors_oriented_magnitude / lattice_vectors_magnitude) * np.array(duplicates)
        minimum_orthogonal_size = minimum_orthogonal_size.astype(int)

        atoms: List[Atom] = []
        for xsize in range(minimum_orthogonal_size[0]):
            for ysize in range(minimum_orthogonal_size[1]):
                for zsize in range(minimum_orthogonal_size[2]):
                    offset = np.matmul(np.array([xsize, ysize, zsize]), lattice_vectors)
                    for data, site in zip(lattice_data, lattice_sites):

                        # assign the cartesian position
                        position = np.matmul(site, lattice_vectors) + offset
                        position = rotation.apply(position)

                        # transform the position back into the bounding box
                        for i in range(3):
                            if position[i] < -tolerance:
                                new_position = position[i]
                                while new_position < -tolerance:
                                    new_position += lattice_vectors_oriented_magnitude[i]
                                position[i] = new_position
                            elif position[i] >= lattice_vectors_oriented_magnitude[i] - tolerance:
                                new_position = position[i]
                                while new_position >= lattice_vectors_oriented_magnitude[i] - tolerance:
                                    new_position -= lattice_vectors_oriented_magnitude[i]
                                position[i] = new_position

                        # accept the atom if the position is not occupied
                        positions = np.array([atom.position for atom in atoms])
                        distance, _ = pbc_nearest_neighbor(position, positions, lattice_vectors_oriented, pbc)
                        if distance > tolerance:
                            atom = Atom(position=position, **data)
                            atoms.append(atom)

        return atoms, lattice_vectors_oriented
