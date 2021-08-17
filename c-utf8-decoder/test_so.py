import os

from ctypes import *
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def libutf8_decoder():
    return cdll.LoadLibrary("libutf8_decoder.so")


@pytest.mark.parametrize("text", [
    "abcd",
    "Hello!",
    "Привет!",
    "你好",
    "🏠",
])
def test_utf8_decoder(libutf8_decoder, text):
    lib = libutf8_decoder
    lib.decode_utf8.restype = c_void_p
    
    array_size = len(text.encode('utf-16-le')) // 2
    buffer = (c_uint32 * array_size)()

    result = lib.decode_utf8(buffer, text.encode('utf-8'))

    result_size = (result - addressof(buffer)) // sizeof(c_uint32)
    assert result_size == array_size

    print(list(buffer))
    utf16_le_bytes = b''.join(map(lambda x: x.to_bytes(2, byteorder='little'), buffer))
    assert utf16_le_bytes == text.encode('utf-16-le')
