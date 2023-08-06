from typing import Union
from .code_cleaner import clean_nl as __clean_nl


def clean_nl(src: Union[bytes, str]) -> bytes:
    return __clean_nl(src)
