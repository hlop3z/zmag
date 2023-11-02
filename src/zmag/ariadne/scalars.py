from decimal import Decimal
import datetime
import json
import re

from ariadne import ScalarType

from .jsql import Util

form_scalar = ScalarType("Form")
list_scalar = ScalarType("Dict")
dict_scalar = ScalarType("List")
json_scalar = ScalarType("JSON")
decimal_scalar = ScalarType("Decimal")
datetime_scalar = ScalarType("Datetime")
date_scalar = ScalarType("Date")
time_scalar = ScalarType("Time")


# -----------------------------------------------
# Form
# -----------------------------------------------


@form_scalar.serializer
def serialize_form(value):
    return value


@form_scalar.value_parser
def parse_form_value(value):
    data = {}
    try:
        data = json.loads(value)
    except:
        pass
    data = {Util.camel_to_snake(key): value for key, value in data.items()}
    return data


# -----------------------------------------------
# JSON
# -----------------------------------------------


@json_scalar.serializer
def serialize_json(value):
    return value


@json_scalar.value_parser
def parse_json_value(value):
    data = {}
    try:
        data = json.loads(value)
    except:
        pass
    return data


# -----------------------------------------------
# Dict
# -----------------------------------------------
dict_scalar.serializer(serialize_json)
dict_scalar.value_parser(parse_json_value)

# -----------------------------------------------
# Dict
# -----------------------------------------------
list_scalar.serializer(serialize_json)
list_scalar.value_parser(parse_json_value)

# -----------------------------------------------
# Decimal
# -----------------------------------------------


@decimal_scalar.serializer
def serialize_decimal(value):
    return str(value)


@decimal_scalar.value_parser
def parse_decimal_value(value):
    data = None
    try:
        data = Decimal(value)
    except:
        pass
    return data


# -----------------------------------------------
# DateTime
# -----------------------------------------------


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value):
    return datetime.datetime.fromisoformat(value)


# -----------------------------------------------
# Date
# -----------------------------------------------


@date_scalar.serializer
def serialize_date(value):
    return value.isoformat()


@date_scalar.value_parser
def parse_date_value(value):
    return datetime.date.fromisoformat(value)


# -----------------------------------------------
# Time
# -----------------------------------------------


@time_scalar.serializer
def serialize_time(value):
    return value.isoformat()


@time_scalar.value_parser
def parse_time_value(value):
    return datetime.time.fromisoformat(value)


SCALARS = [
    form_scalar,
    json_scalar,
    datetime_scalar,
    date_scalar,
    time_scalar,
    dict_scalar,
    list_scalar,
]
