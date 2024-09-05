# -*- coding: utf-8 -*-
"""
Publishers
"""

import zmag


@zmag.pub(seconds=1)
async def generic_other():
    """Generic"""
    response = zmag.Data()
    response.body = {"message": "generic other"}
    return response
