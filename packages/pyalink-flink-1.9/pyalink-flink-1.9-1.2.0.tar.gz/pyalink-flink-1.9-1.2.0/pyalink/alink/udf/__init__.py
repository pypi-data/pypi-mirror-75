#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common.utils.packages import has_pyflink

if has_pyflink():
    from .udtf import udtf, TableFunction

    from pyflink.table.udf import udf, ScalarFunction
    from pyflink.table.types import DataTypes
else:
    from .udtf import udtf, TableFunction
    from .udf import udf, ScalarFunction
    from .data_type import DataTypes

__all__ = ["udf", "udtf", "ScalarFunction", "TableFunction", "DataTypes"]
