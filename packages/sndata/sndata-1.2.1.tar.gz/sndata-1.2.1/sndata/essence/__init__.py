#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``essence`` module provides access to data from the Equation of State:
Supernovae trace Cosmic Expansion survey (ESSENCE). It includes spectroscopic
and photometric data published in Foley et al. 2009 and Narayan et al. 2016
respectively.
"""

from ._narayan16 import Narayan16

survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
survey_abbrev = 'ESSENCE'
