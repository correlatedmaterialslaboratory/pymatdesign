from __future__ import division, print_function, unicode_literals

"""
This module tests the combinatoric generation of compositions.
"""

__author__ = "Chuck-Hou Yee"
__copyright__ = "Copyright 2015, Correlated Materials Laboratory"
__version__ = "0.1"
__maintainer__ = "Chuck-Hou Yee"
__email__ = "chuckyee@physics.rutgers.edu"
__status__ = "Development"
__date__ = "Apr 23, 2015"

import unittest


from pymatgen.core.periodic_table import PeriodicTable
from pymatgen.core.composition import Composition
from pymatdesign import generate_compositions_by_oxidation


class CompositionCombinatoricsTest(unittest.TestCase):
    def generate_species(self, stoichiometry = 1, oxidation_state = 0,
                         common_oxidations = False):
        """
        Reference code to return elements with given oxidations state.
        """
        pt = PeriodicTable()
        possible_species = set()
        for X in pt.all_elements:
            oxidations = X.oxidation_states
            if common_oxidations:
                oxidations = X.common_oxidation_states
            possible_oxidations = [oxi * stoichiometry for oxi in oxidations]
            if oxidation_state in possible_oxidations:
                possible_species.add(Composition(X.symbol))
        return possible_species

    def generate_binaries(self, stoichiometry_A = 1, stoichiometry_X = 1,
                          total_oxidation = 0, common_oxidations = False):
        """
        Reference code to generate possible A_n B_m binary compositions with
        arbitrary total oxidation states.
        """
        pt = PeriodicTable()
        possible_compositions = set()
        for A in pt.all_elements:
            for X in pt.all_elements:
                possible_oxidations = set()
                oxidations_A = A.oxidation_states
                oxidations_X = X.oxidation_states
                if common_oxidations:
                    oxidations_A = A.common_oxidation_states
                if common_oxidations:
                    oxidations_X = X.common_oxidation_states
                for oxi_A in oxidations_A:
                    for oxi_X in oxidations_X:
                        oxi = oxi_A*stoichiometry_A + oxi_X*stoichiometry_X
                        possible_oxidations.add(oxi)
                if total_oxidation in possible_oxidations:
                    new_composition = Composition(
                        {A.symbol: stoichiometry_A,
                         X.symbol: stoichiometry_X})
                    if not new_composition.is_element:
                        possible_compositions.add(new_composition)
    
        return possible_compositions

    def test_ions(self):
        # 3+ ions
        ions = self.generate_species(1, 3, common_oxidations = False)
        args = {'composition': 'X', 'total_oxidation_state': 3,
                'only_common_oxidation_states': False}
        output = generate_compositions_by_oxidation(**args)
        self.assertEqual(ions, output)

        # common 3+ ions
        ions = self.generate_species(1, 3, common_oxidations = True)
        args = {'composition': 'X', 'total_oxidation_state': 3,
                'only_common_oxidation_states': True}
        output = generate_compositions_by_oxidation(**args)
        self.assertEqual(ions, output)

    def test_ions_empty(self):
        # 10- (nonexistent) ions
        ions = self.generate_species(1, -10, common_oxidations = False)
        args = {'composition': 'X', 'total_oxidation_state': -10,
                'only_common_oxidation_states': False}
        output = generate_compositions_by_oxidation(**args)
        self.assertEqual(ions, output)

    def test_binary(self):
        """
        Generate_compositions_by_oxidation should generate all binary
        compounds with given oxidation state
        """
        # AX neutral
        binaries = self.generate_binaries(1, 1, 0, common_oxidations = True)
        args = {'composition': 'AX', 'total_oxidation_state': 0,
                'only_common_oxidation_states': True}
        output = generate_compositions_by_oxidation(**args)
        self.assertEqual(binaries, output)

        # AX2 2- charge
        binaries = self.generate_binaries(1, 2, -2, common_oxidations = True)
        args = {'composition': 'AX2', 'total_oxidation_state': -2,
                'only_common_oxidation_states': True}
        output = generate_compositions_by_oxidation(**args)
        self.assertEqual(binaries, output)


class GenerateVaspTest(unittest.TestCase):
    def test_blank(self):
        pass

if __name__ == "__main__":
    unittest.main()
