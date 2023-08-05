# -*- mode:python; coding: utf-8 -*-
# @file
# @section LICENSE
#
# Copyright (©) 2016-2020 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Helper functions for dumpers
"""
from functools import wraps
from collections import defaultdict
import os
import numpy as np

__all__ = ["make_periodic", "step_dump", "directory_dump"]


def makePeriodic(data):
    data = np.append(data, np.expand_dims(data[:, 0, ...], axis=1), axis=1)
    data = np.append(data, np.expand_dims(data[:, :, 0, ...], axis=2), axis=2)
    return data


def makeTractionPeriodic(data):
    data = np.append(data, np.expand_dims(data[0, ...], axis=0), axis=0)
    data = np.append(data, np.expand_dims(data[:, 0, ...], axis=1), axis=1)
    return data


make_periodic = defaultdict(lambda: makePeriodic,
                            traction=makeTractionPeriodic,
                            gap=makeTractionPeriodic)


def step_dump(cls):
    """
    Decorator for dumper with counter for steps
    """
    orig_init = cls.__init__
    orig_dump = cls.dump

    def __init__(obj, *args, **kwargs):
        orig_init(obj, *args, **kwargs)
        obj.count = 0

    def postfix(obj):
        return "_{:04d}".format(obj.count)

    def dump(obj, *args, **kwargs):
        orig_dump(obj, *args, **kwargs)
        obj.count += 1

    cls.__init__ = __init__
    cls.dump = dump
    cls.postfix = property(postfix)

    return cls


def directory_dump(directory=""):
    "Decorator for dumper in a directory"

    def actual_decorator(cls):
        orig_dump = cls.dump
        orig_filepath = cls.file_path.fget

        @wraps(cls.dump)
        def dump(obj, *args, **kwargs):
            if not os.path.exists(directory):
                os.mkdir(directory)
            if not os.path.isdir(directory):
                raise Exception('{} is not a directory'.format(directory))

            orig_dump(obj, *args, **kwargs)

        @wraps(cls.file_path)
        def file_path(obj):
            return os.path.join(directory, orig_filepath(obj))

        cls.dump = dump
        cls.file_path = property(file_path)

        return cls

    return actual_decorator
