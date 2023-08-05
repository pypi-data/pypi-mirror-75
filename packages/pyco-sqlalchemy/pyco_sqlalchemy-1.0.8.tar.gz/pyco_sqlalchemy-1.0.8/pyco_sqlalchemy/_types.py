import json
from datetime import datetime
from collections import OrderedDict
from dateutil.parser import parse as parse_date
from sqlalchemy import types
import os


class DateTime(types.TypeDecorator):
    """
    # sample 1:
    @declared_attr
    def created_time(self):
        return db.Column(DateTime, default=datetime.utcnow)

    # sample 2:
    updated_time = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """
    impl = types.DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            return parse_date(value)
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        else:
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S.%f")


class FixedBool(types.TypeDecorator):
    impl = types.Boolean

    def process_bind_param(self, value, dialect):
        if value in ["0", 0, "false", "False"]:
            value = False
        elif value in ["1", 1, "true", "True"]:
            value = True
        return value


class TrimString(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, str):
            value = value.strip()
        return value


class StringTags(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, str):
            return ','.join(map(lambda x: x.strip(), value.split(',')))
        return ""


class OrderedJson(types.TypeDecorator):
    impl = types.JSON

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(value)
        return value


class JsonText(types.TypeDecorator):
    # NOTE: actually it supports `sqltypes.JSON`
    # https://docs.sqlalchemy.org/en/13/core/custom_types.html#sqlalchemy.types.TypeDecorator
    impl = types.Text
    JSONDecoder = json.JSONDecoder
    JSONEncoder = json.JSONEncoder

    def process_bind_param(self, value, dialect):
        return json.dumps(value, indent=2, cls=self.JSONEncoder)

    def process_result_value(self, value, dialect):
        return json.loads(value, cls=self.JSONDecoder)
