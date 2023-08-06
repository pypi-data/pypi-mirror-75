# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from copy import copy
from datetime import datetime, timedelta
import inspect
import json
import random
from string import ascii_lowercase
from typing import Any, List, Mapping
import uuid

from spavro.io import validate as spavro_validate
from spavro.schema import parse as parse_schema

from aether.python.avro.schema import Node
from aether.python.avro.tools import (
    AvroValidationException,
    random_avro,
    validate
)
from aether.python.utils import replace_nested

'''
    Utility Functions
'''


def guid():
    return str(uuid.uuid4())


def single_choice(choices):
    # return one item from a list
    return random.choice(choices)


def subset(choices, max=None):
    # return a random subset from some choices
    if not max:
        max = len(choices)
    size = random.randint(1, max)
    return random.sample(choices, size)


def str_time_prop(start, end, fraction):
    # get an iso string of a point a fraction
    # between a start and end datetime
    stime = datetime.fromisoformat(start)
    etime = datetime.fromisoformat(end)
    new_time = stime + fraction * (etime - stime)
    return new_time.isoformat()


'''
    Callable From the Generator
    (only uses kwargs, and might know how to use Nodes)
'''


def random_date(start=None, end=None, min_prop=0, max_prop=1):
    prop = min_prop + random.random() * (max_prop - min_prop)
    return str_time_prop(start, end, prop)


def random_str(constant=None, max=32):
    if constant:
        return constant
    return ''.join([
        c for i in range(max) for c in random.choice(ascii_lowercase)
    ])


def random_numeric(min=0, max=1, cast=int):
    return cast(random.random() * (max - min) + min)


def select1(choices=None, node=None):
    if not choices:
        choices = [i.get('value') for i in node.__lookup]
    return single_choice(choices)


def select_many(choices=None, node=None, max=None, path=None):
    if not choices:
        choices = [i.get('value') for i in node.__lookup]
    return subset(choices, max)


class SampleGenerator(object):

    _base_name: str
    _limits: Mapping[str, List[Any]]
    _exclude: List[str]
    extended_handlers: Mapping[str, tuple]
    regular_handlers: Mapping[str, tuple]
    named_handlers: Mapping[str, tuple]
    value_overrides: Mapping[str, str]

    def __init__(self, schema: Mapping[Any, Any] = None, node: Node = None, raw_schema: str = None):
        if not any([schema, node, raw_schema]):
            raise ValueError(
                'Must include one of: schema (dict) node (Node) or raw_schema (JSON)')
        if node:
            schema = node
        else:
            if schema:
                schema = Node(schema)
            else:
                schema = Node(json.loads(raw_schema))
        self._base_name = schema.name
        self.load_defaults()
        self.schema = schema
        self.spavro_schema = parse_schema(self.schema._source)

    def load_defaults(self):
        self._limits = {
            'datetime': [
                (datetime.now() - timedelta(days=365)).isoformat(),
                datetime.now().isoformat()
            ],
            'int': [0, 1000],
            'float': [0.0, 1.0]
        }
        self._exclude = []
        # handlers are defined in form: (fn, **default_kwargs)
        self.extended_handlers = {
            'string': (random_str, {'max': 10}),
            'select': (select_many, {}),
            'select1': (select1, {}),
            'dateTime': (random_date, {
                'start': self._limits['datetime'][0],
                'end': self._limits['datetime'][1]
            })
        }
        # If there is not an explicit handler, we will use the avro.tools.random_avro tool to fill.
        self.regular_handlers = {
            'string': (random_str, {'max': 10}),
            'int': (random_numeric, {
                'min': self._limits['int'][0],
                'max': self._limits['int'][1]
            }),
            'float': (random_numeric, {
                'min': self._limits['float'][0],
                'max': self._limits['float'][1],
                'cast': float
            })
        }
        self.named_handlers = {
            'id': (guid, None),
            '_id': (guid, None)
        }
        self.value_overrides = {}

    '''
        Internal function / argument handling
    '''

    def get_kwargs(self, fn, kwargs, path, node):
        kwargs = copy(kwargs)
        sig = inspect.signature(fn)
        allowed = [i for i in sig.parameters.keys()]
        if 'path' in allowed:
            kwargs['path'] = path
        if 'node' in allowed:
            kwargs['node'] = node
        name = path[len(self._base_name) + 1::]
        rules = self.value_overrides.get(name, [])
        for arg in rules:
            if arg in allowed:
                kwargs[arg] = rules.get(arg)
        return kwargs

    def handle(self, fn, kwargs):
        if kwargs:
            return fn(**kwargs)
        else:
            return fn()

    '''
        Set Handlers
    '''

    def register_type_handler(self, _type, handler, extended=False):
        if extended:
            self.extended_handlers[_type] = handler
        else:
            self.regular_handlers[_type] = handler

    def register_field_handler(self, path, handler):
        self.named_handlers[path] = handler

    def set_overrides(self, path, rules):
        for k, v in rules.items():
            self.set_override(path, k, v)

    def set_override(self, path, _type, value):
        rules = self.value_overrides.get(path, {})
        rules[_type] = value
        self.value_overrides[path] = rules

    def set_exclusion(self, exclusion):
        self._exclude.append(exclusion)

    '''
        Render the sample
    '''

    def from_schema(self, path):
        if path in self.named_handlers:
            return self.handle(*self.named_handlers[path])
        path = f'{self.schema.name}.{path}'
        node = self.schema.get_node(path)
        try:
            _type = getattr(node, '__extended_type')
            if _type not in self.extended_handlers:
                raise AttributeError(f'type: {_type} not handled')
            fn, kwargs = self.extended_handlers[_type]
        except AttributeError:
            _type = node.avro_type
            if isinstance(_type, list) and len(_type) > 1:
                if 'null' in _type:
                    _type.remove('null')
                _type = random.choice(_type)
            elif isinstance(_type, list):
                _type = _type[0]
            try:
                fn, kwargs = self.regular_handlers[_type]
            except KeyError:
                return random_avro(json.loads(node._source))
        extended_kwargs = self.get_kwargs(fn, kwargs, path, node)
        return self.handle(fn, extended_kwargs)

    def make_sample(self):
        out = {}
        for node in self.schema.iter_children():
            path = node[(len(self.schema.name) + 1)::]
            if path in self._exclude:
                continue
            val = self.from_schema(path)
            replace_nested(out, path.split('.'), val)
        ok = spavro_validate(self.spavro_schema, out)
        if not ok:
            result = validate(self.spavro_schema, out)
            if result.errors:
                raise AvroValidationException(result.errors)
            else:
                raise AvroValidationException(
                    'Avro Validation failed, but detailed reporting found no errors.')
        return out
