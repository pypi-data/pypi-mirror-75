It provides:

    - Opening molecular `.xyz` files.
    - Helps generating nicely formatted Molpro or Gaussian input files
      for quantum chemical calculations.
    - Conversion between Cartesian and internal coordinate
      representations.
    - Molecular shape matching based on the Kabsch-Umeyama algorithm.
    - Calculating atomic distances, bond angles and dihedral angles.
    - Calculating the principal moments of inertia.
    - Generating permuted geometries.
    - Calculating the Euler angles from 3-dimensional rotation
      matrices.
    - Calculating the molecular adjacency list based on atomic
      distances.
    - Some chemical graph-theoretical tools derived from the adjacency
      list.

Limitations:

    - Only supporting dummy atoms for converting internal coordinate
      representations (Z-matrices) to Cartesian.
    - A Cartesian representation can be converted to Z-matrix if all
      atoms (with the exception of the first) are connected to at
      least one atom with an index lower than its own.