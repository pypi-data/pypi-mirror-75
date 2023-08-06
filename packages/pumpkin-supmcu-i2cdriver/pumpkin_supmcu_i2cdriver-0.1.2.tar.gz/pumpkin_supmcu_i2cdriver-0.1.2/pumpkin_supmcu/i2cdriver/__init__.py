# coding: utf-8
# ##############################################################################
#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
The `pumpkin_supmcu.i2cdriver` module contains an implementations of the :class:`~pumpkin_supmcu.I2CMaster` for the following
devices:

* The `I2CDriver Board <https://i2cdriver.com/>`_ as :class:`~pumpkin_supmcu.i2cdriver.I2CDriverMaster`.
"""
from .i2cdriver import I2CDriverMaster
