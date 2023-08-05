"""
stride.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np
import pandas as pd
import os
import re
import subprocess


# TODO it would be great to eventually bind stride to Python directly (as opposed to going through subprocess)
# Compute secondary structure with stride
def stride(pdb, executable='stride'):
    """
    Compute the secondary structure using STRIDE

    In addition to the secondary structure, STRIDE outputs phi and psi dihedral angles as well as the solvent-accessible
    surface area.

    Parameters
    ----------
    pdb : str
        Path to PDB file.
    executable : str
        Location of STRIDE executable (Default: stride).

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the results of STRIDE. Columns include: residue_id, chain, secondary_structure,
        secondary_structure_text, phi, psi, and area.

    Examples
    --------
    Computing the secondary structure as you would on the command line with STRIDE.
    >>> from simlib.external import stride
    >>> secondary_structure = stride('my.pdb')['secondary_structure'].values
    >>> print('% random coil = %s' % (secondary_structure == 'C').mean())

    Computing the secondary structure on a Structure (or Trajectory)
    >>> from simlib.analysis.amino import compute_secondary_structure
    >>> from simlib.io import read_pdb
    >>> secondary_structure = compute_secondary_structure(read_pdb('my.pdb'))
    >>> print('% random coil = %s' % (secondary_structure == 'C').mean())
    """

    # Make sure executable exists
    if not os.path.exists(executable):
        raise AttributeError('executable %s not found. Download at http://webclu.bio.wzw.tum.de/stride/' % executable)
    
    # Run STRIDE and capture output
    process = subprocess.Popen([executable, pdb], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    # Error check; make sure STRIDE finishes successfully
    if process.wait() != 0:
        raise SystemError('STRIDE failed')

    # Filter for pertinent records in output
    records = re.sub(r'^(?!ASG).*$', '', output.decode('ASCII'), flags=re.MULTILINE).replace('\n\n', '\n').lstrip()

    # Sections of output
    sections = np.array([
        (3, 'record', '<U3'),
        (5, 'residue', '<U5'),
        (2, 'chain', '<U2'),
        (5, 'residue_id', 'int'),
        (5, 'residue_id2', 'int'),
        (5, 'secondary_structure', '<U4'),
        (14, 'secondary_structure_text', '<U14'),
        (10, 'phi', 'float'),
        (10, 'psi', 'float'),
        (10, 'area', 'float'),
        (10, 'extra', '<U10')
    ], dtype=[('width', 'i1'), ('column', '<U24'), ('type', '<U10')])

    # Parse records and return as DataFrame
    data = np.genfromtxt(records.split('\n'), delimiter=sections['width'], dtype=sections['type'], autostrip=True)
    data = pd.DataFrame(data.tolist(), columns=sections['column'])

    # Drop extraneous columns
    data = data.drop(columns=['record', 'residue_id2', 'extra'])

    # Return data
    return data
