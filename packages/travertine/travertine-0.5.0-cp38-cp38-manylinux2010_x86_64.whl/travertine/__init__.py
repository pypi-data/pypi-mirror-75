#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from ._impl import __doc__  # noqa
from ._impl import Program, NullDemand, UnitaryDemand, ExternalObject  # noqa

from .types import Procedure
from .topo import topological_sort


NULL_DEMAND = NullDemand()


def create_program(procedure: Procedure, capacity: int = None) -> Program:
    """Creates a new program with the entire `procedure` added.

    This function follows a topological sort of the procedure graph so that it
    complies with the API of `Program`:class:.

    The `capacity` should be a close estimate of the number of procedures in
    the program.  You should strive to produce a number as low as possible to
    avoid consuming too much memory.  If unsure leave it as None.

    """
    program = Program(capacity)
    for proc in topological_sort(procedure):
        proc.add_to_travertine_program(program)
    return program
