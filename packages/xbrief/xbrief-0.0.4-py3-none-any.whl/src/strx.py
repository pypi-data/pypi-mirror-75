import re

from xbrief import rn, tb


def wl(m):
    print(m)


def tag(label, item):
    i = indexOfFirstNonTab(label)
    key, text = str(label), str(item)
    if not key.endswith(')'):
        key = f'{key[0:i]}[{key[i:]}]'
    if re.search('\n', text):
        t = ' ' * i
        if (text.endswith('}') or text.endswith(']')) and not text.endswith(']]'):
            text = rn.join(afterFirstNonTab([t + x for x in text.split(rn)]))
        else:
            text = rn.join([''] + ([t + tb + x for x in text.split(rn)]) + [tb])
    return f"{key} ({text})"


def tags(*labels, **items):
    length = len(labels)
    if length == 0:
        label = ''
    elif length == 1:
        label = f'[{labels[0]}]'
    else:
        label = labels[0]
        for v in labels[1:]:
            label = tag(label, v)
    for key, item in items.items():
        label = label + ',\r\n' + tag(key, item)
    return label


def wr_tags(*labels, **items):
    msg = tags(*labels, **items)
    wl(msg)
    return msg


def pad_start(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}>{width}}'


def pad_end(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}<{width}}'


def pad_centered(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}^{width}}'


def link(label, item):
    l, m = str(label), str(item)
    if l:
        if m:
            return l + ', ' + m
        else:
            return l
    else:
        if m:
            return m
        else:
            return ''


def indexOfFirstNonTab(tx):
    t, i = str(tx), 0
    while str.startswith(t, '\t', i) or str.startswith(t, ' ', i):
        i += 1
    return i


def afterFirstNonTab(tx):
    return tx[indexOfFirstNonTab(tx)]


class StrTemp:
    @staticmethod
    def strF2H(tok):
        """全角转半角"""

        def charF2H(q_ch):
            i_code = ord(q_ch)
            if i_code == 12288:  # 全角空格直接转换
                i_code = 32
            elif 65281 <= i_code <= 65374:  # 全角字符（除空格）根据关系转化
                i_code -= 65248
            return chr(i_code)

        return ''.join(map(charF2H, tok))

    @staticmethod
    def strH2F(tok):
        """半角转全角"""

        def charH2F(b_ch):
            i_code = ord(b_ch)
            if i_code == 32:  # 半角空格直接转化
                i_code = 12288
            elif 32 <= i_code <= 126:  # 半角字符（除空格）根据关系转化
                i_code += 65248
            return chr(i_code)

        return ''.join(map(charH2F, tok))

    @staticmethod
    def sn2pl(tok: str):
        return ''

    @staticmethod
    def pl2sn(tok: str):
        return ''

    # 'the_wallstreet_journal_2019 -> 'TheWallstreetJournal2019'
    @staticmethod
    def py2jv(tok: str):
        rsl = tok.title().replace('_', '')
        return rsl

    __plural_rules = {
        r'move$': r'moves',
        r'foot$': r'feet',
        r'child$': r'children',
        r'human$': r'humans',
        r'man$': r'men',
        r'tooth$': r'teeth',
        r'person$': r'people',
        r'([m|l])ouse$': r'\1ice',
        r'(x|ch|ss|sh|us|as|is|os)$': r'\1es',
        r'([^aeiouy]|qu)y$': r'\1ies',
        r'(?:([^f])fe|([lr])f)$': r'\1\2ves',
        r'(shea|lea|loa|thie)f$': r'\1ves',
        r'([ti])um$': r'\1a',
        r'(tomat|potat|ech|her|vet)o$': r'\1oes',
        r'(bu)s$': r'\1ses',
        r'(ax|test)is$': r'\1es',
        r's$': r's',
    }

    @staticmethod
    def pluralize(word):
        for k, v in StrTemp.__plural_rules.items():
            if re.search(k, word, re.I):
                # wL(f'[{word}] matched ({k}), to be replaced by ({v})')
                rsl = re.sub(k, v, word)
                return rsl
        return word + 's'

#
# def test():
#     # GTA5LosSantos -> GTA5 Los Santos
#     words = ['child', 'knife', 'potato', 'bus', 'axis', 'daily']
#     # sps = ['the_wallstreet_journal_2019', '2KGames18', 'GTA5LosSantos']
#     # st = {k: py2jv(k) for k in sps}
#     # wL(mvBrief(st))
#     plu_rsl = {w: pluralize(w) for w in words}
#     wL(mvBrief(plu_rsl))
