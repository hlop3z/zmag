# -*- coding: utf-8 -*-
"""
    { Schema }
"""

import zmag


# Create your <schema> here.
@zmag.schema
class Schema:
    types = [
        {
            "name": "author",
            "config": {
                "unique": ["first_name"],
                "ignore": ["full_name"],
                "auto": ["timestamp"],
                "unique_together": [
                    # ["first_name", "last_name"],
                ],
            },
            "schema": {
                "first_name": "$string",
                "last_name": "$string",
                "full_name": "$string",
                "timestamp": "$datetime",
                "books": ["book"],
            },
        },
        {
            "name": "book",
            "config": {
                # "table_name": None,
                # "primary_key": None,
                # "required": None,
                "index": None,
                "unique": None,
                "unique_together": None,
                "ignore": None,
            },
            "schema": {
                "title": "$string",
                "book": "book",
                "author": "author",
                "meta": "$dict",
            },
        },
    ]
