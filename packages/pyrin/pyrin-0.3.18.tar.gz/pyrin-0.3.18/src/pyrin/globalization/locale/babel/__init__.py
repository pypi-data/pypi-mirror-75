# -*- coding: utf-8 -*-
"""
babel package.
"""

from pyrin.packaging.base import Package


class BabelPackage(Package):
    """
    babel package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'globalization.locale.babel.component'
    CONFIG_STORE_NAMES = ['babel']
    EXTRA_CONFIG_STORE_NAMES = ['babel.mappings']
