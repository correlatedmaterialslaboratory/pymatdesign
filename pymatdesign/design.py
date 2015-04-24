from __future__ import division, print_function, unicode_literals

"""
This module implements the workflow to design new materials.
"""

__author__ = "Chuck-Hou Yee"
__copyright__ = "Copyright 2015, Correlated Materials Laboratory"
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

@profile
def __composition_generator(partial_composition, partial_oxidation,
                            abstract_composition, total_oxidation_state,
                            only_common_oxidation_states):
    pt = PeriodicTable()

    num_elements = len(abstract_composition.elements)
    abstract_element = abstract_composition.elements[0]
    abstract_stoichiometry = abstract_composition[abstract_element]

    possible_compositions = []
    if num_elements == 1:
        for X in pt.all_elements:
            possible_oxidations = set()
            oxidation_states = X.oxidation_states
            if only_common_oxidation_states:
                oxidation_states = X.common_oxidation_states
            for oxi_state in oxidation_states:
                possible_oxidations.add(partial_oxidation + oxi_state * abstract_stoichiometry)
            if total_oxidation_state in possible_oxidations:
                this_composition = partial_composition + Composition({X.symbol: abstract_stoichiometry})
                if partial_composition.num_atoms == 0 or (partial_composition.num_atoms > 0 and not this_composition.is_element):
                    possible_compositions.append(this_composition)
    else:
        new_abstract_composition = abstract_composition - Composition({abstract_element: abstract_stoichiometry})
        for X in pt.all_elements:
            new_composition = partial_composition + Composition({X.symbol: abstract_stoichiometry})
            oxidation_states = X.oxidation_states
            if only_common_oxidation_states:
                oxidation_states = X.common_oxidation_states
            for oxi_state in oxidation_states:
                new_compositions = __composition_generator(new_composition,
                                                           partial_oxidation + oxi_state*abstract_stoichiometry,
                                                           new_abstract_composition,
                                                           total_oxidation_state,
                                                           only_common_oxidation_states)
                possible_compositions += new_compositions
    return possible_compositions

@profile
def generate_compositions_by_oxidation(composition, total_oxidation_state = 0,
                                       only_common_oxidation_states = True):
    """
    Generate all possible realizations of a given abstract composition formula.

    Args:
        composition: abstract composition. Ex: Composition("ABC3")
        total_oxidation_state: constraint on total charge of composition,
            defaults to 0 (neutral).
        only_common_oxidation_states: whether to include rare oxidation states
            of elements

    Returns:
        A set of compositions satisfying specified constraints.
    """
    composition = Composition(composition)
    num_elements = len(composition.elements)
    if num_elements == 0:
        compositions = []
    else:
        compositions = __composition_generator(Composition(), 0, composition,
                                               total_oxidation_state,
                                               only_common_oxidation_states)
    return set(compositions)
