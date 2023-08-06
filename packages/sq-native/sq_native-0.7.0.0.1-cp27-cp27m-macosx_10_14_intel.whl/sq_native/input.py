# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Binding for the WAF Input Data Structure
"""
from ctypes import (POINTER, Structure, byref, c_bool, c_char_p, c_int,
                    c_int64, c_size_t, c_uint64, c_void_p)

from . import get_lib
from ._compat import UNICODE_CLASS

PWI_INVALID = 0
PWI_SIGNED_NUMBER = 1 << 0
PWI_UNSIGNED_NUMBER = 1 << 1
PWI_STRING = 1 << 2
PWI_ARRAY = 1 << 3
PWI_MAP = 1 << 4


class C_PWArgs(Structure):

    _fields_ = [
        ("name", c_char_p),
        ("name_length", c_uint64),
        ("value", c_void_p),
        ("nb_entries", c_uint64),
        ("type", c_int),
    ]


_input_lib = None


def get_input_lib():
    global _input_lib

    if _input_lib is None:
        lib = get_lib()
        lib.powerwaf_createArray.argstype = []
        lib.powerwaf_createArray.restype = C_PWArgs
        lib.powerwaf_createInt.argstype = [c_int64]
        lib.powerwaf_createInt.restype = C_PWArgs
        lib.powerwaf_createUint.argstype = [c_uint64]
        lib.powerwaf_createUint.restype = C_PWArgs
        lib.powerwaf_createMap.restype = C_PWArgs
        lib.powerwaf_createStringWithLength.argstype = [c_char_p, c_size_t]
        lib.powerwaf_createStringWithLength.restype = C_PWArgs

        lib.powerwaf_addToPWArgsArray.argtypes = [
                POINTER(C_PWArgs), C_PWArgs]
        lib.powerwaf_addToPWArgsArray.restype = c_bool
        lib.powerwaf_addToPWArgsMap.argtypes = [
            POINTER(C_PWArgs), c_char_p, c_size_t, C_PWArgs]
        lib.powerwaf_addToPWArgsMap.restype = c_bool

        lib.powerwaf_freeInput.argtypes = [POINTER(C_PWArgs), c_bool]
        lib.powerwaf_freeInput.restype = None
        _input_lib = lib
    return _input_lib


def create_array():
    return get_input_lib().powerwaf_createArray()


def create_int(value):
    return get_input_lib().powerwaf_createInt(c_int64(value))


def create_uint(value):
    return get_input_lib().powerwaf_createUint(c_uint64(value))


def create_map():
    return get_input_lib().powerwaf_createMap()


def create_string(value, max_string_length=4096):
    if isinstance(value, UNICODE_CLASS):
        value = value[:max_string_length].encode("utf-8", errors="surrogatepass")

    if not isinstance(value, bytes):
        raise ValueError("value must be a string or bytes")

    value = value[:max_string_length]
    return get_input_lib().powerwaf_createStringWithLength(value, len(value))


def append_to_array(array, value):
    return get_input_lib().powerwaf_addToPWArgsArray(byref(array), value)


def append_to_map(array, key, value):
    if isinstance(key, UNICODE_CLASS):
        key = key.encode("utf-8", errors="surrogatepass")

    if not isinstance(key, bytes):
        raise ValueError("value must be a string or bytes")

    return get_input_lib().powerwaf_addToPWArgsMap(byref(array), key, 0, value)


def free(value):
    get_input_lib().powerwaf_freeInput(byref(value), False)


def create(value, max_depth=10, ignore_none=True, max_string_length=4096,
           max_items=150):
    """ Lower-level function to convert a Python value to input value
    """
    if isinstance(value, str) or isinstance(value, bytes):
        return create_string(value, max_string_length=max_string_length)

    if isinstance(value, bool):
        return create_uint(int(value))

    if isinstance(value, int):
        if value < 0:
            return create_int(value)
        else:
            return create_uint(value)

    if isinstance(value, list) or isinstance(value, tuple):
        obj = create_array()
        if max_depth <= 0:
            # ignore if deeply nested
            return obj
        for i, item in enumerate(value):
            if i >= max_items or (item is None and ignore_none):
                continue
            item_obj = create(item, max_depth=max_depth - 1)
            ret = append_to_array(obj, item_obj)
            if ret is False:
                free(item_obj)
        return obj

    if isinstance(value, dict):
        obj = create_map()
        if max_depth <= 0:
            # ignore if deeply nested
            return obj
        for i, (k, v) in enumerate(value.items()):
            if i >= max_items or (v is None and ignore_none):
                continue
            item_obj = create(v, max_depth=max_depth - 1)
            ret = append_to_map(obj, k, item_obj)
            if ret is False:
                free(item_obj)
        return obj

    return create_string(UNICODE_CLASS(value), max_string_length=max_string_length)


class PWArgs:
    """
    Higher-level bridge between Python values and input values.
    """

    def __init__(self, obj):
        self._obj = obj

    def __del__(self):
        if self._obj is None:
            return
        free(self._obj)
        self._obj = None

    @classmethod
    def from_python(cls, value, **kwargs):
        """ Convert a Python value to a PWArgs.
        """
        return cls(create(value, **kwargs))

    def __repr__(self):
        return "<{} obj={!r}>".format(self.__class__.__name__, self._obj)
