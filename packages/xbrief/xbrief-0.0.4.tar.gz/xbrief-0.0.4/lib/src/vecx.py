import math

from xbrief import Preci


def vbrief(arr: list,
           abstract=None,
           head: int = None,
           tail: int = None):
    preci = Preci.from_arr(arr, head, tail).map(abstract).stringify()
    elements = preci \
        .ject_head(tags_indexed) \
        .ject_tail(lambda ar: tags_indexed(ar, len(arr) - tail)) \
        .to_list('...')
    if elements:
        return '\r\n'.join(elements)
    else:
        return '(Ø)'


def hbrief(arr: list,
           delimiter: str = ', ',
           abstract=None,
           head: int = None,
           tail: int = None):
    preci = Preci.from_arr(arr, head, tail).map(abstract)
    elements = preci.to_list('...')
    if elements:
        return delimiter.join(elements)
    else:
        return '(Ø)'


def format_tag(key, val, k_fmt=None, v_fmt=None):
    if k_fmt is None:
        if v_fmt is None:
            return f'[{key}] ({val})'
        else:
            return f'[{key}] ({val:{v_fmt}})'
    else:
        if v_fmt is None:
            return f'[{key:{k_fmt}}] ({val})'
        else:
            return f'[{key:{k_fmt}}] ({val:{v_fmt}})'


def is_empty(arr: list):
    if not arr:
        return True
    else:
        return False


def tags_indexed(arr, start_index: int = 1, index_format=None):
    if index_format:
        return [f'[{str(i + start_index):{index_format}}] {x}' for i, x in enumerate(arr)]
    else:
        max_idx_len = math.floor(math.log10(len(arr) + start_index)) + 1
        return [f'[{str(i + start_index): >{max_idx_len}}] {x}' for i, x in enumerate(arr)]
