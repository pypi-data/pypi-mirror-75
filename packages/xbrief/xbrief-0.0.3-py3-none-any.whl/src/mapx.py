from xbrief import strx, Preci, aeu, rn


def hbrief(lex: dict,
           delimiter=', ',
           abstract=None,
           head: int = None,
           tail: int = None):
    if abstract:
        actual_abstract = lambda kv: f'{kv[0]}:({abstract(kv[1])})'
    else:
        actual_abstract = lambda kv: f'{kv[0]}:({kv[1]})'
    preci = Preci \
        .from_arr(list(lex.items()), head, tail) \
        .map(actual_abstract)
    elements = preci.to_list('...')
    if elements:
        return delimiter.join(elements)
    else:
        return aeu


def vbrief(lex: dict,
           abstract=None,
           head: int = None,
           tail: int = None):
    if abstract:
        actual_abstract = lambda kv: (f'{kv[0]}', f'{abstract(kv[1])}')
    else:
        actual_abstract = lambda kv: (f'{kv[0]}', f'{kv[1]}')
    preci = Preci \
        .from_arr(list(lex.items()), head, tail) \
        .map(actual_abstract)
    length = max(preci.map(lambda kv: len(kv[0])).to_list())
    # f'{kvp[0]: <{length}}', kvp[1]
    elements = preci \
        .map(lambda kvp: strx.tag(strx.pad_start(kvp[0], length), kvp[1])) \
        .to_list(strx.pad_start('...', length))
    if elements:
        return rn.join(elements)
    else:
        return aeu
