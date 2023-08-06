from typing import Union
from .comment_remover import js_rem_comments as __js_rem_comments


def js_rem_comments(src: Union[bytes, str]) -> bytes:
    return __js_rem_comments(src)
