# -*- coding: utf-8 -*-
"""
core globals module.
"""

from flask_babel import gettext
from sqlalchemy.util._collections import AbstractKeyedTuple

from pyrin.core.structs import CoreObject


# this value should be used as `None`, where the `None` itself has a meaning.
NULL = CoreObject()

# this value should be used where we need to reference class type of None objects.
NONE_TYPE = type(None)

# this value should be used where we want to determine if an object is a list type or not.
LIST_TYPES = (list, tuple, set)

# this method should be used for localizable strings.
_ = gettext

# this value should be used when working on AbstractKeyedTuple objects.
ROW_RESULT = AbstractKeyedTuple
