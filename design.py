from __future__ import division, unicode_literals

"""
This module implements the workflow to design new materials.
"""

__author__ = "Chuck-Hou Yee"
__copyright__ = "Copyright 2015, The Correlated Materials Laboratory"
__version__ = "0.1"
__maintainer__ = "Chuck-Hou Yee"
__email__ = "chuckyee@physics.rutgers.edu"
__status__ = "Development"
__date__ = "Apr 21, 2015"

import six
from six.moves import filter, map, zip

import pymatgen as mp
from pymatgen.core.composition import Composition
from pymatgen.core.periodic_table import PeriodicTable, Element


if __name__ == '__main__':
    # Find all binary compositions AX2 which have 2- charge.
    #   Example: (HgSe2)Ba2CuO2

    pt = PeriodicTable()
    elements = pt.all_elements

    possible_compositions = []
    for A in elements:
        for X in elements:
            possible_oxidations = set()
            for oxi_A in A.oxidation_states:
                for oxi_X in X.oxidation_states:
                    possible_oxidations.add(oxi_A + 2*oxi_X)
            if -2 in possible_oxidations:
                possible_compositions.append(Composition(A.symbol + X.symbol + "2"))
    print possible_compositions
