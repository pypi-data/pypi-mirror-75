from xbrief import Preci, strx


def xbrief(matrix,
           abstract=None,
           rows_head: int = None,
           rows_tail: int = None,
           columns_head: int = None,
           columns_tail: int = None):
    if abstract:
        rowwise_abstract = lambda row: [f'{abstract(x)}' for x in row]
    else:
        rowwise_abstract = lambda row: [f'{x}' for x in row]
    rows_preci = Preci.from_arr(matrix, rows_head, rows_tail) \
        .map(lambda row: Preci.from_arr(row, columns_head, columns_tail).to_list('...')) \
        .map(rowwise_abstract)
    col_indexes = [i for i, v in enumerate(rows_preci.to_list()[0])]
    row_list = rows_preci.to_list(['..' for _ in col_indexes])
    column_list = [[row[c] for row in row_list] for c in col_indexes]
    widths = [max([len(x) for x in column]) for column in column_list]
    lines = [
        ' | '.join([strx.pad_start(v, widths[i])
                    for i, v in enumerate(row)])
        for row in row_list
    ]
    return '[' + ',\r\n '.join([f'[{row}]' for row in lines]) + ']'
