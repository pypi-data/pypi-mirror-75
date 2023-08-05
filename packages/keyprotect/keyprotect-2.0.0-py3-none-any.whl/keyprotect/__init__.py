from __future__ import absolute_import

import redstone
from redstone import auth as bxauth  # noqa: F401


def Client(*args, **kwargs):  # noqa: N802
    cl = redstone.service("KeyProtect", *args, **kwargs)
    return cl
