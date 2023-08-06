# meow.validators
#
# Copyright (c) 2020-present Andrey Churin (aachurin@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from .container import (
    V,
    field,
    get_validator,
    Container,
)
from .elements import (
    Validator,
    Optional,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    Date,
    Time,
    UUID,
    Const,
    Any,
    Tuple,
    TypedTuple,
    Object,
    TypedObject,
    Mapping,
    TypedMapping,
    List,
    TypedList,
    Set,
    FrozenSet,
    Union,
    If,
    Enum,
    Choice,
)
from .exception import ValidationError


__version__ = "1.3.9"
__all__ = (
    "V",
    "field",
    "get_validator",
    "ValidationError",
    "Validator",
    "Optional",
    "String",
    "Float",
    "Integer",
    "Boolean",
    "DateTime",
    "Date",
    "Time",
    "UUID",
    "Const",
    "Any",
    "Tuple",
    "TypedTuple",
    "Object",
    "TypedObject",
    "Mapping",
    "TypedMapping",
    "List",
    "TypedList",
    "Set",
    "FrozenSet",
    "Union",
    "If",
    "Enum",
    "Choice",
    "Container",
)
